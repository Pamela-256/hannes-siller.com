import os
import json
from flask import Flask, render_template

app = Flask(__name__)
# Absolute path to prevent Windows pathing issues
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, 'static', 'projects')

def get_portfolio_data():
    structure = {}
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        return structure

    # 1. MASTER LEVEL: Sort Categories (Photography, etc.)
    master_json_path = os.path.join(PROJECTS_DIR, 'info.json')
    all_cats = sorted([d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))])
    
    if not os.path.exists(master_json_path):
        with open(master_json_path, 'w', encoding='utf-8') as f:
            json.dump({"category_order": all_cats, "description": "Main Portfolio"}, f, indent=4)
    
    with open(master_json_path, 'r', encoding='utf-8') as f:
        m_data = json.load(f)
        m_order = m_data.get('category_order', [])
        categories = [c for c in m_order if c in all_cats] + [c for c in all_cats if c not in m_order]

    # 2. CATEGORY LEVEL: Sort Projects within Categories
    for cat in categories:
        cat_path = os.path.join(PROJECTS_DIR, cat)
        cat_json_path = os.path.join(cat_path, 'info.json')
        all_projs = sorted([p for p in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, p))])
        
        if not os.path.exists(cat_json_path):
            with open(cat_json_path, 'w', encoding='utf-8') as f:
                json.dump({"title": cat.replace('-', ' ').title(), "description": "", "project_order": all_projs}, f, indent=4)
        
        with open(cat_json_path, 'r', encoding='utf-8') as f:
            c_data = json.load(f)
            p_order = c_data.get('project_order', [])
            projects = [p for p in p_order if p in all_projs] + [p for p in all_projs if p not in p_order]
            
        project_details = []
        for p in projects:
            p_path = os.path.join(cat_path, p)
            p_json = os.path.join(p_path, 'info.json')
            
            # 3. PROJECT LEVEL: Sort Images within Projects
            files_on_disk = sorted([f for f in os.listdir(p_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
            
            if not os.path.exists(p_json):
                p_data = {"title": p.replace('-', ' ').title(), "description": "", "order": files_on_disk}
                with open(p_json, 'w', encoding='utf-8') as f:
                    json.dump(p_data, f, indent=4)
            
            with open(p_json, 'r', encoding='utf-8') as f:
                p_data = json.load(f)
                # Sync images (Remove deleted, add new to end)
                cur_order = p_data.get('order', [])
                synced = [f for f in cur_order if f in files_on_disk]
                new_imgs = [f for f in files_on_disk if f not in synced]
                p_data['order'] = synced + new_imgs
                
                # Save sync if changed
                if p_data['order'] != cur_order:
                    with open(p_json, 'w', encoding='utf-8') as f:
                        json.dump(p_data, f, indent=4)
            
            project_details.append({
                'slug': p, 
                'title': p_data.get('title', p.title()), 
                'desc': p_data.get('description', "")
            })
            
        structure[cat] = {
            'display_name': c_data.get('title', cat.title()),
            'description': c_data.get('description', ""),
            'projects': project_details
        }
    return structure

@app.route('/')
def index():
    nav_data = get_portfolio_data()
    return render_template('index.html', nav=nav_data, active_category=None)

@app.route('/<category>/<project_name>/')
def project_page(category, project_name):
    nav_data = get_portfolio_data()
    project_path = os.path.join(PROJECTS_DIR, category, project_name)
    json_path = os.path.join(project_path, 'info.json')
    
    # Final data load for the specific page
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return render_template('project.html', 
                           nav=nav_data, 
                           category=category,
                           active_category=category,
                           name=project_name, 
                           display_title=data.get('title'),
                           images=data.get('order', []),
                           description=data.get('description', ''))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
