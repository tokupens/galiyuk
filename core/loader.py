import os
import importlib

def run_plugins(output):
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file not in ["__init__.py", "loader.py"]:
            module = importlib.import_module(f"plugins.{file[:-3]}")
            print(f"[PLUGIN] {file}")
            module.run(output)
