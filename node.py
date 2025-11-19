import os
import re
import random
import subprocess
import tempfile


# =========================
# 1. SORT LIST STRING NODE
# =========================
class SortListString:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "list_string": ("STRING", {"forceInput": True}),
                "sort_method": (
                    [
                        "default",       # so sánh nguyên chuỗi
                        "filename",      # theo tên file
                        "parent_folder", # theo thư mục cha
                        "full_path",     # giống default (để cho dễ hiểu)
                        "numeric",       # sort theo số trong tên file (LTT-1,2,3,...)
                        "date",          # sort theo chuỗi số kiểu ngày (20251119...)
                        "random",        # xáo trộn
                    ],
                    {"default": "numeric"},
                ),
                "sort_ascending": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("sorted_list",)
    FUNCTION = "sort_list"
    CATEGORY = "custom/sortlist"

    # ---------- Helpers ----------

    @staticmethod
    def _get_filename(path: str) -> str:
        return os.path.basename(path)

    @staticmethod
    def _get_parent_folder(path: str) -> str:
        return os.path.basename(os.path.dirname(path))

    @staticmethod
    def _natural_numeric_key(text: str):
        """
        Natural sort theo tất cả các cụm số trong chuỗi.

        Ví dụ:
        'LTT-1_00001.mp4'   -> (1, 1)
        'LTT-10_00001.mp4'  -> (10, 1)
        'LTT-35_00001.mp4'  -> (35, 1)

        => đảm bảo thứ tự: 1,2,3,...,9,10,11,...,35
        """
        nums = re.findall(r'\d+', text)
        if not nums:
            return (99999999,)
        return tuple(int(n) for n in nums)

    @staticmethod
    def _date_key(text: str):
        """
        Sort kiểu 'date' đơn giản:
        Ghép tất cả số lại thành một int.

        Ví dụ:
        'clip_20251119_123045.mp4' -> 20251119123045
        """
        nums = re.findall(r'\d+', text)
        if not nums:
            return 0
        return int("".join(nums))

    # ---------- Main ----------

    def sort_list(self, list_string, sort_method, sort_ascending):
        # Tách từng dòng thành 1 phần tử
        items = [i.strip() for i in list_string.split("\n") if i.strip()]

        if not items:
            return ("",)

        # Chọn key sort theo sort_method
        if sort_method in ("default", "full_path"):
            key_func = lambda x: x
        elif sort_method == "filename":
            key_func = lambda x: self._get_filename(x)
        elif sort_method == "parent_folder":
            key_func = lambda x: self._get_parent_folder(x)
        elif sort_method == "numeric":
            # Natural numeric sort theo FILENAME để tránh dính số trong path
            key_func = lambda x: self._natural_numeric_key(self._get_filename(x))
        elif sort_method == "date":
            # Dựa trên chuỗi số trong FILENAME (thường chứa ngày/giờ)
            key_func = lambda x: self._date_key(self._get_filename(x))
        elif sort_method == "random":
            # Random thì không dùng sorted, mà shuffle luôn
            random_items = items[:]
            random.shuffle(random_items)
            return ("\n".join(random_items),)
        else:
            # fallback
            key_func = lambda x: x

        items_sorted = sorted(
            items,
            key=key_func,
            reverse=not sort_ascending
        )

        return ("\n".join(items_sorted),)


# ==============================
# 2. VIDEO DIR COMBINER NODE
# ==============================
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
            # Nếu không có dir, dùng hiện tại
            dir_path = directory_path if directory_path else "."
            out_path = os.path.join(dir_path, output_filename)

        # Thêm đuôi .mp4 nếu chưa có
        root, ext = os.path.splitext(out_path)
        if ext == "":
            out_path = root + ".mp4"

        # Tạo thư mục nếu chưa tồn tại
        out_dir = os.path.dirname(out_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        return os.path.abspath(out_path)

    def combine_videos(self, video_list, directory_path, output_filename):
        # Parse list video
        videos = [v.strip() for v in video_list.split("\n") if v.strip()]

        if len(videos) == 0:
            print("[video_dir_combiner] No videos in list.")
            return ("",)

        out_path = self._build_output_path(directory_path, output_filename)

        # Tạo file tạm chứa danh sách video cho ffmpeg concat
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f:
            list_file = f.name
            for v in videos:
                # Cho phép path có khoảng trắng, dùng format chuẩn concat
                f.write(f"file '{v}'\n")

        # Gộp bằng ffmpeg
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
                # nếu lỗi, trả về chuỗi rỗng
                return ("",)
        except Exception as e:
            print(f"[video_dir_combiner] Exception: {e}")
            return ("",)

        return (out_path,)


# =========================
# NODE MAPPINGS
# =========================
NODE_CLASS_MAPPINGS = {
    "sort_list_string": SortListString,
    "video_dir_combiner": VideoDirCombiner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "sort_list_string": "Sort List String",
    "video_dir_combiner": "Video Dir Combiner",
}
