"""
StringConcat - Gộp nhiều STRING input thành 1 list.
Dựa vào giá trị từ `input_count` để xác định số đầu vào. Mọi string sẽ được gộp và tách lại bằng dấu xuống dòng.
"""


class StringConcat:
    """
    Nhận nhiều STRING input xác định bởi `input_count`.
    Gộp tất cả lại thành 1 string duy nhất (có thể nhiều dòng).
    Sau đó phân tách các dòng tạo thành một STRING list.
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
        "Gộp nhiều STRING input lại, sau đó tách mỗi dòng thành 1 phần tử danh sách (LIST). "
    )

    def build(self, input_count, **kwargs):
        texts = []
        
        # Đọc dữ liệu từ tất cả slot đang cắm
        for i in range(1, input_count + 1):
            key = f"string_{i}"
            val = kwargs.get(key)
            if val is not None and str(val).strip():
                texts.append(str(val))
                
        # Gộp tất cả string đã nhận
        full_text = "\n".join(texts)
        
        # Tách từng dòng làm 1 string trong list (bỏ qua dòng trống)
        result = [line.strip() for line in full_text.split("\n") if line.strip()]

        # Đảm bảo luôn trả về ít nhất 1 phần tử để tránh lỗi downstream
        if not result:
            result = [""]

        return (result,)


NODE_CLASS_MAPPINGS = {
    "StringConcat": StringConcat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringConcat": "String Concat 🔤",
}
