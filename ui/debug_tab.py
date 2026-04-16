import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime


class DebugTab:
    def __init__(self, parent, runtime):
        self.frame = tk.Frame(parent)
        parent.add(self.frame, text="Debug")

        self.log_box = scrolledtext.ScrolledText(
            self.frame,
            bg="#0b0b0b",
            fg="#00ffcc",
            insertbackground="white",
            font=("Consolas", 10)
        )
        self.log_box.pack(fill="both", expand=True)
        self.log_box.config(state="disabled")

        # ✅ THIS is what connects everything
        runtime.debug_callback = self.log

        # tags
        self.log_box.tag_config("VOICE", foreground="#00ffaa")
        self.log_box.tag_config("SYSTEM", foreground="#ffaa00")
        self.log_box.tag_config("ERROR", foreground="#ff4444")
        self.log_box.tag_config("AI", foreground="#66aaff")

    # ========================
    # LOG FUNCTION
    # ========================

    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")

        tag = "SYSTEM"
        if "[VOICE]" in msg:
            tag = "VOICE"
        elif "[ERROR]" in msg:
            tag = "ERROR"
        elif "[AI]" in msg:
            tag = "AI"

        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert("end", f"[{timestamp}] {msg}\n", tag)
        self.log_box.config(state=tk.DISABLED)
        self.log_box.see("end")