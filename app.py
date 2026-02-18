import os
import json
from flask import Flask, render_template

app = Flask(__name__)

# This helps Python find your images on Windows
PROJECTS_DIR = os.path.join('static', 'projects')

@app.route('/')
def index():
    # Find all folder names in /static/projects
    folders = [f for f in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, f))]
    return render_template('index.html', projects=folders)

@app.route('/project/<name>/')
def project(name):
    # Find all images in the specific folder
    project_path = os.path.join(PROJECTS_DIR, name)
    json_path = os.path.join(project_path, 'info.json')

    # 1. Check if info.json exists
    if not os.path.exists(json_path):
        # 2. Generate standard alphabetical list of images
        images = [f for f in os.listdir(project_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        images.sort() # Standard alphabetical sorting
        
        # 3. Create the data structure
        new_data = {
            "title": name.replace('-', ' ').title(),
            "order": images,
            "description": ""
        }
        
        # 4. Save to file so you can edit it later in VS Code
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=4)
        
        print(f"Generated new info.json for: {name}")

    # 5. Now load the data (either the one just made or the existing one)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return render_template('project.html', 
                           name=data.get('title', name), 
                           images=data.get('order', []),
                           description=data.get('description', ''))

if __name__ == '__main__':
    app.run(debug=True)
