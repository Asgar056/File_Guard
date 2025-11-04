FileGuard v4

FileGuard is a reliable file integrity monitoring tool with both CLI and GUI interfaces. It detects new, modified, and deleted files in any directory on your system and logs alerts.

Features:

Scan any folder on your system

Detects new, modified, and deleted files

Create a baseline for comparison

Manual scan or automatic periodic scan (Watch Mode)

Logs alerts to console, GUI, and alerts.log

Optional Tkinter GUI with colored, scrollable alerts

Installation on Ubuntu:

Install Python 3 (if not already)

Check Python version:

python3 --version

If not installed:

sudo apt update
sudo apt install python3 python3-venv python3-pip -y

Install Tkinter (required for GUI)

sudo apt install python3-tk -y

Verify installation:

python3 -c "import tkinter; print('Tkinter works!')"

Clone the GitHub repository

git clone https://github.com/Asgar056/File_Guard.git

cd File_Guard

Create and activate a virtual environment (recommended)

python3 -m venv venv
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Usage:

CLI Mode:

Create baseline:

python3 fileguard.py --init --dir /path/to/test-folder

Run scan:

python3 fileguard.py --dir /path/to/test-folder

Watch mode (automatic scanning):

python3 fileguard.py --dir /path/to/test-folder --watch --interval 30

GUI Mode:

python3 fileguard_gui_main.py

Click Browse to select a folder

Click Create Baseline to initialize

Click Run Scan to check for changes

Click Start Watch to enable automatic monitoring

Enter Interval (seconds) for automatic scans

Click Stop Watch to stop automatic monitoring

Alerts are color-coded in the scrollable window and written to alerts.log

One-Command Installation on Ubuntu:

You can set up FileGuard on a fresh Ubuntu system with one command. This script will:

Install Python 3, pip, and Tkinter (if missing)

Clone the GitHub repository

Create and activate a virtual environment

Install required Python packages

Launch the GUI

Step 1: Run the one-command installer

bash -c "$(curl -fsSL https://raw.githubusercontent.com/Asgar056/File_Guard/main/setup_ubuntu.sh
)"

Step 2: setup_ubuntu.sh content

#!/bin/bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-tk git

if [ ! -d "File_Guard" ]; then
git clone https://github.com/Asgar056/File_Guard.git

fi

cd File_Guard

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python3 fileguard_gui_main.py

Step 3: How it works

The script automatically installs all dependencies and launches the GUI.

After the first run, you can manually activate the virtual environment and run:

source venv/bin/activate
python3 fileguard_gui_main.py

Alerts will be shown in the GUI and saved to alerts.log.

Baseline is stored in baseline.json.

Notes:

Recommended to use a virtual environment on Linux/Ubuntu to avoid system Python issues.

Alerts log (alerts.log) and baseline (baseline.json) are created automatically.

Tkinter is required for GUI mode.

License:

MIT License (or choose your own)

Contribution:

Feel free to fork, improve, and submit pull requests.
