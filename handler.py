from .response import http_200, http_404, http_200_with_body, http_200_file_response
import os


def handle_client(client_socket, directory=None):
    try:
        request = client_socket.recv(4096).decode("utf-8", errors="ignore")
        print(f"Received request:\n{request}")

        headers_end = request.find("\r\n\r\n")
        header_section = request[:headers_end]
        body_start = headers_end + 4

        lines = header_section.split("\r\n")
        request_line = lines[0]
        headers = lines[1:]

        parts = request_line.split(" ")
        if len(parts) < 2:
            client_socket.sendall(http_404().encode("utf-8"))
            client_socket.close()
            return

        method, path = parts[0], parts[1]

        # Header parsing (case-insensitive)
        header_map = {}
        for header in headers:
            if ": " in header:
                k, v = header.split(": ", 1)
                header_map[k.lower()] = v

        if method == "GET":
            if path == "/":
                response = http_200()

            elif path.startswith("/echo/"):
                echo_str = path[len("/echo/"):]
                accept_encoding = header_map.get("accept-encoding", "")
                use_gzip = "gzip" in accept_encoding.lower()
                response = http_200_with_body(echo_str, use_gzip=use_gzip)


            elif path == "/user-agent":
                user_agent = header_map.get("user-agent", "")
                response = http_200_with_body(user_agent)

            elif path.startswith("/files/") and directory:
                filename = path[len("/files/"):]
                file_path = os.path.join(directory, filename)

                if os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                    response = http_200_file_response(file_bytes)
                else:
                    response = http_404()
            else:
                response = http_404()

        elif method == "POST" and path.startswith("/files/") and directory:
            filename = path[len("/files/"):]
            file_path = os.path.join(directory, filename)

            content_length = int(header_map.get("content-length", 0))

            # Get body (it might already be in buffer)
            request_bytes = request.encode("utf-8", errors="ignore")
            body = request_bytes[body_start:]
            while len(body) < content_length:
                body += client_socket.recv(content_length - len(body))

            # Write body to file
            with open(file_path, "wb") as f:
                f.write(body)

            response = "HTTP/1.1 201 Created\r\n\r\n"

        else:
            response = http_404()

        # Send response
        if isinstance(response, bytes):
            client_socket.sendall(response)
        else:
            client_socket.sendall(response.encode("utf-8"))

    except Exception as e:
        print(f"Error: {e}")
        client_socket.sendall(http_404().encode("utf-8"))
    finally:
        client_socket.close()
