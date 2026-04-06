import socket
import threading
import os
from utils import log_request

HOST = "127.0.0.1"
PORT = 5000

USERNAME = "admin"
PASSWORD = "1234"


def load_html(file_name):
    with open(f"templates/{file_name}", "r", encoding="utf-8") as f:
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
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n\r\n"
            f"{response_body}"
        )
        client_socket.send(response.encode("utf-8"))
        client_socket.close()
        return

    elif path.startswith("/home"):
        if f"username={USERNAME}&password={PASSWORD}" in request:
            files = [
                f for f in os.listdir()
                if f not in ["__pycache__", ".git"]
                and not f.endswith(".pyc")
            ]

            file_list = "".join(
                [f'<li><a href="/{file}">{file}</a></li>' for file in files]
            )

            response_body = load_html("index.html").replace("{{files}}", file_list)
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n\r\n"
                f"{response_body}"
            )
        else:
            response_body = "<h1>Unauthorized</h1>"
            response = (
                "HTTP/1.1 401 Unauthorized\r\n"
                "Content-Type: text/html; charset=utf-8\r\n\r\n"
                f"{response_body}"
            )

        client_socket.send(response.encode("utf-8"))
        client_socket.close()
        return

    else:
        file_path = path.lstrip("/")

        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                content = f.read()

            header = b"HTTP/1.1 200 OK\r\n\r\n"
            client_socket.send(header + content)
        else:
            response_body = "<h1>404 Not Found</h1>"
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html; charset=utf-8\r\n\r\n"
                f"{response_body}"
            )
            client_socket.send(response.encode("utf-8"))

        client_socket.close()
        return


def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen(5)

    print(f"Server running at http://{HOST}:{port}")
    print(f"Open in browser: http://127.0.0.1:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connected by {addr}")

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    start_server(PORT)
