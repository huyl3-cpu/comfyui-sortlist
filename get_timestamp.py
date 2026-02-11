from datetime import datetime


class GetTimestamp:
    """Get current timestamp for filename prefix."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "format": (["YYYYMMDD_HHMMSS", "YYYY-MM-DD_HH-MM-SS", "YYYYMMDD", "HHMMSS", "custom"], {
                    "default": "YYYYMMDD_HHMMSS"
                }),
            },
            "optional": {
                "custom_format": ("STRING", {
                    "default": "%Y%m%d_%H%M%S",
                    "multiline": False,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("timestamp",)
    FUNCTION = "get_timestamp"
    CATEGORY = "comfyui-sortlist"

    def get_timestamp(self, format, custom_format="%Y%m%d_%H%M%S"):
        now = datetime.now()
        
        if format == "YYYYMMDD_HHMMSS":
            result = now.strftime("%Y%m%d_%H%M%S")
        elif format == "YYYY-MM-DD_HH-MM-SS":
            result = now.strftime("%Y-%m-%d_%H-%M-%S")
        elif format == "YYYYMMDD":
            result = now.strftime("%Y%m%d")
        elif format == "HHMMSS":
            result = now.strftime("%H%M%S")
        elif format == "custom":
            result = now.strftime(custom_format)
        else:
            result = now.strftime("%Y%m%d_%H%M%S")
        
        return (result,)


NODE_CLASS_MAPPINGS = {
    "Get Timestamp": GetTimestamp,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Get Timestamp": "Get Timestamp",
}
