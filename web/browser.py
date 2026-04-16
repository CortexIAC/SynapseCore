from cefpython3 import cefpython as cef
import tkinter as tk
import ctypes


class TitleHandler:
    def __init__(self, browser_instance):
        self.browser_instance = browser_instance

    def OnTitleChange(self, browser, title):
        if hasattr(self.browser_instance, "on_title_change"):
            self.browser_instance.on_title_change(title)


class LoadHandler:
    def __init__(self, browser_instance):
        self.browser_instance = browser_instance

    def OnLoadEnd(self, browser, frame, **kwargs):
        if frame.IsMain():
            url = frame.GetUrl()
            if hasattr(self.browser_instance, "on_url_change"):
                self.browser_instance.on_url_change(url)


class Browser:
    def __init__(self, parent, url):
        self.parent = parent
        self.url = url
        self.browser = None

        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)  # ✅ THIS LINE ONLY

        top = tk.Frame(self.frame)
        top.pack(fill="x")

        btn = {"font": ("Segoe UI", 11), "width": 3}

        tk.Button(top, text="←", command=self.go_back, **btn).pack(side="left")
        tk.Button(top, text="→", command=self.go_forward, **btn).pack(side="left")
        tk.Button(top, text="⟳", command=self.reload, **btn).pack(side="left")

        self.url_bar = tk.Entry(top, font=("Segoe UI", 11))
        self.url_bar.pack(side="left", fill="x", expand=True, padx=5, pady=4)
        self.url_bar.insert(0, url)

        self.url_bar.bind("<Return>", self.load_url)

        tk.Button(top, text="Go", command=self.load_url).pack(side="left")

        self.browser_frame = tk.Frame(self.frame, bg="black")
        self.browser_frame.pack(fill="both", expand=True)

        self.frame.after(0, self._init_browser)

    def _init_browser(self):
        hwnd = self.browser_frame.winfo_id()

        width = self.browser_frame.winfo_width() or 1200
        height = self.browser_frame.winfo_height() or 800

        window_info = cef.WindowInfo()
        window_info.SetAsChild(hwnd, [0, 0, width, height])

        self.browser = cef.CreateBrowserSync(
            window_info=window_info,
            url=self.url
        )

        self.browser.SetClientHandler(TitleHandler(self))
        self.browser.SetClientHandler(LoadHandler(self))

        self.browser_frame.bind("<Configure>", self._on_resize)

    def force_focus(self):
        try:
            self.frame.focus_force()
            self.url_bar.focus_set()
        except:
            pass

    def on_title_change(self, title):
        if hasattr(self, "title_callback"):
            self.title_callback(title)

    def on_url_change(self, url):
        self.url_bar.delete(0, tk.END)
        self.url_bar.insert(0, url)

    def load_url(self, event=None):
        url = self.url_bar.get()
        if not url.startswith("http"):
            url = "https://" + url

        self.browser.LoadUrl(url)

    def go_back(self):
        if self.browser:
            self.browser.GoBack()

    def go_forward(self):
        if self.browser:
            self.browser.GoForward()

    def reload(self):
        if self.browser:
            self.browser.Reload()

    def _on_resize(self, event):
        if not self.browser:
            return

        hwnd = self.browser.GetWindowHandle()

        ctypes.windll.user32.SetWindowPos(
            hwnd, 0, 0, 0, event.width, event.height, 0x0002
        )

        self.browser.NotifyMoveOrResizeStarted()

    def refresh_view(self):
        self._on_resize(type("e", (), {
            "width": self.browser_frame.winfo_width(),
            "height": self.browser_frame.winfo_height()
        }))

    def close(self):
        if self.browser:
            try:
                self.browser.CloseBrowser(False)
            except:
                pass
            self.browser = None