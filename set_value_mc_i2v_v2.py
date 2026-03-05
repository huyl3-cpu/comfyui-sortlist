class SetValueForMC_I2V_V2:
    """
    Set configuration values for MC I2V V2 workflow.
    Includes: audio path, Vietnamese motion prompt.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Đường dẫn audio": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn file audio (.mp3/.wav)",
                }),
                "Đường dẫn thư mục lưu": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn thư mục lưu kết quả",
                }),
                "Prompt cử động tiếng việt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "Mô tả cử động bằng tiếng Việt",
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("audio_path", "save_folder", "motion_prompt_vi")
    FUNCTION = "set_values"
    CATEGORY = "comfyui-sortlist"

    def set_values(self, **kwargs):
        return (
            kwargs["Đường dẫn audio"],
            kwargs["Đường dẫn thư mục lưu"],
            kwargs["Prompt cử động tiếng việt"],
        )


NODE_CLASS_MAPPINGS = {
    "Set Value For MC I2V V2": SetValueForMC_I2V_V2,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Set Value For MC I2V V2": "Set Value For MC I2V V2",
}
