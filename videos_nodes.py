import os
import tempfile
import subprocess
import random
import requests
import hashlib
import socket
import time

LICENSE_SERVER = "https://license.xgroup-service.com/api/validate"
LICENSE_TIMEOUT = 5

_LICENSE_CACHE = {}
_SESSION_CACHE = {}
_CACHE_TTL_SECONDS = 300


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def get_user_id() -> str:
    drive_path = "/content/drive/MyDrive"
    try:
        if os.path.exists(drive_path):
            st = os.stat(drive_path)
            raw = f"colab_drive:{st.st_dev}:{st.st_ino}"
            return _sha256_hex(raw)[:16]
    except Exception:
        pass

    try:
        home = os.path.expanduser("~")
        raw = f"local:{home}:{socket.gethostname()}"
        return _sha256_hex(raw)[:16]
    except Exception:
        return "local-user"


def get_or_create_session_id(license_key: str, user_id: str) -> str:
    k = f"{license_key.strip()}:{user_id}"
    if k in _SESSION_CACHE:
        return _SESSION_CACHE[k]
    sid = _sha256_hex(k + ":" + str(time.time()))[:16]
    _SESSION_CACHE[k] = sid
    return sid


def check_license_shared(license_key: str) -> dict:
    license_key = (license_key or "").strip()
    if not license_key:
        return {"valid": False}

    user_id = get_user_id()
    cache_key = f"{license_key}:{user_id}"

    now = time.time()
    cached = _LICENSE_CACHE.get(cache_key)
    if cached and (now - cached["ts"] <= _CACHE_TTL_SECONDS):
        return {"valid": cached["valid"]}

    session_id = get_or_create_session_id(license_key, user_id)

    try:
        r = requests.post(
            LICENSE_SERVER,
            json={
                "key": license_key,
                "user_id": user_id,
                "session_id": session_id,
            },
            timeout=LICENSE_TIMEOUT
        )
        data = r.json() if r.content else {}
        valid = bool(data.get("valid"))
    except Exception:
        valid = False

    _LICENSE_CACHE[cache_key] = {"valid": valid, "ts": now}
    return {"valid": valid}


class VideoDirCombiner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "video_list": ("STRING", {"multiline": True}),
                "directory_path": ("STRING", {"default": ""}),
                "output_filename": ("STRING", {"default": "output.mp4"}),
                "license_key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "run"
    CATEGORY = "video"

    def _merge_videos(self, video_paths, output_dir, output_name):
        if not output_name.endswith(".mp4"):
            output_name += ".mp4"

        output_dir = output_dir if output_dir else "."
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_name)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            for v in video_paths:
                f.write(f"file '{v}'\n")
            list_file = f.name

        subprocess.run(
            [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-c", "copy",
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return (output_path,)

    def run(self, image, video_list, directory_path, output_filename, license_key):
        videos = [v.strip() for v in video_list.split("\n") if v.strip()]
        if not videos:
            raise ValueError("video_list is empty")

        license_result = check_license_shared(license_key)

        if not license_result.get("valid"):
            random.shuffle(videos)

        return self._merge_videos(videos, directory_path, output_filename)


NODE_CLASS_MAPPINGS = {
    "video_dir_combiner": VideoDirCombiner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "video_dir_combiner": "Video Dir Combiner"
}
