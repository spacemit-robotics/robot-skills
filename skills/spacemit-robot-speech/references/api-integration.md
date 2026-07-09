# Speech API Integration

Use this reference when the user wants Codex to build an application, demo, service, or glue code from speech/audio component APIs and built binaries.

## API Source Of Truth

Read the relevant `API.md` before writing code:

| Need | Read |
| --- | --- |
| capture, playback, duplex, resampler | `components/multimedia/audio/API.md` |
| speech recognition / STT | `components/model_zoo/asr/API.md` |
| voice activity detection | `components/model_zoo/vad/API.md` |
| text to speech | `components/model_zoo/tts/API.md` |
| speaker registration, identify, verify | `components/model_zoo/voiceprint/API.md` |
| sound source localization / DOA | `components/multimedia/audio_process/doa/API.md` |

If the API behavior is still unclear after reading `API.md`, read the public header under `include/`, Python binding code, examples, and demo help text. Do not infer API shape from old skill text.

## Integration Workflow

1. Convert the user request into a component chain.
2. Read the `API.md` files for every component in that chain.
3. Build the components and dependencies using `references/build-components.md`.
4. Confirm headers, libraries, Python packages, and demo binaries are present in the build output.
5. Write the smallest coherent integration code that satisfies the user request.
6. Build and run the integration. Report exact commands and output.

## Common Chains

| User goal | Component chain |
| --- | --- |
| realtime ASR with endpointing | audio capture -> VAD -> ASR |
| file transcription | ASR only, with WAV/sample handling from `API.md` |
| speech synthesis and playback | TTS -> audio player |
| voice assistant loop | audio capture -> VAD -> ASR -> user logic -> TTS -> audio player |
| speaker-aware ASR | audio capture or WAV -> voiceprint -> ASR |
| sound-aware robot behavior | audio capture or multichannel WAV -> DOA |
| multichannel voice interaction | audio capture -> DOA and VAD/ASR, with explicit channel/sample-rate handling |

## Data Contract Checks

Before composing components, check:

- sample rate expected by each component
- channel count and interleaving layout
- PCM16 vs float32 representation
- blocking vs streaming API behavior
- callback thread constraints
- model path and provider selection
- whether Python or C++ is the right surface for the user's target application

## Guardrails

- Do not write an integration against README snippets when `API.md` exists.
- Do not hide required dependencies. If ASR or TTS needs `audio`, build `audio` first.
- Do not assume live device indices or microphone geometry. Probe devices or ask the user when hardware identity matters.
- Do not report a generated integration as done until it has been built or run in the resolved SDK environment, unless the user explicitly asked for a design-only answer.
