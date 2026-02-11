class SetValueForMC:
    """
    Set configuration values for MC workflow.
    4 string fields for common paths and settings.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "duong_dan_video": ("STRING", {
                    "default": "/content/drive/MyDrive/audio/1.mp4",
                    "multiline": False,
                    "placeholder": "Đường dẫn video",
                }),
                "thu_muc_audio": ("STRING", {
                    "default": "/content/drive/MyDrive/audio",
                    "multiline": False,
                    "placeholder": "Thư mục Audio",
                }),
                "thu_muc_ket_qua": ("STRING", {
                    "default": "/content/drive/MyDrive/output/videos",
                    "multiline": False,
                    "placeholder": "Thư mục kết quả",
                }),
                "prompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "Prompt",
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("path_origin", "path_folder", "save_videos", "prompt")
    FUNCTION = "set_values"
    CATEGORY = "comfyui-sortlist"

    def set_values(self, duong_dan_video, thu_muc_audio, thu_muc_ket_qua, prompt):
        return (duong_dan_video, thu_muc_audio, thu_muc_ket_qua, prompt)


NODE_CLASS_MAPPINGS = {
    "Set Value For MC": SetValueForMC,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Set Value For MC": "Set Value For MC",
}
