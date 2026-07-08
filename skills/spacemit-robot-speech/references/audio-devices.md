# Audio Device Troubleshooting

Use this reference when a speech/audio binary reports an empty device list or fails to open a capture/playback stream on a real board, even though the operating system seems to see the sound card. This covers `voice_chat`, `audio_demo`, `asr_stream_demo`, `tts_*_demo` playback, `ssl_demo` live mode, and any voiceprint/mic capture.

## First, Separate Hardware From The Audio Stack

An empty device list is usually NOT a broken microphone. Split the two layers before changing anything:

1. Kernel/ALSA layer — does the card exist?
   - `cat /proc/asound/cards`, `arecord -l`, `aplay -l`
   - Prove raw capture works, bypassing the library: `arecord -D hw:<card>,<dev> -f S16_LE -r 16000 -c <ch> -d 1 /tmp/mic.wav`
2. Library layer — what does the binary's audio library actually see?
   - Most speech binaries use PortAudio. Run the binary's own list command, e.g. `voice_chat -l` or `audio_demo list`.

If step 1 works but step 2 shows no devices, the hardware is fine and the problem is in the audio library the binary loaded. Do not keep re-running `arecord -l`; it will keep passing and lead nowhere.

## PortAudio `Unanticipated host error` / Empty Device List

Symptom: the binary prints something like `Failed to initialize PortAudio: Unanticipated host error` and lists no input/output devices, while ALSA capture works.

Cause: PortAudio initializes every host API backend compiled into it. If it was built with the JACK or PulseAudio backend and no `jackd` / PulseAudio server is running, that backend fails during `Pa_Initialize()`, and PortAudio aborts the whole init — so the working ALSA backend is never enumerated. This commonly happens when a binary links the distro's system PortAudio (which bundles JACK + PulseAudio) instead of the ALSA-only PortAudio built from the SDK `audio` component.

Diagnose which PortAudio is loaded and whether extra backends are pulled in:

```bash
ldd <speech-binary> | grep -iE "portaudio|jack|pulse|asound"
```

- If you see `libjack.so` / `libpulse.so`, the loaded PortAudio has non-ALSA backends.
- Compare with the SDK-built library from the `audio` component build output (typically an ALSA-only `libportaudio.so` under the SDK staging lib dir); `ldd` on it should show `libasound` only.
- Confirm no audio server is running (no `jackd`, no PulseAudio); env flags like `JACK_NO_START_SERVER` do not reliably prevent the failing backend from aborting init.

Fix, preferred order:

1. Make the binary use the SDK's ALSA-only PortAudio instead of the system one (for example by preloading or prepending the SDK staging lib on the library search path). Re-run the binary's list command to confirm devices now appear.
2. Otherwise, provide the missing server, or rebuild PortAudio without the JACK/PulseAudio backends so only ALSA remains.

Report which PortAudio was loaded, its `ldd` audio dependencies, and which fix was applied.

## Related Device Mismatches

Once devices enumerate, capture/playback can still fail on parameters. Check the component `API.md` and the `audio` component notes, then:

- Sample rate not supported by the card → inspect `cat /proc/asound/card<N>/stream0` for supported rates; resample instead of forcing an unsupported rate.
- Wrong channel count / interleaving → match the card's real channel layout; multichannel mic arrays often expose more capture channels than the speech path consumes (pick the speech channel explicitly).
- Playback plays too fast/slow → WAV sample rate differs from the playback config; resample or set the rate explicitly.

## Guardrails

- Do not report a microphone or board as broken based only on an empty device list. Prove the layer first with raw `arecord`/`aplay`, then with the binary's own device list.
- Do not hardcode a card index, device id, or library path from another machine. Probe `arecord -l` / the binary's list output on the actual board.
- Do not silently swap system libraries system-wide to work around a single binary; scope the fix to the run (library search path or preload) unless the user asks to change the system.
