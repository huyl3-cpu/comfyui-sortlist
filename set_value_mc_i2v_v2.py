class SetValueForMC_I2V_V2:
    """
    Set configuration values for MC I2V V2 workflow.
    Fields: Đường dẫn hình ảnh, Đường dẫn audio, Đường dẫn thư mục lưu, Mô tả ...
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Đường dẫn hình ảnh": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
                "Đường dẫn audio": ("STRING", {
                    "default": "/content/drive/MyDrive/audio",
                    "multiline": False,
                }),
                "Đường dẫn thư mục lưu": ("STRING", {
                    "default": "/content/drive/MyDrive/output/videos",
                    "multiline": False,
                }),
                "Mô tả ...": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("path_image", "path_audio", "save_dir", "prompt")
    FUNCTION = "set_values"
    CATEGORY = "comfyui-sortlist"

    def set_values(self, **kwargs):
        return (kwargs["Đường dẫn hình ảnh"], kwargs["Đường dẫn audio"], kwargs["Đường dẫn thư mục lưu"], kwargs["Mô tả ..."])


NODE_CLASS_MAPPINGS = {
    "Set Value For MC I2V V2": SetValueForMC_I2V_V2,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Set Value For MC I2V V2": "Set Value For MC I2V V2",
}
