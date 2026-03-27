"""
Split MP3 V2 Node for ComfyUI
Cắt file MP3 thành các đoạn tối đa 3 phút.
- Nếu file < 3 phút: không cắt, trả về file gốc
- Nếu file >= 3 phút: cắt thành các đoạn 3 phút, đoạn cuối là phần dư
"""

import os
import subprocess
import json
import math


MAX_DURATION_SEC = 180  # 3 phút = 180 giây


class SplitMP3V2Node:
    """
    Cắt file MP3 thành các đoạn tối đa 3 phút (180 giây).

    Rules:
    - duration <= 180s : không cắt, output = [file gốc]
    - duration >  180s : cắt thành [0-180s], [180-360s], ..., [phần dư]

    Output: list đầy đủ path các file đã cắt + tổng số file.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mp3_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn file MP3",
                    "tooltip": "Đường dẫn tuyệt đối đến file .mp3",
                }),
                "output_folder": ("STRING", {
                    "default": "/content/ComfyUI/output/mp3_split",
                    "multiline": False,
                    "placeholder": "Thư mục lưu file output",
                    "tooltip": "Thư mục lưu các file sau khi cắt",
                }),
            },
            "optional": {
                "max_minutes": ("FLOAT", {
                    "default": 3.0,
                    "min": 0.5,
                    "max": 60.0,
                    "step": 0.5,
                    "tooltip": "Độ dài tối đa mỗi đoạn (phút). Mặc định 3 phút.",
                }),
            },
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("file_paths", "count")
    FUNCTION = "split"
    CATEGORY = "utils"
    DESCRIPTION = """
    Cắt file MP3 thành từng đoạn tối đa N phút (mặc định 3 phút).

    - Nếu duration <= max_minutes: không cắt, trả về file gốc
    - Nếu duration >  max_minutes: cắt thành nhiều đoạn, đoạn cuối = phần dư

    Output:
    - file_paths : STRING hiển thị tất cả path (mỗi file 1 dòng)
    - count      : tổng số file output (INT)
    """

    def _get_duration(self, mp3_path: str) -> float:
        """Lấy độ dài file MP3 bằng ffprobe (giây)."""
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            mp3_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"[SplitMP3V2] ffprobe lỗi: {result.stderr}")
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])

    def _run_ffmpeg(self, input_path: str, start: float, duration: float, output_path: str) -> bool:
        """Cắt 1 đoạn bằng ffmpeg, trả về True nếu thành công."""
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-ss", f"{start:.3f}",
            "-t",  f"{duration:.3f}",
            "-c", "copy",
            "-avoid_negative_ts", "make_zero",
            output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[SplitMP3V2] ⚠️ ffmpeg lỗi: {result.stderr[-300:]}")
            return False
        return True

    def split(self, mp3_path: str, output_folder: str, max_minutes: float = 3.0):
        mp3_path = mp3_path.strip().strip('"').strip("'")

        if not mp3_path or not os.path.isfile(mp3_path):
            raise FileNotFoundError(f"[SplitMP3V2] File không tồn tại: '{mp3_path}'")

        max_sec = max_minutes * 60.0

        # Lấy độ dài file gốc
        duration = self._get_duration(mp3_path)
        base_name = os.path.splitext(os.path.basename(mp3_path))[0]

        print(
            f"[SplitMP3V2] {base_name}.mp3 | duration={duration:.1f}s "
            f"| max={max_sec:.0f}s ({max_minutes}min)"
        )

        # Nếu file ngắn hơn hoặc bằng giới hạn → không cắt
        if duration <= max_sec:
            print(f"[SplitMP3V2] ✅ Không cắt (duration <= {max_minutes} phút), trả về file gốc.")
            return (mp3_path, 1)

        # Tính các segment
        num_full = int(duration // max_sec)
        remainder = duration - num_full * max_sec

        segments = []
        for i in range(num_full):
            segments.append((i * max_sec, max_sec))
        if remainder > 0.5:  # bỏ qua nếu quá ngắn (<0.5s)
            segments.append((num_full * max_sec, remainder))

        print(f"[SplitMP3V2] Cắt thành {len(segments)} đoạn...")

        # Tạo thư mục output
        os.makedirs(output_folder, exist_ok=True)

        # Thực hiện cắt
        output_files = []
        for idx, (start, dur) in enumerate(segments, start=1):
            out_file = os.path.join(output_folder, f"{base_name}_{idx:03d}.mp3")
            success = self._run_ffmpeg(mp3_path, start, dur, out_file)
            if success:
                output_files.append(out_file)
                print(f"[SplitMP3V2]   [{idx:03d}] {start:.1f}s → {start+dur:.1f}s → {out_file}")
            else:
                print(f"[SplitMP3V2]   [{idx:03d}] ❌ Cắt thất bại")

        print(f"[SplitMP3V2] ✅ Xong: {len(output_files)}/{len(segments)} file")
        result_str = "\n".join(output_files)
        return (result_str, len(output_files))


# Node registration
NODE_CLASS_MAPPINGS = {
    "SplitMP3V2": SplitMP3V2Node,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SplitMP3V2": "Split MP3 V2 (3min segments) ✂️",
}
