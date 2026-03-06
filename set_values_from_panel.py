class SetValuesFromPanel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "stt": ("INT", {
                    "default": 1,
                    "label": "STT",
                    "display_name": "STT",
                }),

                "fps": ("FLOAT", {
                    "default": 16.0,
                    "label": "FPS",
                    "display_name": "FPS",
                }),

                "convert_folder": ("STRING", {
                    "default": "/content/drive/MyDrive/anime",
                    "label": "THƯ MỤC chuyển style",
                    "display_name": "THƯ MỤC chuyển style",
                }),

                "save_path": ("STRING", {
                    "default": "/content/drive/MyDrive/anime",
                    "label": "THƯ MỤC lưu",
                    "display_name": "THƯ MỤC lưu",
                }),

            }
        }

    RETURN_TYPES = (
        "INT",
        "FLOAT",
        "STRING",
        "STRING",
    )

    RETURN_NAMES = (
        "stt",
        "fps",
        "convert_folder",
        "save_path",
    )

    FUNCTION = "execute"
    CATEGORY = "HuyL3/Utilities"

    def execute(
        self,
        stt,
        fps,
        convert_folder,
        save_path,
    ):
        return (
            stt,
            fps,
            convert_folder,
            save_path,
        )


NODE_CLASS_MAPPINGS = {
    "SetValuesFromPanel": SetValuesFromPanel
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetValuesFromPanel": "Set Values From Panel"
}
