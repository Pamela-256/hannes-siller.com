# Hannes Siller Website - Development Documentation

## Overview
This is the source code for Hannes Siller's personal website, a portfolio showcasing various creative works across different categories.

## Project Structure
```
/
├── static/
│   ├── projects/
│   │   ├── Art/
│   │   │   ├── Robodraw/
│   │   │   ├── Robodraw-Exhibition/
│   │   │   └── info.json
│   │   ├── Film/
│   │   │   ├── Norway/
│   │   │   ├── Sweden/
│   │   │   └── info.json
│   │   ├── Hannes-Siller/
│   │   │   └── info.json
│   │   ├── Impressum/
│   │   │   ├── index.html
│   │   │   └── info.json
│   │   ├── Motion/
│   │   │   ├── GWA/
│   │   │   ├── Muesli/
│   │   │   ├── Showreel/
│   │   │   └── info.json
│   │   ├── Photo/
│   │   │   ├── ADAC/
│   │   │   ├── Art Fairs/
│   │   │   ├── Gallery Hoffmann/
│   │   │   ├── Luminale/
│   │   │   ├── Nordic Game/
│   │   │   └── info.json
│   │   └── info.json
│   └── styles.css
├── templates/
│   ├── custom_page.html
│   ├── index.html
│   ├── layout.html
│   └── project.html
├── .gitignore
├── .vibeignore
├── app.py
├── build.py
├── freeze.py
└── requirements.txt
```

## Setup

### Prerequisites
- Python 3.x
- pip

### Installation
1. Clone the repository
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Running the Website

### Development Server
To run the website in development mode:
```bash
python app.py
```

### Building the Website
To build the website for production:
```bash
python build.py
```

## File Structure

### Templates
- `templates/layout.html`: Base template for the website
- `templates/index.html`: Home page template
- `templates/project.html`: Project page template
- `templates/custom_page.html`: Custom page template

### Static Files
- `static/styles.css`: Main stylesheet for the website
- `static/projects/`: Directory containing all project files

### Python Files
- `app.py`: Main application file
- `build.py`: Build script for the website
- `freeze.py`: Freeze script for the website

## Contributing

### Code Style
- Follow PEP 8 guidelines for Python code
- Use consistent indentation (4 spaces)
- Use descriptive variable and function names

### Testing
- Write unit tests for new features
- Ensure all tests pass before submitting a pull request

### Documentation
- Update this README.md file with any new features or changes
- Add comments to your code to explain complex logic

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or issues, please contact the project maintainer.
