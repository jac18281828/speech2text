# AGENTS.md

Instructions for agents running transcriptions in this repo.

## Model choice

The script default is `small.en`. Until the user states a model preference,
never run it silently. Before the first transcription in a session, offer:

- `small.en`: fast draft; mishears names and jargon.
- `distil-large-v3`: faster than `large-v3`; mixed accuracy on names and jargon, coarse timestamps.
- `large-v3`: most accurate expected, slowest.

If the user has already stated a choice in the conversation, use it without asking.

Record the user's chosen model here once decided:

Chosen model: (not yet chosen)

Once a model is recorded, use it without asking.

## Running

- Pass the choice explicitly with `--model <name>`.
- For `distil-large-v3` and `large-v3`, also pass `--language en` for English audio; the `.en` auto-language shortcut applies only to `*.en` models.
- Use `--vad-filter` for conversation recordings.
- Models download to `./.cache` inside the repo on first use (`distil-large-v3` ~1.4 GB, `small.en` ~0.5 GB). The first run with a new model is slower.
- When comparing models on the same audio, give each run a distinct `--output-prefix` that includes the model name, for example `<audio-stem>.<model>`. The default prefix overwrites a prior run.

```bash
./transcribe.sh /path/to/audio.mp3 --model distil-large-v3 --language en --vad-filter \
  --output-prefix /path/to/audio.distil-large-v3
```
