
import time
import sys
import json
import os
import subprocess
from core.fingerprint import fingerprint_site
from core.nmap_module import scan_ports
from core.form_finder import find_forms

def print_banner():
    print()
    print(" █████╗ ██╗     ██╗███████╗███╗   ██╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗")
    print("██╔══██╗██║     ██║██╔════╝████╗  ██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝")
    print("███████║██║     ██║█████╗  ██╔██╗ ██║███████╗██║     ██║   ██║██████╔╝█████╗  ")
    print("██╔══██║██║     ██║██╔══╝  ██║╚██╗██║╚════██║██║     ██║   ██║██╔═══╝ ██╔══╝  ")
    print("██║  ██║███████╗██║███████╗██║ ╚████║███████║╚██████╗╚██████╔╝██║     ███████╗")
    print("╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝")
    print("       beginner-friendly recon scanner from the Alien37 archives
")
    time.sleep(1.5)
    animate_title("ALIENSCOPE")
    print_scope_animation()

def animate_title(title):
    print("    ", end="")
    for char in title:
        print(char, end="", flush=True)
        time.sleep(0.15)
    print("
")

def print_scope_animation():
    frames = [
        """          +-------------+
          |             |
          |      +      |
          |             |
+---------+------+------+---------+
          |             |
          |      +      |
          |             |
          +-------------+
        """,
        """          +-------------+
          |             |
          |      ✛      |
          |             |
+---------+------+------+---------+
          |             |
          |      ✛      |
          |             |
          +-------------+
        """,
        """          +-------------+
          |             |
          |      ◉      |
          |             |
+---------+------+------+---------+
          |             |
          |      ◉      |
          |             |
          +-------------+
        """
    ]
    for _ in range(2):
        for frame in frames:
            os.system('clear' if os.name == 'posix' else 'cls')
            print(frame)
            time.sleep(0.2)
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <url or IP>")
        return

    url = sys.argv[1]
    target_host = url.replace("http://", "").replace("https://", "").split(":")[0]

    print_banner()

    print("[+] Step 0: Scanning ports and services with Nmap...")
    print("    → Command used: nmap -sV --top-ports 1000 -v {}".format(target_host))
    print("    → Tip: Start with top 1000 ports for speed. Use full range (-p-) if nothing is found.
")
    print("[~] Running Nmap... This may take a moment.")

    process = subprocess.Popen(
        ["nmap", "-sV", "--top-ports", "1000", "-v", target_host],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    for line in iter(process.stdout.readline, ''):
        print("    " + line.strip())
    process.stdout.close()
    process.wait()

    ports = scan_ports(target_host)
    if not ports:
        print("
[!] No open ports found or Nmap scan failed. Exiting.")
        return

    print("
[+] Open Ports and Services:")
    for port in ports:
        print("    - Port {}/{}: {} {} {}".format(
            port['port'], port['protocol'], port['state'], port['name'],
            f"({port['product']} {port['version']})" if port['product'] else ""
        ))

    http_ports = [p for p in ports if 'http' in p['name']]
    if not http_ports:
        print("
[!] No HTTP service detected. Skipping HTTP fingerprinting and form discovery.")
        return

    http_port = http_ports[0]['port']
    if ":" not in url:
        url += f":{http_port}"

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
        print(f"    → Adjusted URL to {url} for proper HTTP request formatting.")

    print("
[+] Step 1: Fingerprinting the target using HTTP GET request...")
    print("    → Simulated command: curl -I {}".format(url))
    print("    → Tip: Look for 'Server' or 'X-Powered-By' headers — they may reveal technologies.")

    result = fingerprint_site(url)
    if "error" in result:
        print("
[!] Error: {}".format(result["error"]))
        return

    print("
[+] Fingerprint Summary:")
    print("    URL: {}".format(result["url"]))
    print("    Status Code: {}".format(result["status_code"]))
    print("    Page Title: {}".format(result["title"]))
    print("    Detected Headers:")
    for k, v in result["headers"].items():
        print("      - {}: {}".format(k, v))

    print("
[+] Step 2: Searching for HTML forms...")
    print("    → Tip: Forms are common injection points — look for login fields, search boxes, file uploads.")

    forms = find_forms(url)
    if isinstance(forms, dict) and "error" in forms:
        print("    [!] Error discovering forms: {}".format(forms["error"]))
    elif not forms:
        print("    [!] No forms found on the page.")
    else:
        print("    [+] Found {} form(s):".format(len(forms)))
        for idx, form in enumerate(forms, 1):
            print("      {}. {} → {}".format(idx, form["method"], form["action"]))
            for input_field in form["inputs"]:
                print("         - {} ({})".format(input_field["name"], input_field["type"]))
        result["forms"] = forms

    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "fingerprint_report.json")

    with open(report_path, "w") as f:
        json.dump(result, f, indent=4)

    print("
[✔] Report saved to {}".format(report_path))

if __name__ == "__main__":
    main()
