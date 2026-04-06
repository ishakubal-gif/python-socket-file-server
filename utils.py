import platform
from datetime import datetime

# Colored output
def print_color(text, color="green"):
    colors = {
        "green": "\033[92m",
        "blue": "\033[94m",
        "red": "\033[91m",
        "end": "\033[0m"
    }
    print(colors.get(color, "") + text + colors["end"])

# System info
def system_info():
    return f"""
System: {platform.system()}
Node: {platform.node()}
Release: {platform.release()}
Processor: {platform.processor()}
"""

# Logging
def log_request(msg):
    with open("logs.txt", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")