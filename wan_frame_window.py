"""
WanVideo Frame Window Size Calculator
Tính frame_window_size (x) từ tổng số frame và số lần sampling (n).

Công thức WanVideo:  output_frames = x * n + 1
Suy ra:              x = round((total_frames - 1) / n)
Ràng buộc:           x < 121  (frame_window_size tối đa WanVideo)

Tự động n=1 khi total_frames nhỏ (total_frames-1 <= 120):
    → video ngắn, 1 window là đủ, không cần sampling nhiều lần
"""
import math


class WanFrameWindowSize:
    """
    Tính frame_window_size (x) cho WanVideo với 2 ràng buộc:

    1. x < 121 luôn đảm bảo (tự tăng n nếu cần)
    2. Nếu total_frames nhỏ (total_frames-1 <= 120) → force n=1
       tránh sampling quá nhiều lần cho video ngắn
    """

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
                "n": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 1000,
                    "step": 1,
                    "tooltip": "Số lần sampling mong muốn (tự động giảm về 1 nếu video ngắn)",
                }),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT")
    RETURN_NAMES = ("frame_window_size", "output_frames", "frame_diff", "n_used")
    FUNCTION = "calculate"
    CATEGORY = "utils"
    DESCRIPTION = """
Tính frame_window_size (x) sao cho x * n + 1 ≈ total_frames, với x < 121.

Quy tắc:
  • total_frames - 1 <= 120  → n=1 tự động (video ngắn, 1 window đủ)
  • x >= 121                 → tự tăng n cho đến khi x < 121

Ví dụ (n=4):
  total=81   → x=20,  n=1  (nhỏ → n=1)   output=21  diff=-60
  total=81   → x=20,  n=4  → n=1 vì 80<=120
  total=161  → x=40,  n=4  → output=161  diff=0
  total=485  → x=121? → tăng n=5 → x=96  output=481  diff=-4
  total=700  → x=175? → tăng n=6 → x=117 output=703  diff=+3
"""

    X_MAX = 100  # frame_window_size tối đa (x < 101)

    def calculate(self, total_frames: int, n: int):
        raw = total_frames - 1  # số khoảng cần chia

        # ── Rule 1: video ngắn → n=1 (total_frames ~ x) ─────────────────────
        if raw <= self.X_MAX:
            effective_n = 1
            x = raw  # x * 1 + 1 = total_frames chính xác
        else:
            # ── Rule 2: tính x với n đã cho ──────────────────────────────────
            effective_n = n
            x = round(raw / effective_n)

            # ── Rule 3: x >= 121 → tăng n cho đến khi x < 121 ───────────────
            if x > self.X_MAX:
                effective_n = math.ceil(raw / self.X_MAX)
                x = round(raw / effective_n)

        # Safety cap (phòng trường hợp làm tròn ra đúng 121)
        x = min(x, self.X_MAX)

        output_frames = x * effective_n + 1
        frame_diff = output_frames - total_frames

        reason = ""
        if effective_n != n:
            if n > effective_n and effective_n == 1:
                reason = " [auto n=1: video ngắn]"
            else:
                reason = f" [auto n={effective_n}: x quá lớn]"

        print(
            f"[WanFrameWindow] total={total_frames}, n_req={n}{reason}"
            f" → x={x}, n_used={effective_n}"
            f" → output={output_frames} (diff={frame_diff:+d})"
        )

        return (x, output_frames, frame_diff, effective_n)


# Node registration
NODE_CLASS_MAPPINGS = {
    "WanFrameWindowSize": WanFrameWindowSize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanFrameWindowSize": "Wan Frame Window Size 🎞️",
}

