from .response import http_200, http_404, http_200_with_body, http_200_file_response
import os


def handle_client(client_socket, directory=None):
    buffer = b""

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break  # client disconnected
            buffer += data

            while b"\r\n\r\n" in buffer:
                # Extract request headers
                header_end = buffer.find(b"\r\n\r\n")
                request_data = buffer[:header_end + 4]
                buffer = buffer[header_end + 4:]

                request_text = request_data.decode("utf-8", errors="ignore")
                print(f"Received request:\n{request_text}")

                lines = request_text.split("\r\n")
                if not lines or len(lines[0].split(" ")) < 2:
                    client_socket.sendall(http_404())
                    continue

                request_line = lines[0]
                headers = lines[1:]

                parts = request_line.split(" ")
                method, path = parts[0], parts[1]

                # Parse headers into a dictionary
                header_map = {}
                for h in headers:
                    if ": " in h:
                        k, v = h.split(": ", 1)
                        header_map[k.lower()] = v

                # Detect if client wants to close connection
                connection_header = header_map.get("connection", "").lower()
                should_close = connection_header == "close"

                # Handle request body if needed
                content_length = int(header_map.get("content-length", 0))
                body = b""
                if content_length > 0:
                    while len(buffer) < content_length:
                        more = client_socket.recv(4096)
                        if not more:
                            break
                        buffer += more
                    body = buffer[:content_length]
                    buffer = buffer[content_length:]

                # Build response
                if method == "GET":
                    if path == "/":
                        response = http_200(add_connection_close=should_close)

                    elif path.startswith("/echo/"):
                        echo_str = path[len("/echo/"):]
                        accept_encoding = header_map.get("accept-encoding", "")
                        use_gzip = "gzip" in accept_encoding.lower()
                        response = http_200_with_body(
                            echo_str,
                            use_gzip=use_gzip,
                            add_connection_close=should_close,
                        )

                    elif path == "/user-agent":
                        user_agent = header_map.get("user-agent", "")
                        response = http_200_with_body(
                            user_agent,
                            add_connection_close=should_close,
                        )

                    elif path.startswith("/files/") and directory:
                        filename = path[len("/files/"):]
                        file_path = os.path.join(directory, filename)
                        if os.path.isfile(file_path):
                            with open(file_path, "rb") as f:
                                file_bytes = f.read()
                            response = http_200_file_response(
                                file_bytes, add_connection_close=should_close
                            )
                        else:
                            response = http_404()
                    else:
                        response = http_404()

                elif method == "POST" and path.startswith("/files/") and directory:
                    filename = path[len("/files/"):]
                    file_path = os.path.join(directory, filename)
                    with open(file_path, "wb") as f:
                        f.write(body)
                    response = b"HTTP/1.1 201 Created\r\n\r\n"
                else:
                    response = http_404()

                # Send response (always bytes)
                if isinstance(response, str):
                    response = response.encode("utf-8")
                client_socket.sendall(response)

                if should_close:
                    return  # exit request loop and close connection

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
