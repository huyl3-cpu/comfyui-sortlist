"""
Adaptive Resolution Node for ComfyUI
Auto-determines output resolution based on minimum input dimension
"""

class AdaptiveResolution:
    """
    Automatically scales resolution based on input dimensions.
    
    Logic:
    - If min(width, height) <= 480 → Output: 720
    - If 480 < min(width, height) <= 720 → Output: 1080
    - If min(width, height) > 720 → Output: 1080
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 8192,
                    "step": 8,
                    "tooltip": "Input width"
                }),
                "height": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 8192,
                    "step": 8,
                    "tooltip": "Input height"
                }),
            },
        }
    
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("resolution",)
    FUNCTION = "calculate_resolution"
    CATEGORY = "utils"
    DESCRIPTION = """
    Automatically determines output resolution based on input dimensions.
    
    Rules:
    - min(w,h) ≤ 480 → 720p output
    - 480 < min(w,h) ≤ 720 → 1080p output  
    - min(w,h) > 720 → 1080p output
    """
    
    def calculate_resolution(self, width, height):
        """
        Calculate output resolution based on minimum dimension.
        
        Args:
            width: Input width
            height: Input height
            
        Returns:
            int: Output resolution (720 or 1080)
        """
        min_dimension = min(width, height)
        
        if min_dimension <= 480:
            output_resolution = 720
        elif min_dimension <= 720:
            output_resolution = 1080
        else:
            output_resolution = 1080
        
        return (output_resolution,)


# Node registration
NODE_CLASS_MAPPINGS = {
    "AdaptiveResolution": AdaptiveResolution,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdaptiveResolution": "Adaptive Resolution 📐",
}
