
import os
import requests

SECLISTS_DIR = "/usr/share/wordlists/seclists"
DEFAULT_WORDLIST = os.path.join(SECLISTS_DIR, "Discovery/Web-Content/common.txt")

def ensure_seclists():
    if not os.path.exists(DEFAULT_WORDLIST):
        print("[!] SecLists not found at /usr/share/wordlists/seclists.")
        print("    → Please install it: sudo apt install seclists")
    else:
        print("[✔] SecLists detected at /usr/share/wordlists/seclists")

def fuzz_directories(url, codes=[200, 301, 302], extensions=["", ".php", ".bak", ".txt", ".html"]):
    ensure_seclists()

    if not os.path.exists(DEFAULT_WORDLIST):
        return {"error": "SecLists wordlist not available."}

    found = []
    with open(DEFAULT_WORDLIST, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            path = line.strip()
            for ext in extensions:
                full_url = f"{url.rstrip('/')}/{path}{ext}"
                try:
                    r = requests.get(full_url, timeout=5)
                    if r.status_code in codes:
                        found.append({
                            "url": full_url,
                            "code": r.status_code,
                            "length": len(r.text)
                        })
                        print(f"[+] {r.status_code} → {full_url}")
                except requests.RequestException:
                    continue
    return found
