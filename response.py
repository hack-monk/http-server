import gzip

def http_200():
    return "HTTP/1.1 200 OK\r\n\r\n"

def http_404():
    return "HTTP/1.1 404 Not Found\r\n\r\n"


def http_200_with_body(body: str, use_gzip: bool = False) -> bytes:
    content_type = "text/plain"

    if use_gzip:
        compressed_body = gzip.compress(body.encode("utf-8"))
        headers = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}\r\n"
            "Content-Encoding: gzip\r\n"
            f"Content-Length: {len(compressed_body)}\r\n"
            "\r\n"
        ).encode("utf-8")
        return headers + compressed_body
    else:
        body_bytes = body.encode("utf-8")
        headers = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            "\r\n"
        ).encode("utf-8")
        return headers + body_bytes


def http_200_file_response(file_bytes: bytes) -> bytes:
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/octet-stream\r\n"
        "Content-Encoding: identity\r\n"
        f"Content-Length: {len(file_bytes)}\r\n"
        "\r\n"
    ).encode("utf-8")
    return headers + file_bytes
