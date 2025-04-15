## CEH v12 Study Guide – Chapter 4: Footprinting and Reconnaissance

---

### 🎯 Chapter Objective
Understand how attackers gather intelligence about their targets before any direct engagement. This phase — also known as reconnaissance — is critical for planning attacks and finding weaknesses without alerting the target.

---

## 🔍 SECTION: WHOIS Lookups

### 🧠 What is WHOIS?
WHOIS is a TCP-based query/response protocol used to obtain information about domain ownership and IP address allocations. It’s one of the first tools used in passive reconnaissance.

### 📌 What You Can Learn From WHOIS:
- Domain registrant name and organization
- Admin/technical contact email and phone
- Creation and expiration dates of domains
- Name servers in use
- Registrar info

### 📖 CEH-Relevant Usage:
WHOIS can help identify:
- A company’s primary domain and registration patterns
- Internal email formats (e.g., john.doe@example.com)
- Names of IT admins and phone numbers (useful for social engineering)

### 🧪 Tools & Syntax:
```bash
whois example.com
```
- Linux built-in `whois`
- Web: whois.domaintools.com, whois.net

### 🧠 CEH Trap:
- Know that WHOIS is **passive recon**, not active scanning

---

## 🔍 SECTION: DNS Reconnaissance

### 🧠 What is DNS Recon?
DNS reconnaissance involves querying the Domain Name System (DNS) to gather intel about a target’s infrastructure. This can reveal subdomains, mail servers, and sometimes internal IPs.

### 📌 Key DNS Record Types:
| Record Type | Description                     |
|-------------|---------------------------------|
| A           | Maps hostname to IPv4 address  |
| AAAA        | Maps hostname to IPv6 address  |
| MX          | Mail servers for the domain    |
| NS          | Nameservers for the domain     |
| TXT         | Misc data (e.g., SPF records)  |
| SOA         | Start of authority, domain metadata |

### 🧪 Commands:
```bash
dig example.com any
dig mx example.com
dig ns example.com
```
- Use `dig axfr @ns1.example.com example.com` for zone transfer attempts

### ⚠️ CEH Alert:
- Zone transfers (AXFR) should be **disabled** on production DNS
- CEH exam may give you a dig output and ask what record type you're looking at

---

## 🔍 SECTION: Google Dorking (Google Hacking)

### 🧠 What is Google Hacking?
Using advanced Google search operators to locate sensitive or misconfigured data exposed to the public. Completely passive and extremely powerful.

### 🔎 Must-Know Operators:
| Operator      | Use Case                                      |
|---------------|-----------------------------------------------|
| site:         | Limit search to a domain                     |
| filetype:     | Look for specific file types (xls, pdf, etc) |
| intitle:      | Match page title                             |
| inurl:        | Match URL path                               |
| intext:       | Search for text in body                      |

### 📌 CEH Examples:
| Objective                      | Query                                      |
|-------------------------------|---------------------------------------------|
| Find Excel docs               | site:example.com filetype:xls              |
| Find login portals            | intitle:"login" inurl:admin                |
| Find webcams                  | inurl:view/index.shtml                     |
| Find config files             | filetype:conf | filetype:ini               |
| Find passwords in text files | intext:password filetype:txt               |

---

## 🔍 SECTION: Email and Employee Enumeration

### 🧠 Purpose:
Discover company email formats, personnel names, and roles that may help with spear phishing or social engineering.

### 🛠️ Tools:
- `theHarvester` – Collects emails from public sources
```bash
theharvester -d example.com -b google
```
- LinkedIn, Hunter.io, and social media profiles

### 👀 Look For:
- Executive names (CEO, CTO)
- IT roles (sysadmins, netsec leads)
- Email naming conventions (first.last@example.com)

---

## 🔍 SECTION: Shodan Reconnaissance

### 🧠 What is Shodan?
Shodan is a search engine for internet-connected devices. It indexes banners from open ports across the internet.

### 📌 What Shodan Reveals:
- Open ports & services (FTP, SSH, HTTP)
- Device types (routers, webcams, printers)
- Software versions (Apache, nginx, etc.)
- Possible vulnerabilities (based on known versions)

### 🛠️ Usage:
- Web UI: https://www.shodan.io
- CLI: `shodan search apache` (requires API key)

### 📖 CEH Example:
"What does port:502 mean in a Shodan query?" → 502 is used by **Modbus**, an industrial control protocol

---

## 🧠 Final CEH Notes for Chapter 4
- WHOIS, DNS, and Google are all **passive recon**
- Zone transfers are **misconfigurations**, not standard behavior
- Know your operators (`filetype:`, `site:`, `inurl:`) inside and out
- Memorize RIR regions (ARIN = NA, RIPE = Europe, etc.)
- Shodan = "Internet of Things intel"
- theHarvester = email and name scraping
- CEH will test your ability to **match tools to use cases**

Want Chapter 5 next?

