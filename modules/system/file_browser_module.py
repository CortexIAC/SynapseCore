import os


class FileBrowserModule:
    name = "files"

    def run(self, command=None):
        import os

        if not command:
            return "[files] commands: ls, open, delete"

        parts = command.split()
        cmd = parts[0]

        try:
            if cmd == "ls":
                path = parts[1] if len(parts) > 1 else os.getcwd()
                return "\n".join(os.listdir(path))

            elif cmd == "open":
                path = parts[1]
                os.startfile(path)
                return f"[files] opened {path}"

            elif cmd == "delete":
                path = parts[1]
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    os.remove(path)
                return f"[files] deleted {path}"

            else:
                return "[files] unknown command"

        except Exception as e:
            return f"[files] error: {e}"