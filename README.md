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
./transcribe.sh /path/to/audio.mp3 --model distil-large-v3 --language en --vad-filter
```

Default behavior:

- Uses the `small.en` Whisper model.
- Stores downloaded model files in `./.cache`.
- Writes `audio_name.transcript.txt` and `audio_name.transcript.json` next to the source audio.

Common options:

```bash
./transcribe.sh /path/to/audio.mp3 --model distil-large-v3 --language en
./transcribe.sh /path/to/audio.mp3 --model large-v3 --language en
./transcribe.sh /path/to/audio.mp3 --model base.en
./transcribe.sh /path/to/audio.mp3 --output-prefix /tmp/my_transcript
./transcribe.sh /path/to/audio.mp3 --stdout
./transcribe.sh /path/to/audio.mp3 --task translate
```

If you want VAD-based silence trimming, add `--vad-filter`.

`--language en` is implied only for `*.en` models; pass it for `distil-large-v3` and `large-v3` on English audio.

## Choosing a model

| Model | Approx. size | Speed | Notes |
| --- | --- | --- | --- |
| `small.en` | ~0.5 GB | Fast (~4 min for 30 min of audio, CPU, int8) | Script default. Good draft; mishears names and jargon. |
| `distil-large-v3` | ~1.4 GB | Slower than `small.en`, faster than `large-v3` | Near `large-v3` English accuracy. Recommended starting point. |
| `large-v3` | ~3 GB | Slowest | Most accurate. |

The first run with a model downloads it to `./.cache`.

## Agents

See [AGENTS.md](AGENTS.md) for how agents choose a model.
