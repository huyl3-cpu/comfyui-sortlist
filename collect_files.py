import os
import shutil


class CollectFiles:
    """
    Lọc các dòng chứa pattern từ string list multiline,
    rồi copy các file đó vào thư mục đích.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "String list (multiline)",
                }),
                "pattern": ("STRING", {
                    "default": "audio.mp4",
                    "multiline": False,
                    "placeholder": "Pattern lọc, ví dụ: audio.mp4",
                }),
                "dest_folder": ("STRING", {
                    "default": "/content/ComfyUI/output/I2V",
                    "multiline": False,
                    "placeholder": "Thư mục đích",
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)
    FUNCTION = "collect"
    CATEGORY = "comfyui-sortlist"

    def collect(self, text, pattern, dest_folder):
        os.makedirs(dest_folder, exist_ok=True)

        # Lọc các dòng chứa pattern
        lines = text.strip().split("\n")
        matched = []
        for line in lines:
            clean = line.strip().strip('",').strip("'")
            if pattern in clean and os.path.isfile(clean):
                matched.append(clean)

        # Copy từng file vào thư mục đích
        copied = []
        for src in matched:
            basename = os.path.basename(src)
            dest = os.path.join(dest_folder, basename)
            # Xử lý trùng tên
            if os.path.exists(dest):
                name, ext = os.path.splitext(basename)
                counter = 1
                while os.path.exists(dest):
                    dest = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                    counter += 1
            shutil.copy2(src, dest)
            copied.append(dest)

        result = "\n".join(copied) if copied else "Không tìm thấy file nào khớp pattern"
        return (result,)


NODE_CLASS_MAPPINGS = {
    "CollectFiles": CollectFiles,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CollectFiles": "Collect Files",
}
