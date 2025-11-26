class SetValuesFromPanel:
    """
    Node lấy 7 giá trị từ Workflow Input Panel và trả ra đúng định dạng:
    (int, float, string, string, string, int, int)
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
                "width": ("INT", {"default": 912}),
                "height": ("INT", {"default": 512}),
            }
        }

    RETURN_TYPES = ("INT", "FLOAT", "STRING", "STRING", "STRING", "INT", "INT")
    RETURN_NAMES = ("stt", "fps", "file_name", "save_path", "convert_folder", "width", "height")
    FUNCTION = "execute"
    CATEGORY = "HuyL3/Utilities"

    def execute(self, stt, fps, file_name, save_path, convert_folder, width, height):
        return (stt, fps, file_name, save_path, convert_folder, width, height)


NODE_CLASS_MAPPINGS = {
    "SetValuesFromPanel": SetValuesFromPanel
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetValuesFromPanel": "Set Values From Panel"
}
