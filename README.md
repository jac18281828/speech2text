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
./transcribe.sh /path/to/audio.mp3 --model large-v3 --language en --vad-filter
```

Default behavior:

- Uses the `small.en` Whisper model.
- Stores downloaded model files in `./.cache`.
- Writes `audio_name.transcript.txt` and `audio_name.transcript.json` next to the source audio.

Common options:

```bash
./transcribe.sh /path/to/audio.mp3 --model small.en
./transcribe.sh /path/to/audio.mp3 --model large-v3 --language en
./transcribe.sh /path/to/audio.mp3 --output-prefix /tmp/my_transcript
./transcribe.sh /path/to/audio.mp3 --stdout
./transcribe.sh /path/to/audio.mp3 --task translate
```

If you want VAD-based silence trimming, add `--vad-filter`.

`--language en` is implied only for `*.en` models; pass it for `large-v3` on English audio.

## Choosing a model

| Model | Role | Approx. size | Speed (30 min of audio, CPU, int8) | Notes |
| --- | --- | --- | --- | --- |
| `small.en` | Default | ~0.5 GB | ~4 min, fast | Mishears names and jargon. |
| `large-v3` | Fallback | ~3 GB | ~20 min including first download | Most accurate expected. |

The first run with a model downloads it to `./.cache`.

## Agents

See [AGENTS.md](AGENTS.md) for how agents choose a model.
