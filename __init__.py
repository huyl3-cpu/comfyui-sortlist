# ============================
# comfyui-sortlist __init__.py
# ============================

# Sort node
from .sort_nodes import NODE_CLASS_MAPPINGS as SORT_NODE_CLASSES
from .sort_nodes import NODE_DISPLAY_NAME_MAPPINGS as SORT_NODE_NAMES

# Video node
from .video_nodes import NODE_CLASS_MAPPINGS as VIDEO_NODE_CLASSES
from .video_nodes import NODE_DISPLAY_NAME_MAPPINGS as VIDEO_NODE_NAMES

# -----------------------------
# NEW: Video Scene Splitter
# -----------------------------
from .video_scene_splitter import NODE_CLASS_MAPPINGS as SPLIT_NODE_CLASSES
from .video_scene_splitter import NODE_DISPLAY_NAME_MAPPINGS as SPLIT_NODE_NAMES

# -----------------------------
# NEW: Move File (mv.py)
# -----------------------------
from .mv import NODE_CLASS_MAPPINGS as MV_NODE_CLASSES
from .mv import NODE_DISPLAY_NAME_MAPPINGS as MV_NODE_NAMES

# Filter node
from .filter_nodes import NODE_CLASS_MAPPINGS as FILTER_NODE_CLASSES
from .filter_nodes import NODE_DISPLAY_NAME_MAPPINGS as FILTER_NODE_NAMES

# Old steganography alpha nodes
from .steg_alpha_embed import NODE_CLASS_MAPPINGS as STEG_ALPHA_EMBED
from .steg_alpha_extract import NODE_CLASS_MAPPINGS as STEG_ALPHA_EXTRACT
from .steg_alpha_embed import NODE_DISPLAY_NAME_MAPPINGS as STEG_ALPHA_EMBED_NAMES
from .steg_alpha_extract import NODE_DISPLAY_NAME_MAPPINGS as STEG_ALPHA_EXTRACT_NAMES

# New steganography RGB nodes
from .steg_rgb_embed import StegRGBEmbed
from .steg_rgb_extract import StegRGBExtract

# NEW NODE: Image to SHA256
from .i2sha import ImageToSHA256

# 🌟 NEW: Set Values From Panel
from .set_values_from_panel import NODE_CLASS_MAPPINGS as PANEL_NODE_CLASSES
from .set_values_from_panel import NODE_DISPLAY_NAME_MAPPINGS as PANEL_NODE_NAMES


# ============================
# Register all nodes
# ============================

NODE_CLASS_MAPPINGS = {}

NODE_CLASS_MAPPINGS.update(SORT_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(VIDEO_NODE_CLASSES)

# Add NEW Video Scene Splitter
NODE_CLASS_MAPPINGS.update(SPLIT_NODE_CLASSES)

# Add NEW Move File node
NODE_CLASS_MAPPINGS.update(MV_NODE_CLASSES)

NODE_CLASS_MAPPINGS.update(FILTER_NODE_CLASSES)
NODE_CLASS_MAPPINGS.update(STEG_ALPHA_EMBED)
NODE_CLASS_MAPPINGS.update(STEG_ALPHA_EXTRACT)

# Add RGB steganography nodes
NODE_CLASS_MAPPINGS.update({
    "steg_rgb_embed": StegRGBEmbed,
    "steg_rgb_extract": StegRGBExtract,
})

# Add Image to SHA256 node
NODE_CLASS_MAPPINGS.update({
    "image_to_sha256": ImageToSHA256,
})

# 🌟 Add NEW SetValuesFromPanel node
NODE_CLASS_MAPPINGS.update(PANEL_NODE_CLASSES)


# ============================
# Display names mapping
# ============================

NODE_DISPLAY_NAME_MAPPINGS = {}

NODE_DISPLAY_NAME_MAPPINGS.update(SORT_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(VIDEO_NODE_NAMES)

# Add NEW Video Scene Splitter display name
NODE_DISPLAY_NAME_MAPPINGS.update(SPLIT_NODE_NAMES)

# Add NEW Move File display name
NODE_DISPLAY_NAME_MAPPINGS.update(MV_NODE_NAMES)

NODE_DISPLAY_NAME_MAPPINGS.update(FILTER_NODE_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(STEG_ALPHA_EMBED_NAMES)
NODE_DISPLAY_NAME_MAPPINGS.update(STEG_ALPHA_EXTRACT_NAMES)

NODE_DISPLAY_NAME_MAPPINGS.update({
    "steg_rgb_embed": "Steganography: Embed String in Colors (RGB)",
    "steg_rgb_extract": "Steganography: Extract String From Colors (RGB)",
    "image_to_sha256": "Image to SHA256",
})

# 🌟 Add NEW SetValuesFromPanel display name
NODE_DISPLAY_NAME_MAPPINGS.update(PANEL_NODE_NAMES)
