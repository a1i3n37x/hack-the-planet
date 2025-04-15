# CEH Chapter 5: Scanning Networks - Lecture Notes

## Introduction

Okay class, let's dive into **Chapter 5: Scanning Networks**, a crucial phase in ethical hacking. Remember, we've finished our footprinting and reconnaissance from Chapter 4, gathering initial information about our target. Now, we actively start probing the target systems.

**Important Ethical Note:** Before we begin, always remember that actively scanning networks requires **explicit permission**. Unauthorized scanning is illegal and unethical. Scanning can sometimes cause system instability or outages, especially on fragile systems, so ensure your client understands the potential risks.

## Overview of Network Scanning

The primary goal of scanning is to identify live hosts, open ports, and the services running on those ports within the target network. This information helps us understand the attack surface and pinpoint potential vulnerabilities.

This chapter covers several key techniques:

* **Ping Sweeps:** Identifying live hosts on the network.
* **Port Scanning:** Discovering open TCP and UDP ports and the services listening on them.
* **Vulnerability Scanning:** Using automated tools to identify known weaknesses.
* **Packet Crafting & Manipulation:** Manually creating or modifying network packets to test responses or bypass defenses.
* **Evasion Techniques:** Methods to avoid detection by security systems like firewalls and Intrusion Detection Systems (IDS).
* **Protection & Detection:** Understanding how defenders protect against and detect these scanning activities.

---

## Ping Sweeps

Before launching detailed scans, we often want to know which hosts are actually online and responsive. A ping sweep helps us identify these "live" systems.

* **How it works:** Sends ICMP echo requests (like the standard `ping` command) to multiple hosts in a target range. Hosts that are up should respond with an ICMP echo reply.
* **Tools:**
    * **fping:** A command-line tool designed specifically for sending pings to multiple targets efficiently. It can show alive hosts, elapsed time, and generate targets from address blocks.
    * **MegaPing:** A GUI-based Windows tool that includes an IP Scanner function for ping sweeps, among other network utilities. It can also resolve MAC addresses and hostnames.
    * **Nmap:** Can also perform ping sweeps, often as a preliminary step before port scanning.
* **Limitations:** Ping sweeps aren't foolproof. Firewalls often block ICMP messages, so a lack of response doesn't always mean a host is down. It might just mean the ping is being blocked.

---

## Port Scanning

Once we have a list of potentially live hosts, port scanning helps us find open doors – the listening TCP and UDP ports – and identify the services behind them.

* **Ports:** Network services "listen" on specific ports (0-65535) for incoming connections. Common services use well-known ports (e.g., HTTP on 80, SSH on 22).
* **TCP Scanning:** Exploits the TCP handshake process.
    * **SYN Scan (-sS):** Often called a "half-open" scan. Sends a SYN packet. If the port is open, the target sends SYN/ACK; the scanner responds RST (closing before completion). If closed, the target sends RST. Requires administrative privileges.
    * **Connect Scan (-sT):** Completes the full three-way handshake (SYN, SYN/ACK, ACK) before closing. Doesn't require special privileges but is easily logged.
    * **FIN, Null, Xmas Scans (-sF, -sN, -sX):** Send packets with unusual flag combinations. Open ports often don't respond (per RFC), while closed ports send RST. Can sometimes bypass older firewalls/IDS but often report ports as "open|filtered" if no response is received.
* **UDP Scanning (-sU):** More challenging as UDP is connectionless; there's no standard handshake.
    * Sends UDP packets to target ports.
    * An ICMP "Port Unreachable" message usually indicates a closed port.
    * No response might mean the port is open, or the packet/response was lost, or a firewall blocked it. Scanners often retransmit probes and wait longer, making UDP scans slower.
* **Tools:**
    * **Nmap:** The standard tool. Offers various scan types, OS detection (-O), service version detection (-sV), and scripting capabilities (--script).
    * **Zenmap:** The official GUI front-end for Nmap, providing visualization and scan comparison features.
    * **masscan:** Designed for extremely high-speed scanning, potentially across the entire internet. Uses Nmap-like syntax but is faster for large ranges. Can grab banners (--banners).
    * **MegaPing:** Includes various port scan options, including scanning predefined lists like "Hostile Ports".
    * **Metasploit:** Contains auxiliary modules for various scan types (SYN, ACK, Xmas, etc.). Integrates results into its database.
* **Service/Version Detection (-sV):** Crucial step. Goes beyond just finding open ports to identify the actual software and version listening. Nmap sends probes and analyzes application banners.
* **OS Detection (-O):** Nmap attempts to identify the target operating system by analyzing responses to specific probes (TCP/IP fingerprinting). Requires at least one open and one closed TCP port for accuracy. Results can be guesses if conditions aren't ideal or the OS isn't in Nmap's database.

---

## Vulnerability Scanning

Identifying services is good, but knowing their weaknesses is better. Vulnerability scanners automate the process of checking systems against databases of known vulnerabilities.

* **How it works:** Probes open ports and identified services, running specific checks (plugins or tests) designed to detect known vulnerabilities based on service responses, banners, and configurations.
* **Goal:** To identify *potential* vulnerabilities, not necessarily exploit them.
* **Important Caveats:**
    * **False Positives:** Scanner reports a vulnerability that isn't actually present. **Always manually verify scanner findings**.
    * **False Negatives:** Scanner fails to detect a vulnerability that *is* present.
* **Tools:**
    * **OpenVAS (GVM):** An open-source vulnerability scanner, originally forked from Nessus. Uses Network Vulnerability Tests (NVTs) organized into families. Features a web interface (Greenbone Security Assistant - GSA). Allows creating targets, scan configs, and schedules. Can use credentials for authenticated (local) scans. Results can be reviewed, filtered, and overridden (e.g., marking as false positive).
    * **Nessus:** A popular commercial scanner (with a free Home feed). Also uses plugins and policies (like Basic Network Scan, Advanced Scan). Supports credentialed scans for various protocols (SSH, Windows, databases). Provides detailed reports with descriptions, solutions, references, and remediation advice. Can also create rules to adjust severity based on host or plugin ID.
    * **Metasploit:** Includes numerous scanner modules, often targeted at specific vulnerabilities (like MS17-010/EternalBlue).

---

## Packet Crafting and Manipulation

Sometimes, standard tools don't create the exact packet needed, or we want to send malformed packets to test how systems or security devices react.

* **Goal:** Bypass the OS network stack to gain complete control over packet headers and payload. Used for testing, evasion, or exploiting protocol weaknesses.
* **Tools:**
    * **hping3:** Command-line tool, considered a "Swiss Army knife" for TCP/IP. Can send ICMP, TCP, UDP packets with custom flags, ports, sizes, and even spoofed source addresses (-a). Useful for probing ports or testing firewall rules. Requires root privileges.
    * **packETH:** GUI tool for building packets layer by layer (Ethernet, IP, TCP/UDP). Allows setting all header fields manually and defining payloads (hex patterns or text). Can send single packets or generate streams. Can load/save packet definitions and import from PCAP files.
    * **fragroute:** Intercepts outgoing packets to a specific target and mangles them based on rules in a configuration file. Can fragment packets (ip_frag), add chaff/duplicates (ip_chaff, tcp_chaff), reorder packets (order random), introduce delays, etc. Used to test IDS/firewall evasion or potentially crash target network stacks.

---

## Evasion Techniques

Security devices like firewalls and IDS/IPS aim to block or detect malicious scanning activity. Evasion techniques try to bypass these defenses.

* **Common Techniques:**
    * **Obfuscation/Encryption:** Hiding data using encoding (like URL encoding) or encryption makes it unreadable to DPI/IDS.
    * **Alteration/Polymorphism:** Modifying malware slightly changes its signature (hash), potentially evading signature-based detection.
    * **Fragmentation:** Sending packets in small fragments forces security devices to reassemble, adding latency; some may not bother or handle it poorly. Tools like `fragroute` and `nmap -f` or `--mtu` can do this.
    * **Overlapping Fragments:** Sending fragments with overlapping sequence numbers/offsets can confuse reassembly, potentially leading the IDS/firewall and the target OS to interpret the data differently.
    * **Malformed Packets:** Using unexpected flag combinations (like Nmap's FIN/Null/Xmas scans) or exploiting protocol ambiguities might bypass less sophisticated filters.
    * **Low and Slow:** Scanning very slowly (e.g., one probe per hour) makes the activity look less like a scan and harder to correlate. Nmap's timing templates (-T0, -T1) can help.
    * **Resource Consumption:** Overloading a security device (CPU/memory) might cause it to fail open, letting traffic pass unchecked.
    * **Decoys/Smoke Screen:** Generating excessive "noise" (benign alerts) can overwhelm human analysts, helping malicious traffic slip through unnoticed. Nmap's decoy scan (-D) generates traffic from spoofed IPs alongside the real scan.
    * **Tunneling:** Encapsulating traffic within another protocol (e.g., DNS, ICMP, HTTP) can hide its true nature.
* **Nmap Evasion Features:**
    * Unusual scan types (FIN, Null, Xmas).
    * Idle Scan (-sI): Uses a third "zombie" host to relay the scan, hiding the scanner's true IP.
    * Decoys (-D).
    * Fragmentation (-f, --mtu).
    * Source Port Spoofing (-g): Sets a specific source port (e.g., 53 for DNS) which might bypass simple firewall rules.
    * MAC Address Spoofing (--spoof-mac): Useful only on the local network against MAC-based filters.

---

## Protecting and Detecting Scans

Defenders can implement measures to block or detect scanning activity.

* **Firewalls:** Block unsolicited inbound traffic, including ICMP pings or probes to non-allowed ports. Can use egress filtering to block spoofed internal addresses originating from the outside.
* **IDS/IPS:** Can detect scan patterns (many probes to different ports/hosts from one source). Can identify probes matching known vulnerability checks or malformed packets used in evasion. Can detect ARP spoofing by watching for excessive gratuitous ARPs.
* **Logging & Monitoring:** Centralized logging (Syslog, SIEM) helps detect patterns over time, including slow scans or probes hitting unusual ports. Monitoring DHCP logs can reveal starvation attacks (excessive DISCOVERs) or rogue servers.
* **Network Configuration:** Using switched networks limits sniffing. Disabling responses to broadcast pings prevents Smurf amplification. Proper router configuration (like reverse path verification) can help drop spoofed packets. Using secure protocols like DNS over TCP or DNSSEC helps prevent DNS spoofing.

---

That covers the core concepts of network scanning. It's a phase where we shift from passive observation to active interaction, gathering vital details for the next stages of our ethical hack. Any questions before we move on?