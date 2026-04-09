"""
StringListBuilder - Gom nhiều STRING input thành 1 list.
Dựa vào giá trị từ `input_count` để điều chỉnh số lượng dây (siêu nhẹ, không dùng onConnectionsChange).
"""


class StringListBuilder:
    """
    Nhận nhiều STRING input xác định bởi `input_count`,
    trả về một STRING list.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_count": ("INT", {"default": 2, "min": 1, "max": 100, "step": 1}),
            },
            "optional": {
                # Các slot string_1, string_2... sẽ được thêm động bằng JS khi đổi input_count
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string_list",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "build"
    CATEGORY = "sortlist/value"
    DESCRIPTION = (
        "Gom nhiều STRING input thành một danh sách (LIST). "
        "Số lượng input do bạn tự tùy chỉnh bằng thanh 'input_count' cực kỳ nhẹ."
    )

    def build(self, input_count, **kwargs):
        result = []
        
        # Duyệt đúng số lượng input_count mà node yêu cầu
        for i in range(1, input_count + 1):
            key = f"string_{i}"
            val = kwargs.get(key)
            if val is not None:
                result.append(str(val))
            # Nếu người dùng không nối dây, ô đó bị bỏ qua, không gây đứt gãy list
                
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
