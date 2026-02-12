# YouTube Subtitles Downloaders

This repo includes two subtitle downloader scripts:

- `youtube-subs-downloader.py` - Downloads subtitles as plain text, SRT, and JSON3
- `clip-subs-downloader.py` - Downloads only JSON3 subtitles

## Installation

```bash
pip3 install youtube-transcript-api requests
```

## Script: youtube-subs-downloader.py

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
- `subtitles.json3` - JSON3 subtitle payload (when available)

## Script: clip-subs-downloader.py

Downloads only JSON3 subtitles using command line parameters.

Usage:

```bash
python3 clip-subs-downloader.py VIDEO_ID [OUTPUT_FILENAME] [--start-ms MS] [--end-ms MS] [--language CODE]
```

Examples:

```bash
# Uses default output filename: clip.json3
python3 clip-subs-downloader.py r0trwOLcEGQ

# Uses custom output filename
python3 clip-subs-downloader.py r0trwOLcEGQ my-subs.json3

# Keeps only subtitles between 60,000ms and 120,000ms
python3 clip-subs-downloader.py r0trwOLcEGQ clip.json3 --start-ms 60000 --end-ms 120000

# Uses English subtitles (default is Estonian: et)
python3 clip-subs-downloader.py r0trwOLcEGQ clip.json3 --language en
```

## Notes

- Scripts automatically detect available subtitle languages
- Scripts default to Estonian (`et`) and fall back to the first available language
- Works with both manual and auto-generated subtitles
- `clip-subs-downloader.py` clips by time locally after download (YouTube APIs do not expose transcript range download)
- `--start-ms` and `--end-ms` use milliseconds to match JSON3 timing fields
