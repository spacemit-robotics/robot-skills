# Speech Performance

Use this reference when the user asks for model performance, demo performance, latency, RTF, throughput, bandwidth, memory, or repeated benchmark results for speech/audio components.

## Measurement Workflow

1. Resolve execution location with `spacemit-robot-shared`. For board performance, run on the named board; do not substitute host-only results.
2. Build the target component and speech dependencies using `references/build-components.md`.
3. Find the real demo binary from the build output. Run `-h` or `--help` before choosing flags.
4. Use a real model and real input sample. If the model, sample, provider, or device is missing, report that blocker instead of inventing numbers.
5. Run one warmup iteration and exclude it from the summary.
6. Run enough measured iterations for the request. If the user does not specify, prefer at least 5 iterations for quick checks and 20+ for formal reports.
7. Capture raw logs and exact commands. Report where the logs were saved.

## Component Notes

| Component | Measurement source |
| --- | --- |
| audio | Use `audio_demo` or component tests for capture/playback/resampler behavior. This is not a model component. |
| ASR/STT | Use the built ASR file demo or stream demo with the selected backend/model and a fixed WAV sample. Collect text result, audio duration, wall time, and RTF when available. |
| VAD | Use `vad_simple_demo`, stream demo, or a known WAV/frame set. Collect frame count, speech segments, processing time, and RTF if available. |
| TTS | Use `tts_file_demo -h` first. Measure selected backend/model/provider with fixed text, output path, wall time, audio duration, RTF, and optional memory/bandwidth tools. |
| voiceprint | Use available register/identify/verify demo or API harness with fixed enrollment/test samples. Collect score, decision, processing time, and RTF if available. |
| DOA | Use `ssl_demo` for synthetic, WAV, or live mic runs. This is an algorithm/demo benchmark, not a model benchmark. For live mode, confirm mic geometry and channel map first. |

## Reporting Format

Always include:

- component path and current commit or branch
- board/host, execution mode, and target if used
- model/backend/provider and model path when applicable
- input sample or text
- exact build and run commands
- warmup count and measured iteration count
- average metric plus min/max or p50/p95 when available
- raw log paths
- missing preconditions or skipped checks

## Guardrails

- Do not count the first run in model performance summaries unless the user explicitly wants cold-start data.
- Do not compare runs with different providers, inputs, sample rates, thread counts, or model paths without stating the difference.
- Do not treat manual microphone or speaker smoke as a required benchmark precondition unless the user asked for live hardware behavior.
- If a demo falls into interactive mode, stop it, read its help text, and rerun with explicit flags.
