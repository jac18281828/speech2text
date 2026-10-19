# speech2text

Minimal local audio transcription helper built on `faster-whisper`.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

## Usage

```bash
./transcribe.sh /path/to/audio.mp3
```

Default behavior:

- Uses the `small.en` Whisper model.
- Stores downloaded model files in `./.cache`.
- Writes `audio_name.transcript.txt` and `audio_name.transcript.json` next to the source audio.

Common options:

```bash
./transcribe.sh /path/to/audio.mp3 --model base.en
./transcribe.sh /path/to/audio.mp3 --output-prefix /tmp/my_transcript
./transcribe.sh /path/to/audio.mp3 --stdout
./transcribe.sh /path/to/audio.mp3 --task translate
```

If you want VAD-based silence trimming, add `--vad-filter`.
