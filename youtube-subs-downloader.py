from youtube_transcript_api import YouTubeTranscriptApi
import json
import requests

video_id = 'r0trwOLcEGQ'

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

try:
    api = YouTubeTranscriptApi()
    
    # First, list available transcripts
    print("Checking available transcripts...")
    transcript_list = api.list(video_id)
    
    print(f"\nAvailable transcripts:")
    for transcript_info in transcript_list:
        print(f"  - Language: {transcript_info.language} ({transcript_info.language_code})")
        print(f"    Auto-generated: {transcript_info.is_generated}")
    
    # Try to fetch Estonian first, then fall back to any available
    try:
        print("\nTrying to fetch Estonian subtitles...")
        transcript_track = transcript_list.find_transcript(['et'])
    except:
        print("Estonian not found, trying first available language...")
        # Get the first available transcript
        transcript_track = list(transcript_list)[0]

    transcript = transcript_track.fetch()

    print(f"\nFetching subtitles in {transcript.language} ({transcript.language_code})...")
    
    # Save as plain text
    with open('subtitles.txt', 'w', encoding='utf-8') as f:
        for snippet in transcript.snippets:
            f.write(f"{snippet.text}\n")
    
    # Save in SRT format with timestamps
    with open('subtitles.srt', 'w', encoding='utf-8') as f:
        for i, snippet in enumerate(transcript.snippets, 1):
            start = snippet.start
            end = start + snippet.duration
            
            f.write(f"{i}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(f"{snippet.text}\n\n")

    # Save JSON3 track payload (contains extra timing metadata when provided by YouTube).
    json3_saved = False
    json3_error = None
    try:
        json3_url = f"{transcript_track._url}&fmt=json3"
        json3_response = requests.get(json3_url, timeout=15)
        json3_response.raise_for_status()
        json3_data = json3_response.json()

        if isinstance(json3_data, dict) and "events" in json3_data:
            with open('subtitles.json3', 'w', encoding='utf-8') as f:
                json.dump(json3_data, f, ensure_ascii=False, indent=2)
            json3_saved = True
        else:
            json3_error = "JSON3 payload does not include events."
    except Exception as err:
        json3_error = str(err)

    print(f"\n✓ Subtitles saved successfully!")
    print(f"  - Plain text: subtitles.txt")
    print(f"  - SRT format: subtitles.srt")
    if json3_saved:
        print(f"  - JSON3 format: subtitles.json3")
    else:
        print(f"  - JSON3 format: not available ({json3_error})")
    print(f"\nLanguage: {transcript.language} ({transcript.language_code})")
    print(f"Auto-generated: {transcript.is_generated}")
    print(f"Total snippets: {len(transcript.snippets)}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nThis video may not have subtitles available.")
