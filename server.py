import socket
import threading
import os
from utils import log_request

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 10000))

USERNAME = "admin"
PASSWORD = "1234"

def load_html(file):
    with open(f"templates/{file}", "r", encoding="utf-8") as f:
        return f.read()

def handle_client(client_socket):
    request = client_socket.recv(4096).decode(errors="ignore")
    if not request:
        client_socket.close()
        return

    request_line = request.split("\n")[0]
    parts = request_line.split()
    if len(parts) < 2:
        client_socket.close()
        return

    method, path = parts[0], parts[1]
    log_request(f"{method} {path}")

    if path == "/":
        response_body = load_html("login.html")

    elif path.startswith("/home"):
        if f"username={USERNAME}&password={PASSWORD}" in request:
            files = [
                f for f in os.listdir()
                if f not in ["__pycache__", ".git"] and not f.endswith(".pyc")
            ]
            file_list = "".join([f'<li><a href="/{f}">{f}</a></li>' for f in files])
            response_body = load_html("index.html").replace("{{files}}", file_list)
        else:
            response_body = "<h1>Unauthorized</h1>"

    else:
        file_path = path.lstrip("/")
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n" + content)
            client_socket.close()
            return
        else:
            response_body = "<h1>404 Not Found</h1>"

    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_body}"
    client_socket.send(response.encode())
    client_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen(5)

    print(f"Server running at http://{HOST}:{port}")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server(PORT)
