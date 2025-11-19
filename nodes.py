# comfyui-huyl2-nodes/nodes.py

import os
import re
import random


class SortListV2_huyl2:
    """
    sort list v2 (huyl2)
    - Bản nâng cấp của Sort List (TinyBee) + thêm mode 'numeric'
    - Các mode:
        default      : sort theo chuỗi
        filename     : sort theo tên file (basename)
        parent folder: sort theo tên thư mục cha
        full path    : sort theo full string
        numeric      : sort theo số trong tên file (1, 2, 10, 11, ...)
        date         : sort theo thời gian chỉnh sửa file
        random       : trộn ngẫu nhiên với seed
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_list": ("LIST",),
                "sort_method": ([
                    "default",
                    "filename",
                    "parent folder",
                    "full path",
                    "numeric",
                    "date",
                    "random",
                ], {"default": "filename"}),
                "sort_ascending": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2**31 - 1,
                    "step": 1,
                }),
            }
        }

    RETURN_TYPES = ("LIST",)
    FUNCTION = "sort_list_v2"
    CATEGORY = "huyl2"          # category xuất hiện trong menu node

    # -------- helpers --------
    @staticmethod
    def _extract_number(path_str: str) -> int:
        """
        Lấy số cuối trong tên file.
        Ví dụ: LTT-12_a_3.mp4 -> 3
        Nếu không có số -> trả về số rất lớn để đẩy xuống cuối.
        """
        base = os.path.basename(path_str)
        nums = re.findall(r"\d+", base)
        if not nums:
            return 10**12
        return int(nums[-1])

    # -------- main --------
    def sort_list_v2(self, string_list, sort_method, sort_ascending, seed):
        # đảm bảo là list string
        items = [str(x) for x in (string_list or [])]
        reverse = not bool(sort_ascending)

        if sort_method == "default":
            sorted_list = sorted(items, reverse=reverse)

        elif sort_method == "filename":
            sorted_list = sorted(
                items,
                key=lambda p: os.path.basename(p),
                reverse=reverse,
            )

        elif sort_method == "parent folder":
            sorted_list = sorted(
                items,
                key=lambda p: os.path.basename(os.path.dirname(p)),
                reverse=reverse,
            )

        elif sort_method == "full path":
            sorted_list = sorted(items, key=lambda p: p, reverse=reverse)

        elif sort_method == "numeric":
            sorted_list = sorted(
                items,
                key=lambda p: self._extract_number(p),
                reverse=reverse,
            )

        elif sort_method == "date":
            def _mtime_safe(p):
                try:
                    return os.path.getmtime(p)
                except Exception:
                    return 0.0

            sorted_list = sorted(
                items,
                key=_mtime_safe,
                reverse=reverse,
            )

        elif sort_method == "random":
            rnd = random.Random(int(seed))
            sorted_list = items[:]
            rnd.shuffle(sorted_list)

        else:
            sorted_list = items

        return (sorted_list,)


# Bắt buộc để ComfyUI nhận node
NODE_CLASS_MAPPINGS = {
    "SortListV2_huyl2": SortListV2_huyl2,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SortListV2_huyl2": "sort list v2 (huyl2)",
}
