import os
import time
import socket
import argparse
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def __init__(self, server_address):
        super().__init__()
        self.server_address = server_address

    def on_any_event(self, event):
        file_size = 0
        file_path = event.src_path

        if not event.is_directory:
            if event.event_type == "created":
                event_type = "created"
                file_size = os.path.getsize(file_path)

            elif event.event_type == "modified":
                event_type = "modified"
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                else:
                    return
                    #event_type = "deleted"

            elif event.event_type == "deleted":
                event_type = "deleted"

            else:
                return

            message = {
                "file_path": file_path,
                "file_size": file_size,
                "event_type": event_type
            }
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(self.server_address)
                sock.sendall(json.dumps(message).encode("utf-8"))




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to watch")
    parser.add_argument("ip", help="IP address of the server")
    parser.add_argument("port", help="port of the server", type=int)
    args = parser.parse_args()

    event_handler = MyHandler((args.ip, args.port))
    observer = Observer()
    observer.schedule(event_handler, args.path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
