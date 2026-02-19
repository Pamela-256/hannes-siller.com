import os
import json
from flask import Flask, render_template

app = Flask(__name__)
PROJECTS_DIR = os.path.join('static', 'projects')

def get_portfolio_data():
    structure = {}  # <--- THIS WAS MISSING
    if not os.path.exists(PROJECTS_DIR):
        return structure

    categories = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
    
    for cat in categories:
        cat_path = os.path.join(PROJECTS_DIR, cat)
        projects = [p for p in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, p))]
        
        project_details = []
        for p in projects:
            p_path = os.path.join(cat_path, p)
            json_path = os.path.join(p_path, 'info.json')
            title = p.replace('-', ' ').title()
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    title = data.get('title', title)
            project_details.append({'slug': p, 'title': title})
            
        structure[cat] = {
            'display_name': cat.replace('-', ' ').title(),
            'projects': project_details
        }
    return structure

@app.route('/')
def index():
    nav_data = get_portfolio_data()
    return render_template('index.html', nav=nav_data)

@app.route('/<category>/<project_name>/')
def project_page(category, project_name):
    nav_data = get_portfolio_data()
    project_path = os.path.join(PROJECTS_DIR, category, project_name)
    json_path = os.path.join(project_path, 'info.json')
    
    # 1. Get images from disk
    files_on_disk = [f for f in os.listdir(project_path) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

    # 2. Sync Logic (Load/Update JSON)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        original_order = data.get('order', [])
        synced_order = [f for f in original_order if f in files_on_disk]
        new_files = sorted([f for f in files_on_disk if f not in synced_order])
        updated_order = synced_order + new_files
        if updated_order != original_order:
            data['order'] = updated_order
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
    else:
        data = {"title": project_name.replace('-', ' ').title(), "order": sorted(files_on_disk)}
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    return render_template('project.html', 
                           nav=nav_data, 
                           category=category, 
                           name=project_name, 
                           display_title=data.get('title'),
                           images=data.get('order', []))

if __name__ == '__main__':
    app.run(debug=True)
    