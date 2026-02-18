import os
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
    path = os.path.join(PROJECTS_DIR, name)
    images = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return render_template('project.html', name=name, images=images)

if __name__ == '__main__':
    app.run(debug=True)
