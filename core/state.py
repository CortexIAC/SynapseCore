class SystemState:
    def __init__(self):
        self.user = "Dom"
        self.role = "admin"
        self.model = "llama3"
        self.interface = "default"

    def set_user(self, username, role="user"):
        self.user = username
        self.role = role