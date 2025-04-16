import os
import requests
import hashlib

SECLISTS_DIR = "/usr/share/wordlists/seclists"
DEFAULT_WORDLIST = os.path.join(SECLISTS_DIR, "Discovery/Web-Content/common.txt")

def ensure_seclists():
    if not os.path.exists(DEFAULT_WORDLIST):
        print("[!] SecLists not found at /usr/share/wordlists/seclists.")
        print("    → Please install it: sudo apt install seclists")
    else:
        print("[✔] SecLists detected at /usr/share/wordlists/seclists")

def get_baseline(url):
    try:
        bogus_path = url.rstrip("/") + "/thisshouldnotexist1337"
        r = requests.get(bogus_path, timeout=5)
        return {
            "length": len(r.text),
            "hash": hashlib.md5(r.text.encode()).hexdigest()
        }
    except requests.RequestException:
        return {"length": -1, "hash": ""}

def fuzz_directories(url, codes=[200, 301, 302], extensions=["", ".php", ".bak", ".txt", ".html"]):
    ensure_seclists()

    if not os.path.exists(DEFAULT_WORDLIST):
        return {"error": "SecLists wordlist not available."}

    print("[~] Establishing baseline response fingerprint...")
    baseline = get_baseline(url)
    print(f"    → Baseline length: {baseline['length']} | MD5: {baseline['hash']}")

    found = []
    with open(DEFAULT_WORDLIST, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            path = line.strip()
            for ext in extensions:
                full_url = f"{url.rstrip('/')}/{path}{ext}"
                try:
                    r = requests.get(full_url, timeout=5)
                    body_hash = hashlib.md5(r.text.encode()).hexdigest()
                    if r.status_code in codes:
                        if len(r.text) == baseline["length"] and body_hash == baseline["hash"]:
                            continue  # looks like fallback page
                        found.append({
                            "url": full_url,
                            "code": r.status_code,
                            "length": len(r.text)
                        })
                        print(f"[+] {r.status_code} → {full_url}")
                except requests.RequestException:
                    continue
    return found
