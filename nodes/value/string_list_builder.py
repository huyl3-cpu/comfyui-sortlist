"""
StringListBuilder - Gom nhiều STRING input thành 1 list.
Input slots tự động tăng thêm khi cái cuối được nối dây (via JS extension).
"""


class StringListBuilder:
    """
    Nhận nhiều STRING input (tự động mở rộng khi nối dây),
    trả về một STRING list.

    - Mỗi input là một string riêng biệt (1 slot = 1 phần tử trong list)
    - Khi nối dây vào slot cuối cùng, slot mới tự động được thêm vào
    - Slot rỗng ở cuối tự động bị dọn khi ngắt kết nối
    - Output là LIST of STRING
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "string_1": ("STRING", {"forceInput": True}),
                "string_2": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string_list",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "build"
    CATEGORY = "sortlist/value"
    DESCRIPTION = (
        "Gom nhiều STRING input thành một danh sách (LIST). "
        "Số lượng input tự động tăng khi nối dây vào slot cuối cùng."
    )

    def build(self, **kwargs):
        result = []
        i = 1
        while True:
            key = f"string_{i}"
            if key not in kwargs:
                break
            val = kwargs[key]
            if val is not None:
                result.append(str(val))
            i += 1

        # Đảm bảo luôn trả về ít nhất 1 phần tử để tránh lỗi downstream
        if not result:
            result = [""]

        return (result,)


NODE_CLASS_MAPPINGS = {
    "StringListBuilder": StringListBuilder,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringListBuilder": "String List Builder 📝",
}
