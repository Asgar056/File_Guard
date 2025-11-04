import tkinter as tk
from tkinter import filedialog, scrolledtext
from threading import Thread
from fileguard import run_scan, scan_directory, save_baseline

class FileGuardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FileGuard v4 GUI")
        self.root.geometry("850x600")
        self.watch_running = False
        self.baseline_file = "baseline.json"
        self.alerts_log = "alerts.log"

        # Top Frame: Directory selection
        top_frame = tk.Frame(root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        tk.Label(top_frame, text="Directory to monitor:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.dir_entry = tk.Entry(top_frame, width=55)
        self.dir_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Browse", command=self.browse_dir, bg="#4CAF50", fg="white").pack(side=tk.LEFT)

        # Middle Frame: Controls
        mid_frame = tk.Frame(root, padx=10, pady=10)
        mid_frame.pack(fill=tk.X)
        tk.Button(mid_frame, text="Create Baseline", command=self.create_baseline, bg="#2196F3", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(mid_frame, text="Run Scan", command=self.run_scan_gui, bg="#FFC107", fg="black", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(mid_frame, text="Start Watch", command=self.start_watch_thread, bg="#FF5722", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(mid_frame, text="Stop Watch", command=self.stop_watch, bg="#9E9E9E", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Label(mid_frame, text="Interval (sec):", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.interval_entry = tk.Entry(mid_frame, width=5)
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack(side=tk.LEFT)

        # Bottom Frame: Alerts
        bottom_frame = tk.Frame(root, padx=10, pady=10)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        self.alerts_box = scrolledtext.ScrolledText(bottom_frame, width=100, height=25, state=tk.DISABLED)
        self.alerts_box.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_label = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    # --- Functions ---
    def browse_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, folder)

    def append_alert(self, msg, color="black"):
        self.alerts_box.config(state=tk.NORMAL)
        self.alerts_box.insert(tk.END, msg + "\n", color)
        self.alerts_box.tag_config(color, foreground=color)
        self.alerts_box.see(tk.END)
        self.alerts_box.config(state=tk.DISABLED)
        self.status_label.config(text=msg)

    def create_baseline(self):
        directory = self.dir_entry.get()
        baseline_data = scan_directory(directory)
        save_baseline(self.baseline_file, baseline_data)
        self.append_alert(f"Baseline created for {directory}", "green")

    def run_scan_gui(self):
        directory = self.dir_entry.get()
        run_scan(directory, self.baseline_file, self.alerts_log, callback=self.append_alert)
        self.append_alert("Scan completed.", "cyan")

    def watch_mode(self):
        self.watch_running = True
        directory = self.dir_entry.get()
        interval = int(self.interval_entry.get())
        while self.watch_running:
            run_scan(directory, self.baseline_file, self.alerts_log, callback=self.append_alert)
            import time
            time.sleep(interval)

    def start_watch_thread(self):
        if not self.watch_running:
            t = Thread(target=self.watch_mode, daemon=True)
            t.start()
            self.append_alert(f"Watch mode started (every {self.interval_entry.get()} sec)...", "magenta")

    def stop_watch(self):
        if self.watch_running:
            self.watch_running = False
            self.append_alert("Watch mode stopped.", "gray")

# --- Run GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FileGuardGUI(root)
    root.mainloop()
