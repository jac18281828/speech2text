#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from faster_whisper import WhisperModel
except ImportError as exc:
    raise SystemExit(
        "Missing dependency 'faster-whisper'. Run ./transcribe.sh --help after setting up the virtualenv."
    ) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file with faster-whisper."
    )
    parser.add_argument("audio_path", type=Path, help="Path to an audio file.")
    parser.add_argument(
        "--model",
        default="small.en",
        help="Whisper model to use. Default: small.en",
    )
    parser.add_argument(
        "--language",
        help="Language code, for example 'en'. Defaults to 'en' for *.en models.",
    )
    parser.add_argument(
        "--task",
        default="transcribe",
        choices=("transcribe", "translate"),
        help="Whisper task to run. Default: transcribe",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Beam size for decoding. Default: 5",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Execution device. Default: cpu",
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="Model compute type. Default: int8",
    )
    parser.add_argument(
        "--vad-filter",
        action="store_true",
        help="Enable voice activity detection filtering.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(__file__).resolve().parent / ".cache",
        help="Directory for downloaded model files.",
    )
    parser.add_argument(
        "--output-prefix",
        type=Path,
        help="Write outputs to <prefix>.txt and <prefix>.json. Defaults next to the audio file.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the timestamped transcript to stdout instead of writing files.",
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Skip the JSON sidecar output.",
    )
    return parser


def choose_output_prefix(audio_path: Path, output_prefix: Path | None) -> Path:
    if output_prefix is not None:
        return output_prefix
    return audio_path.with_name(f"{audio_path.stem}.transcript")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    audio_path = args.audio_path.expanduser().resolve()
    if not audio_path.exists():
        parser.error(f"audio file not found: {audio_path}")

    cache_dir = args.cache_dir.expanduser().resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)

    language = args.language
    if language is None and args.model.endswith(".en"):
        language = "en"

    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
        download_root=str(cache_dir),
    )

    segments, info = model.transcribe(
        str(audio_path),
        beam_size=args.beam_size,
        language=language,
        vad_filter=args.vad_filter,
        task=args.task,
    )

    transcript_lines = [
        f"# language={info.language} probability={info.language_probability:.4f}"
    ]
    segment_rows: list[dict[str, object]] = []

    for segment in segments:
        text = segment.text.strip()
        transcript_lines.append(
            f"[{segment.start:8.2f} -> {segment.end:8.2f}] {text}"
        )
        segment_rows.append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": text,
            }
        )

    transcript = "\n".join(transcript_lines) + "\n"

    if args.stdout:
        sys.stdout.write(transcript)
        return 0

    output_prefix = choose_output_prefix(audio_path, args.output_prefix)
    output_prefix.parent.mkdir(parents=True, exist_ok=True)

    text_path = output_prefix.with_name(f"{output_prefix.name}.txt")
    text_path.write_text(transcript, encoding="utf-8")

    if not args.no_json:
        json_path = output_prefix.with_name(f"{output_prefix.name}.json")
        json_path.write_text(
            json.dumps(
                {
                    "language": info.language,
                    "language_probability": info.language_probability,
                    "segments": segment_rows,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    print(f"Wrote transcript to {text_path}")
    if not args.no_json:
        print(f"Wrote segment JSON to {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
