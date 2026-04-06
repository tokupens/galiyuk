from core.utils import run_cmd, ensure_dir

async def run(config, output):
    ensure_dir(output)
    target = config["target"]

    run_cmd(f"subfinder -d {target} -silent > {output}/subs.txt")
    run_cmd(f"httpx -l {output}/subs.txt -silent -tech-detect -o {output}/live.txt")
    run_cmd(f"katana -list {output}/live.txt -o {output}/urls.txt")
