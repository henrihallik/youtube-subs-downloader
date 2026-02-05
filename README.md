# YouTube Subtitles Downloader

Download subtitles from YouTube videos in plain text or SRT format.

## Installation
```bash
pip3 install youtube-transcript-api
```

## Usage

1. Edit the `video_id` in `youtube-subs-downloader.py`:
```python
video_id = 'YOUR_VIDEO_ID_HERE'  # From youtube.com/watch?v=VIDEO_ID
```

2. Run the script:
```bash
python3 youtube-subs-downloader.py
```

3. Output files:
   - `subtitles.txt` - Plain text
   - `subtitles.srt` - SRT format with timestamps

## Notes

- Script automatically detects available languages
- Tries Estonian first, falls back to other available languages
- Works with both manual and auto-generated subtitles
