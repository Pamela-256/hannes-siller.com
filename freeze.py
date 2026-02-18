import os
import webbrowser
import http.server
import socketserver
from threading import Thread
from flask_frozen import Freezer
from app import app

freezer = Freezer(app)
BUILD_DIR = 'build'
PORT = 8000

def serve_forever():
    """Starts a local server in the build directory."""
    os.chdir(BUILD_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving static site at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    # 1. Generate the static files
    print("Freezing the site...")
    freezer.freeze()
    
    # 2. Start the server in a background thread
    print("Starting preview server...")
    Thread(target=serve_forever, daemon=True).start()
    
    # 3. Open the browser automatically
    webbrowser.open(f"http://localhost:{PORT}")
    
    print("Previewing site. Press CTRL+C in this terminal to stop.")
    
    # Keep the main script running so the server stays alive
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping preview server.")
