import os
import subprocess
import math
from concurrent.futures import ProcessPoolExecutor, as_completed

class VideoCutToSegments:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_url": ("STRING", {"default": ""}),
                "segment_duration": ("INT", {"default": 8, "min": 1, "max": 3600}),
                "output_prefix": ("STRING", {"default": "a"}),
                "use_gpu": ("BOOLEAN", {"default": True}),
                "accurate_cut": ("BOOLEAN", {"default": True}),
                "parallel_workers": ("INT", {"default": 4, "min": 1, "max": 16}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("videos_list", "output_directory",)
    FUNCTION = "cut_video"
    CATEGORY = "video"

    @staticmethod
    def _cut_single_segment(args):
        """Cắt một segment duy nhất (static method để dùng với ProcessPoolExecutor)"""
        video_url, start_time, duration, output_path, use_gpu, accurate_cut = args
        
        if use_gpu:
            # GPU mode: NVENC H.264 optimized for ComfyUI
            cmd = [
                "ffmpeg",
                "-y",
                "-hwaccel", "cuda",
                "-hwaccel_output_format", "cuda",
                "-ss", str(start_time),
                "-accurate_seek" if accurate_cut else "-noaccurate_seek",
                "-i", video_url,
                "-t", str(duration),
                "-c:v", "h264_nvenc",
                "-preset", "p1",
                "-tune", "hq",
                "-profile:v", "high",
                "-pix_fmt", "yuv420p",
                "-rc", "vbr",
                "-cq", "23",
                "-b:v", "0",
                "-maxrate", "10M",
                "-bufsize", "20M",
                "-c:a", "aac",
                "-b:a", "128k",
                "-avoid_negative_ts", "1",
                "-max_muxing_queue_size", "9999",
                "-movflags", "+faststart",
                output_path
            ]
        else:
            # CPU mode: libx264 H.264 optimized for ComfyUI
            cmd = [
                "ffmpeg",
                "-y",
                "-ss", str(start_time),
                "-accurate_seek" if accurate_cut else "-noaccurate_seek",
                "-i", video_url,
                "-t", str(duration),
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-tune", "zerolatency",
                "-profile:v", "high",
                "-pix_fmt", "yuv420p",
                "-threads", "0",
                "-c:a", "aac",
                "-b:a", "128k",
                "-avoid_negative_ts", "1",
                "-movflags", "+faststart",
                output_path
            ]
        
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return output_path, None
        except subprocess.CalledProcessError as e:
            return None, str(e)

    def cut_video(self, video_url, segment_duration, output_prefix, use_gpu, accurate_cut, parallel_workers):
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
                accurate_cut
            ))
        
        # Xử lý song song với ProcessPoolExecutor (tránh GIL của Python)
        cut_videos = []
        errors = []
        
        mode_str = f"GPU (NVENC-p1)" if use_gpu else "CPU (veryfast)"
        accuracy_str = "accurate" if accurate_cut else "fast"
        print(f"Starting to cut video into {num_segments} segments using {parallel_workers} workers...")
        print(f"Mode: {mode_str} | Accuracy: {accuracy_str}")
        
        with ProcessPoolExecutor(max_workers=parallel_workers) as executor:
            # Submit all tasks
            future_to_segment = {executor.submit(VideoCutToSegments._cut_single_segment, task): i+1 
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
            return (f"ERROR: Some segments failed:\n{error_msg}", "")
        
        # Trả về danh sách các đường dẫn, mỗi dòng một video
        videos_list_str = "\n".join(cut_videos)
        
        print(f"✓ Successfully cut video into {num_segments} segments")
        print(f"Output directory: {output_dir}")
        
        return (videos_list_str, output_dir)


NODE_CLASS_MAPPINGS = {
    "video_cut_to_segments": VideoCutToSegments
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "video_cut_to_segments": "Video Cut to 8s Segments"
}
