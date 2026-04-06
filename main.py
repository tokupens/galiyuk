import argparse
import subprocess
import yaml
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

# ===== BANNER =====
def banner():
    print(r"""
   ██████╗  █████╗ ██╗     ██╗██╗   ██╗██╗   ██╗██╗  ██╗
  ██╔════╝ ██╔══██╗██║     ██║╚██╗ ██╔╝╚██╗ ██╔╝██║ ██╔╝
  ██║  ███╗███████║██║     ██║ ╚████╔╝  ╚████╔╝ █████╔╝ 
  ██║   ██║██╔══██║██║     ██║  ╚██╔╝    ╚██╔╝  ██╔═██╗ 
  ╚██████╔╝██║  ██║███████╗██║   ██║      ██║   ██║  ██╗
   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝

        🔥 GaliYuk! - Bug Bounty Automation Tool 🔥
              ⚡ Created by hackerkokgtu ⚡
    """)

# ===== LOAD CONFIG =====
def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

# ===== RUN COMMAND =====
def run_cmd(cmd):
    print(f"[+] Running: {cmd}")
    subprocess.run(cmd, shell=True)

# ===== PIPELINE =====
def subdomain_enum(target, output):
    run_cmd(f"subfinder -d {target} -silent > {output}/subs.txt")

def live_hosts(output):
    run_cmd(f"httpx -l {output}/subs.txt -silent -o {output}/live.txt")

def crawl(output):
    run_cmd(f"katana -list {output}/live.txt -o {output}/urls.txt")

def extract_api(output):
    print("[+] Extracting API endpoint...")
    run_cmd(f"grep -E '/api/' {output}/urls.txt > {output}/api.txt")

def fuzz_api(config, output):
    wl = config["wordlists"]["api"]
    run_cmd(f"ffuf -u FUZZ -w {wl} -mc 200 -o {output}/fuzz.json")

def xss_scan(output):
    run_cmd(f"cat {output}/urls.txt | dalfox pipe > {output}/xss.txt")

# ===== ASYNC WRAPPER =====
async def run_all(config):
    target = config["target"]
    output = config["output"]["folder"]

    os.makedirs(output, exist_ok=True)

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=5) as executor:
        await loop.run_in_executor(executor, subdomain_enum, target, output)
        await loop.run_in_executor(executor, live_hosts, output)
        await loop.run_in_executor(executor, crawl, output)
        await loop.run_in_executor(executor, extract_api, output)
        await loop.run_in_executor(executor, fuzz_api, config, output)
        await loop.run_in_executor(executor, xss_scan, output)

# ===== PLUGIN SYSTEM =====
def load_plugins(output):
    plugin_dir = "plugins"
    if not os.path.exists(plugin_dir):
        return

    for file in os.listdir(plugin_dir):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"plugins.{file[:-3]}"
            module = __import__(module_name, fromlist=["run"])
            print(f"[+] Running plugin: {file}")
            module.run(output)

# ===== MAIN =====
def main():
    parser = argparse.ArgumentParser(
        description="🔥 GaliYuk! - Bug Bounty Automation Tool"
    )
    parser.add_argument("-c", "--config", default="config.yaml", help="Config file")
    parser.add_argument("--no-plugin", action="store_true", help="Disable plugin")

    args = parser.parse_args()

    banner()

    config = load_config(args.config)

    asyncio.run(run_all(config))

    if not args.no_plugin:
        load_plugins(config["output"]["folder"])

    print("\n[✔] Selesai boss 😈")

if __name__ == "__main__":
    main()
