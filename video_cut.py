import os
import subprocess
import math

class VideoCutToSegments:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "segment_duration": ("INT", {"default": 8, "min": 1, "max": 3600}),
                "output_prefix": ("STRING", {"default": "a"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("videos_list",)
    FUNCTION = "cut_video"
    CATEGORY = "video"

    def cut_video(self, video_url, segment_duration, output_prefix):
        video_url = video_url.strip()
        
        # Kiểm tra file video có tồn tại không
        if not os.path.isfile(video_url):
            return (f"ERROR: Video file not found → {video_url}",)
        
        # Lấy thư mục chứa video gốc
        video_dir = os.path.dirname(video_url)
        video_basename = os.path.basename(video_url)
        video_name, video_ext = os.path.splitext(video_basename)
        
        # Tạo thư mục videos_cut
        output_dir = os.path.join(video_dir, "videos_cut")
        os.makedirs(output_dir, exist_ok=True)
        
        # Lấy độ dài video bằng ffprobe
        duration_cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_url
        ]
        
        try:
            result = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
            total_duration = float(result.stdout.strip())
        except Exception as e:
            return (f"ERROR: Failed to get video duration → {str(e)}",)
        
        # Tính số lượng segment
        num_segments = math.ceil(total_duration / segment_duration)
        
        # Danh sách các video đã cắt
        cut_videos = []
        
        # Cắt video thành các segment
        for i in range(num_segments):
            start_time = i * segment_duration
            output_filename = f"{output_prefix}-{i+1}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            
            # FFmpeg command để cắt video
            cut_cmd = [
                "ffmpeg",
                "-y",  # Ghi đè file nếu đã tồn tại
                "-i", video_url,
                "-ss", str(start_time),
                "-t", str(segment_duration),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-avoid_negative_ts", "1",
                output_path
            ]
            
            try:
                subprocess.run(cut_cmd, capture_output=True, check=True)
                cut_videos.append(output_path)
                print(f"Created segment {i+1}/{num_segments}: {output_filename}")
            except subprocess.CalledProcessError as e:
                return (f"ERROR: Failed to cut segment {i+1} → {str(e)}",)
        
        # Sắp xếp danh sách video theo thứ tự (đã được tạo theo thứ tự rồi)
        # Trả về danh sách các đường dẫn, ngăn cách bởi dấu phẩy
        videos_list_str = ",".join(cut_videos)
        
        print(f"Successfully cut video into {num_segments} segments")
        print(f"Output directory: {output_dir}")
        
        return (videos_list_str,)


NODE_CLASS_MAPPINGS = {
    "video_cut_to_segments": VideoCutToSegments
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "video_cut_to_segments": "Video Cut to 8s Segments"
}
