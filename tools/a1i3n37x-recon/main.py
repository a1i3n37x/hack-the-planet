import time
import sys
import json
import os
from core.fingerprint import fingerprint_site

def print_banner():
    print("\n")
    print(" █████╗ ██╗     ██╗███████╗███╗   ██╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗")
    print("██╔══██╗██║     ██║██╔════╝████╗  ██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝")
    print("███████║██║     ██║█████╗  ██╔██╗ ██║███████╗██║     ██║   ██║██████╔╝█████╗  ")
    print("██╔══██║██║     ██║██╔══╝  ██║╚██╗██║╚════██║██║     ██║   ██║██╔═══╝ ██╔══╝  ")
    print("██║  ██║███████╗██║███████╗██║ ╚████║███████║╚██████╗╚██████╔╝██║     ███████╗")
    print("╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝")
    print("       beginner-friendly recon scanner from the Alien37 archives\n")
    print_scope_animation()

def print_scope_animation():
    frames = [
        """\
          +-------------+
          |             |
          |      +      |
          |             |
+---------+------+------+---------+
          |             |
          |      +      |
          |             |
          +-------------+
        """,
        """\
          +-------------+
          |             |
          |      ✛      |
          |             |
+---------+------+------+---------+
          |             |
          |      ✛      |
          |             |
          +-------------+
        """,
        """\
          +-------------+
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
        print("Usage: python3 main.py <url>")
        return

    url = sys.argv[1]

    print_banner()

    print("[+] Step 1: Fingerprinting the target using HTTP GET request...")
    print("    → Simulated command: curl -I {}".format(url))
    print("    → Tip: Look for 'Server' or 'X-Powered-By' headers — they may reveal technologies.")

    result = fingerprint_site(url)

    if "error" in result:
        print("\n[!] Error: {}".format(result["error"]))
        return

    print("\n[+] Fingerprint Summary:")
    print("    URL: {}".format(result["url"]))
    print("    Status Code: {}".format(result["status_code"]))
    print("    Page Title: {}".format(result["title"]))
    print("    Detected Headers:")
    for k, v in result["headers"].items():
        print("      - {}: {}".format(k, v))

    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "fingerprint_report.json")

    with open(report_path, "w") as f:
        json.dump(result, f, indent=4)

    print("\n[✔] Report saved to {}".format(report_path))

if __name__ == "__main__":
    main()
