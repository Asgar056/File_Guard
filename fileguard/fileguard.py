def scan_directory(monitor_dir):
    """Return dictionary of file_path -> hash for all files in directory."""
    import os, hashlib
    file_hashes = {}
    for root, _, files in os.walk(monitor_dir):
        for file in files:
            path = os.path.join(root, file)
            sha256 = hashlib.sha256()
            try:
                with open(path, "rb") as f:
                    while chunk := f.read(4096):
                        sha256.update(chunk)
                file_hashes[path] = sha256.hexdigest()
            except:
                file_hashes[path] = None
    return file_hashes


def save_baseline(baseline_file, data):
    import json
    with open(baseline_file, "w") as f:
        json.dump(data, f, indent=4)


def run_scan(monitor_dir, baseline_file, alerts_log=None, update_baseline=False, callback=None):
    import os, json
    # load baseline
    if os.path.exists(baseline_file):
        with open(baseline_file, "r") as f:
            baseline = json.load(f)
    else:
        baseline = {}

    current = scan_directory(monitor_dir)

    new_files = [f for f in current if f not in baseline]
    deleted_files = [f for f in baseline if f not in current]
    modified_files = [f for f in current if f in baseline and current[f] != baseline[f]]

    ts = __import__("datetime").datetime.utcnow().isoformat() + "Z"
    for f in new_files:
        line = f"[{ts}] [NEW] {f}"
        if callback: callback(line, "green")
        if alerts_log: open(alerts_log, "a").write(line+"\n")
    for f in modified_files:
        line = f"[{ts}] [MODIFIED] {f}"
        if callback: callback(line, "orange")
        if alerts_log: open(alerts_log, "a").write(line+"\n")
    for f in deleted_files:
        line = f"[{ts}] [DELETED] {f}"
        if callback: callback(line, "red")
        if alerts_log: open(alerts_log, "a").write(line+"\n")

    if update_baseline:
        save_baseline(baseline_file, current)
