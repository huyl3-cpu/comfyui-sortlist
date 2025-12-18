class SetValuesFromPanel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "stt": ("INT", {"default": 1}),
                "fps": ("FLOAT", {"default": 16.0}),
                "file_name": ("STRING", {"default": "all.mp4"}),
                "save_path": ("STRING", {"default": "/content/drive/MyDrive/anime"}),
                "convert_folder": ("STRING", {"default": "/content/drive/MyDrive/anime"}),
                "resolution": (
                    "INT",
                    {
                        "default": 720,
                        "choices": [480, 720]
                    }
                ),
                "type_audio": ("INT", {"default": 0}),
                "type_prompt": ("INT", {"default": 0}),
                "license_key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = (
        "INT",
        "FLOAT",
        "STRING",
        "STRING",
        "STRING",
        "INT",
        "INT",
        "INT",
        "STRING",
    )

    RETURN_NAMES = (
        "stt",
        "fps",
        "file_name",
        "save_path",
        "convert_folder",
        "resolution",
        "type_audio",
        "type_prompt",
        "license_key",
    )

    FUNCTION = "execute"
    CATEGORY = "HuyL3/Utilities"

    def execute(
        self,
        stt,
        fps,
        file_name,
        save_path,
        convert_folder,
        resolution,
        type_audio,
        type_prompt,
        license_key,
    ):
        return (
            stt,
            fps,
            file_name,
            save_path,
            convert_folder,
            resolution,
            type_audio,
            type_prompt,
            license_key,
        )


NODE_CLASS_MAPPINGS = {
    "SetValuesFromPanel": SetValuesFromPanel
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetValuesFromPanel": "Set Values From Panel"
}
