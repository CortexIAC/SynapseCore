import tkinter as tk
import threading
from ai.router import chat

class ChatTab:
    def __init__(self, parent, state, runtime):
        self.state = state

        self.frame = tk.Frame(parent, bg="#000000")

        self.output = tk.Text(self.frame, bg="#000000", fg="#00ff88")
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.frame, bg="#001a10", fg="#00ff88")
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.send)

        self.write("AI READY\n")
        self.mode = "chat"  # or "code"

        parent.add(self.frame, text="Chat")

    def ask(self, msg):
        try:
            if self.mode == "code":
                response = f"[CODE MODE]\n\nAnalyzing:\n{msg}"
            else:
                response = chat(msg, self.state)

            self.frame.after(0, lambda: self.write(response + "\n"))

        except Exception as e:
            self.frame.after(0, lambda: self.write(f"[ERROR] {e}\n"))

    def write(self, text):
        self.output.insert("end", text)
        self.output.see("end")

    def send(self, event=None):
        msg = self.entry.get()
        self.entry.delete(0, "end")

        self.write(f"\n> {msg}\n")

        threading.Thread(
            target=self.ask,
            args=(msg,),
            daemon=True
        ).start()

    def enable_dev_tools(self):
        if hasattr(self, "dev_tools_loaded"):
            return

        self.dev_tools_loaded = True

        panel = tk.Frame(self.frame, bg="#001a10")
        panel.pack(fill="x")

        tk.Label(
            panel,
            text="Development Tools",
            fg="#00ff88",
            bg="#001a10"
        ).pack(side="left", padx=10)

        tk.Button(
            panel,
            text="Run Code",
            command=lambda: self.write("[DEV] Run Code\n"),
            bg="#003322",
            fg="#00ff88"
        ).pack(side="left", padx=5)

        tk.Button(
            panel,
            text="Explain Code",
            command=lambda: self.write("[DEV] Explain Mode\n"),
            bg="#003322",
            fg="#00ff88"
        ).pack(side="left", padx=5)