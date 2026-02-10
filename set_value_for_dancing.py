class SetValueForDancing:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Bật mask": ("BOOLEAN", {
                    "default": True,
                }),
                "Tách mask": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Tách mask",
                }),
                "Bật background": ("BOOLEAN", {
                    "default": True,
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

    RETURN_TYPES = ("BOOLEAN", "STRING", "BOOLEAN", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "Bật mask",
        "Tách mask",
        "Bật background",
        "Tên file cần lưu",
        "Thư mục lưu video kết quả",
        "Đường dẫn thư mục videos",
        "Đường dẫn thư mục hình ảnh",
        "License_key",
    )
    FUNCTION = "run"
    CATEGORY = "comfyui-sortlist"

    def run(self, **kwargs):
        bat_mask = kwargs.get("Bật mask", True)
        mask_prompt = kwargs.get("Tách mask", "") or ""
        bat_background = kwargs.get("Bật background", True)
        file_name = kwargs.get("Tên file cần lưu", "") or ""
        save_path = kwargs.get("Thư mục lưu video kết quả", "") or ""
        videos_dir = kwargs.get("Đường dẫn thư mục videos", "") or ""
        images_dir = kwargs.get("Đường dẫn thư mục hình ảnh", "") or ""
        license_key = kwargs.get("License_key", "") or ""

        return (bat_mask, mask_prompt, bat_background, file_name, save_path, videos_dir, images_dir, license_key)


NODE_CLASS_MAPPINGS = {
    "Set Value For Dancing": SetValueForDancing,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Set Value For Dancing": "Set Value For Dancing",
}
