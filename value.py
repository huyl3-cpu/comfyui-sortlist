import random
import torch
from .videos_nodes import check_license_shared


def _rand_hw():
    return random.randint(513, 1023), random.randint(513, 1023)


def _black_image(batch: int, h: int, w: int):
    return torch.zeros((batch, h, w, 3), dtype=torch.float32)


def _white_mask(batch: int, h: int, w: int):
    return torch.ones((batch, h, w), dtype=torch.float32)


class VF9_SetValue:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "license_key": ("STRING", {"default": "", "multiline": False}),
                "enable_background": ("BOOLEAN", {"default": True}),
                "enable_face": ("BOOLEAN", {"default": True}),
                "enable_mask": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "background": ("IMAGE",),
                "face": ("IMAGE",),
                "mask": ("MASK",),
            },
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "MASK")
    RETURN_NAMES = ("background", "face", "mask")
    FUNCTION = "run"
    CATEGORY = "comfyui-sortlist"

    def run(
        self,
        license_key: str,
        enable_background: bool,
        enable_face: bool,
        enable_mask: bool,
        background=None,
        face=None,
        mask=None,
    ):
    
        batch = 1
        if isinstance(background, torch.Tensor) and background.ndim == 4:
            batch = int(background.shape[0])
        elif isinstance(face, torch.Tensor) and face.ndim == 4:
            batch = int(face.shape[0])
        elif isinstance(mask, torch.Tensor) and mask.ndim == 3:
            batch = int(mask.shape[0])

        def fb_img():
            return _black_image(batch, 512, 512)

        def fb_mask():
            return _white_mask(batch, 512, 512)


        try:
            res = check_license_shared(license_key)
            valid = (res.get("valid") is True)
        except Exception:
            valid = False

        if valid:
            out_bg = background if (enable_background and background is not None) else fb_img()
            out_face = face if (enable_face and face is not None) else fb_img()
            out_mask = mask if (enable_mask and mask is not None) else fb_mask()
            return (out_bg, out_face, out_mask)

        if enable_background:
            h, w = _rand_hw()
            out_bg = _black_image(batch, h, w)
        else:
            out_bg = background if background is not None else fb_img()

        if enable_face:
            h, w = _rand_hw()
            out_face = _black_image(batch, h, w)
        else:
            out_face = face if face is not None else fb_img()

        if enable_mask:
            h, w = _rand_hw()
            out_mask = _white_mask(batch, h, w)  # full trắng
        else:
            out_mask = mask if mask is not None else fb_mask()

        return (out_bg, out_face, out_mask)


NODE_CLASS_MAPPINGS = {"VF9_SetValue": VF9_SetValue}
NODE_DISPLAY_NAME_MAPPINGS = {"VF9_SetValue": "Set Value"}
