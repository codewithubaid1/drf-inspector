from pathlib import Path

from django.conf import settings


IGNORE_FOLDERS = [

    "__pycache__",
    "migrations",
    ".git",
    "node_modules",
    "venv",
    "env"
]


IGNORE_FILES = [

    ".pyc",
    ".sqlite3"
]



def walk_directory(path):

    structure = []

    for item in path.iterdir():

        if item.name in IGNORE_FOLDERS:
            continue

        if any(
            item.name.endswith(ext)
            for ext in IGNORE_FILES
        ):
            continue

        if item.is_dir():

            structure.append({

                "type": "folder",

                "name": item.name,

                "children": walk_directory(item)
            })

        else:

            structure.append({

                "type": "file",

                "name": item.name
            })

    return structure



def analyze_project_structure():

    base_dir = Path(settings.BASE_DIR)

    return {

        "project_name":
            base_dir.name,

        "installed_apps":
            list(settings.INSTALLED_APPS),

        "structure":
            walk_directory(base_dir)
    }