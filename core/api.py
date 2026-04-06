from core.utils import run_cmd

async def run(config, output):
    wl = config["wordlists"]["api"]

    run_cmd(f"grep -E '/api/' {output}/urls.txt > {output}/api.txt")
    run_cmd(f"ffuf -u FUZZ -w {wl} -mc 200 -o {output}/fuzz.json")
