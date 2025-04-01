# 🛠️ MITRE ATT&CK: Privilege Escalation Techniques
> Field Ops Reference • CEH-Aligned • Maintained by [a1i3n37x](https://github.com/a1i3n37x)

These are the 12 primary MITRE ATT&CK techniques under the **Privilege Escalation** tactic (TA0004). Each includes real-world tools and notes for CEH preparation and offensive security labs.

---

<details>
<summary>🔼 <strong>1. Abuse Elevation Control Mechanism (T1548)</strong></summary>

**Description:**  
Misuse of tools like `sudo`, `runas`, or setuid binaries to gain elevated privileges.

**Tools & Scripts:**  
`sudo`, `runas`, [`GTFOBins`](https://gtfobins.github.io/), `PowerUp`, `Linux Exploit Suggester`

**CEH Tie-In:**  
Understand how sudo misconfigurations (e.g., `NOPASSWD`) or vulnerable binaries allow privilege escalation without exploitation.

</details>

---

<details>
<summary>🔼 <strong>2. Access Token Manipulation (T1134)</strong></summary>

**Description:**  
Hijacking or duplicating user tokens to impersonate higher-privilege users.

**Tools & Scripts:**  
`Incognito`, `Tokenvator`, `Mimikatz`

**CEH Tie-In:**  
Token impersonation is common in post-exploitation. Essential for lateral movement and maintaining elevated sessions.

</details>

---

<details>
<summary>🔼 <strong>3. Boot or Logon Autostart Execution (T1547)</strong></summary>

**Description:**  
Persistence by modifying autorun locations like registry keys or startup folders.

**Tools & Scripts:**  
`Autoruns`, `WinPEAS`, `Reg.exe`, `schtasks`

**CEH Tie-In:**  
A frequent tactic for persistence and privilege escalation, especially on misconfigured systems.

</details>

---

<details>
<summary>🔼 <strong>4. Boot or Logon Initialization Scripts (T1037)</strong></summary>

**Description:**  
Backdooring init scripts that execute during user login or system boot.

**Tools & Scripts:**  
`~/.bashrc`, `~/.profile`, PowerShell profile scripts, GPO startup scripts

**CEH Tie-In:**  
Look for writable login scripts or startup folders during recon and escalation phases.

</details>

---

<details>
<summary>🔼 <strong>5. Create or Modify System Process (T1543)</strong></summary>

**Description:**  
Creating or modifying services or daemons to execute attacker code with system-level privileges.

**Tools & Scripts:**  
`sc.exe`, `systemctl`, `WinPEAS`, `NSSM`

**CEH Tie-In:**  
Attackers often turn scripts/binaries into services to escalate and persist.

</details>

---

<details>
<summary>🔼 <strong>6. Event Triggered Execution (T1546)</strong></summary>

**Description:**  
Leveraging event-based mechanisms like file changes, cron jobs, or WMI subscriptions to escalate.

**Tools & Scripts:**  
`cron`, `inotify`, `WMI`, PowerShell `Register-WmiEvent`

**CEH Tie-In:**  
Advanced persistence and escalation technique that shows up in Red Team operations.

</details>

---

<details>
<summary>🔼 <strong>7. Exploitation for Privilege Escalation (T1068)</strong></summary>

**Description:**  
Exploiting known local vulnerabilities to gain higher privileges.

**Tools & Scripts:**  
`SearchSploit`, `Metasploit`, `Linux Exploit Suggester`, `Windows Exploit Suggester`

**CEH Tie-In:**  
Exploit escalation is common in labs and real-world targets. Keep your local exploit arsenal updated.

</details>

---

<details>
<summary>🔼 <strong>8. Hijack Execution Flow (T1574)</strong></summary>

**Description:**  
Redirecting how binaries execute using DLL hijacking, PATH manipulation, or binary planting.

**Tools & Scripts:**  
Procmon, `Sudo PATH hijack`, DLL hijack frameworks, Ghidra

**CEH Tie-In:**  
A stealthy and creative way to elevate privileges or gain persistence in trusted processes.

</details>

---

<details>
<summary>🔼 <strong>9. Process Injection (T1055)</strong></summary>

**Description:**  
Injecting malicious code into another running process to execute under its context.

**Tools & Scripts:**  
`Metasploit`, `Cobalt Strike`, `PowerShell Empire`, `SharpShooter`

**CEH Tie-In:**  
Critical to understand how malware hides in memory. Master the basics of shellcode, memory allocation, and injection types.

</details>

---

<details>
<summary>🔼 <strong>10. Scheduled Task/Job (T1053)</strong></summary>

**Description:**  
Creating scheduled tasks that run payloads as SYSTEM/root or privileged user.

**Tools & Scripts:**  
`schtasks`, `at`, `cron`, `systemd timers`

**CEH Tie-In:**  
Great for stealthy privilege escalation. Look for writable tasks or misconfigurations.

</details>

---

<details>
<summary>🔼 <strong>11. Valid Accounts (T1078)</strong></summary>

**Description:**  
Using stolen, leaked, or default credentials to log in as a privileged user.

**Tools & Scripts:**  
`Mimikatz`, `CrackMapExec`, `Hydra`, `Kerbrute`

**CEH Tie-In:**  
CEH heavily covers password attacks, Kerberos abuse, and credential theft. Token reuse = gold.

</details>

---

<details>
<summary>🔼 <strong>12. User Execution (T1204)</strong></summary>

**Description:**  
Getting a user to manually execute malicious code (e.g., phishing, macros, USB drops).

**Tools & Scripts:**  
`MSFvenom`, macro builders, `.hta` payloads, `social engineering toolkits`

**CEH Tie-In:**  
Often the first step in privilege escalation — trick the user, then pivot and escalate.

</details>

---

### 🧠 Bonus: Tools to Explore
- [linPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS)
- [winPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS)
- [GTFOBins](https://gtfobins.github.io/)
- [LOLBAS](https://lolbas-project.github.io/)

---

> Stay sharp, elevate smart, and leave no footprint. 👽 — *a1i3n37x*
