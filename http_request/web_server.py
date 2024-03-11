# app.py
from flask import Flask, request, jsonify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

estimated_position = "Server Rack"
ENV_OUTPUT = "data/env_output.txt"
RSSI_OUTPUT = "data/rssi_output.txt"

class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_modified(self, event):
        if event.src_path == ENV_OUTPUT or event.src_path == RSSI_OUTPUT:
            send_env()
            send_rssi()

@app.route('/env_location')
def send_env():
    with open(ENV_OUTPUT, 'r') as env:
        envString = env.read()
        envJson = "null"
        if "Charging Station" in envString:
            envJson = "Charging Station"
        elif "Server Rack" in envString:
            envJson = "Server Rack"
        elif "Entrance" in envString:
            envJson = "Entrance"
    return jsonify({'location': envJson})

@app.route('/rssi_location')
def send_rssi():
    with open(RSSI_OUTPUT, 'r') as rssi:
        rssiString = rssi.read()
        rssiJson = "null"
        if "Charging Station" in rssiString:
            rssiJson = "Charging Station"
        elif "Server Rack" in rssiString:
            rssiJson = "Server Rack"
        elif "Entrance" in rssiString:
            rssiJson = "Entrance"
    return jsonify({'location': rssiJson})

if __name__ == '__main__':
    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive= False)
    observer.start()

    try:
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
