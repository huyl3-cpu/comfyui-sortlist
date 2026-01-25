# Ví dụ sử dụng Video Cut Node trong ComfyUI Workflow

## Workflow đơn giản (Simple Workflow)

```
[Video Cut to 8s Segments]
├─ video_url: "/content/drive/MyDrive/girl/djaskd1.mp4"
├─ segment_duration: 8
├─ output_prefix: "a"
└─ OUTPUT: videos_list → Danh sách các video đã cắt
```

## Workflow nâng cao (Advanced Workflow)

Bạn có thể kết hợp node này với các node khác để xử lý video:

### 1. Cắt video + Xử lý từng segment

```
[Video Cut to 8s Segments] 
    ↓ videos_list
[String Split] (split by comma)
    ↓ individual video paths
[Loop/Iterate each video]
    ↓
[Your processing node] (e.g., upscale, filter, etc.)
    ↓
[Save/Output]
```

### 2. Cắt nhiều video cùng lúc

```python
# Ví dụ code Python để cắt nhiều video
video_urls = [
    "/content/drive/MyDrive/girl/video1.mp4",
    "/content/drive/MyDrive/girl/video2.mp4",
    "/content/drive/MyDrive/girl/video3.mp4"
]

for i, url in enumerate(video_urls):
    # Sử dụng node với prefix khác nhau cho mỗi video
    prefix = f"video{i+1}"
    # Node sẽ tạo: video1-1.mp4, video1-2.mp4, ...
    #              video2-1.mp4, video2-2.mp4, ...
```

## Kết hợp với các node khác trong comfyui-sortlist

### Example 1: Cắt video và rename

```
[Video Cut to 8s Segments]
    ↓ videos_list
[String to List Converter]
    ↓
[Rename File Node]
    ↓
[New organized videos]
```

### Example 2: Cắt video và lọc

```
[Video Cut to 8s Segments]
    ↓ videos_list
[Video Frame Guard] (chỉ giữ video có đủ frames)
    ↓
[Filtered videos]
```

## Custom prefix cho các mục đích khác nhau

```
Cắt video cho training: output_prefix = "train"
→ train-1.mp4, train-2.mp4, train-3.mp4

Cắt video cho testing: output_prefix = "test"
→ test-1.mp4, test-2.mp4, test-3.mp4

Cắt video theo scene: output_prefix = "scene"
→ scene-1.mp4, scene-2.mp4, scene-3.mp4
```

## Xử lý danh sách output

Output `videos_list` là một string với các đường dẫn phân cách bởi dấu phẩy. 
Bạn có thể xử lý nó như sau:

### Trong Python:
```python
videos_list = "/path/to/a-1.mp4,/path/to/a-2.mp4,/path/to/a-3.mp4"
video_paths = videos_list.split(",")

for path in video_paths:
    print(f"Processing: {path}")
    # Xử lý từng video
```

### Trong ComfyUI workflow:
- Sử dụng node "String to List" hoặc tương tự để tách danh sách
- Iterate qua từng video path
- Áp dụng các xử lý bạn cần

## Troubleshooting

### Lỗi: "Video file not found"
→ Kiểm tra đường dẫn video_url có đúng không

### Lỗi: "Failed to get video duration"
→ Đảm bảo FFmpeg và FFprobe đã được cài đặt

### Video bị mất âm thanh
→ Node này giữ nguyên audio. Nếu video gốc không có audio, các segment cũng sẽ không có.

### Segment cuối cùng ngắn hơn 8 giây
→ Đây là hành vi bình thường. Segment cuối sẽ chứa phần còn lại của video.
