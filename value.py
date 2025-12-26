# value.py
# Set Value - rgthree-like frontend-only bypass using OPT_CONNECTION
# JS will remove/rewire before queue prompt. Backend should never execute it.

class SetValue:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "enable_background": ("BOOLEAN", {"default": True}),
                "enable_face": ("BOOLEAN", {"default": True}),
                "enable_mask": ("BOOLEAN", {"default": True}),
                "mask_text": ("STRING", {"default": "", "multiline": False}),
            },
            "optional": {
                "background": ("OPT_CONNECTION",),
                "face": ("OPT_CONNECTION",),
                "mask": ("OPT_CONNECTION",),
            },
        }

    RETURN_TYPES = ("OPT_CONNECTION", "OPT_CONNECTION", "OPT_CONNECTION", "OPT_CONNECTION")
    RETURN_NAMES = ("background", "face", "mask", "mask_text")

    FUNCTION = "noop"
    CATEGORY = "sortlist/utils"

    def noop(self, **kwargs):
        # Should never run (JS deletes/rewires). Keep safe.
        return (None, None, None, None)


NODE_CLASS_MAPPINGS = {"Set Value": SetValue}
NODE_DISPLAY_NAME_MAPPINGS = {"Set Value": "Set Value"}
