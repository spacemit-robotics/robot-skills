# Build Speech Components

Use this reference when the user asks to build, rebuild, validate build output, or fix build order for SpacemiT Robot SDK speech/audio components.

## Component Map

| Component | SDK path | Speech dependency order |
| --- | --- | --- |
| audio | `components/multimedia/audio` | no speech dependency |
| ASR/STT | `components/model_zoo/asr` | build `components/multimedia/audio` first |
| VAD | `components/model_zoo/vad` | no speech dependency |
| TTS | `components/model_zoo/tts` | build `components/multimedia/audio` first |
| voiceprint | `components/model_zoo/voiceprint` | no speech dependency |
| DOA | `components/multimedia/audio_process/doa` | core algorithm has no speech dependency; live mic demo needs `components/multimedia/audio` available |

## Build Workflow

1. Use `spacemit-robot-shared` to resolve SDK root, mode, remote host, and target only if target context is actually required.
2. Read the target component `package.xml` before building. Treat `<depend>` as the source of truth if it differs from this reference.
3. Build dependent speech components first. If a dependency fails, stop and report that failure before returning to the target component.
4. Source `build/envsetup.sh` from the resolved SDK root, then run `mm` from the component directory.
5. Confirm installed binaries, libraries, and Python artifacts from the build output when they matter to the user request.

## Expected Build Targets

| Component | Typical outputs to look for after build |
| --- | --- |
| audio | `audio_demo`, `libspacemit_audio`, `audio_resampler`, Python package `spacemit_audio` when enabled |
| ASR/STT | ASR/STT library, file/stream demos, Python package `spacemit_asr` when enabled |
| VAD | `vad_simple_demo`, `vad_stream_demo` when enabled, Python package `spacemit_vad` when enabled |
| TTS | `tts_file_demo`, `tts_stream_demo` when enabled, Python package `spacemit_tts` when enabled |
| voiceprint | speaker registration / identify demos if present, C++ library and Python bindings if enabled |
| DOA | `ssl_demo`, `libsound_locator`, Python package `spacemit_audio_process` when enabled |

## Guardrails

- Do not run SDK build commands from the `robot-skills` repository.
- Do not guess missing system dependencies; read `package.xml`, CMake output, and failing logs.
- Do not promote PR scope tests to manual device tests. Build success and PR tests must remain independent of real microphones, speakers, or model downloads unless the user explicitly asks for them.
- For hybrid mode, sync only the requested component paths and their dependencies before building on the board.
