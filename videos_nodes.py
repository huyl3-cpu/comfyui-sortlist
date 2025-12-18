import os
import tempfile
import subprocess
import random
import requests
import hashlib
import socket
import time
import threading

# ============================================================
# License endpoints
# - validate: kiểm tra license và tạo/duy trì session
# - heartbeat: chỉ "touch" session để cập nhật last_seen mượt (10–30s)
# ============================================================
LICENSE_SERVER = "https://license.xgroup-service.com/api/validate"
LICENSE_HEARTBEAT = "https://license.xgroup-service.com/api/heartbeat"
LICENSE_TIMEOUT = 5

# Cache validate để giảm tải server (giữ nguyên 300s theo bản cũ).
_LICENSE_CACHE = {}
_SESSION_CACHE = {}
_CACHE_TTL_SECONDS = 300

# Heartbeat: mỗi key+user chỉ chạy 1 thread (daemon)
_HEARTBEAT_THREADS = {}
_HEARTBEAT_LOCK = threading.Lock()
_HEARTBEAT_INTERVAL_SECONDS = 20  # nằm trong 10–30s


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def get_user_id() -> str:
    """User-based ID:
    - Colab: dựa trên inode Google Drive mount (ổn định hơn reset runtime)
    - Local: dựa trên home + hostname
    """
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


def _ensure_heartbeat(cache_key: str, license_key: str, user_id: str, session_id: str):
    """Start 1 daemon thread per cache_key to call /api/heartbeat every ~20s.
    This keeps 'last_seen' updating smoothly in admin dashboard without forcing /api/validate.
    """
    if not license_key or not user_id or not session_id:
        return

    with _HEARTBEAT_LOCK:
        if _HEARTBEAT_THREADS.get(cache_key):
            return
        _HEARTBEAT_THREADS[cache_key] = True

    def _loop():
        while True:
            try:
                requests.post(
                    LICENSE_HEARTBEAT,
                    json={"key": license_key, "user_id": user_id, "session_id": session_id},
                    timeout=LICENSE_TIMEOUT
                )
            except Exception:
                pass
            time.sleep(_HEARTBEAT_INTERVAL_SECONDS)

    t = threading.Thread(target=_loop, daemon=True)
    t.start()


def check_license_shared(license_key: str) -> dict:
    """Shared license check used by multiple nodes.
    - Uses cached /api/validate (TTL=300s)
    - If license is valid, starts heartbeat thread to keep session 'last_seen' fresh (10–30s)
    """
    license_key = (license_key or "").strip()
    if not license_key:
        return {"valid": False}

    user_id = get_user_id()
    cache_key = f"{license_key}:{user_id}"
    session_id = get_or_create_session_id(license_key, user_id)

    now = time.time()
    cached = _LICENSE_CACHE.get(cache_key)
    if cached and (now - cached["ts"] <= _CACHE_TTL_SECONDS):
        if cached.get("valid"):
            _ensure_heartbeat(cache_key, license_key, user_id, session_id)
        return {"valid": bool(cached.get("valid"))}

    # Nếu cache hết hạn -> gọi validate 1 lần
    try:
        r = requests.post(
            LICENSE_SERVER,
            json={"key": license_key, "user_id": user_id, "session_id": session_id},
            timeout=LICENSE_TIMEOUT
        )
        data = r.json() if r.content else {}
        valid = bool(data.get("valid"))
    except Exception:
        valid = False

    _LICENSE_CACHE[cache_key] = {"valid": valid, "ts": now}

    if valid:
        _ensure_heartbeat(cache_key, license_key, user_id, session_id)

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

        # Nếu không có license hợp lệ -> shuffle như cũ
        if not license_result.get("valid"):
            random.shuffle(videos)

        return self._merge_videos(videos, directory_path, output_filename)


NODE_CLASS_MAPPINGS = {
    "video_dir_combiner": VideoDirCombiner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "video_dir_combiner": "Video Dir Combiner"
}
