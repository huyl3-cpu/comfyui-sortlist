"""
WanVideo Frame Window Size Calculator
Tính frame_window_size phù hợp từ tổng số frame input.

WanVideo VAE temporal compression factor = 4
Công thức: output_frames = (frame_window_size - 1) × 4 + 1
Ngược lại:  ideal_latent  = (total_frames  - 1) / 4 + 1

frame_window_size hợp lệ phải là 4n+1 và nằm trong [81, 101]:
  81, 85, 89, 93, 97, 101
"""

# Valid frame_window_size values: 4n+1, n=20..25
VALID_WINDOW_SIZES = [81, 85, 89, 93, 97, 101]


class WanFrameWindowSize:
    """
    Tính frame_window_size tối ưu cho WanVideo từ tổng số frame input.

    WanVideo VAE nén temporal theo hệ số 4:
        output_frames = (frame_window_size - 1) × 4 + 1

    Node này tìm giá trị frame_window_size (4n+1) gần nhất trong [81-101]
    sao cho output_frames gần nhất với total_frames.
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
                    "tooltip": "Tổng số frame của video input (loaded_frame_count)"
                }),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT")
    RETURN_NAMES = ("frame_window_size", "output_frames", "frame_diff")
    FUNCTION = "calculate"
    CATEGORY = "utils"
    DESCRIPTION = """
    Tính frame_window_size tối ưu cho WanVideo Animate Embeds.

    - Input:  total_frames = tổng frame video gốc
    - Output: frame_window_size = giá trị 4n+1 gần nhất trong [81, 101]
              output_frames = số frame sẽ được generate
              frame_diff    = chênh lệch so với input (output - input)

    Các giá trị hợp lệ: 81, 85, 89, 93, 97, 101
    """

    def calculate(self, total_frames: int):
        # Tính ideal latent frames từ total_frames
        # Công thức ngược: ideal = (total_frames - 1) / 4 + 1
        ideal_latent = (total_frames - 1) / 4.0 + 1.0

        # Tìm giá trị trong VALID_WINDOW_SIZES gần ideal_latent nhất
        best_window = min(VALID_WINDOW_SIZES, key=lambda w: abs(w - ideal_latent))

        # Tính lại output_frames từ frame_window_size đã chọn
        output_frames = (best_window - 1) * 4 + 1

        # Chênh lệch: dương = generate nhiều hơn, âm = ít hơn
        frame_diff = output_frames - total_frames

        print(
            f"[WanFrameWindow] total_frames={total_frames} "
            f"→ ideal_latent={ideal_latent:.2f} "
            f"→ frame_window_size={best_window} "
            f"→ output_frames={output_frames} "
            f"(diff={frame_diff:+d})"
        )

        return (best_window, output_frames, frame_diff)


# Node registration
NODE_CLASS_MAPPINGS = {
    "WanFrameWindowSize": WanFrameWindowSize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WanFrameWindowSize": "Wan Frame Window Size 🎞️",
}
