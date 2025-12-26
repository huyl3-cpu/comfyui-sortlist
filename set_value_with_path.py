class SetValueWithPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
       
                "mask_prompt": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Tách mask",
                }),

                "file_name": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Tên file",
                }),

                "convert_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn video gốc",
                }),

                "save_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn lưu video",
                }),

 
                "license_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "License_key",
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("mask_prompt", "file_name", "convert_path", "save_path", "license_key")
    FUNCTION = "run"
    CATEGORY = "comfyui-sortlist"

    def run(self, mask_prompt: str, file_name: str, convert_path: str, save_path: str, license_key: str):
        return (
            mask_prompt or "",
            file_name or "",
            convert_path or "",
            save_path or "",
            license_key or "",
        )


NODE_CLASS_MAPPINGS = {
    "Set Value With Path": SetValueWithPath,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Set Value With Path": "Set Value With Path",
}
