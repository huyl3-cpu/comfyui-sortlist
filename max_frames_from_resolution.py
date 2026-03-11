# max_frames_from_resolution.py
# Calculates max supported frames (4n+1) for a given resolution,
# based on a reference resolution and its known max frames.

class MaxFramesFromResolution:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width":  ("INT", {"default": 848,  "min": 64, "max": 9999, "step": 8}),
                "height": ("INT", {"default": 480,  "min": 64, "max": 9999, "step": 8}),
                "ref_width":      ("INT", {"default": 1280, "min": 64, "max": 9999, "step": 8}),
                "ref_height":     ("INT", {"default": 720,  "min": 64, "max": 9999, "step": 8}),
                "ref_max_frames": ("INT", {"default": 257,  "min": 1,  "max": 99999}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "FLOAT")
    RETURN_NAMES = ("max_frames_4n1", "n", "ratio")
    FUNCTION = "execute"
    CATEGORY = "HuyL3/Utilities"

    def execute(self, width, height, ref_width, ref_height, ref_max_frames):
        ref_pixels = ref_width * ref_height
        cur_pixels = width * height

        if cur_pixels <= 0:
            return (1, 0, 0.0)

        ratio = ref_pixels / cur_pixels
        raw_frames = ref_max_frames * ratio

        # Find largest 4n+1 <= raw_frames
        n = int((raw_frames - 1) // 4)
        max_frames = 4 * n + 1

        if max_frames < 1:
            max_frames = 1
            n = 0

        return (max_frames, n, round(ratio, 4))


NODE_CLASS_MAPPINGS = {
    "MaxFramesFromResolution": MaxFramesFromResolution,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaxFramesFromResolution": "Max Frames From Resolution (4n+1)",
}
