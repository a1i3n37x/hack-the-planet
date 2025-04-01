# 🛡️ Alien37 Field Ops Guide: Defense Evasion (MITRE ATT&CK TA0005)

> "In the shadows of the system, evasion is the first magic." – a1i3n37x

This section of the Field Ops Guide maps **MITRE ATT&CK Defense Evasion (TA0005)** techniques to attacker behavior, tools, and mitigation/detection strategies. It’s written for field use—quick lookup, practical summaries, and real-world tool links.

---

## 📘 Organization
- **Grouped by Method**: Obfuscation, Masquerading, Impairment, etc.
- **MITRE ID Linked**
- **Quick Use Tags**: 🧪 Tool, 🔍 Detect, 🛡️ Mitigate
- **Use Case Tips for CTF, Red Team, or Lab**

---

## 🔮 Obfuscation & Packing

### `T1027` – [Obfuscated Files or Information](https://attack.mitre.org/techniques/T1027/)
- 🧪 Tools: `Base64`, `PowerShell`, `Invoke-Obfuscation`, `UPX`
- 🔍 Detect: YARA rules, script content inspection, AV/EDR unpacking heuristics
- 🛡️ Mitigate: Monitor for abnormal script execution, enforce code signing
- 💡 **Use Case**: Custom obfuscation for payloads on HTB/THM to evade AVs in labs

### `T1027.001` – [Binary Padding](https://attack.mitre.org/techniques/T1027/001/)
- 🧪 Tools: Manual or scripted junk padding
- 🔍 Detect: Compare hashes, file size anomalies
- 🛡️ Mitigate: Normalize binaries in sandbox before analysis

### `T1027.002` – [Software Packing](https://attack.mitre.org/techniques/T1027/002/)
- 🧪 Tools: `UPX`, custom packers
- 🔍 Detect: Known packer signatures, dynamic analysis in sandbox
- 🛡️ Mitigate: Block known packer-generated binaries, deeper behavioral scanning

### `T1140` – [Deobfuscate/Decode Files or Information](https://attack.mitre.org/techniques/T1140/)
- 🧪 Tools: CyberChef, `base64`, `xor`, PowerShell decoding tools
- 🔍 Detect: Monitor file read + decode combo, decode execution patterns
- 💡 **Use Case**: Reverse engineering encoded payloads or implants

---

## 🥸 Masquerading & Proxy Execution

### `T1036` – [Masquerading](https://attack.mitre.org/techniques/T1036/)
- 🧪 Tools: Rename binaries to `svchost.exe`, copy icons
- 🔍 Detect: File path anomalies, digital signature mismatch
- 🛡️ Mitigate: Application allowlisting, executable signing enforcement

### `T1218` – [Signed Binary Proxy Execution](https://attack.mitre.org/techniques/T1218/)
- 🧪 Tools: `rundll32`, `mshta`, `regsvr32`, `InstallUtil`, `wmic`, `powershell.exe`
- 🔍 Detect: Unusual parent-child process trees
- 🛡️ Mitigate: Block abuse of signed binaries where possible
- 💡 **Use Case**: Bypass application whitelisting on a restricted HTB machine

### Sub-techniques to expand later:
- `T1218.001` – Compilers
- `T1218.004` – InstallUtil
- `T1218.005` – Mshta
- `T1218.011` – Rundll32

---

## 🧨 Impairing Defenses

### `T1562` – [Impair Defenses](https://attack.mitre.org/techniques/T1562/)
- 🧪 Tools: `netsh advfirewall`, `reg`, `sc`, `powershell`
- 🔍 Detect: Sudden changes in firewall or Defender settings
- 🛡️ Mitigate: GPO enforcement, audit logs

### Sub-techniques (to expand):
- `T1562.001` – Disable or Modify Tools
- `T1562.004` – Disable or Modify System Firewall

---

## 🫥 Hiding Artifacts

### `T1564` – [Hide Artifacts](https://attack.mitre.org/techniques/T1564/)
- 🧪 Tools: Hidden files/folders, renamed services, timestamp manipulation
- 🔍 Detect: Alternate Data Streams (ADS), hidden file scans
- 🛡️ Mitigate: Monitor for hidden directories or unexpected startup changes
- 💡 **Use Case**: Timestomp for post-exploitation stealth

### `T1070` – [Indicator Removal on Host](https://attack.mitre.org/techniques/T1070/)
- 🧪 Tools: `wevtutil`, `del`, `Clear-EventLog`
- 🔍 Detect: Correlation gaps, event log truncation
- 🛡️ Mitigate: Remote logging, tamper-evident systems
- 💡 **Use Case**: Clean up evidence before submitting a flag on HTB

---

## 🧬 Hijack Execution Flow

### `T1574` – [Hijack Execution Flow](https://attack.mitre.org/techniques/T1574/)
- 🧪 Tools: DLL side-loading, path interception, COM hijacking
- 🔍 Detect: Monitor registry, abnormal DLL loads, unsigned binaries in system paths
- 🛡️ Mitigate: DLL safe-loading practices, code signing, controlled folder access
- 💡 **Use Case**: Sneak custom payloads into trusted processes

---

## 🧪 Alternate Authentication Material

### `T1550` – [Use Alternate Authentication Material](https://attack.mitre.org/techniques/T1550/)
- 🧪 Tools: `Mimikatz`, stolen cookies, tokens, SSH keys
- 🔍 Detect: Logon events without password use, unusual credential store access
- 🛡️ Mitigate: MFA, restrict token reuse, vault key management
- 💡 **Use Case**: Move laterally without triggering password-based alerts

---

## 🔏 Subvert Trust Controls

### `T1553` – [Subvert Trust Controls](https://attack.mitre.org/techniques/T1553/)
- 🧪 Tools: Unsigned driver loading, cert forgery, tampered app manifests
- 🔍 Detect: Check certificate chains, monitor for unverified driver loads
- 🛡️ Mitigate: Secure boot, code integrity policies, strict app control
- 💡 **Use Case**: Make your malware look like it belongs

---

## 🧿 Virtualization/Sandbox Evasion

### `T1497` – [Virtualization/Sandbox Evasion](https://attack.mitre.org/techniques/T1497/)
- 🧪 Tools: VM checks (`cpuid`, MAC/OUI, sleep timers)
- 🔍 Detect: Short sleep calls, debug flag checks, sandbox evasion logic
- 🛡️ Mitigate: Deception systems, monitor for anti-analysis behavior
- 💡 **Use Case**: Prevent your malware from triggering in sandboxes or malware labs

---

> 💬 Want this exported to GitHub Markdown, HTML, or printable PDF for your kit? Just ask!

