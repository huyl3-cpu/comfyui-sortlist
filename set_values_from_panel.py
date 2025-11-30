class SetValuesFromPanel:
    """
    Node lấy giá trị từ Workflow Input Panel và trả ra đúng định dạng:
    (int, float, string, string, string, int, int, int)
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "stt": ("INT", {"default": 1}),
                "fps": ("FLOAT", {"default": 16.0}),
                "file_name": ("STRING", {"default": "all.mp4"}),
                "save_path": ("STRING", {"default": "/content/drive/MyDrive/anime"}),
                "convert_folder": ("STRING", {"default": "/content/drive/MyDrive/anime"}),

                # ⭐ resolution dropdown (INT)
                "resolution": (
                    "INT",
                    {
                        "default": 720,
                        "choices": [480, 720]
                    }
                ),

                # ⭐ type_audio (INT)
                "type_audio": ("INT", {"default": 0}),

                # ⭐ NEW: type_prompt (INT)
                "type_prompt": ("INT", {"default": 0}),
            }
        }

    # Output thêm 1 trường => TOTAL = 8 output values
    RETURN_TYPES = (
        "INT",    # stt
        "FLOAT",  # fps
        "STRING", # file_name
        "STRING", # save_path
        "STRING", # convert_folder
        "INT",    # resolution
        "INT",    # type_audio
        "INT",    # type_prompt  <-- NEW
    )

    RETURN_NAMES = (
        "stt",
        "fps",
        "file_name",
        "save_path",
        "convert_folder",
        "resolution",
        "type_audio",
        "type_prompt",  # NEW
    )

    FUNCTION = "execute"
    CATEGORY = "HuyL3/Utilities"

    def execute(self, stt, fps, file_name, save_path, convert_folder, resolution, type_audio, type_prompt):
        return (stt, fps, file_name, save_path, convert_folder, resolution, type_audio, type_prompt)


NODE_CLASS_MAPPINGS = {
    "SetValuesFromPanel": SetValuesFromPanel
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetValuesFromPanel": "Set Values From Panel"
}
