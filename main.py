import argparse
from core import recon, api, vuln
from plugins import loader
from core.utils import load_config, banner

def main():
    parser = argparse.ArgumentParser(
        description="🔥 GaliYuk! - Bug Bounty Automation Tool"
    )

    parser.add_argument("-c", "--config", default="config.yaml")

    # MODULE FLAG
    parser.add_argument("--subdomain", action="store_true", help="Subdomain discovery")
    parser.add_argument("--httpx", action="store_true", help="Live host detection")
    parser.add_argument("--crawl", action="store_true", help="Crawling URL")
    parser.add_argument("--api", action="store_true", help="API discovery & fuzz")
    parser.add_argument("--xss", action="store_true", help="XSS scan (dalfox)")
    parser.add_argument("--cve", action="store_true", help="CVE scan (nuclei)")

    args = parser.parse_args()

    banner()
    config = load_config(args.config)
    output = config["output"]["folder"]

    if args.subdomain:
        recon.subdomain(config, output)

    if args.httpx:
        recon.httpx_scan(output)

    if args.crawl:
        recon.crawl(output)

    if args.api:
        api.run(config, output)

    if args.xss:
        vuln.run(config, output)

    if args.cve:
        loader.run_plugins(output)

    print("\n[✔] Done 😈")

if __name__ == "__main__":
    main()
