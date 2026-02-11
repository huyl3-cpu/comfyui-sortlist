import numpy as np
import torch


class MP3ExtractFromImage:
    """Extract MP3 audio data from image RGB channels (LSB steganography)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("mp3_info",)
    FUNCTION = "extract"
    CATEGORY = "comfyui-sortlist"

    def extract(self, image):
        arr = image.detach().cpu().numpy()
        if arr.ndim == 4:
            arr = arr[0]

        if arr.max() <= 1.0:
            arr = (arr * 255).astype(np.uint8)
        else:
            arr = arr.astype(np.uint8)

        H, W, C = arr.shape
        if C < 3:
            return ("<invalid image: not RGB>",)

        # Read LSB from RGB channels
        flat = arr[:, :, :3].reshape(-1)
        total_bits = len(flat)

        # Read 32-bit length header
        if total_bits < 32:
            return ("<image too small>",)

        data_len = 0
        for i in range(32):
            data_len = (data_len << 1) | (flat[i] & 1)

        needed_bits = 32 + data_len * 8
        if needed_bits > total_bits or data_len <= 0 or data_len > 100000:
            return (f"<no valid data found, len={data_len}>",)

        # Read audio bytes
        byte_list = []
        for j in range(data_len):
            byte_val = 0
            for k in range(8):
                bit_idx = 32 + j * 8 + k
                byte_val = (byte_val << 1) | (flat[bit_idx] & 1)
            byte_list.append(byte_val)

        audio_bytes = bytes(byte_list)

        return (f"Audio found: {data_len} bytes ({data_len/1024:.1f}KB), 8kHz mono 8-bit PCM, ~1s",)


NODE_CLASS_MAPPINGS = {
    "MP3 Extract From Image": MP3ExtractFromImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MP3 Extract From Image": "MP3 Extract From Image (RGB)",
}
