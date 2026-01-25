# Video Cut to Segments Node

## Mô tả (Description)
Node này cắt video thành các đoạn nhỏ với độ dài cố định (mặc định 8 giây).

This node cuts a video into small segments with a fixed duration (default 8 seconds).

## Input Parameters

1. **video_url** (STRING): Đường dẫn đến file video gốc
   - Example: `/content/drive/MyDrive/girl/djaskd1.mp4`
   - Hoặc (Or): `c:\Users\lehie\Videos\example.mp4`

2. **segment_duration** (INT): Độ dài mỗi đoạn video (giây)
   - Mặc định (Default): 8 giây
   - Khoảng giá trị (Range): 1 - 3600 giây

3. **output_prefix** (STRING): Tiền tố tên file cho các video đã cắt
   - Mặc định (Default): "a"
   - Kết quả (Result): a-1.mp4, a-2.mp4, a-3.mp4, ...

## Output

**videos_list** (STRING): Danh sách các đường dẫn video đã cắt, phân cách bởi dấu phẩy

Example output:
```
/content/drive/MyDrive/girl/videos_cut/a-1.mp4,/content/drive/MyDrive/girl/videos_cut/a-2.mp4,/content/drive/MyDrive/girl/videos_cut/a-3.mp4
```

## Cách hoạt động (How it works)

1. Kiểm tra file video có tồn tại không
2. Tạo thư mục `videos_cut` trong cùng thư mục với video gốc
3. Sử dụng `ffprobe` để lấy độ dài video
4. Tính số lượng segment cần cắt
5. Sử dụng `ffmpeg` để cắt video thành các segment
6. Trả về danh sách các đường dẫn video đã cắt

## Ví dụ (Example)

**Input:**
- video_url: `/content/drive/MyDrive/girl/djaskd1.mp4`
- segment_duration: `8`
- output_prefix: `a`

**Output directory structure:**
```
/content/drive/MyDrive/girl/
├── djaskd1.mp4 (video gốc)
└── videos_cut/
    ├── a-1.mp4 (0-8s)
    ├── a-2.mp4 (8-16s)
    ├── a-3.mp4 (16-24s)
    └── ...
```

**Output:**
```
videos_list = "/content/drive/MyDrive/girl/videos_cut/a-1.mp4,/content/drive/MyDrive/girl/videos_cut/a-2.mp4,/content/drive/MyDrive/girl/videos_cut/a-3.mp4"
```

## Yêu cầu hệ thống (System Requirements)

- FFmpeg phải được cài đặt và có trong PATH
- FFprobe (đi kèm với FFmpeg)

## Lưu ý (Notes)

- Video được cắt sẽ được mã hóa lại bằng codec H.264 (video) và AAC (audio)
- Nếu segment cuối cùng ngắn hơn `segment_duration`, nó vẫn sẽ được tạo với độ dài còn lại
- Thư mục `videos_cut` sẽ được tạo tự động nếu chưa tồn tại
