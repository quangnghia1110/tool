import yt_dlp
import os
import time

class YouTubeConverter:
    def __init__(self):
        self.ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'
        self.output_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        
        # Thêm cấu hình proxy nếu cần
        self.proxy = None
        # self.proxy = 'socks5://127.0.0.1:1080'  # Uncomment nếu muốn dùng proxy

    def get_formats(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': self.ffmpeg_path
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            
            # Lọc các format audio và thêm thông tin chi tiết hơn
            for f in info['formats']:
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    # Lấy bitrate
                    abr = f.get('abr', 0)  # audio bitrate
                    if abr:
                        quality = f"{int(abr)}kbps"
                    else:
                        asr = f.get('asr', 0)  # audio sampling rate
                        if asr:
                            quality = f"{int(asr/1000)}kHz"
                        else:
                            continue  # Bỏ qua format không có thông tin bitrate
                    
                    # Tính kích thước
                    filesize = f.get('filesize', 0)
                    if filesize == 0:
                        filesize = f.get('filesize_approx', 0)
                    
                    if filesize > 0:
                        size_mb = filesize / (1024 * 1024)
                        size_text = f"{size_mb:.1f} MB"
                    else:
                        size_text = "N/A"
                    
                    formats.append({
                        'format_id': f['format_id'],
                        'quality': quality,
                        'filesize': size_text,
                        'ext': f.get('ext', 'unknown')
                    })
            
            # Sắp xếp theo chất lượng giảm dần
            formats.sort(key=lambda x: float(x['quality'].replace('kbps', '').replace('kHz', '')), reverse=True)
            
            return formats, info['title']

    def get_video_title(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': self.ffmpeg_path
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['title']

    def download_with_progress(self, url, format_id):
        try:
            # Lấy thông tin video trước để ước tính thời gian
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info['title']
                
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = os.path.join(self.output_path, safe_title)
            
            ydl_opts = {
                'format': format_id,
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [self.progress_hook],
                'outtmpl': filename + '.%(ext)s',
                'concurrent_fragments': 5,
                'buffersize': 4096*1024,
                'http_chunk_size': 20971520,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_args': [
                    '-threads', '4',
                    '-preset', 'ultrafast',
                    '-movflags', 'faststart'
                ],
                'socket_timeout': 30,
                'retries': 5,
                'fragment_retries': 5,
                'skip_unavailable_fragments': True,
                'noprogress': False
            }
            
            if self.proxy:
                ydl_opts['proxy'] = self.proxy
                
            self.current_file = filename + '.mp3'
            
            # Download file
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            if os.path.exists(self.current_file):
                # Bắt đầu đếm ngược 10 giây
                for i in range(10):
                    progress = i * 10  # Mỗi giây tăng 10%
                    seconds_left = 10 - i
                    yield {
                        'status': 'countdown', 
                        'progress': progress,
                        'text': f'Preparing download... {seconds_left}s remaining'
                    }
                    time.sleep(1)  # Đợi 1 giây
                    
                # Hoàn thành 100%
                yield {
                    'status': 'complete', 
                    'progress': 100, 
                    'text': 'Download complete!', 
                    'filename': self.current_file
                }
            else:
                raise Exception("Downloaded file not found")

        except Exception as e:
            print(f"Download error: {str(e)}")
            yield {'status': 'error', 'message': str(e)}

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    speed = d.get('speed', 0)
                    speed_text = f'{speed / (1024 * 1024):.1f} MB/s' if speed else 'N/A'
                    
                    total_mb = total / (1024 * 1024)
                    downloaded_mb = downloaded / (1024 * 1024)
                    
                    eta = d.get('eta', 0)
                    eta_text = ''
                    if eta:
                        minutes, seconds = divmod(eta, 60)
                        eta_text = f'{minutes}m {seconds}s' if minutes else f'{seconds}s'
                    
                    return {
                        'status': 'downloading',
                        'progress': 0,  # Giữ progress ở 0 trong lúc download
                        'text': f'{speed_text} - {downloaded_mb:.1f}MB of {total_mb:.1f}MB - {eta_text} remaining'
                    }
                
            except Exception as e:
                print(f"Progress calculation error: {str(e)}")
                return None
                
        elif d['status'] == 'finished':
            return {
                'status': 'converting',
                'progress': 0,  # Giữ progress ở 0 trong lúc convert
                'text': 'Converting to MP3...'
            }