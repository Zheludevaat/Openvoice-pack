# Openvoice-pack
One-click Windows installer for MyShell-AI OpenVoice V2. A single Python file silently installs Miniconda, Git, Python 3.9, clones OpenVoice, fetches V2 checkpoints, chooses GPU/CPU PyTorch, verifies SHA-256, and launches the demo. Zero prompts, idempotent, built for non-coders.

The installer also drops `long_synth.py`—a helper for long-form voice generation. After installation you can run:

```
conda activate openvoice
python long_synth.py input.txt reference.wav output.wav
```

where `input.txt` contains one sentence per line.

## Graphical Launcher

After installation, run `openvoice_ui.py` for a simple GUI to access the
installer, demo, and long-form synthesis helper.

```bash
python openvoice_ui.py
```

![UI screenshot](screenshot.png)

## Complete Voice Setup & Styling

1. **Load Reference Voice**
   - Click “Load Clip…” and choose your WAV/MP3 (3–60 s, 24 kHz, quiet).
2. **Extract & Save Timbre**
   ```bash
   python extract_se.py my_voice.wav --name MY_VOICE
   ```

Creates `OpenVoice/checkpoints_v2/custom_ses/MY_VOICE.pth`.
3. **Choose Base Voice & Language**

* Pick from English-US, English-AU, Spanish, French, Chinese, Japanese, Korean.

4. **Adjust Style Controls**

   * **Speed** (0.7–1.3×)
   * **Rhythm** (0.5–1.5×)
   * **Normalize Volume** (on/off)
5. **Type or Load Text**

   * Paste into the text box or load a `.txt` file.
6. **Preview & Generate**

   * Click **Preview Chunk** for the first sentence.
   * Click **Generate Full Audio** to save your long-form WAV/MP3.
