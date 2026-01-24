import os
import subprocess
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

class VideoCutToSegments:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "segment_duration": ("INT", {"default": 8, "min": 1, "max": 3600}),
                "output_prefix": ("STRING", {"default": "a"}),
                "use_gpu": ("BOOLEAN", {"default": True}),
                "fast_mode": ("BOOLEAN", {"default": False}),
                "parallel_workers": ("INT", {"default": 4, "min": 1, "max": 16}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("videos_list",)
    FUNCTION = "cut_video"
    CATEGORY = "video"

    def _cut_single_segment(self, args):
        """Cắt một segment duy nhất (để dùng với parallel processing)"""
        video_url, start_time, duration, output_path, use_gpu, fast_mode = args
        
        if fast_mode:
            # Fast mode: copy codec, không re-encode (rất nhanh nhưng cắt tại keyframe)
            cmd = [
                "ffmpeg",
                "-y",
                "-ss", str(start_time),
                "-i", video_url,
                "-t", str(duration),
                "-c", "copy",
                "-avoid_negative_ts", "1",
                output_path
            ]
        elif use_gpu:
            # GPU mode: sử dụng NVENC (NVIDIA T4)
            cmd = [
                "ffmpeg",
                "-y",
                "-hwaccel", "cuda",
                "-hwaccel_output_format", "cuda",
                "-i", video_url,
                "-ss", str(start_time),
                "-t", str(duration),
                "-c:v", "h264_nvenc",
                "-preset", "p4",  # p1=fastest, p7=slowest (p4=balanced)
                "-b:v", "5M",
                "-c:a", "aac",
                "-b:a", "128k",
                "-avoid_negative_ts", "1",
                output_path
            ]
        else:
            # CPU mode: libx264 với multi-threading
            cmd = [
                "ffmpeg",
                "-y",
                "-i", video_url,
                "-ss", str(start_time),
                "-t", str(duration),
                "-c:v", "libx264",
                "-preset", "fast",
                "-threads", "8",
                "-c:a", "aac",
                "-b:a", "128k",
                "-avoid_negative_ts", "1",
                output_path
            ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path, None
        except subprocess.CalledProcessError as e:
            return None, str(e)

    def cut_video(self, video_url, segment_duration, output_prefix, use_gpu, fast_mode, parallel_workers):
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
        
        # Chuẩn bị danh sách tasks cho parallel processing
        tasks = []
        for i in range(num_segments):
            start_time = i * segment_duration
            output_filename = f"{output_prefix}-{i+1}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            
            tasks.append((
                video_url,
                start_time,
                segment_duration,
                output_path,
                use_gpu,
                fast_mode
            ))
        
        # Xử lý song song với ThreadPoolExecutor
        cut_videos = []
        errors = []
        
        print(f"Starting to cut video into {num_segments} segments using {parallel_workers} workers...")
        print(f"Mode: {'Fast (copy)' if fast_mode else 'GPU (NVENC)' if use_gpu else 'CPU (libx264)'}")
        
        with ThreadPoolExecutor(max_workers=parallel_workers) as executor:
            # Submit all tasks
            future_to_segment = {executor.submit(self._cut_single_segment, task): i+1 
                                for i, task in enumerate(tasks)}
            
            # Collect results as they complete
            for future in as_completed(future_to_segment):
                segment_num = future_to_segment[future]
                try:
                    output_path, error = future.result()
                    if error:
                        errors.append(f"Segment {segment_num}: {error}")
                    else:
                        cut_videos.append((segment_num, output_path))
                        print(f"✓ Completed segment {segment_num}/{num_segments}")
                except Exception as exc:
                    errors.append(f"Segment {segment_num}: {exc}")
        
        # Sắp xếp theo thứ tự segment
        cut_videos.sort(key=lambda x: x[0])
        cut_videos = [path for _, path in cut_videos]
        
        if errors:
            error_msg = "\n".join(errors)
            return (f"ERROR: Some segments failed:\n{error_msg}",)
        
        # Trả về danh sách các đường dẫn, ngăn cách bởi dấu phẩy
        videos_list_str = ",".join(cut_videos)
        
        print(f"✓ Successfully cut video into {num_segments} segments")
        print(f"Output directory: {output_dir}")
        
        return (videos_list_str,)


NODE_CLASS_MAPPINGS = {
    "video_cut_to_segments": VideoCutToSegments
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "video_cut_to_segments": "Video Cut to 8s Segments"
}
