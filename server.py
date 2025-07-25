import socket
import threading
from .handler import handle_client


def start_server(host="localhost", port=4221, directory=None):
    print(f"HTTP server running on {host}:{port}, serving files from: {directory}")

    server_socket = socket.create_server((host, port), reuse_port=True)
    server_socket.listen()

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, directory))
        thread.daemon = True
        thread.start()
