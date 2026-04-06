import subprocess

def run(output):
    print("[PLUGIN] CVE Scan jalan...")

    subprocess.run("nuclei -update-templates", shell=True)
    subprocess.run(f"nuclei -l {output}/live.txt -t cves/ -o {output}/cve.txt", shell=True)

    print("[PLUGIN] selesai")
