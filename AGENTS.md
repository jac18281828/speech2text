# AGENTS.md

Instructions for agents running transcriptions in this repo.

## Model policy

Run `small.en` first for every transcription, without asking. If the result has quality issues, re-run with `large-v3`. The user can ask for that directly; otherwise the agent checks with the user.

Quality issues:

- Garbled or inconsistent proper nouns and jargon: company names, product and protocol names, acronyms.
- Looping or repeated lines.
- Nonsense phrases.
- Long empty or mistimed segments.

On seeing any of these, say what you saw and offer a `large-v3` re-run. Never switch silently.

`large-v3` is much slower: about 20 min for a 30 min recording on CPU int8, including a one-time ~3 GB model download, against about 4 min for `small.en`. It is the user's chosen fallback because accuracy outweighs the wait.

After a `large-v3` re-run, watch for its own failure modes and tell the user: repeated looping lines, a run of "Bye." past the end of the audio, timestamps collapsing to 1 s steps.

Chosen model: small.en by default; large-v3 on quality issues

## Running

- Pass the model explicitly with `--model <name>`.
- For `large-v3`, also pass `--language en` for English audio; the `.en` auto-language shortcut applies only to `*.en` models.
- Use `--vad-filter` for conversation recordings.
- Models download to `./.cache` inside the repo on first use (`small.en` ~0.5 GB, `large-v3` ~3 GB). The first `large-v3` run is slower.
- When comparing models or re-running, give each run a distinct `--output-prefix` that includes the model name, for example `<audio-stem>.<model>`, so the `small.en` output is not overwritten. The default prefix overwrites a prior run.

```bash
./transcribe.sh /path/to/audio.mp3 --model small.en --vad-filter \
  --output-prefix /path/to/audio.small.en
./transcribe.sh /path/to/audio.mp3 --model large-v3 --language en --vad-filter \
  --output-prefix /path/to/audio.large-v3
```
