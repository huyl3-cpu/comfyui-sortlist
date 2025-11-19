import os
import tempfile
import subprocess


class VideoDirCombiner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_list": ("STRING", {"forceInput": True}),
                "directory_path": ("STRING", {"default": ""}),
                "output_filename": ("STRING", {"default": "all.mp4"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "combine_videos"
    CATEGORY = "custom/sortlist"

    def _build_output_path(self, directory_path: str, output_filename: str) -> str:
        # Nếu output_filename đã là full path tuyệt đối -> dùng luôn
        if os.path.isabs(output_filename):
            out_path = output_filename
        else:
            dir_path = directory_path if directory_path else "."
            out_path = os.path.join(dir_path, output_filename)

        # Thêm .mp4 nếu thiếu
        root, ext = os.path.splitext(out_path)
        if ext == "":
            out_path = root + ".mp4"

        # Tạo thư mục nếu chưa tồn tại
        out_dir = os.path.dirname(out_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        return os.path.abspath(out_path)

    def combine_videos(self, video_list, directory_path, output_filename):
        videos = [v.strip() for v in video_list.split("\n") if v.strip()]

        if len(videos) == 0:
            print("[video_dir_combiner] No videos in list.")
            return ("",)

        out_path = self._build_output_path(directory_path, output_filename)

        # File tạm chứa danh sách video cho ffmpeg concat
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f:
            list_file = f.name
            for v in videos:
                f.write(f"file '{v}'\n")

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            out_path,
        ]

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if proc.returncode != 0:
                print("[video_dir_combiner] ffmpeg error:")
                print(proc.stderr)
                return ("",)
        except Exception as e:
            print(f"[video_dir_combiner] Exception: {e}")
            return ("",)

        return (out_path,)


NODE_CLASS_MAPPINGS = {
    "video_dir_combiner": VideoDirCombiner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "video_dir_combiner": "Video Dir Combiner"
}
