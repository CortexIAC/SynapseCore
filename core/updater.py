import json
import os
from tkinter import messagebox

VERSION_FILE = "data/version.json"
LAST_VERSION_FILE = "data/last_version.json"


def load_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def check_for_updates():
    current = load_json(VERSION_FILE)
    last = load_json(LAST_VERSION_FILE)

    if not current:
        return

    current_version = current.get("version")

    # First run
    if not last:
        show_changelog(current)  # 👈 SHOW ON FIRST RUN
        save_json(LAST_VERSION_FILE, {"version": current_version})
        return

    last_version = last.get("version")

    if current_version != last_version:
        show_changelog(current)
        save_json(LAST_VERSION_FILE, {"version": current_version})


def show_changelog(data):
    changelog = data.get("changelog", {})

    msg = f"Updated to version {data.get('version')}\n\n"

    for section in ["added", "changed", "fixed"]:
        if section in changelog:
            msg += section.upper() + ":\n"
            for item in changelog[section]:
                msg += f" - {item}\n"
            msg += "\n"

    messagebox.showinfo("Update", msg)