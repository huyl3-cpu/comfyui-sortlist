class SetValueForDancing:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Tách mask": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Tách mask",
                }),
                "Tên file cần lưu": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Tên file cần lưu",
                }),
                "Thư mục lưu video kết quả": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Thư mục lưu video kết quả",
                }),
                "Đường dẫn thư mục videos": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn thư mục videos",
                }),
                "Đường dẫn thư mục hình ảnh": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn thư mục hình ảnh",
                }),
                "License_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "License_key",
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "Tách mask",
        "Tên file cần lưu",
        "Thư mục lưu video kết quả",
        "Đường dẫn thư mục videos",
        "Đường dẫn thư mục hình ảnh",
        "License_key",
    )
    FUNCTION = "run"
    CATEGORY = "comfyui-sortlist"

    def run(self, **kwargs):
        mask_prompt = kwargs.get("Tách mask", "") or ""
        file_name = kwargs.get("Tên file cần lưu", "") or ""
        save_path = kwargs.get("Thư mục lưu video kết quả", "") or ""
        videos_dir = kwargs.get("Đường dẫn thư mục videos", "") or ""
        images_dir = kwargs.get("Đường dẫn thư mục hình ảnh", "") or ""
        license_key = kwargs.get("License_key", "") or ""

        return (mask_prompt, file_name, save_path, videos_dir, images_dir, license_key)


NODE_CLASS_MAPPINGS = {
    "Set Value For Dancing": SetValueForDancing,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Set Value For Dancing": "Set Value For Dancing",
}
