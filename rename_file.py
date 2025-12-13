import os

class RenameFileNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_file_path": ("STRING", {"default": ""}),
                "new_file_name": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_file_path",)
    FUNCTION = "rename"
    CATEGORY = "HuyL3/File"

    def rename(self, input_file_path, new_file_name):
        input_file_path = input_file_path.strip()
        new_file_name = new_file_name.strip()

        if not os.path.isfile(input_file_path):
            return (f"ERROR: File not found → {input_file_path}",)

        dir_path = os.path.dirname(input_file_path)
        old_name = os.path.basename(input_file_path)
        old_base, old_ext = os.path.splitext(old_name)

        # Nếu new_file_name không có extension → giữ extension cũ
        if "." not in new_file_name:
            new_file_name = new_file_name + old_ext

        new_path = os.path.join(dir_path, new_file_name)

        try:
            os.rename(input_file_path, new_path)
        except Exception as e:
            return (f"ERROR: Rename failed → {e}",)

        return (new_path,)


NODE_CLASS_MAPPINGS = {
    "rename_file": RenameFileNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "rename_file": "Rename File"
}
