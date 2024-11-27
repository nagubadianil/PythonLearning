
import sys
import os
import builtins
import subprocess
from importlib.metadata import distribution

# Create a set to track explicit imports
explicit_imports = set()

# Save the original __import__ function
original_import = builtins.__import__

# Wrap the __import__ function to track imports
def track_import(name, globals=None, locals=None, fromlist=(), level=0):
    explicit_imports.add(name)
    return original_import(name, globals, locals, fromlist, level)

builtins.__import__ = track_import


def is_standard_library(module_name):
    return module_name in sys.stdlib_module_names

def get_pip_name(import_name):
    try:
        # Try the given import_name first
        dist = distribution(import_name)
        return dist.metadata['Name']
    except ModuleNotFoundError:
        # If that fails, handle known aliases like 'sklearn' -> 'scikit-learn'
        alias_mapping = {
            'sklearn': 'scikit-learn',
            'PIL': 'Pillow',
            'bs4': 'beautifulsoup4',
            'yaml': 'pyyaml',
            'dateutil': 'python-dateutil',
            'sqlalchemy': 'SQLAlchemy',
            'serial': 'pyserial',
        }
        if import_name in alias_mapping:
            return alias_mapping[import_name]
        return None
    
def get_imported_modules():
    imported_modules = set()
    for exp_import in explicit_imports:
        exp_import = exp_import.split(".")[0]
        
        if exp_import.startswith("__"):
            continue
            
        for module_name in sys.modules:
            if module_name == exp_import:
                if is_standard_library(module_name):
                    #print("STD LIB: ", module_name)
                    pass
                else:
                    #print("May be PIP INSTALLED: ", module_name)
                    if module_name is None:
                        continue
                    imported_modules.add(module_name)
    return imported_modules

def get_pip_installed():
    imported_modules = get_imported_modules()
    pip_installed = set()
    for module_name in imported_modules:
        pip_name = get_pip_name(module_name)
        if pip_name is None:
            continue
        else:
            pip_installed.add(pip_name)
            
    outliers = {"None", "packaging" , "more-itertools", "platformdirs"}
    pip_installed -= outliers 
    return pip_installed

def get_version(package_name):
    try:
        result = subprocess.run(
            ["pip", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if line.lower().startswith(package_name.lower()):
                return line.split()[1]  # Second column is the version
    except subprocess.CalledProcessError:
        return None
def get_versions():
    pip_installed = get_pip_installed()

    dict_versions = dict()
    for installed in pip_installed:
        version = get_version(installed)
        dict_versions[installed] = version
    return dict_versions

def write_requirements():
    with open("requirements.txt", "w") as file:
        for key, value in get_versions().items():
            file.write(f"{key}=={value}\n")
       


if __name__=="__main__":
    sys.path.insert(0, os.path.dirname(r"C:\Dev\Experiments\Python Learning\games\bricks_and_ball\game.py"))
    import game
    
    #pip_name = get_pip_name("pandas")
    #print(pip_name)
    #pip_name = get_pip_name("pygame")
    #print(pip_name)
    #get_pip_installed()
    #write_requirements()
    print("name=", get_pip_name("sklearn"))