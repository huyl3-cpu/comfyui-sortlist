# max_frames_from_resolution.py
# Calculates max supported frames (4n+1) based on resolution height (16:9).
# Reference: 720p (1280x720) = 257 frames

# Standard 16:9 widths for each height
_RESOLUTION_MAP = {
    480:  848,
    720:  1280,
    1080: 1920,
}

# Reference: 720p = 257 frames
_REF_PIXELS = 1280 * 720
_REF_FRAMES = 257

class MaxFramesFromResolution:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "resolution": ("INT", {"default": 720, "min": 64, "max": 9999, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("max_frames_4n1",)
    FUNCTION = "execute"
    CATEGORY = "HuyL3/Utilities"

    def execute(self, resolution: int):
        # Get width: use lookup table for standard resolutions, else estimate 16:9
        if resolution in _RESOLUTION_MAP:
            width = _RESOLUTION_MAP[resolution]
        else:
            width = round(resolution * 16 / 9 / 8) * 8  # nearest multiple of 8

        cur_pixels = width * resolution
        if cur_pixels <= 0:
            return (1,)

        ratio = _REF_PIXELS / cur_pixels
        raw_frames = _REF_FRAMES * ratio

        # Largest 4n+1 <= raw_frames
        n = int((raw_frames - 1) // 4)
        max_frames = 4 * n + 1

        return (max(1, max_frames),)


NODE_CLASS_MAPPINGS = {
    "MaxFramesFromResolution": MaxFramesFromResolution,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaxFramesFromResolution": "Max Frames From Resolution (4n+1)",
}
