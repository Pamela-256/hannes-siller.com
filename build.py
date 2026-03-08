#!/usr/bin/env python
"""
Build script for Hannes Siller portfolio website.
Generates static HTML from Flask templates and serves preview.
"""

import os
import sys
import argparse
import webbrowser
import http.server
import socketserver
import time
from threading import Thread

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from freeze import freezer, BUILD_DIR, PORT


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Build static site')
    parser.add_argument('--no-preview', action='store_true', 
                       help='Skip preview after build')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port for preview server')
    parser.add_argument('--build-dir', type=str, default='build',
                       help='Build directory')
    return parser.parse_args()


def serve_forever(port, build_dir):
    """Start a local server in the build directory."""
    abspath = os.path.abspath(build_dir)
    if not os.path.exists(abspath):
        os.makedirs(abspath)
    
    os.chdir(abspath)
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(('', port), handler) as httpd:
        print(f"[PREVIEW] Serving static site at http://localhost:{port}")
        httpd.serve_forever()


def main():
    """Main build function."""
    args = parse_args()
    
    print("--- BUILDING STATIC SITE ---")
    try:
        freezer.freeze()
        print(f"Success! Static files generated in /{BUILD_DIR}")
    except Exception as e:
        print(f"Error during freeze: {e}")
        sys.exit(1)
    
    if not args.no_preview:
        print("\n--- STARTING PREVIEW ---")
        server_thread = Thread(target=serve_forever, 
                              args=(args.port, args.build_dir), daemon=True)
        server_thread.start()
        
        time.sleep(1)
        webbrowser.open(f"http://localhost:{args.port}")
        
        print("Keep this terminal open to continue previewing.")
        print("Press CTRL+C to stop the server when finished.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping preview server. Goodbye!")


if __name__ == '__main__':
    main()
