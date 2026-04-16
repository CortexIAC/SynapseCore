import tkinter as tk
from tkinter import ttk

from ui.chat_tab import ChatTab
from ui.debug_tab import DebugTab
from ui.file_manager_tab import FileManagerTab
from ui.system_monitor_tab import SystemMonitorTab
from ui.panels.control_panel import ControlPanel


class MainWindow:
    def __init__(self, root, runtime):
        self.root = root
        self.runtime = runtime
        self.state = runtime.state
        self.state.app = self

        # =========================
        # CLEAR SCREEN
        # =========================
        for w in root.winfo_children():
            w.destroy()

        root.configure(bg="#020402")

        # =========================
        # MENU BAR
        # =========================
        menu_bar = tk.Frame(root, bg="#001a10", height=25)
        menu_bar.pack(fill="x")

        self.interfaces = {
            "default": ["chat", "debug", "files", "system", "control"],

            "development": ["chat", "debug", "assistant"],

            "game modding": ["files", "quickbms", "brickbench", "debug"],

            "internet security": ["system", "nmap", "wireshark", "debug"],
        }

        # FILE
        self.create_dropdown(menu_bar, "FILE", [
            ("Main Menu", self.runtime.load_menu),
            ("Restart", self.runtime.start),
            ("Shutdown", self.runtime.shutdown),
        ])

        # VIEW
        self.view_btn, self.view_menu = self.create_dropdown(menu_bar, "VIEW", [])

        # INTERFACE
        self.interface_btn, self.interface_menu = self.create_dropdown(menu_bar, "INTERFACE", [])

        self.interface_menu.add_command(label="Default", command=lambda: self.set_interface("default"))
        self.interface_menu.add_command(label="Development", command=lambda: self.set_interface("development"))
        self.interface_menu.add_command(label="Game Modding", command=lambda: self.set_interface("game modding"))
        self.interface_menu.add_command(label="Internet Security", command=lambda: self.set_interface("internet security"))

        # HELP
        self.create_dropdown(menu_bar, "HELP", [
            ("About", lambda: self.runtime.debug("[SYSTEM] AI OS v1")),
            ("Debug Log", lambda: self.switch_main_tab("debug")),
        ])

        # =========================
        # TOP BAR
        # =========================
        top = tk.Frame(root, bg="#003322", height=30)
        top.pack(fill="x")

        tk.Label(
            top,
            text=f"AI OS | USER: {self.state.user} | ROLE: {self.state.role.upper()} | MODEL: {self.state.model}",
            fg="#00ff88",
            bg="#003322",
            font=("Consolas", 10)
        ).pack(side="left", padx=10)

        tk.Button(
            top,
            text="SHUTDOWN",
            command=self.runtime.shutdown,
            bg="#220000",
            fg="#ff4444",
            relief="flat"
        ).pack(side="right", padx=10)

        # =========================
        # MAIN AREA
        # =========================
        container = tk.Frame(root, bg="#020402")
        container.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        # =========================
        # BOTTOM BAR (GLOBAL)
        # =========================
        self.bottom_bar = tk.Frame(root, bg="#001a10", height=40)
        self.bottom_bar.pack(side="bottom", fill="x")

        # TABS
        self.chat_tab = ChatTab(self.notebook, self.state, self.runtime)
        self.debug_tab = DebugTab(self.notebook, self.runtime)
        self.file_tab = FileManagerTab(self.notebook)
        self.system_tab = SystemMonitorTab(self.notebook, self.state)
        self.control_tab = ControlPanel(self.notebook, self.state)

        # 🔥 IMPORTANT
        self.tabs = {
            "chat": self.chat_tab,
            "debug": self.debug_tab,
            "files": self.file_tab,
            "system": self.system_tab,
            "control": self.control_tab,
        }

        self.build_view_menu()
        self.notebook.select(0)

        # =========================
        # MIC VISUAL
        # =========================
        self.mic_canvas = tk.Canvas(root, width=120, height=40,
                                    bg="#020402", highlightthickness=0)
        self.mic_canvas.place(x=10, rely=1.0, anchor="sw")

        self.voice_label = tk.Label(root, text="●", fg="#003322",
                                    bg="#020402", font=("Consolas", 12))
        self.voice_label.place(x=135, rely=1.0, anchor="sw")

        self.animate_mic()

    # =========================
    # DROPDOWN BUILDER
    # =========================
    def create_dropdown(self, parent, title, options):
        btn = tk.Menubutton(
            parent,
            text=title,
            bg="#001a10",
            fg="#00ff88",
            relief="flat",
            font=("Consolas", 10)
        )

        menu = tk.Menu(btn, tearoff=0,
                       bg="#001a10", fg="#00ff88")

        for label, command in options:
            menu.add_command(label=label, command=command)

        btn.config(menu=menu)
        btn.pack(side="left", padx=6)

        return btn, menu

    # =========================
    # VIEW MENU
    # =========================
    def build_view_menu(self):
        self.view_menu.delete(0, "end")

        for name in self.tabs:
            self.view_menu.add_command(
                label=name.capitalize(),
                command=lambda n=name: self.switch_main_tab(n)
            )

    # =========================
    # TAB SWITCH
    # =========================
    def switch_main_tab(self, name):
        for i in range(len(self.notebook.tabs())):
            if name in self.notebook.tab(i, "text").lower():
                self.notebook.select(i)
                return

    # =========================
    # INTERFACE SYSTEM
    # =========================
    def enable_code_mode(self):
        self.tabs["chat"].mode = "code"
        self.runtime.debug("[SYSTEM] Code Assistant Enabled")

    def set_interface(self, name):
        self.state.interface = name

        self.interface_btn.config(text=f"INTERFACE [{name.upper()}]")
        self.runtime.debug(f"[SYSTEM] Interface → {name}")

        tab_profile = self.interfaces.get(name, self.interfaces["default"])

        self.build_tabs(tab_profile)

        self.notebook.select(0)

        # =========================
        # DEVELOPMENT
        # =========================
        if name == "development":
            self.enable_code_mode()

            self.set_bottom_tools([
                ("Run Code", lambda: self.tabs["chat"].write("[DEV] Run\n")),
                ("Explain Code", lambda: self.tabs["chat"].write("[DEV] Explain\n")),
            ])

            self.switch_main_tab("chat")

        # =========================
        # MODDING
        # =========================
        elif name == "game modding":
            self.set_bottom_tools([
                ("QuickBMS", lambda: print("QuickBMS")),
                ("BrickBench", lambda: print("BrickBench")),
            ])

            self.switch_main_tab("files")

        # =========================
        # SECURITY
        # =========================
        elif name == "internet security":
            self.set_bottom_tools([
                ("Nmap", lambda: print("Nmap")),
                ("Wireshark", lambda: print("Wireshark")),
            ])

            self.switch_main_tab("system")

        # =========================
        # DEFAULT
        # =========================
        else:
            self.set_bottom_tools([])  # 🔥 clears buttons
            self.switch_main_tab("chat")

    def set_bottom_tools(self, tools):
        # clear existing
        for w in self.bottom_bar.winfo_children():
            w.destroy()

        for label, cmd in tools:
            tk.Button(
                self.bottom_bar,
                text=label,
                command=cmd,
                bg="#003322",
                fg="#00ff88",
                relief="flat"
            ).pack(side="left", padx=5, pady=5)

    def build_tabs(self, tab_list):
        # clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)

        self.tabs = {}

        for tab_name in tab_list:

            if tab_name == "chat":
                self.tabs["chat"] = ChatTab(self.notebook, self.state, self.runtime)

            elif tab_name == "debug":
                self.tabs["debug"] = DebugTab(self.notebook, self.runtime)

            elif tab_name == "files":
                self.tabs["files"] = FileManagerTab(self.notebook)

            elif tab_name == "system":
                self.tabs["system"] = SystemMonitorTab(self.notebook, self.state)

            elif tab_name == "control":
                self.tabs["control"] = ControlPanel(self.notebook, self.state)

            # 🔥 NEW MODULE TABS
            elif tab_name == "assistant":
                self.tabs["assistant"] = ChatTab(self.notebook, self.state, self.runtime)
                self.tabs["assistant"].mode = "code"

            elif tab_name == "quickbms":
                self.tabs["quickbms"] = self.simple_tab("QuickBMS Tool")

            elif tab_name == "brickbench":
                self.tabs["brickbench"] = self.simple_tab("BrickBench Tool")

            elif tab_name == "nmap":
                self.tabs["nmap"] = self.simple_tab("Nmap Scanner")

            elif tab_name == "wireshark":
                self.tabs["wireshark"] = self.simple_tab("Wireshark Viewer")

    def simple_tab(self, title):
        frame = tk.Frame(self.notebook, bg="#000000")

        tk.Label(
            frame,
            text=title,
            fg="#00ff88",
            bg="#000000",
            font=("Consolas", 14)
        ).pack(pady=20)

        self.notebook.add(frame, text=title)

        return frame