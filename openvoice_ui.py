#!/usr/bin/env python3
"""Simple Tkinter GUI for MyShell‑AI OpenVoice V2 helpers.

This launcher lets you:
  • Run / re‑run the installer into a chosen directory
  • Start the web‑demo (`openvoice_app --share`)
  • Call the long‑form synthesiser (`long_synth.py`)
  • Extract timbre embeddings, preview a single sentence and generate full audio

It expects the helper scripts (long_synth.py, extract_se.py, say.py …) to live
next to this file. The installer puts copies of them in your chosen directory
and also copies itself so you can re‑install later.
"""
import tkinter as tk
from tkinter import filedialog, scrolledtext, simpledialog
import subprocess
import threading
import shlex
import sys
from pathlib import Path


# -----------------------------------------------------------------------------
# Helper: spawn a subprocess and stream its output to the log widget
# -----------------------------------------------------------------------------

def run_process(cmd_list):
    """Run *cmd_list* (a list of tokens) in a background thread and stream
    stdout/stderr into the global *log* scrolled‑text widget."""
    command = " ".join(shlex.quote(c) for c in cmd_list)
    log.insert(tk.END, f"$ {command}\n")
    log.see(tk.END)

    def worker():
        proc = subprocess.Popen(cmd_list, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            log.insert(tk.END, line)
            log.see(tk.END)
        proc.wait()
        log.insert(tk.END, f"[exit {proc.returncode}]\n")
        log.see(tk.END)

    threading.Thread(target=worker, daemon=True).start()


# -----------------------------------------------------------------------------
# Top‑level actions (installer, demo, long‑form synthesis)
# -----------------------------------------------------------------------------

def run_installer():
    cmd = [sys.executable, "install_openvoice_full.py", "--dir", install_dir_var.get()]
    run_process(cmd)


def launch_demo():
    cmd = [sys.executable, "-m", "openvoice_app", "--share"]
    run_process(cmd)


def run_long_synth():
    txt = filedialog.askopenfilename(title="Select text file",
                                     filetypes=[("Text", "*.txt")])
    if not txt:
        return
    ref = filedialog.askopenfilename(title="Select reference WAV",
                                     filetypes=[("WAV", "*.wav")])
    if not ref:
        return
    out = filedialog.asksaveasfilename(title="Save output WAV",
                                       defaultextension=".wav",
                                       filetypes=[("WAV", "*.wav")])
    if not out:
        return
    cmd = [sys.executable, "long_synth.py", txt, ref, out]
    run_process(cmd)


# -----------------------------------------------------------------------------
# GUI setup
# -----------------------------------------------------------------------------

root = tk.Tk()
root.title("OpenVoice V2 UI")

# --- model‑state variables ----------------------------------------------------
install_dir_var = tk.StringVar(value=str(Path.cwd()))
clip_path       = tk.StringVar()
embedding_path  = tk.StringVar()
lang_var        = tk.StringVar(value="EN")
base_var        = tk.StringVar(value="en_default")
speed_var       = tk.DoubleVar(value=1.0)
rhythm_var      = tk.DoubleVar(value=1.0)
norm_var        = tk.BooleanVar(value=False)

# --- top‑level buttons -------------------------------------------------------
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

inst_row = tk.Frame(frame)
inst_row.pack(fill="x")

tk.Label(inst_row, text="Install Dir:").pack(side="left")
entry = tk.Entry(inst_row, textvariable=install_dir_var, width=40)
entry.pack(side="left", expand=True, fill="x")


def browse_install_dir():
    path = filedialog.askdirectory(title="Select install directory")
    if path:
        install_dir_var.set(path)


tk.Button(inst_row, text="Browse", command=browse_install_dir).pack(side="left", padx=5)

btn_install = tk.Button(frame, text="Run Installer",   width=25, command=run_installer)
btn_demo    = tk.Button(frame, text="Launch Demo",     width=25, command=launch_demo)
btn_long    = tk.Button(frame, text="Run long_synth.py", width=25, command=run_long_synth)

btn_install.pack(fill="x")
btn_demo.pack(fill="x", pady=5)
btn_long.pack(fill="x")

# --- voice setup & generation pane ------------------------------------------

def load_clip():
    path = filedialog.askopenfilename(title="Select reference clip",
                                      filetypes=[("Audio", "*.wav *.mp3")])
    if path:
        clip_path.set(path)
        log.insert(tk.END, f"Clip: {path}\n")
        log.see(tk.END)


def extract_timbre():
    if not clip_path.get():
        load_clip()
        if not clip_path.get():
            return
    name = simpledialog.askstring("Embedding name", "Name for embedding:")
    if not name:
        return
    cmd = [sys.executable, "extract_se.py", clip_path.get(), "--name", name]
    embedding_path.set(f"OpenVoice/checkpoints_v2/custom_ses/{name}.pth")
    run_process(cmd)


def load_embedding():
    path = filedialog.askopenfilename(title="Select embedding",
                                      filetypes=[("Embedding", "*.pth")])
    if path:
        embedding_path.set(path)
        log.insert(tk.END, f"Embedding: {path}\n")
        log.see(tk.END)


def preview_chunk():
    text = text_box.get("1.0", "end").strip()
    if not text:
        return
    line = text.splitlines()[0]
    if not embedding_path.get():
        log.insert(tk.END, "Select or extract an embedding first\n")
        log.see(tk.END)
        return
    cmd = [
        sys.executable,
        "say.py",
        "--text",   line,
        "--voice",  Path(embedding_path.get()).stem,
        "--base",   base_var.get(),
        "--lang",   lang_var.get(),
        "--speed",  f"{speed_var.get():.2f}",
        "--rhythm", f"{rhythm_var.get():.2f}",
    ]
    if norm_var.get():
        cmd.append("--normalize")
    cmd += ["--out", "preview.wav"]
    run_process(cmd)


def generate_audio():
    if not clip_path.get():
        load_clip()
        if not clip_path.get():
            return
    text_file = filedialog.askopenfilename(title="Select text file",
                                           filetypes=[("Text", "*.txt")])
    if not text_file:
        return
    out_file = filedialog.asksaveasfilename(title="Save output",
                                            defaultextension=".wav",
                                            filetypes=[("WAV", "*.wav"), ("MP3", "*.mp3")])
    if not out_file:
        return
    cmd = [
        sys.executable, "long_synth.py", text_file, clip_path.get(), out_file,
        "--lang",       lang_var.get(),
        "--base",       base_var.get(),
        "--emotion",    "neutral",
        "--speed",      f"{speed_var.get():.2f}",
        "--rhythm",     f"{rhythm_var.get():.2f}",
        "--format",     "WAV",
        "--samplerate", "24000",
        "--channels",   "mono",
    ]
    run_process(cmd)


# Layout for voice‑controls ----------------------------------------------------

top = tk.Frame(root)
top.pack(padx=10, pady=10, fill="x")

# row 0: clip / embedding ------------------------------------------------------

tk.Button(top, text="Load Clip…",             command=load_clip).grid(      row=0, column=0, sticky="ew")

tk.Button(top, text="Extract & Save Timbre", command=extract_timbre).grid(row=0, column=1, sticky="ew")

tk.Button(top, text="Load Embedding…",       command=load_embedding).grid(  row=0, column=2, sticky="ew")

# row 1: language / base -------------------------------------------------------
tk.Label(top, text="Language:").grid(     row=1, column=0, sticky="e")
lang_menu = tk.OptionMenu(top, lang_var, "EN", "ES", "FR", "ZH", "JP", "KR")
lang_menu.grid(row=1, column=1, sticky="w")


tk.Label(top, text="Accent/Base:").grid( row=1, column=2, sticky="e")
base_menu = tk.OptionMenu(top, base_var, "en_default", "en_au", "es_default", "fr_default",
                          "zh_default", "ja_default", "kr_default")
base_menu.grid(row=1, column=3, sticky="w")

# row 2: style sliders ---------------------------------------------------------

tk.Label(top, text="Speed:").grid(  row=2, column=0, sticky="e")
spd = tk.Scale(top, variable=speed_var, from_=0.7, to=1.3, resolution=0.01,
               orient="horizontal")
spd.grid(row=2, column=1, sticky="ew")


tk.Label(top, text="Rhythm:").grid(row=2, column=2, sticky="e")
ryt = tk.Scale(top, variable=rhythm_var, from_=0.5, to=1.5, resolution=0.01,
               orient="horizontal")
ryt.grid(row=2, column=3, sticky="ew")

# row 3: check‑box -------------------------------------------------------------

tk.Checkbutton(top, text="Normalize Volume", variable=norm_var).grid(row=3, column=0,
                                                                      columnspan=2, sticky="w")

# row 4: text box --------------------------------------------------------------
text_box = scrolledtext.ScrolledText(top, width=60, height=10)
text_box.grid(row=4, column=0, columnspan=4, pady=5, sticky="nsew")

# row 5: preview / generate ----------------------------------------------------

tk.Button(top, text="Preview Chunk",      command=preview_chunk).grid( row=5, column=0, columnspan=2, sticky="ew")

tk.Button(top, text="Generate Full Audio", command=generate_audio).grid(row=5, column=2, columnspan=2, sticky="ew")

# column weights for nicer resizing -------------------------------------------

top.columnconfigure(1, weight=1)
top.columnconfigure(3, weight=1)

# -----------------------------------------------------------------------------
# Scroll‑back log
# -----------------------------------------------------------------------------

log = scrolledtext.ScrolledText(root, width=80, height=12)
log.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
