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
# 1. Get all actual image files currently in the folder
    current_files = [f for f in os.listdir(project_path) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    current_files.sort()

    # 2. Check if info.json exists
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Sync: Find files that are in the folder but NOT in the JSON list
        existing_order = data.get('order', [])
        new_files = [f for f in current_files if f not in existing_order]
        
        if new_files:
            data['order'] = existing_order + new_files # Append new ones to the end
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"Updated {name}/info.json with {len(new_files)} new images.")
    else:
        # 3. Create new info.json if it doesn't exist (Your previous logic)
        data = {
            "title": name.replace('-', ' ').title(),
            "order": current_files,
            "description": "Add a project description here."
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Generated new info.json for: {name}")

    return render_template('project.html', 
                           name=data.get('title', name), 
                           images=data.get('order', []),
                           description=data.get('description', ''))
    
if __name__ == '__main__':
    app.run(debug=True)
