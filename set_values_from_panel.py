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

                "file_name": ("STRING", {
                    "default": "all.mp4",
                    "label": "Tên file cần lưu",
                    "display_name": "Tên file cần lưu",
                }),

                "save_path": ("STRING", {
                    "default": "/content/drive/MyDrive/anime",
                    "label": "Đường dẫn thư mục lưu",
                    "display_name": "Đường dẫn thư mục lưu",
                }),

                "convert_folder": ("STRING", {
                    "default": "/content/drive/MyDrive/anime",
                    "label": "Đường dẫn thư mục chuyển đổi",
                    "display_name": "Đường dẫn thư mục chuyển đổi",
                }),

            }
        }

    RETURN_TYPES = (
        "INT",
        "FLOAT",
        "STRING",
        "STRING",
        "STRING",
    )

    RETURN_NAMES = (
        "stt",
        "fps",
        "file_name",
        "save_path",
        "convert_folder",
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
    ):
        return (
            stt,
            fps,
            file_name,
            save_path,
            convert_folder,
        )


NODE_CLASS_MAPPINGS = {
    "SetValuesFromPanel": SetValuesFromPanel
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetValuesFromPanel": "Set Values From Panel"
}
