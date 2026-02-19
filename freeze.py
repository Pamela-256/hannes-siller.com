import os
import webbrowser
import http.server
import socketserver
import time
from threading import Thread
from flask_frozen import Freezer
from app import app  # Ensure your Flask object in app.py is named 'app'

# Configuration
freezer = Freezer(app)
BUILD_DIR = 'build'
PORT = 8000

# 1. URL GENERATOR
# This fixed version yields BOTH 'category' and 'project_name' at the same time
@freezer.register_generator
def project_page():
    # Absolute path to your projects folder
    base_path = os.path.abspath(os.path.dirname(__file__))
    projects_dir = os.path.join(base_path, 'static', 'projects')
    
    if not os.path.exists(projects_dir):
        return

    # Scan for Categories (e.g., photography, cinematography)
    for category in os.listdir(projects_dir):
        cat_path = os.path.join(projects_dir, category)
        
        if os.path.isdir(cat_path):
            # Scan for Projects inside each Category (e.g., gallery-hoffmann)
            for project in os.listdir(cat_path):
                proj_path = os.path.join(cat_path, project)
                
                if os.path.isdir(proj_path):
                    # This MUST yield all variables required by your @app.route
                    # route: '/<category>/<project_name>/'
                    yield {
                        'category': category, 
                        'project_name': project
                    }

# 2. PREVIEW SERVER LOGIC
def serve_forever():
    """Starts a local server in the build directory."""
    abspath = os.path.abspath(BUILD_DIR)
    if not os.path.exists(abspath):
        os.makedirs(abspath)
    
    os.chdir(abspath)
    handler = http.server.SimpleHTTPRequestHandler
    # Allow port reuse to avoid "Address already in use" errors on Windows
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"\n[PREVIEW] Serving static site at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    # Step 1: Generate the static HTML/CSS files
    print("--- 1. FREEZING SITE ---")
    try:
        freezer.freeze()
        print(f"Success! Static files generated in /{BUILD_DIR}")
    except Exception as e:
        print(f"Error during freeze: {e}")
        # Stop here if freeze fails so we don't preview an old version
        input("Press Enter to exit...") 
        exit(1)
    
    # Step 2: Start preview server in a background thread
    print("\n--- 2. STARTING PREVIEW ---")
    server_thread = Thread(target=serve_forever, daemon=True)
    server_thread.start()
    
    # Step 3: Wait a moment for server to start, then open browser
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}")
    
    print("Keep this terminal open to continue previewing.")
    print("Press CTRL+C to stop the server when finished.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping preview server. Goodbye!")
