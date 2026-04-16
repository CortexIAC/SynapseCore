import tkinter as tk
from core.permissions import is_admin


class ControlPanel:
    def __init__(self, parent, state):
        self.frame = tk.Frame(parent, bg="#001a10")

        # 🔥 REQUIRED
        parent.add(self.frame, text="Control")

        tk.Label(self.frame, text="CENTRAL CONTROL",
                 fg="#00ff88", bg="#001a10").pack(pady=10)

        if not is_admin(state):
            tk.Label(self.frame, text="ACCESS DENIED",
                     fg="red", bg="#001a10").pack()
            return

        self.btn("Restart AI", self.restart)
        self.btn("Clear Memory", self.clear)

    def btn(self, text, cmd):
        tk.Button(self.frame, text=text, command=cmd,
                  bg="#002211", fg="#00ff88", width=25).pack(pady=5)

    def restart(self):
        print("Restarting AI...")

    def clear(self):
        print("Memory cleared")