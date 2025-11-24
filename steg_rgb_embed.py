
import numpy as np
import torch


class StegRGBEmbed:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "data_string": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image_out",)
    FUNCTION = "embed"
    CATEGORY = "custom/steganography"

    def embed(self, image, data_string):
        # tensor -> numpy 0..255 uint8
        arr = image.detach().cpu().numpy()

        if arr.ndim == 4:
            arr = arr[0]

        if arr.max() <= 1.0:
            arr = (arr * 255).astype(np.uint8)
        else:
            arr = arr.astype(np.uint8)

        H, W, C = arr.shape
        if C < 3:
            raise Exception("Image must have at least RGB channels.")

        # string -> bits
        b = data_string.encode("utf-8")
        bits = "".join([format(x, "08b") for x in b])
        bits += "0000000000000000"  # end marker (2 bytes zero)

        flat = arr.reshape(-1, 3)
        if len(bits) > len(flat) * 3:
            raise Exception("String too long to embed in RGB LSB.")

        idx = 0
        for i in range(len(flat)):
            for k in range(3):
                if idx < len(bits):
                    flat[i][k] = (flat[i][k] & 0xFE) | int(bits[idx])
                    idx += 1

        arr = flat.reshape(H, W, 3)
        out = torch.tensor(arr / 255.0).unsqueeze(0).float()
        return (out,)
