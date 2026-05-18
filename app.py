import os
import json
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
# Absolute path to prevent Windows pathing issues
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, 'static', 'projects')

def get_portfolio_data():
    structure = {}
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        return structure

    # 1. MASTER LEVEL: Sync Categories (Photography, Home, etc.)
    master_json_path = os.path.join(PROJECTS_DIR, 'info.json')
    all_cats_on_disk = sorted([d for d in os.listdir(PROJECTS_DIR) 
                               if os.path.isdir(os.path.join(PROJECTS_DIR, d))])
    
    if not os.path.exists(master_json_path):
        m_data = {"category_order": all_cats_on_disk, "description": "Main Portfolio", "default": ""}
        with open(master_json_path, 'w', encoding='utf-8') as f:
            json.dump(m_data, f, indent=4)
    
    with open(master_json_path, 'r', encoding='utf-8') as f:
        m_data = json.load(f)
    
    # Sync new folders (like "Home") into the Master JSON automatically
    cur_m_order = m_data.get('category_order', [])
    synced_cats = [c for c in cur_m_order if c in all_cats_on_disk]
    new_cats = [c for c in all_cats_on_disk if c not in synced_cats]
    final_m_order = synced_cats + new_cats

    if final_m_order != cur_m_order:
        m_data['category_order'] = final_m_order
        with open(master_json_path, 'w', encoding='utf-8') as f:
            json.dump(m_data, f, indent=4)

    # 2. CATEGORY LEVEL: Sort Projects or gather direct images
    for cat in final_m_order:
        cat_path = os.path.join(PROJECTS_DIR, cat)
        cat_json_path = os.path.join(cat_path, 'info.json')
        
        # Identify subfolders (projects) and direct images
        all_items = os.listdir(cat_path)
        all_projs_on_disk = sorted([p for p in all_items if os.path.isdir(os.path.join(cat_path, p))])
        direct_images = sorted([f for f in all_items if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
        
        if not os.path.exists(cat_json_path):
            c_init = {"title": cat.replace('-', ' ').title(), "description": "", "project_order": all_projs_on_disk}
            with open(cat_json_path, 'w', encoding='utf-8') as f:
                json.dump(c_init, f, indent=4)
        
        with open(cat_json_path, 'r', encoding='utf-8') as f:
            c_data = json.load(f)
            
        # Sync project folders
        cur_p_order = c_data.get('project_order', [])
        synced_projs = [p for p in cur_p_order if p in all_projs_on_disk]
        new_projs = [p for p in all_projs_on_disk if p not in synced_projs]
        final_p_order = synced_projs + new_projs
        
        if final_p_order != cur_p_order:
            c_data['project_order'] = final_p_order
            with open(cat_json_path, 'w', encoding='utf-8') as f:
                json.dump(c_data, f, indent=4)
            
        project_details = []
        for p in final_p_order:
            p_path = os.path.join(cat_path, p)
            p_json = os.path.join(p_path, 'info.json')
            imgs_on_disk = sorted([f for f in os.listdir(p_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
            
            if not os.path.exists(p_json):
                p_init = {"title": p.replace('-', ' ').title(), "description": "", "order": imgs_on_disk}
                with open(p_json, 'w', encoding='utf-8') as f:
                    json.dump(p_init, f, indent=4)
            
            with open(p_json, 'r', encoding='utf-8') as f:
                p_data = json.load(f)
                # Sync images inside project
                cur_img_order = p_data.get('order', [])
                synced_imgs = [f for f in cur_img_order if f in imgs_on_disk]
                new_imgs = [f for f in imgs_on_disk if f not in synced_imgs]
                p_data['order'] = synced_imgs + new_imgs
                
                if p_data['order'] != cur_img_order:
                    with open(p_json, 'w', encoding='utf-8') as f:
                        json.dump(p_data, f, indent=4)
            
            project_details.append({
                'slug': p, 
                'title': p_data.get('title', p.title()), 
                'desc': p_data.get('description', ""),
                'images': p_data.get('order', [])
            })
            
        structure[cat] = {
            'display_name': c_data.get('title', cat.title()),
            'description': c_data.get('description', ""),
            'projects': project_details,
            'direct_images': direct_images
        }
    # Expose master-level metadata (e.g. default project) to templates
    structure['_master'] = m_data
    return structure

@app.route('/')
def index():
    nav_data = get_portfolio_data()
    # Check master JSON for a default path like "Category" or "Category/Project"
    master = nav_data.get('_master', {})
    default_path = (master or {}).get('default')
    if default_path:
        parts = default_path.strip('/').split('/')
        if len(parts) == 1 and parts[0]:
            return redirect(url_for('project_page', category=parts[0]))
        elif len(parts) >= 2:
            return redirect(url_for('project_page', category=parts[0], project_name=parts[1]))

    return render_template('index.html', nav=nav_data, active_category=None)

@app.route('/<category>/', defaults={'project_name': None})
@app.route('/<category>/<project_name>/')
def project_page(category, project_name):
    nav_data = get_portfolio_data()
    cat_data = nav_data.get(category)
    
    if not cat_data:
        return "Category not found", 404

    # CASE 1: No project_name or Category has no sub-projects
    if not project_name or not cat_data['projects']:
        # Check for custom index.html in category folder
        custom_html_path = os.path.join(PROJECTS_DIR, category, 'index.html')
        if os.path.exists(custom_html_path):
            # Read the custom HTML content
            with open(custom_html_path, 'r', encoding='utf-8') as f:
                custom_content = f.read()
            
            # Render with layout template
            return render_template('custom_page.html',
                                   nav=nav_data,
                                   category=category,
                                   active_category=category,
                                   display_title=cat_data['display_name'],
                                   custom_content=custom_content)
        
        # Default behavior: show direct images
        return render_template('project.html', 
                               nav=nav_data, 
                               category=category,
                               active_category=category,
                               name=None, 
                               display_title=cat_data['display_name'],
                               images=cat_data['direct_images'],
                               description=cat_data['description'])

    # CASE 2: Standard Project folder
    project_path = os.path.join(PROJECTS_DIR, category, project_name)
    json_path = os.path.join(project_path, 'info.json')
    
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
