class SetValuesFromPanel:
    """
    Node lấy 6 giá trị từ Workflow Input Panel và trả ra đúng định dạng:
    (float, string, string, string, int, int)
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "fps": ("FLOAT", {"default": 33.0}),
                "file_name": ("STRING", {"default": "all.mp4"}),
                "save_path": ("STRING", {"default": "/content/drive/MyDrive/anime"}),
                "convert_folder": ("STRING", {"default": "/content/drive/MyDrive/anime"}),
                "width": ("INT", {"default": 912}),
                "height": ("INT", {"default": 512}),
            }
        }

    RETURN_TYPES = ("FLOAT", "STRING", "STRING", "STRING", "INT", "INT")
    RETURN_NAMES = ("fps", "file_name", "save_path", "convert_folder", "width", "height")
    FUNCTION = "execute"
    CATEGORY = "HuyL3/Utilities"

    def execute(self, fps, file_name, save_path, convert_folder, width, height):
        return (fps, file_name, save_path, convert_folder, width, height)


NODE_CLASS_MAPPINGS = {
    "SetValuesFromPanel": SetValuesFromPanel
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetValuesFromPanel": "Set Values From Panel"
}
