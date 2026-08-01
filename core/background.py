import subprocess

subprocess.Popen(
    ["python", "wake.py"],
    creationflags=subprocess.CREATE_NO_WINDOW
)