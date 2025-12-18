# ============================
# comfyui-sortlist __init__.py
# ============================

from .sort_nodes import NODE_CLASS_MAPPINGS as SORT_NODE_CLASSES
from .sort_nodes import NODE_DISPLAY_NAME_MAPPINGS as SORT_NODE_NAMES

from .videos_nodes import NODE_CLASS_MAPPINGS as VIDEOS_NODE_CLASSES
from .videos_nodes import NODE_DISPLAY_NAME_MAPPINGS as VIDEOS_NODE_NAMES

from .video_scene_splitter import NODE_CLASS_MAPPINGS as SPLIT_NODE_CLASSES
from .video_scene_splitter import NODE_DISPLAY_NAME_MAPPINGS as SPLIT_NODE_NAMES

from .video_audio_concat import NODE_CLASS_MAPPINGS as VA_CONCAT_CLASSES
from .video_audio_concat import NODE_DISPLAY_NAME_MAPPINGS as VA_CONCAT_NAMES

from .video_mute import NODE_CLASS_MAPPINGS as MUTE_NODE_CLASSES
from .video_mute import NODE_DISPLAY_NAME_MAPPINGS as MUTE_NODE_NAMES

from .mv import NODE_CLASS_MAPPINGS as MV_NODE_CLASSES
from .mv import NODE_DISPLAY_NAME_MAPPINGS as MV_NODE_NAMES

from .rename_file import NODE_CLASS_MAPPINGS as RENAME_NODE_CLASSES
from .rename_file import NODE_DISPLAY_NAME_MAPPINGS as RENAME_NODE_NAMES

from .filter_nodes import NODE_CLASS_MAPPINGS as FILTER_NODE_CLASSES
from .filter_nodes import NODE_DISPLAY_NAME_MAPPINGS as FILTER_NODE_NAMES

from .steg_alpha_embed import NODE_CLASS_MAPPINGS as STEG_ALPHA_EMBED
from .steg_alpha_extract import NODE_CLASS_MAPPINGS as STEG_ALPHA_EXTRACT
from .steg_alpha_embed import NODE_DISPLAY_NAME_MAPPINGS as STEG_ALPHA_EMBED_NAMES
from .steg_alpha_extract import NODE_DISPLAY_NAME_MAPPINGS as STEG_ALPHA_EXTRACT_NAMES

from .steg_rgb_embed import StegRGBEmbed
from .steg_rgb_extract import StegRGBExtract

from .i2sha import ImageToSHA256

from .set_values_from_panel import NODE_CLASS_MAPPINGS as PANEL_NODE_CLASSES
from .set_values_from_panel import NODE_DISPLAY_NAME_MAPPINGS as PANEL_NODE_NAMES


NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(SORT_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(VIDEOS_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(SPLIT_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(VA_CONCAT_CLASSES)
NODE_CLASS_MAPPINGS.update(MUTE_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(MV_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(RENAME_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(FILTER_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(STEG_ALPHA_EMBED)
NODE_CLASS_MAPPINGS.update(STEG_ALPHA_EXTRACT)

NODE_CLASS_MAPPINGS.update({
    "steg_rgb_embed": StegRGBEmbed,
    "steg_rgb_extract": StegRGBExtract,
    "image_to_sha256": ImageToSHA256,
})

NODE_CLASS_MAPPINGS.update(PANEL_NODE_CLASSES)


NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(SORT_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(VIDEOS_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(SPLIT_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(VA_CONCAT_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(MUTE_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(MV_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(RENAME_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(FILTER_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(STEG_ALPHA_EMBED_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(STEG_ALPHA_EXTRACT_NAMES)

NODE_DISPLAY_NAME_MAPPINGS.update({
    "steg_rgb_embed": "Steganography: Embed String in Colors (RGB)",
    "steg_rgb_extract": "Steganography: Extract String From Colors (RGB)",
    "image_to_sha256": "Image to SHA256",
})

NODE_DISPLAY_NAME_MAPPINGS.update(PANEL_NODE_NAMES)
