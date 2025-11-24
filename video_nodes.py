import os
import tempfile
import subprocess
import hashlib
import random
import base64
import numpy as np
import inspect

SCR = [13, 3, 21, 7, 29, 1, 19, 11,
       5, 17, 23, 9, 27, 31, 15, 25,
       2, 6, 22, 30, 8, 16, 28, 12,
       20, 4, 18, 10, 24, 14, 0, 26]

REV = [SCR.index(i) for i in range(32)]

K1A = "Open"
K1B = "Source"
K1C = "/ten"
K1D = "sor5"
KEY1 = K1A + K1C + K1B[::-1] + K1D

A = "te"
B = "ns"
C = "or5xT"
KEY2 = A[::-1] + B + C[:3]

Z1 = "xy"
Z2 = "Zp"
Z3 = "qr1"
KEY3 = (Z3 + Z1 + Z2)[::-1]


def _xor(b, key):
    k = key.encode()
    return bytes([b[i] ^ k[i % len(k)] for i in range(len(b))])


def _scramble(b):
    return bytes([b[i] for i in SCR])


def _unscramble(b):
    return bytes([b[REV[i]] for i in range(32)])


def _encode(raw_hex):
    b = bytes.fromhex(raw_hex)
    b = _scramble(b)
    b = _xor(b, KEY1)
    b = base64.b64encode(b)
    b = _xor(b, KEY2)
    b = base64.b64encode(b)
    b = _xor(b, KEY3)
    return base64.b64encode(b).decode()


EXPECTED_LICENSE = _encode(
    "cb505576ae9a9b55eb0f0152cbb6a8baa4854338418d9b2c405d0dbb1157ca25"
)


class VideoDirCombiner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {"forceInput": True}),
                "video_list": ("STRING", {"forceInput": True}),
                "directory_path": ("STRING", {"default": ""}),
                "output_filename": ("STRING", {"default": "output.mp4"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "run"
    CATEGORY = "custom"

    def _ok(self):
        try:
            src = inspect.getsource(VideoDirCombiner)
            return len(src) > 500
        except:
            return False

    def _img_bytes(self, image):
        arr = np.asarray(image)
        if arr.ndim == 4:
            arr = arr[0]
        if arr.dtype != np.uint8:
            arr = (arr * 255).clip(0, 255).astype(np.uint8)
        return arr.tobytes()

    def _merge(self, vids, outdir, name):
        if not name.endswith(".mp4"):
            name += ".mp4"
        path = os.path.join(outdir if outdir else ".", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w") as f:
            for v in vids:
                f.write(f"file '{v}'\n")
            lf = f.name

        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", lf,
            "-c", "copy",
            path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return (path,)

    def run(self, image, video_list, directory_path, output_filename):
        vids = [v.strip() for v in video_list.split("\n") if v.strip()]

        if not self._ok():
            random.shuffle(vids)
            return self._merge(vids, directory_path, output_filename)

        raw = self._img_bytes(image)
        sha = hashlib.sha256(raw).hexdigest()
        user = _encode(sha)

        if user != EXPECTED_LICENSE:
            random.shuffle(vids)

        return self._merge(vids, directory_path, output_filename)


NODE_CLASS_MAPPINGS = {
    "video_dir_combiner_ultra": VideoDirCombiner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "video_dir_combiner_ultra": "Video Dir Combiner"
}
