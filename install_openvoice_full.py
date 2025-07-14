#!/usr/bin/env python3
"""Write helper scripts used with OpenVoice.

This installer does not install Conda, Git or other dependencies.
It simply copies utility programs into the chosen directory.
"""
from pathlib import Path
import argparse

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def write_long_synth(dest: Path):
    """Write helper script for long-form synthesis (placeholder)."""
    code = '''#!/usr/bin/env python3
import argparse
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("text_file")
    p.add_argument("reference_wav")
    p.add_argument("output_wav")
    p.add_argument("--lang", default="EN")
    p.add_argument("--base", default="en_default")
    p.add_argument("--emotion", default="neutral")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--rhythm", type=float, default=1.0)
    p.add_argument("--format", default="WAV")
    p.add_argument("--samplerate", default="24000")
    p.add_argument("--channels", default="mono")
    args = p.parse_args()
    print("long_synth placeholder:", args)

if __name__ == "__main__":
    main()
'''
    (dest / 'long_synth.py').write_text(code)
    print(f"{GREEN}long_synth.py written to {dest}{RESET}")


def write_openvoice_ui(dest: Path):
    """Copy GUI launcher into destination directory."""
    src = Path(__file__).with_name('openvoice_ui.py')
    code = src.read_text()
    (dest / 'openvoice_ui.py').write_text(code)
    print(f"{GREEN}openvoice_ui.py written to {dest}{RESET}")


def write_extract_se(dest: Path):
    """Write helper for timbre extraction."""
    code = '''#!/usr/bin/env python3
from pathlib import Path
import torch, argparse
from openvoice.api import ToneColorConverter

p = argparse.ArgumentParser()
p.add_argument("wav", help="Reference WAV/MP3")
p.add_argument("-n","--name", default=None, help="Name for embedding")
args = p.parse_args()

ckpt = Path("OpenVoice/checkpoints_v2/converter")
conv = ToneColorConverter(str(ckpt/"config.json"))
conv.load_ckpt(str(ckpt/"checkpoint.pth"))

emb, _ = conv.get_tone_embedding(args.wav)
name = (args.name or Path(args.wav).stem)
out = Path("OpenVoice/checkpoints_v2/custom_ses")
out.mkdir(parents=True, exist_ok=True)
torch.save(emb, out/f"{name}.pth")
print("Saved embedding \u2192", out/f"{name}.pth")
'''
    (dest / 'extract_se.py').write_text(code)
    print(f"{GREEN}extract_se.py written to {dest}{RESET}")


def write_say(dest: Path):
    """Write CLI to generate audio from text and embeddings."""
    code = '''#!/usr/bin/env python3
import argparse, tempfile
from pathlib import Path
import torch
from melo.api import TTS
from openvoice.api import ToneColorConverter

p = argparse.ArgumentParser()
p.add_argument("--text",   required=True, help="Text to speak")
p.add_argument("--voice",  required=True, help="Embedding name (no .pth)")
p.add_argument("--base",   default="en_default", help="Base speaker token")
p.add_argument("--lang",   default="EN", help="Language code")
p.add_argument("--speed",  type=float, default=1.0, help="0.7–1.3×")
p.add_argument("--rhythm", type=float, default=1.0, help="0.5–1.5×")
p.add_argument("--normalize", action="store_true", help="Normalize volume")
p.add_argument("--out",    default="out.wav", help="Output file")
args = p.parse_args()

CKPT = Path("OpenVoice/checkpoints_v2")
device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS(language=args.lang, device=device)
conv = ToneColorConverter(str(CKPT/"converter"/"config.json"), device=device)
conv.load_ckpt(str(CKPT/"converter"/"checkpoint.pth"))

src = torch.load(str(CKPT/"base_speakers"/"ses"/f"{args.base}.pth"), map_location=device)
tgt = torch.load(str(CKPT/"custom_ses"/f"{args.voice}.pth"), map_location=device)

with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
    tts.tts_to_file(args.text, tts.hps.data.spk2id[args.base], tmp.name,
                    speed=args.speed)
    conv.convert(tmp.name, src, tgt, args.out,
                 rhythm_scale=args.rhythm,
                 normalize_volume=args.normalize)
print("Generated \u2192", args.out)
'''
    (dest / 'say.py').write_text(code)
    print(f"{GREEN}say.py written to {dest}{RESET}")


def copy_self(dest: Path):
    """Place a copy of this installer in the destination."""
    src = Path(__file__)
    (dest / src.name).write_text(src.read_text())
    print(f"{GREEN}{src.name} copied to {dest}{RESET}")


def main():
    parser = argparse.ArgumentParser(description="Install OpenVoice helpers")
    parser.add_argument("--dir", default=".", help="Installation directory")
    args = parser.parse_args()

    dest = Path(args.dir).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)

    print(f"{CYAN}--- OpenVoice V2 Installer ---{RESET}")
    write_long_synth(dest)
    write_openvoice_ui(dest)
    write_extract_se(dest)
    write_say(dest)
    copy_self(dest)
    print(f"{GREEN}Installation complete in {dest}!{RESET}")
    print("To launch the demo:")
    print(f"{YELLOW}conda activate openvoice{RESET}")
    print(f"{YELLOW}python -m openvoice_app --share{RESET}")
    print(f"{YELLOW}python {dest / 'long_synth.py'} input.txt reference.wav output.wav{RESET}")
    print(f"{YELLOW}python {dest / 'openvoice_ui.py'}{RESET}")


if __name__ == "__main__":
    main()
