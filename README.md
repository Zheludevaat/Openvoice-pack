# Openvoice-pack
Helper utilities for MyShell-AI OpenVoice V2. The installer script only writes
the helper programs and does **not** automatically install Conda, Git, Python or
PyTorch. Install those requirements manually before using the helpers.

The installer also drops `long_synth.py`—a helper for long-form voice generation and copies itself into the chosen directory so you can rerun it later. After installation you can run:

```
conda activate openvoice
python long_synth.py input.txt reference.wav output.wav
```

where `input.txt` contains one sentence per line.

## Graphical Launcher

After installation, run `openvoice_ui.py` for a simple GUI to access the
installer, demo, and long-form synthesis helper. Choose your install directory in the top field before running the installer. A copy of the installer is placed there so you can rerun it later.

```bash
python openvoice_ui.py
```


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
