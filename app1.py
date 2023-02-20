import socket
import argparse
import json
from datetime import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address to bind")
    parser.add_argument("port", help="port to bind", type=int)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((args.ip, args.port))
        sock.listen()

        while True:
            conn, addr = sock.accept()
            with conn:
                print(f"New connection from {addr}")

                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    try:
                        message = json.loads(data.decode("utf-8"))
                        file_path = message["file_path"]
                        file_size = message["file_size"]
                        event_type = message["event_type"]

                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{timestamp} - {file_path} ({event_type}) - {file_size} bytes")

                    except json.JSONDecodeError:
                        print(f"Received malformed message: {data}")
