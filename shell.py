import os
import subprocess
import threading
from server import start_server
from utils import print_color, system_info

def run_shell():
    print_color("Welcome to MyShell 🚀", "blue")

    while True:
        try:
            cmd = input("mysh> ").strip()

            if cmd == "":
                continue

            # EXIT
            if cmd == "exit":
                print_color("Exiting shell...", "red")
                break

            # PWD
            elif cmd == "pwd":
                print(os.getcwd())

            # CD
            elif cmd.startswith("cd "):
                try:
                    os.chdir(cmd.split(" ", 1)[1])
                except Exception as e:
                    print_color(str(e), "red")

            # LS
            elif cmd == "ls":
                for file in os.listdir():
                    print(file)

            # SYSTEM INFO
            elif cmd == "sysinfo":
                print(system_info())

            # SHOW LOGS
            elif cmd == "logs":
                try:
                    with open("logs.txt", "r") as f:
                        print(f.read())
                except:
                    print("No logs yet.")

            # START SERVER
            elif cmd.startswith("start-server"):
                try:
                    port = int(cmd.split()[1])
                    thread = threading.Thread(target=start_server, args=(port,), daemon=True)
                    thread.start()
                except:
                    print_color("Usage: start-server <port>", "red")

            # RUN EXTERNAL COMMAND
            else:
                subprocess.run(cmd, shell=True)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")

if __name__ == "__main__":
    run_shell()