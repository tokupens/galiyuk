from core.utils import run_cmd, ensure_dir

def subdomain(config, output):
    ensure_dir(output)
    target = config["target"]
    run_cmd(f"subfinder -d {target} -silent | tee {output}/subs.txt")

def httpx_scan(output):
    run_cmd(f"httpx -l {output}/subs.txt -silent -tech-detect | tee {output}/live.txt")

def crawl(output):
    run_cmd(f"katana -list {output}/live.txt | tee {output}/urls.txt")
