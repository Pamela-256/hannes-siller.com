import os
from flask_frozen import Freezer
from app import app  # Import your app object from app.py

# 1. Initialize the freezer
freezer = Freezer(app)

# 2. Place the URL generator HERE
# It must be before the freezer.freeze() call
@freezer.register_generator
def project_page():
    # Iterate through every category and every project folder
    for cat in os.listdir(PROJECTS_DIR):
        cat_path = os.path.join(PROJECTS_DIR, cat)
        if os.path.isdir(cat_path):
            for proj in os.listdir(cat_path):
                if os.path.isdir(os.path.join(cat_path, proj)):
                    yield {'category': cat, 'project_name': proj}


if __name__ == '__main__':
    # 3. Finally, execute the freeze
    # This generates the 'build/' folder
    freezer.freeze()
