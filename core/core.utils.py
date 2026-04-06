import subprocess
import yaml
import os

def banner():
    print(r"""
   ██████╗  █████╗ ██╗     ██╗██╗   ██╗██╗   ██╗██╗  ██╗
  ██╔════╝ ██╔══██╗██║     ██║╚██╗ ██╔╝╚██╗ ██╔╝██║ ██╔╝
  ██║  ███╗███████║██║     ██║ ╚████╔╝  ╚████╔╝ █████╔╝ 
  ██║   ██║██╔══██║██║     ██║  ╚██╔╝    ╚██╔╝  ██╔═██╗ 
  ╚██████╔╝██║  ██║███████╗██║   ██║      ██║   ██║  ██╗
   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝

        🔥 GaliYuk! - Created by hackerkokgtu 🔥
    """)

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_cmd(cmd):
    print(f"[+] {cmd}")
    subprocess.run(cmd, shell=True)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
