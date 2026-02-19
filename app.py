import os
import json
from flask import Flask, render_template

app = Flask(__name__)
# Absolute path helps prevent Windows 'File Not Found' errors
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, 'static', 'projects')

def get_portfolio_data():
    structure = {}
    master_json_path = os.path.join(PROJECTS_DIR, 'info.json')
    
    if not os.path.exists(PROJECTS_DIR):
        return structure

    all_cats = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
    
    # 1. Sort Top-Level Categories
    if os.path.exists(master_json_path):
        with open(master_json_path, 'r', encoding='utf-8') as f:
            m_data = json.load(f)
            order = m_data.get('category_order', [])
            categories = [c for c in order if c in all_cats] + [c for c in all_cats if c not in order]
    else:
        categories = sorted(all_cats)

    for cat in categories:
        cat_path = os.path.join(PROJECTS_DIR, cat)
        cat_json_path = os.path.join(cat_path, 'info.json')
        
        # Get all sub-project folders currently on disk
        all_projs = sorted([p for p in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, p))])
        
        # 2. AUTO-GENERATE Category info.json if missing
        if not os.path.exists(cat_json_path):
            cat_init_data = {
                "title": cat.replace('-', ' ').title(),
                "description": f"Explore our {cat.replace('-', ' ')} work.",
                "project_order": all_projs
            }
            with open(cat_json_path, 'w', encoding='utf-8') as f:
                json.dump(cat_init_data, f, indent=4, ensure_ascii=False)
            print(f"Generated missing category JSON for: {cat}")

        # 3. Load Category Data
        with open(cat_json_path, 'r', encoding='utf-8') as f:
            c_data = json.load(f)
            cat_display = c_data.get('title', cat.replace('-', ' ').title())
            cat_desc = c_data.get('description', "")
            p_order = c_data.get('project_order', [])

        # Sync Project Order (Add new folders to the end of navigation)
        projects = [p for p in p_order if p in all_projs] + [p for p in all_projs if p not in p_order]
            
        project_details = []
        for p in projects:
            p_path = os.path.join(cat_path, p)
            p_json = os.path.join(p_path, 'info.json')
            p_title = p.replace('-', ' ').title()
            p_desc = ""
            
            if os.path.exists(p_json):
                with open(p_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    p_title = data.get('title', p_title)
                    p_desc = data.get('description', "")
            
            project_details.append({'slug': p, 'title': p_title, 'desc': p_desc})
            
        structure[cat] = {
            'display_name': cat_display,
            'description': cat_desc,
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
    
    # Get physical images
    files_on_disk = [f for f in os.listdir(project_path) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Auto-Sync: Remove deleted, Add new
        original_order = data.get('order', [])
        synced_order = [f for f in original_order if f in files_on_disk]
        new_files = sorted([f for f in files_on_disk if f not in synced_order])
        data['order'] = synced_order + new_files
        
        # Save if changed
        if data['order'] != original_order:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        # Create new JSON if missing
        data = {
            "title": project_name.replace('-', ' ').title(),
            "order": sorted(files_on_disk),
            "description": "Enter project description here..."
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return render_template('project.html', 
                           nav=nav_data, 
                           category=category, 
                           name=project_name, 
                           display_title=data.get('title'),
                           images=data.get('order', []),
                           description=data.get('description', ''))

if __name__ == '__main__':
    # Using a different port just in case 5000 is busy on Windows
    app.run(debug=True, port=5000)
