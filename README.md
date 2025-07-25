# 🧭 Simple HTTP Server

A lightweight HTTP/1.1 server written in Python from scratch. This project demonstrates how core features of a web server work, including request parsing, persistent connections, file handling, and gzip compression.

---

## Features

- Handles basic HTTP GET and POST requests
- Serves files from a specified directory using `/files/{filename}`
- Echo endpoint with `/echo/{text}`
- Reads the `User-Agent` header from `/user-agent`
- Supports persistent connections (HTTP/1.1 default)
- Supports `Connection: close` for explicit disconnection
- Gzip compression support via `Accept-Encoding: gzip`
- Graceful fallback for unknown routes (404)

---

## Supported Endpoints

| Endpoint            | Method | Description                                |
| ------------------- | ------ | ------------------------------------------ |
| `/`                 | GET    | Returns `200 OK` (empty body)              |
| `/echo/{text}`      | GET    | Responds with the given `{text}`           |
| `/user-agent`       | GET    | Returns the `User-Agent` request header    |
| `/files/{filename}` | GET    | Returns the contents of a file             |
| `/files/{filename}` | POST   | Creates a file with the given body content |


---

## Compression Support

- If the client sends:
    Accept-Encoding: gzip

- The server will:
    Compress the response using gzip
    Return Content-Encoding: gzip

---

## Persistent Connections

- HTTP/1.1 connections are persistent by default.
- Include the Connection: close header in a request to force the server to close the connection.
- The server responds with the same header and closes the TCP socket.

---

## Development Notes

- Python version: 3.10+ recommended
- Uses standard library only: socket, gzip, threading, os
- Multi-threaded server for handling concurrent client connections

---

## Testing
-- You can use curl or tools like Postman for testing:
'''bash

curl -v http://localhost:4221/echo/hello
curl -v --data "abc" -H "Content-Type: application/octet-stream" http://localhost:4221/files/sample.txt
curl -v -H "Accept-Encoding: gzip" http://localhost:4221/echo/compressme

  
