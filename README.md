# Openvoice-pack
One-click Windows installer for MyShell-AI OpenVoice V2. A single Python file silently installs Miniconda, Git, Python 3.9, clones OpenVoice, fetches V2 checkpoints, chooses GPU/CPU PyTorch, verifies SHA-256, and launches the demo. Zero prompts, idempotent, built for non-coders.

## Installing via Visual Studio Code

The project can also be set up manually inside VS Code:

1. Open a folder in **Visual Studio Code**.
2. Go to **Terminal** ➜ **New Terminal**.
3. Clone the repository:
   ```bash
   git clone https://github.com/myshell-ai/OpenVoice.git
   ```
4. Press **F1** ➜ **Python: Create Environment**, select **venv** and pick **Python&nbsp;3.9**.
5. Activate the newly created `.venv` and install the dependencies (run `pip install -r requirements.txt` if VS Code does not do so automatically).
6. Install `ipykernel` and `ipwidgets` if prompted.
7. Download the model checkpoints and place them in the `openvoice` folder.
8. Open `demo_part1.ipynb` and any other notebooks and follow the prompts to run them.

Alternatively, you may run `install_openvoice.py` for a fully automated setup.
