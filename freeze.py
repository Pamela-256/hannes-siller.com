import os
from flask_frozen import Freezer
from app import app  # Import your app object from app.py

# 1. Initialize the freezer
freezer = Freezer(app)

# 2. Place the URL generator HERE
# It must be before the freezer.freeze() call
@freezer.register_generator
def project_page():
    # This logic matches your new photography/cinematography structure
    projects_dir = os.path.join('static', 'projects')
    for cat in os.listdir(projects_dir):
        cat_path = os.path.join(projects_dir, cat)
        if os.path.isdir(cat_path):
            for proj in os.listdir(cat_path):
                if os.path.isdir(os.path.join(cat_path, proj)):
                    # This tells Frozen-Flask to 'visit' these nested URLs
                    yield {'category': cat, 'project_name': proj}

if __name__ == '__main__':
    # 3. Finally, execute the freeze
    # This generates the 'build/' folder
    freezer.freeze()
