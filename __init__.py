WEB_DIRECTORY = "."

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

def _safe_merge(module_name: str):
    global NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
    try:
        mod = __import__(f"{__name__}.{module_name}", fromlist=["*"])
        cls_map = getattr(mod, "NODE_CLASS_MAPPINGS", None)
        name_map = getattr(mod, "NODE_DISPLAY_NAME_MAPPINGS", None)

        if isinstance(cls_map, dict):
            NODE_CLASS_MAPPINGS.update(cls_map)
        if isinstance(name_map, dict):
            NODE_DISPLAY_NAME_MAPPINGS.update(name_map)

    except Exception as e:
        print(f"[comfyui-sortlist] Skipped '{module_name}' due to import error: {e}")


_safe_merge("sort_nodes")
_safe_merge("videos_nodes")
_safe_merge("video_scene_splitter")
_safe_merge("video_audio_concat")
_safe_merge("video_mute")
_safe_merge("mv")
_safe_merge("rename_file")
_safe_merge("filter_nodes")

_safe_merge("steg_alpha_embed")
_safe_merge("steg_alpha_extract")

try:
    from .steg_rgb_extract import StegRGBExtract
    NODE_CLASS_MAPPINGS.update({"steg_rgb_extract": StegRGBExtract})
    NODE_DISPLAY_NAME_MAPPINGS.update({
        "steg_rgb_extract": "Steganography: Extract String From Colors (RGB)",
    })
except Exception as e:
    print(f"[comfyui-sortlist] Skipped 'steg_rgb_extract' due to import error: {e}")

try:
    from .i2sha import ImageToSHA256
    NODE_CLASS_MAPPINGS.update({"image_to_sha256": ImageToSHA256})
    NODE_DISPLAY_NAME_MAPPINGS.update({"image_to_sha256": "Image to SHA256"})
except Exception as e:
    print(f"[comfyui-sortlist] Skipped 'i2sha' due to import error: {e}")

_safe_merge("set_values_from_panel")

# giữ nguyên phần video_frame_guard (bọc try để không làm chết toàn bộ package)
try:
    from .video_frame_guard import VHS_VideoFrameGuard, VHS_VideoPickMinFrames
    NODE_CLASS_MAPPINGS.update({
        "VHS_VideoFrameGuard": VHS_VideoFrameGuard,
        "VHS_VideoPickMinFrames": VHS_VideoPickMinFrames,
    })
    NODE_DISPLAY_NAME_MAPPINGS.update({
        "VHS_VideoFrameGuard": "Video Frame Guard (<=210 frames)",
        "VHS_VideoPickMinFrames": "Pick Video With Min Frames",
    })
except Exception as e:
    print(f"[comfyui-sortlist] Skipped 'video_frame_guard' due to import error: {e}")

# QUAN TRỌNG: import value CUỐI để override node Set Value
_safe_merge("value")
