#!/usr/bin/env python3
"""Basic technical QA for Gothic Phoenix image and video assets."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv"}


def ffprobe(path: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size:stream=codec_type,width,height,r_frame_rate",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def validate(path: Path) -> dict:
    report = {"path": str(path), "exists": path.exists(), "passed": False, "errors": [], "warnings": []}
    if not path.exists():
        report["errors"].append("File does not exist")
        return report
    if path.stat().st_size == 0:
        report["errors"].append("File is empty")
        return report

    suffix = path.suffix.lower()
    if suffix in VIDEO_EXTENSIONS:
        try:
            metadata = ffprobe(path)
            report["metadata"] = metadata
            streams = metadata.get("streams", [])
            video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
            if not video_streams:
                report["errors"].append("No video stream found")
            else:
                stream = video_streams[0]
                width = int(stream.get("width", 0))
                height = int(stream.get("height", 0))
                if width < 1080 or height < 1080:
                    report["warnings"].append("Resolution is below preferred social master size")
                if height <= width:
                    report["warnings"].append("Asset is not vertical; confirm intended platform")
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as exc:
            report["errors"].append(f"ffprobe validation failed: {exc}")
    elif suffix in IMAGE_EXTENSIONS:
        report["warnings"].append("Add Pillow/OpenCV checks for dimensions, blur, safe zones, and OCR in the production environment")
    else:
        report["errors"].append(f"Unsupported extension: {suffix}")

    report["passed"] = not report["errors"]
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    report = validate(Path(args.input))
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
