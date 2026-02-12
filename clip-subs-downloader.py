import argparse
import json
import requests
from youtube_transcript_api import YouTubeTranscriptApi


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download YouTube subtitles in JSON3 format."
    )
    parser.add_argument(
        "video_id",
        help="YouTube video ID (from youtube.com/watch?v=VIDEO_ID)",
    )
    parser.add_argument(
        "output_filename",
        nargs="?",
        default="clip.json3",
        help="Output filename for JSON3 subtitles (default: clip.json3)",
    )
    parser.add_argument(
        "--start-ms",
        type=int,
        default=None,
        help="Clip start time in milliseconds (inclusive).",
    )
    parser.add_argument(
        "--end-ms",
        type=int,
        default=None,
        help="Clip end time in milliseconds (exclusive).",
    )
    return parser.parse_args()


def clip_events(events, start_ms=None, end_ms=None):
    if start_ms is None and end_ms is None:
        return events

    start_ms_limit = float("-inf") if start_ms is None else start_ms
    end_ms_limit = float("inf") if end_ms is None else end_ms

    clipped = []
    for event in events:
        event_start = event.get("tStartMs")
        if event_start is None:
            clipped.append(event)
            continue

        duration = event.get("dDurationMs", 0)
        if duration and duration > 0:
            event_end = event_start + duration
            if event_end > start_ms_limit and event_start < end_ms_limit:
                clipped.append(event)
        else:
            if start_ms_limit <= event_start < end_ms_limit:
                clipped.append(event)

    return clipped


def main():
    args = parse_args()
    api = YouTubeTranscriptApi()

    if args.start_ms is not None and args.start_ms < 0:
        print("\n✗ Error: --start-ms must be >= 0.")
        return
    if args.end_ms is not None and args.end_ms < 0:
        print("\n✗ Error: --end-ms must be >= 0.")
        return
    if (
        args.start_ms is not None
        and args.end_ms is not None
        and args.end_ms <= args.start_ms
    ):
        print("\n✗ Error: --end-ms must be greater than --start-ms.")
        return

    try:
        print("Checking available transcripts...")
        transcript_list = api.list(args.video_id)
    except Exception as err:
        print(f"\n✗ Error: {err}")
        print("\nThis video may not have subtitles available.")
        return

    print("\nAvailable transcripts:")
    for transcript_info in transcript_list:
        print(f"  - Language: {transcript_info.language} ({transcript_info.language_code})")
        print(f"    Auto-generated: {transcript_info.is_generated}")

    try:
        print("\nTrying to fetch Estonian subtitles...")
        transcript_track = transcript_list.find_transcript(["et"])
    except Exception:
        print("Estonian not found, trying first available language...")
        transcript_track = list(transcript_list)[0]

    try:
        json3_url = f"{transcript_track._url}&fmt=json3"
        response = requests.get(json3_url, timeout=15)
        response.raise_for_status()
        json3_data = response.json()
    except Exception as err:
        print(f"\n✗ Error downloading JSON3 subtitles: {err}")
        return

    if not (isinstance(json3_data, dict) and "events" in json3_data):
        print("\n✗ Error: JSON3 payload does not include events.")
        return

    original_count = len(json3_data["events"])
    json3_data["events"] = clip_events(
        json3_data["events"],
        start_ms=args.start_ms,
        end_ms=args.end_ms,
    )
    clipped_count = len(json3_data["events"])

    with open(args.output_filename, "w", encoding="utf-8") as file:
        json.dump(json3_data, file, ensure_ascii=False, indent=2)

    print("\n✓ JSON3 subtitles saved successfully!")
    print(f"  - File: {args.output_filename}")
    if args.start_ms is not None or args.end_ms is not None:
        start_label = "beginning" if args.start_ms is None else str(args.start_ms)
        end_label = "end" if args.end_ms is None else str(args.end_ms)
        print(f"  - Time range: {start_label}ms to {end_label}ms")
        print(f"  - Events kept: {clipped_count}/{original_count}")
    print(f"\nLanguage: {transcript_track.language} ({transcript_track.language_code})")
    print(f"Auto-generated: {transcript_track.is_generated}")


if __name__ == "__main__":
    main()
