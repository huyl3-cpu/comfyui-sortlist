"""
WanVideo Frame Window Size Calculator
Tính frame_window_size (x) từ tổng số frame và số lần sampling (n).

Công thức WanVideo:  output_frames = x * n + 1
Wan VAE yêu cầu:     x = 4k+1  (k = 0,1,2,...) tức là x ∈ {1,5,9,...,93,97,101,...}
Ràng buộc:           x < 101  (x_max = 97)

Thuật toán tìm x:
  1. min_x = ceil(total_frames / n)  (để x*n + 1 > total_frames → không thiếu frame)
  2. x = nearest 4k+1 >= min_x
  3. Nếu x >= 101 → tăng n và thử lại

Tự động n=1 khi total_frames <= 101 (video ngắn, 1 window là đủ).

Ví dụ (n=4):
  total=357  → min_x=ceil(357/4)=90 → x=93 (4*23+1)
              → output_frames=93*4+1=373 (thừa 373-357=16 frame cuối)

Node 2 (WanTrimFrames): cắt bỏ frame thừa, giữ lại đúng total_frames frame.
"""
import math
# torch imported lazily inside WanTrimFrames.trim() to allow standalone testing


# ── Helpers ───────────────────────────────────────────────────────────────────

def _next_4k1(n: int) -> int:
    """Tìm số nhỏ nhất dạng 4k+1 mà >= n.
       Dãy: 1, 5, 9, 13, ..., 89, 93, 97, 101, ...
    """
    if n <= 1:
        return 1
    # k = ceil((n-1)/4)
    k = (n - 2) // 4 + 1   # equivalent to ceil((n-1)/4) for n >= 2
    return 4 * k + 1


# ── Node 1: WanFrameWindowSize ────────────────────────────────────────────────

class WanFrameWindowSize:
    """
    Tính frame_window_size (x) cho WanVideo:
      • x phải có dạng 4k+1  (yêu cầu của Wan VAE)
      • x < 101  (x_max = 97)
      • x*n + 1 >= total_frames  (đủ frame để sample)
      • x nhỏ nhất thỏa mãn (tối thiểu waste)

    Đặc biệt:
      • total_frames <= 101 → n=1 tự động (video ngắn, 1 window đủ)
      • Nếu x vẫn >= 101 → tự tăng n cho đến khi x <= 97
    """

    X_MAX = 97   # max valid 4k+1 < 101

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "total_frames": ("INT", {
                    "default": 81,
                    "min": 1,
                    "max": 99999,
                    "step": 1,
                    "tooltip": "Tổng số frame của video input",
                }),
            },
        }

    RETURN_TYPES  = ("INT", "INT", "INT", "INT")
    RETURN_NAMES  = ("frame_window_size", "output_frames", "frame_diff", "n_used")
    FUNCTION      = "calculate"
    CATEGORY      = "utils"
    DESCRIPTION   = (
        "Tự động tính frame_window_size (x = 4k+1, x ≤ 97) và n nhỏ nhất\n"
        "sao cho x*n+1 > total_frames.\n"
        "Output frame_diff = output_frames - total_frames (số frame thừa cần trim)."
    )

    def calculate(self, total_frames: int):
        # ── Trường hợp đặc biệt: 1 frame ──────────────────────────────────
        if total_frames <= 1:
            print("[WanFrameWindow] total=1 → x=1, n=1")
            return (1, 2, 1, 1)

        # ── Video ngắn: total_frames <= 98 → 1 window đủ ──────────────────
        # next_4k1(total_frames-1) luôn <= 97 khi total_frames-1 <= 97
        if total_frames <= 98:
            effective_n = 1
            x = _next_4k1(total_frames - 1)   # guaranteed <= 97
            output_frames = x * effective_n + 1
            frame_diff = output_frames - total_frames
            print(
                f"[WanFrameWindow] total={total_frames} → n=1 (video ngắn)"
                f" → x={x} (4*{(x-1)//4}+1), output={output_frames} (diff={frame_diff:+d})"
            )
            return (x, output_frames, frame_diff, effective_n)

        # ── Tự động tìm n nhỏ nhất sao cho x <= 97 ───────────────────────
        # min_x = (total_frames-1)//n + 1  → x = next_4k1(min_x) <= 97
        effective_n = 1
        while True:
            min_x = (total_frames - 1) // effective_n + 1
            x = _next_4k1(min_x)
            if x <= self.X_MAX:
                break
            effective_n += 1

        output_frames = x * effective_n + 1
        frame_diff = output_frames - total_frames

        print(
            f"[WanFrameWindow] total={total_frames}"
            f" → auto n={effective_n}, x={x} (4*{(x-1)//4}+1)"
            f" → output={output_frames} (diff={frame_diff:+d}, trim {frame_diff} frame cuối)"
        )
        return (x, output_frames, frame_diff, effective_n)


# ── Node 2: WanTrimFrames ─────────────────────────────────────────────────────

class WanTrimFrames:
    """
    Cắt bỏ frame thừa ở cuối, giữ lại đúng total_frames frame đầu tiên.

    WanVideo sampling tạo ra output_frames = x*n+1 frames, nhưng video gốc
    chỉ có total_frames frames. Node này trả về đúng total_frames frame
    (frame 0 → frame total_frames-1), loại bỏ frame thừa ở cuối.

    Ví dụ:
      x=93, n=4 → output = 93*4+1 = 373 frames
      total_frames = 357
      → giữ lại frame 0–356, loại frame 357–372 (16 frame cuối)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {
                    "tooltip": "Batch ảnh từ WanVideo decode (shape: [F, H, W, C])",
                }),
                "total_frames": ("INT", {
                    "default": 81,
                    "min": 1,
                    "max": 99999,
                    "step": 1,
                    "tooltip": "Số frame gốc cần giữ lại (từ WanFrameWindowSize → output_frames hoặc total_frames gốc)",
                }),
            },
        }

    RETURN_TYPES  = ("IMAGE", "INT")
    RETURN_NAMES  = ("images", "frames_kept")
    FUNCTION      = "trim"
    CATEGORY      = "utils"
    DESCRIPTION   = (
        "Giữ lại đúng total_frames frame đầu (frame 0 → total_frames-1).\n"
        "Loại bỏ frame dư ở cuối do WanVideo sampling tạo thêm.\n"
        "Dùng sau WanVideo Decode kết hợp với WanFrameWindowSize."
    )

    def trim(self, images, total_frames: int):
        """
        images: torch.Tensor shape [F, H, W, C]  (lazy import)
        total_frames: số frame cần giữ
        """
        import torch  # lazy — only loaded inside ComfyUI environment
        F = images.shape[0]

        if total_frames >= F:
            # Không cần trim (hoặc video ngắn hơn dự kiến)
            print(
                f"[WanTrimFrames] total_frames={total_frames} >= available={F}"
                f" → giữ nguyên {F} frame"
            )
            return (images, F)

        trimmed = images[:total_frames]
        removed = F - total_frames

        print(
            f"[WanTrimFrames] {F} → {total_frames} frame"
            f" (loại bỏ {removed} frame cuối: frame {total_frames}–{F-1})"
        )

        return (trimmed, total_frames)


# ── Registration ──────────────────────────────────────────────────────────────

NODE_CLASS_MAPPINGS = {
    "WanFrameWindowSize": WanFrameWindowSize,
    "WanTrimFrames":      WanTrimFrames,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanFrameWindowSize": "Wan Frame Window Size 🎞️",
    "WanTrimFrames":      "Wan Trim Frames ✂️",
}


# ── Standalone test (python wan_frame_window.py) ──────────────────────────────
if __name__ == "__main__":
    node = WanFrameWindowSize()
    tests = [
        1, 2, 5, 10, 81, 97, 98, 99, 101, 102,
        357, 373, 388, 389, 700, 1000, 5000,
    ]
    print(f"{'total':>6} | {'x':>4} {'n_auto':>6} {'output':>7} {'diff':>6}  check")
    print("-" * 55)
    for tf in tests:
        x, out, diff, nu = node.calculate(tf)
        ok = "✓" if x == (4 * ((x-1)//4) + 1) and x <= 97 and out > tf else "✗"
        print(f"{tf:>6} | {x:>4} {nu:>6} {out:>7} {diff:>+6}  {ok} x=4*{(x-1)//4}+1")
