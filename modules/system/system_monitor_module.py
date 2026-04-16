import psutil


class SystemMonitorModule:
    name = "system"

    def run(self, command=None):
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            processes = len(psutil.pids())

            result = "[system] Status\n\n"
            result += f"CPU Usage: {cpu}%\n"
            result += f"RAM Usage: {memory.percent}%\n"
            result += f"RAM Used: {round(memory.used / (1024**3), 2)} GB\n"
            result += f"Processes: {processes}\n"

            return result

        except Exception as e:
            return f"[system] Error: {e}"