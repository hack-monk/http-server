import gzip

def http_200(add_connection_close: bool = False) -> bytes:
    headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/plain",
        "Content-Length: 0",
    ]
    if add_connection_close:
        headers.append("Connection: close")

    headers.append("")  # empty line to end headers
    return ("\r\n".join(headers) + "\r\n").encode("utf-8")


def http_404():
    return "HTTP/1.1 404 Not Found\r\n\r\n"


def http_200_with_body(body: str, use_gzip: bool = False, add_connection_close: bool = False) -> bytes:
    content_type = "text/plain"

    if use_gzip:
        compressed_body = gzip.compress(body.encode("utf-8"))
        headers = [
            "HTTP/1.1 200 OK",
            f"Content-Type: {content_type}",
            "Content-Encoding: gzip",
            f"Content-Length: {len(compressed_body)}"
        ]
        if add_connection_close:
            headers.append("Connection: close")
        headers.append("")  # end of headers
        return ("\r\n".join(headers) + "\r\n").encode("utf-8") + compressed_body

    else:
        body_bytes = body.encode("utf-8")
        headers = [
            "HTTP/1.1 200 OK",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body_bytes)}"
        ]
        if add_connection_close:
            headers.append("Connection: close")
        headers.append("")  # end of headers
        return ("\r\n".join(headers) + "\r\n").encode("utf-8") + body_bytes



def http_200_file_response(file_bytes: bytes, add_connection_close: bool = False) -> bytes:
    headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: application/octet-stream",
        "Content-Encoding: identity",
        f"Content-Length: {len(file_bytes)}"
    ]

    if add_connection_close:
        headers.append("Connection: close")

    headers.append("")  # empty line to end headers
    return ("\r\n".join(headers) + "\r\n").encode("utf-8") + file_bytes

