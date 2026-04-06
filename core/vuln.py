from core.utils import run_cmd

async def run(config, output):
    run_cmd(f"cat {output}/urls.txt | dalfox pipe > {output}/xss.txt")

    # Open Redirect simple test
    run_cmd(f"grep '=' {output}/urls.txt > {output}/params.txt")
