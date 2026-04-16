import tkinter as tk
import psutil
import os
import random


class SystemMonitorTab:
    def __init__(self, parent, state):
        self.state = state

        # Colors
        self.bg = "#1a1a1a"
        self.panel = "#262626"
        self.text = "#eaeaea"
        self.accent = "#00ffaa"

        # Root frame
        self.frame = tk.Frame(parent, bg=self.bg)

        # Grid layout config
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        parent.add(self.frame, text="System")

        # ========================
        # LEFT PANEL
        # ========================
        self.left = tk.Frame(self.frame, bg=self.panel)
        self.left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.cpu_label = tk.Label(self.left, text="CPU: --%", bg=self.panel, fg=self.text)
        self.cpu_label.pack(anchor="w")

        self.ram_label = tk.Label(self.left, text="RAM: --%", bg=self.panel, fg=self.text)
        self.ram_label.pack(anchor="w")

        self.proc_label = tk.Label(self.left, text="Processes: --", bg=self.panel, fg=self.text)
        self.proc_label.pack(anchor="w")

        # ========================
        # RIGHT PANEL
        # ========================
        self.right = tk.Frame(self.frame, bg=self.panel)
        self.right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.disk_label = tk.Label(self.right, text="Disk: --%", bg=self.panel, fg=self.text)
        self.disk_label.pack(anchor="w")

        self.net_label = tk.Label(self.right, text="Network: -- KB/s", bg=self.panel, fg=self.text)
        self.net_label.pack(anchor="w")

        self.weather_label = tk.Label(self.right, text="Weather: --", bg=self.panel, fg=self.text)
        self.weather_label.pack(anchor="w")

        # 🔥 NOW SAFE (after both exist)
        self.left.pack_propagate(False)
        self.right.pack_propagate(False)

        # ========================
        # CONTROL PANEL
        # ========================
        self.controls = tk.Frame(self.frame, bg=self.panel)
        self.controls.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        tk.Button(self.controls, text="Reload AI",
                  command=lambda: self.state.engine.load_modules()).pack(side="left")

        tk.Button(self.controls, text="Run Test",
                  command=lambda: self.state.engine.run("test")).pack(side="left")

        tk.Button(self.controls, text="Clear Temp",
                  command=self.clear_temp).pack(side="left")

        # ========================
        # CLOCK
        # ========================
        self.clock = tk.Label(
            self.frame,
            text="00:00:00",
            font=("Consolas", 16),
            bg=self.bg,
            fg="#ffffff"
        )
        self.clock.grid(row=2, column=0, columnspan=2, pady=5)

        # ========================
        # ASCII PET
        # ========================
        self.pet = tk.Label(self.frame, text="", bg=self.bg, fg=self.accent)
        self.pet.grid(row=3, column=1, sticky="se", padx=10, pady=10)

        # ========================
        # NETWORK TRACKING
        # ========================
        self.last_bytes = psutil.net_io_counters().bytes_recv

        # Start loops
        self.update_loop()
        self.update_clock()
        self.update_pet()

    # ========================
    # SYSTEM UPDATE LOOP
    # ========================
    def update_loop(self):
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage(os.getcwd())
            procs = len(psutil.pids())

            net = psutil.net_io_counters().bytes_recv
            speed = (net - self.last_bytes) / 1024
            self.last_bytes = net

            self.cpu_label.config(text=f"CPU: {cpu}%")
            self.ram_label.config(text=f"RAM: {mem.percent}%")
            self.proc_label.config(text=f"Processes: {procs}")

            self.disk_label.config(text=f"Disk: {disk.percent}%")
            self.net_label.config(text=f"Network: {round(speed, 2)} KB/s")

            self.weather_label.config(
                text=f"Weather: {random.randint(60, 90)}°F"
            )

        except Exception as e:
            self.cpu_label.config(text=f"Error: {e}")

        self.frame.after(1000, self.update_loop)

    # ========================
    # CLOCK
    # ========================
    def update_clock(self):
        from datetime import datetime
        self.clock.config(text=datetime.now().strftime("%H:%M:%S"))
        self.frame.after(1000, self.update_clock)

    # ========================
    # ASCII PET
    # ========================
    def update_pet(self):
        self.pet.config(text=random.choice([
            "(=^.^=)",
            "(•‿•)",
            "(^_^)"
        ]))
        self.frame.after(4000, self.update_pet)

    # ========================
    # CLEAR TEMP
    # ========================
    def clear_temp(self):
        import tempfile
        import shutil

        temp = tempfile.gettempdir()

        for f in os.listdir(temp):
            try:
                path = os.path.join(temp, f)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except:
                pass

    def enable_security_tools(self):
        if hasattr(self, "security_loaded"):
            return

        self.security_loaded = True

        panel = tk.Frame(self.frame, bg="#001a10")
        panel.pack(fill="x")

        tk.Label(
            panel,
            text="Security Tools",
            fg="#00ff88",
            bg="#001a10"
        ).pack(side="left", padx=10)

        tk.Button(
            panel,
            text="Nmap",
            command=lambda: print("Run Nmap"),
            bg="#003322",
            fg="#00ff88"
        ).pack(side="left", padx=5)

        tk.Button(
            panel,
            text="Wireshark",
            command=lambda: print("Open Wireshark"),
            bg="#003322",
            fg="#00ff88"
        ).pack(side="left", padx=5)