import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import shutil


class FileManagerTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        parent.add(self.frame, text="Files")

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(1, weight=1)

        # --- Path bar ---
        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(self.frame, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=0, columnspan=3, sticky="ew")

        # --- Tree ---
        self.tree = ttk.Treeview(self.frame)
        self.tree.grid(row=1, column=0, sticky="ns")

        # --- Files ---
        self.files = tk.Listbox(self.frame)
        self.files.grid(row=1, column=1, sticky="nsew")
        self.files.bind("<<ListboxSelect>>", self.preview_file)
        self.files.bind("<Double-Button-1>", lambda e: self.open_item())

        # --- Preview ---
        self.preview = tk.Text(self.frame)
        self.preview.grid(row=1, column=2, sticky="nsew")
        self.preview.config(state="disabled")

        # --- Buttons ---
        btn = tk.Frame(self.frame)
        btn.grid(row=2, column=0, columnspan=3, sticky="ew")

        tk.Button(btn, text="Open", command=self.open_item).pack(side="left")
        tk.Button(btn, text="Delete", command=self.delete_item).pack(side="left")
        tk.Button(btn, text="Refresh", command=self.refresh).pack(side="left")

        # --- Context menu ---
        self.menu = tk.Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Open", command=self.open_item)
        self.menu.add_command(label="Rename", command=self.rename_item)
        self.menu.add_command(label="Delete", command=self.delete_item)

        self.files.bind("<Button-3>", self.show_context_menu)

        self.dragged_item = None

        self.populate_tree()

    # ========================
    # TREE
    # ========================

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())

        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]

        for drive in drives:
            node = self.tree.insert("", "end", text=drive)
            self.tree.insert(node, "end")

        self.tree.bind("<<TreeviewOpen>>", self.expand_tree)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def expand_tree(self, event):
        node = self.tree.focus()
        path = self.get_full_path(node)

        if not path or not os.path.exists(path):
            return

        self.tree.delete(*self.tree.get_children(node))

        try:
            for item in os.listdir(path):
                full = os.path.join(path, item)
                if os.path.isdir(full):
                    child = self.tree.insert(node, "end", text=item)
                    self.tree.insert(child, "end")
        except PermissionError:
            pass

    def get_full_path(self, node):
        if not node:
            return None

        path = self.tree.item(node, "text")
        parent = self.tree.parent(node)

        while parent:
            parent_text = self.tree.item(parent, "text")

            if parent_text.endswith(":\\"):
                path = parent_text + path
            else:
                path = os.path.join(parent_text, path)

            parent = self.tree.parent(parent)

        return path

    # ========================
    # FILE LOADING
    # ========================

    def on_tree_select(self, event):
        path = self.get_full_path(self.tree.focus())

        if path and os.path.exists(path):
            self.path_var.set(path)
            self.load_files(path)

    def load_files(self, path):
        self.files.delete(0, tk.END)

        try:
            for item in os.listdir(path):
                self.files.insert(tk.END, item)
        except PermissionError:
            messagebox.showwarning("Access Denied", path)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ========================
    # FILE ACTIONS
    # ========================

    def open_item(self):
        path = self.path_var.get()
        sel = self.files.curselection()

        if not sel:
            return

        name = self.files.get(sel[0])
        full = os.path.join(path, name)

        try:
            if os.path.isdir(full):
                self.path_var.set(full)
                self.load_files(full)
            else:
                os.startfile(full)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_item(self):
        path = self.path_var.get()
        sel = self.files.curselection()

        if not sel:
            return

        name = self.files.get(sel[0])
        full = os.path.join(path, name)

        if not messagebox.askyesno("Delete", f"Delete {name}?"):
            return

        try:
            if os.path.isdir(full):
                shutil.rmtree(full)  # 🔥 FIXED (recursive delete)
            else:
                os.remove(full)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def rename_item(self):
        path = self.path_var.get()
        sel = self.files.curselection()

        if not sel:
            return

        old = self.files.get(sel[0])
        new = simpledialog.askstring("Rename", "New name:", initialvalue=old)

        if not new:
            return

        try:
            os.rename(os.path.join(path, old), os.path.join(path, new))
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ========================
    # PREVIEW (FIXED)
    # ========================

    def preview_file(self, event=None):
        path = self.path_var.get()
        sel = self.files.curselection()

        if not sel:
            return

        name = self.files.get(sel[0])
        full = os.path.join(path, name)

        self.preview.config(state="normal")
        self.preview.delete("1.0", tk.END)

        try:
            if name.lower().endswith((".txt", ".py", ".json", ".log")):
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    self.preview.insert(tk.END, f.read(5000))

            elif name.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                from PIL import Image, ImageTk
                img = Image.open(full)
                img.thumbnail((300, 300))
                self.img = ImageTk.PhotoImage(img)
                self.preview.image_create(tk.END, image=self.img)

            else:
                size = os.path.getsize(full)
                self.preview.insert(tk.END, f"{name}\n{size} bytes")

        except Exception as e:
            self.preview.insert(tk.END, f"Preview error:\n{e}")

        self.preview.config(state="disabled")

    # ========================
    # UI
    # ========================

    def show_context_menu(self, event):
        try:
            idx = self.files.nearest(event.y)
            self.files.selection_clear(0, tk.END)
            self.files.selection_set(idx)
            self.menu.post(event.x_root, event.y_root)
        except:
            pass

    def refresh(self):
        path = self.path_var.get()
        if path and os.path.exists(path):
            self.load_files(path)

    def enable_mod_tools(self):
        if hasattr(self, "mod_tools_loaded"):
            return

        self.mod_tools_loaded = True

        panel = tk.Frame(self.frame, bg="#001a10")
        panel.pack(fill="x")

        tk.Label(
            panel,
            text="Modding Tools",
            fg="#00ff88",
            bg="#001a10"
        ).pack(side="left", padx=10)

        tk.Button(
            panel,
            text="QuickBMS",
            command=lambda: print("QuickBMS launch"),
            bg="#003322",
            fg="#00ff88"
        ).pack(side="left", padx=5)

        tk.Button(
            panel,
            text="BrickBench",
            command=lambda: print("BrickBench launch"),
            bg="#003322",
            fg="#00ff88"
        ).pack(side="left", padx=5)