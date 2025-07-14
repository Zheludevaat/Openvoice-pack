#!/usr/bin/env python3

import tkinter as tk


def init_gui():
    """Initialize the GUI for OpenVoice."""
    root = tk.Tk()
    root.title("OpenVoice")
    # Additional GUI setup would go here
    return root


if __name__ == "__main__":
    root = init_gui()
    root.mainloop()
