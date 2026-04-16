import tkinter as tk
import random


class MainMenu:
    def __init__(self, root, runtime):
        self.root = root
        self.runtime = runtime

        self.frame = tk.Frame(root, bg="#020402")
        self.frame.pack(fill="both", expand=True)

        # ✅ CENTERED CONTAINER
        container = tk.Frame(self.frame, bg="#020402")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="AI OS",
            fg="#00ff88",
            bg="#020402",
            font=("Consolas", 24)
        ).pack(pady=40)

        tk.Label(
            container,
            text="System Launcher",
            fg="#00ff88",
            bg="#020402",
            font=("Consolas", 14)
        ).pack(pady=10)

        self.make_button(container, "Open Framework", self.runtime.open_framework)
        self.make_button(container, "Restart", self.runtime.start)

        # waveform
        self.wave = tk.Canvas(
            container,
            width=200,
            height=60,
            bg="#020402",
            highlightthickness=0
        )
        self.wave.pack(pady=20)

        self.animate_wave()

    def make_button(self, parent, text, cmd):
        tk.Button(
            parent,
            text=text,
            command=cmd,
            bg="#003322",
            fg="#00ff88",
            relief="flat",
            width=20
        ).pack(pady=5)

    def animate_wave(self):
        if not self.wave.winfo_exists():
            return

        self.wave.delete("all")

        for i in range(20):
            h = random.randint(5, 40)
            self.wave.create_line(i * 10, 50, i * 10, 50 - h, fill="#00ff88")

        self.root.after(100, self.animate_wave)