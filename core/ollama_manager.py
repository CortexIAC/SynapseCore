import subprocess


def get_models():
    try:
        result = subprocess.check_output(["ollama", "list"]).decode()
        lines = result.split("\n")[1:]
        return [l.split()[0] for l in lines if l]
    except:
        return ["llama3"]