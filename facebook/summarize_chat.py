"""
Summarize a chat with someone on Facebook Messenger

The input has an array of something like:
```
{
    "isUnsent": false,
    "media": [],
    "reactions": [],
    "senderName": "SENDER",
    "text": "Hello",
    "timestamp": 1764087941409,
    "type": "text"
}
```
"""
import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


DEFAULT_IN_NAME = "Input.json"


def summarize_chat(input_path, output_path=None, tz_hours=7):
    with open(input_path, "r", encoding="utf-8") as infile:
        in_json = json.load(infile)

    messeges = in_json.get("messages", [])
    out_messages = []
    for msg in messeges:
        if msg.get("isUnsent", False):
            continue
        if msg.get("reactions"):
            continue
        text = msg.get("text", "")
        if not text or not isinstance(text, str):
            continue
        ts_val = msg.get("timestamp")
        if ts_val is None:
            continue
        ts = (
            datetime
            .fromtimestamp(ts_val / 1000, tz=timezone(timedelta(hours=tz_hours)))
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        prefix = f"{msg.get('senderName', 'UNKNOWN')} @ {ts}: "
        out_msg = prefix + text + "\n"
        out_messages.append(out_msg)

    if output_path:
        out_path = Path(output_path)
    else:
        filename = Path(input_path).with_suffix("")
        out_path = Path(f"{filename.name}-summarized.txt")

    with out_path.open("w", encoding="utf-8") as outfile:
        outfile.writelines(out_messages)
    return str(out_path)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Summarize a Facebook Messenger JSON export to text.")
    parser.add_argument("infile", nargs="?", default=DEFAULT_IN_NAME, help="Path to input JSON file (absolute path OK).")
    parser.add_argument("-o", "--output", help="Path to output text file (optional).")
    parser.add_argument("--tz-offset", type=int, default=7, help="Timezone offset in hours for timestamps (default: 7).")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    in_path = Path(args.infile)
    if not in_path.exists():
        print(f"Input file not found: {in_path}", file=sys.stderr)
        sys.exit(2)
    out_file = summarize_chat(str(in_path), output_path=args.output, tz_hours=args.tz_offset)
    print(f"Wrote summarized chat to {out_file}")
