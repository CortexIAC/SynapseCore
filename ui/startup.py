import tkinter as tk
import winsound
import random


class StartupScreen:
    def __init__(self, root, runtime):
        self.root = root
        self.runtime = runtime
        self.alive = True

        self.frame = tk.Frame(root, bg="#020402")
        self.frame.pack(fill="both", expand=True)

        # =========================
        # SCANLINE OVERLAY
        # =========================
        self.overlay = tk.Canvas(self.frame, highlightthickness=0, bg="#020402")
        self.overlay.place(relwidth=1, relheight=1)

        # =========================
        # VIGNETTE OVERLAY
        # =========================
        self.vignette = tk.Canvas(self.frame, highlightthickness=0, bg="#020402")
        self.vignette.place(relwidth=1, relheight=1)

        # =========================
        # CENTER
        # =========================
        center = tk.Frame(self.frame, bg="#020402")
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center,
            text="AI OS",
            fg="#00ff88",
            bg="#020402",
            font=("Consolas", 32)
        ).pack(pady=(0, 10))

        # =========================
        # VAULT BOY
        # =========================
        self.frames = []
        self.done_frames = []
        self.vault_index = 0

        try:
            i = 0
            while True:
                frame = tk.PhotoImage(
                    file=r"C:\Users\Dom\Desktop\ai_os\assets\vaultboy-loading.gif",
                    format=f"gif -index {i}"
                )
                self.frames.append(frame)
                i += 1
        except:
            pass

        try:
            i = 0
            while True:
                frame = tk.PhotoImage(
                    file=r"C:\Users\Dom\Desktop\ai_os\assets\vault-boy.gif",
                    format=f"gif -index {i}"
                )
                self.done_frames.append(frame)
                i += 1
        except:
            pass

        self.current_frames = self.frames

        self.vault_label = tk.Label(center, bg="#020402", bd=0)
        self.vault_label.pack()

        # =========================
        # STATUS
        # =========================
        self.status = tk.Label(
            center,
            text="INITIALIZING...",
            fg="#00ff88",
            bg="#020402",
            font=("Consolas", 10)
        )
        self.status.pack()

        # =========================
        # PROGRESS BAR
        # =========================
        self.bar_width = 300
        self.bar = tk.Canvas(center, width=self.bar_width, height=14,
                             bg="#001a10", highlightthickness=1,
                             highlightbackground="#00ff88")
        self.bar.pack(pady=10)

        # =========================
        # TERMINAL LOG
        # =========================
        self.log = tk.Text(
            center,
            height=5,
            bg="#020402",
            fg="#00ff88",
            font=("Consolas", 9),
            borderwidth=0
        )
        self.log.pack()

        self.lines = [
            "[ OK ] Core initialized",
            "[ OK ] Memory loaded",
            "[ OK ] AI engine online",
            "[ OK ] Modules synced",
            "[ OK ] UI ready",
            "[ OK ] System stable"
        ]

        self.line_index = 0
        self.progress = 0
        self.last_stage = None

        # =========================
        # START LOOPS
        # =========================
        self.animate()
        self.animate_vault()
        self.animate_scanlines()
        self.animate_flicker()
        self.draw_vignette()
        self.animate_text()

    # =========================
    # PROGRESS
    # =========================
    def animate(self):
        if not self.alive or not self.frame.winfo_exists():
            return

        self.progress += 2
        width = int((self.progress / 100) * self.bar_width)

        self.bar.delete("all")

        self.bar.create_rectangle(0, 0, self.bar_width, 14, fill="#001a10", outline="")
        self.bar.create_rectangle(0, 2, width, 12, fill="#00ff88", outline="")
        self.bar.create_rectangle(0, 5, width, 9, fill="#66ffcc", outline="")

        if width > 10:
            self.bar.create_rectangle(width - 10, 2, width, 12, fill="#ccffee", outline="")

        stage_sounds = {
            "core": 500,
            "memory": 650,
            "modules": 800,
            "connect": 950,
            "done": 1100
        }

        stage = "core" if self.progress < 25 else \
                "memory" if self.progress < 50 else \
                "modules" if self.progress < 75 else \
                "connect" if self.progress < 95 else "done"

        if stage != self.last_stage:
            self.last_stage = stage
            try:
                if stage == "done":
                    winsound.Beep(1100, 60)
                    winsound.Beep(1300, 60)
                else:
                    winsound.Beep(stage_sounds[stage], 50)
            except:
                pass

        if self.progress >= 100:
            self.alive = False
            self.current_frames = self.done_frames
            self.root.after(800, self.runtime.load_menu)
        else:
            self.root.after(30, self.animate)

    # =========================
    # VAULT
    # =========================
    def animate_vault(self):
        if not self.alive or not self.vault_label.winfo_exists():
            return

        if self.current_frames:
            frame = self.current_frames[self.vault_index]
            self.vault_label.config(image=frame)
            self.vault_index = (self.vault_index + 1) % len(self.current_frames)

        self.root.after(60, self.animate_vault)

    # =========================
    # TEXT
    # =========================
    def animate_text(self):
        if not self.alive or not self.log.winfo_exists():
            return

        if self.line_index < len(self.lines):
            self.log.insert("end", self.lines[self.line_index] + "\n")
            self.log.see("end")
            self.line_index += 1
            self.root.after(300, self.animate_text)

    # =========================
    # SCANLINES
    # =========================
    def animate_scanlines(self):
        if not self.alive or not self.overlay.winfo_exists():
            return

        self.overlay.delete("all")
        w = self.overlay.winfo_width()
        h = self.overlay.winfo_height()

        for y in range(0, h, 4):
            self.overlay.create_line(0, y, w, y, fill="#002211")

        self.root.after(120, self.animate_scanlines)

    # =========================
    # FLICKER
    # =========================
    def animate_flicker(self):
        if not self.alive or not self.frame.winfo_exists():
            return

        shade = "#020402" if random.random() > 0.1 else "#021004"
        self.frame.configure(bg=shade)

        self.root.after(120, self.animate_flicker)

    # =========================
    # VIGNETTE
    # =========================
    def draw_vignette(self):
        if not self.alive or not self.vignette.winfo_exists():
            return

        self.vignette.delete("all")

        w = self.vignette.winfo_width()
        h = self.vignette.winfo_height()

        for i in range(10):
            pad = int(i * 10)
            color = f"#{i*10:02x}{i*10:02x}{i*10:02x}"

            self.vignette.create_rectangle(
                pad, pad, w - pad, h - pad,
                outline=color
            )

        self.root.after(200, self.draw_vignette)