class SetValueForMC_V2V_V2:
    """
    Set configuration values for MC V2V V2 workflow.
    Includes: video path, audio path, Vietnamese motion prompt.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Đường dẫn video": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn file video (.mp4)",
                }),
                "Đường dẫn audio": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn file audio (.mp3/.wav)",
                }),
                "Prompt cử động tiếng việt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "Mô tả cử động bằng tiếng Việt",
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("video_path", "audio_path", "motion_prompt_vi")
    FUNCTION = "set_values"
    CATEGORY = "comfyui-sortlist"

    def set_values(self, **kwargs):
        return (
            kwargs["Đường dẫn video"],
            kwargs["Đường dẫn audio"],
            kwargs["Prompt cử động tiếng việt"],
        )


NODE_CLASS_MAPPINGS = {
    "Set Value For MC V2V V2": SetValueForMC_V2V_V2,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Set Value For MC V2V V2": "Set Value For MC V2V V2",
}
