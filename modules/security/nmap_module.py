from modules.base_module import BaseModule


class NmapModule(BaseModule):
    name = "Nmap"
    interface = "security"

    def run(self, target):
        return f"[SECURITY] Scanning: {target}"