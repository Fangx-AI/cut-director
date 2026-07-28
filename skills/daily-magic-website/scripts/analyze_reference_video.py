#!/usr/bin/env python3
"""Create a reproducible frame-level audit package for a reference video.

The output directory is intentionally external to the Skill repository because it
contains extracted frames from the supplied source video.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


PTS_RE = re.compile(r"pts_time:([0-9.]+)")
SILENCE_RE = re.compile(r"silence_duration:\s*([0-9.]+)")
LOUDNESS_I_RE = re.compile(r"^\s*I:\s*(-?[0-9.]+)\s+LUFS", re.MULTILINE)
LOUDNESS_LRA_RE = re.compile(r"^\s*LRA:\s*([0-9.]+)\s+LU", re.MULTILINE)


def resolve_binary(value: str | None, default: str) -> str:
    if value:
        candidate = Path(value)
        if not candidate.exists():
            raise FileNotFoundError(f"binary not found: {candidate}")
        return str(candidate)
    resolved = shutil.which(default)
    if not resolved:
        raise FileNotFoundError(
            f"{default} was not found; pass --{default} with an explicit path"
        )
    return resolved


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def fraction(value: str) -> float:
    numerator, denominator = value.split("/", 1)
    return float(numerator) / float(denominator)


def probe(ffprobe: str, video: Path) -> dict:
    result = run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-count_frames",
            "-of",
            "json",
            str(video),
        ],
        capture=True,
    )
    return json.loads(result.stdout)


def extract_frames(ffmpeg: str, video: Path, output: Path) -> None:
    frames = output / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video),
            "-q:v",
            "2",
            str(frames / "frame-%06d.jpg"),
        ]
    )


def create_contact_sheets(
    ffmpeg: str,
    video: Path,
    output: Path,
    contact_fps: float,
) -> list[dict]:
    contacts = output / "contacts"
    contacts.mkdir(parents=True, exist_ok=True)
    tile_count = 25
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video),
            "-vf",
            (
                f"fps={contact_fps},scale=216:384,"
                "tile=5x5:nb_frames=25:padding=2:margin=2:color=black"
            ),
            "-q:v",
            "3",
            str(contacts / "sheet-%03d.jpg"),
        ]
    )

    sheets = sorted(contacts.glob("sheet-*.jpg"))
    index: list[dict] = []
    for sheet_index, sheet in enumerate(sheets):
        tiles = []
        for tile_index in range(tile_count):
            sample_index = sheet_index * tile_count + tile_index
            tiles.append(
                {
                    "tile": tile_index,
                    "timeSeconds": round(sample_index / contact_fps, 6),
                }
            )
        index.append({"sheet": sheet.name, "tiles": tiles})
    (output / "contact-index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return index


def scene_candidates(
    ffmpeg: str,
    video: Path,
    threshold: float,
) -> list[float]:
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-i",
            str(video),
            "-vf",
            f"select='gt(scene,{threshold})',showinfo",
            "-an",
            "-f",
            "null",
            "NUL" if sys.platform == "win32" else "/dev/null",
        ],
        capture=True,
    )
    combined = (result.stdout or "") + "\n" + (result.stderr or "")
    times = [float(value) for value in PTS_RE.findall(combined)]
    clustered: list[float] = []
    for value in times:
        if not clustered or value - clustered[-1] > 0.25:
            clustered.append(value)
    return clustered


def audio_metrics(ffmpeg: str, video: Path) -> dict:
    sink = "NUL" if sys.platform == "win32" else "/dev/null"
    silence_result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-i",
            str(video),
            "-af",
            "silencedetect=noise=-35dB:d=0.12",
            "-f",
            "null",
            sink,
        ],
        capture=True,
    )
    silence_text = (silence_result.stdout or "") + "\n" + (
        silence_result.stderr or ""
    )
    silence_durations = [float(value) for value in SILENCE_RE.findall(silence_text)]

    loudness_result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-i",
            str(video),
            "-af",
            "ebur128=framelog=verbose",
            "-f",
            "null",
            sink,
        ],
        capture=True,
    )
    loudness_text = (loudness_result.stdout or "") + "\n" + (
        loudness_result.stderr or ""
    )
    integrated = LOUDNESS_I_RE.findall(loudness_text)
    lra = LOUDNESS_LRA_RE.findall(loudness_text)
    return {
        "silenceThresholdDb": -35,
        "silenceMinimumSeconds": 0.12,
        "silenceDurationsSeconds": silence_durations,
        "integratedLufs": float(integrated[-1]) if integrated else None,
        "loudnessRangeLu": float(lra[-1]) if lra else None,
    }


def summarize_probe(data: dict) -> dict:
    video_stream = next(
        stream for stream in data["streams"] if stream["codec_type"] == "video"
    )
    audio_stream = next(
        (stream for stream in data["streams"] if stream["codec_type"] == "audio"),
        None,
    )
    fps = fraction(video_stream["avg_frame_rate"])
    frames = int(
        video_stream.get("nb_read_frames")
        or video_stream.get("nb_frames")
        or round(float(data["format"]["duration"]) * fps)
    )
    summary = {
        "width": int(video_stream["width"]),
        "height": int(video_stream["height"]),
        "fps": fps,
        "durationSeconds": float(data["format"]["duration"]),
        "frames": frames,
        "videoCodec": video_stream.get("codec_name"),
    }
    if audio_stream:
        summary["audio"] = {
            "codec": audio_stream.get("codec_name"),
            "sampleRate": int(audio_stream.get("sample_rate", 0)),
            "channels": int(audio_stream.get("channels", 0)),
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    parser.add_argument("--scene-threshold", type=float, default=0.10)
    parser.add_argument("--contact-fps", type=float, default=5.0)
    parser.add_argument(
        "--skip-frames",
        action="store_true",
        help="Skip extraction of every decoded frame.",
    )
    args = parser.parse_args()

    if not args.video.is_file():
        print(f"ERROR: video not found: {args.video}", file=sys.stderr)
        return 2
    if not 0 < args.scene_threshold < 1:
        print("ERROR: --scene-threshold must be between 0 and 1", file=sys.stderr)
        return 2
    if args.contact_fps <= 0:
        print("ERROR: --contact-fps must be positive", file=sys.stderr)
        return 2

    try:
        ffmpeg = resolve_binary(args.ffmpeg, "ffmpeg")
        ffprobe = resolve_binary(args.ffprobe, "ffprobe")
        args.output.mkdir(parents=True, exist_ok=True)

        probe_data = probe(ffprobe, args.video)
        summary = summarize_probe(probe_data)
        if not args.skip_frames:
            extract_frames(ffmpeg, args.video, args.output)
        contact_index = create_contact_sheets(
            ffmpeg,
            args.video,
            args.output,
            args.contact_fps,
        )
        candidates = scene_candidates(
            ffmpeg,
            args.video,
            args.scene_threshold,
        )
        audio = audio_metrics(ffmpeg, args.video)
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    result = {
        "source": {
            "name": args.video.name,
            "sha256": sha256(args.video),
        },
        "technical": summary,
        "sceneThreshold": args.scene_threshold,
        "sceneCandidates": [
            {
                "timeSeconds": round(value, 6),
                "frame": round(value * summary["fps"]),
            }
            for value in candidates
        ],
        "audioMetrics": audio,
        "contactFps": args.contact_fps,
        "contactSheetCount": len(contact_index),
        "fullFramesExtracted": not args.skip_frames,
    }
    (args.output / "analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"PASS: analyzed {summary['frames']} frames into {args.output.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
