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
    
    # 1. Get physical files currently in the folder
    files_on_disk = [f for f in os.listdir(project_path) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 2. REMOVE: Filter out filenames from JSON that no longer exist on disk
        original_order = data.get('order', [])
        synced_order = [f for f in original_order if f in files_on_disk]
        
        # 3. ADD: Find new files on disk that aren't in the JSON yet
        new_files = [f for f in files_on_disk if f not in synced_order]
        new_files.sort() # Sort new additions alphabetically before appending
        
        updated_order = synced_order + new_files
        
        # 4. SAVE: Only write to disk if something actually changed
        if updated_order != original_order:
            data['order'] = updated_order
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"Sync complete for {name}: Removed {len(original_order) - len(synced_order)}, Added {len(new_files)}.")
    else:
        # 5. CREATE info.json if no info.JSON exists yet
        files_on_disk.sort()
        data = {
            "title": name.replace('-', ' ').title(),
            "order": files_on_disk,
            "description": ""
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    return render_template('project.html', 
                           name=data.get('title', name), 
                           images=data.get('order', []),
                           description=data.get('description', ''))
    
if __name__ == '__main__':
    app.run(debug=True)
