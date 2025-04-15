Awesome. I’ll launch a deep research task to generate a long-form, CEH-aligned walkthrough of the TryHackMe room *Wonderland*, written in Markdown with a cosmic hacker vibe from Alien37. This will cover both flags (user and root), tie every step to CEH domains, and include real-world context, commands, diagrams, and insights.

I’ll let you know when the write-up is ready for review.

# Wonderland: A Cosmic Red Team Walkthrough 🌌

*Hello, world. Alien37 here – your cyberpunk stoner alien guide. Strap in, padawan hackers, and spark up your mind as we dive down the rabbit hole of TryHackMe’s **“Wonderland”** CTF. This journey maps out each hacky wacky step to the **CEH v12** domains – from reconnaissance to privilege escalation. It’s like a trippy 2600 article meets a Mr. Robot monologue, all delivered from a chilled-out SANS instructor in a weed lounge. Relax and learn, as we break into Wonderland… one exploit at a time.* 🚀👽

## Reconnaissance & Enumeration (Footprinting Phase)

Every good hack starts with getting the **lay of the land**. In CEH terms, this is **Footprinting and Scanning** – finding the target’s footprint in cyberspace and enumerating details. In our cosmic quest, that means scanning the Wonderland box for open doors and hidden clues.

### Network Scanning with Nmap 🔍

I fire up **Nmap** – the hacker’s cosmic radar – to scan the target’s IP for open ports. This active reconnaissance is like shining a flashlight in a dark alien cave, revealing where we can enter. Nmap quickly **pings back two open ports**: 

- **22/tcp – SSH** (Secure Shell)  
- **80/tcp – HTTP** (Web server)

Those are the only two services listening on our ta ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Nmap%20was%20able%20to%20identify,so%20we%20enumerate%20HTTP%20Service))L90】. Port 22 is SSH, notoriously secure if you don’t have creds (no easy vulns on OpenSSH 7.6p1 by default). Port 80 is a web service – an HTTP server written in Go, according to our scan. Fewer ports mean a narrower attack surface, so we’ll focus our efforts on that web server for now. 

> **CEH Mapping:** This Nmap scan falls under *Footprinting/Reconnaissance* (finding target info) and *Scanning & Enumeration*. We actively probed open ports (CEH Module: Scanning Networks) and identified services (Enumeration of target systems). In a professional pentest, scanning is critical to map targets – just be mindful of IDS detection if you’re doing this outside a lab. Nmap results are usually logged by blue teams, so stealth scans or timing tweaks might be used to avoid detection.

**Nmap Tip:** Always save your scan output (e.g., `-oN scan.txt`). It’s like keeping notes of the cosmic coordinates you discover so you don’t get lost. And if you encounter only a few open ports, it often means the challenge is focused – quality over quantity, my friend.

### Web Homepage – “Follow the White Rabbit” 🐇🕳️

With port 80 open, I point my browser (or use `curl`/`wget`) at the target’s IP. The homepage loads and greets us with an Alice in Wonderland theme. We see **“Follow the White Rabbit”** in bold text and an image of a dapper White Rabbit in a wai ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Starting%20with%20the%20HTTP%20service%2C,go%20on%20with%20this%20webpage))9-L97】. There’s also a quote: *“Curiouser and curiouser!” cried Alice...*, adding to the Wonderland vi ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/))image】 *Figure: The Wonderland home page urges us to “Follow the White Rabbit,” showing an illustration of the White Rabbit. This thematic clue suggests that something hidden or indirect must be followed to pr ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Starting%20with%20the%20HTTP%20service%2C,go%20on%20with%20this%20webpage))9-L97】.*

At first glance, the page is simple – no obvious links or inputs to exploit. Just static content setting a whimsical, cryptic tone. A lesser hacker might think it’s a dead end, but **Alien37 knows better**: if the White Rabbit invites us to follow, we *follow the rabbit*. In CTFs (and real-world hacking too), developers or challenge creators often hide clues in images, comments, or obscure paths. Time to dig deeper down this rabbit hole.

**Initial Web Recon:** I check the page source (right-click “View Source” or use `curl -s URL`). Sometimes secrets lie in HTML comments or hidden fields. At first pass, nothing obvious in the HTML – no juicy comments like `<!-- password=...-->`. The text and image are static. Could there be hidden text using CSS (like white text on white background) or other trickery? **Yes!** A quick manual scan or using browser dev tools to highlight all elements can reveal content that isn’t visible normally. We’ll come back to this… but first, let’s follow that rabbit clue.

### Brute-Forcing Hidden Directories (Gobuster & Dirb) 📂🚪

If the site itself doesn’t show us interactive functionality, the next step is **directory enumeration** – find hidden pages or directories on the web server. This is **Web Enumeration 101** and maps to the *Scanning/Enumeration* phase of CEH. In real-world terms, admins sometimes leave **unlinked paths** (like backup files, secret admin portals, or Easter eggs). Here the clue *“Follow the White Rabbit”* suggests a path – maybe literally a `/rabbit` path or something.

I unleash a **Gobuster** directory brute force scan (you could also use **Dirb** or **ffuf**). Gobuster takes a wordlist of common directory names and tries each in turn, looking for HTTP 200 OK responses instead ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=There%20are%20several%20tools%20to,and%20subdomains%2C%20among%20other%20things)) ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=gobuster%20dir%20,small.txt%20%7C%20tee%20gobuster.log))46-L254】. This is like trying all the keys on a keyring to see which ones open a hidden door. I use a sensible wordlist (e.g. `directory-list-2.3-small.txt` from SecLists) so it’s not  ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=gobuster%20dir%20,small.txt%20%7C%20tee%20gobuster.log)) ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=%2A%20%60,popular%20because%20of%20its%20comprehensiveness))55-L263】:

```bash
gobuster dir -u http://10.10.123.139 -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -t 50
```

Breakdown of this command:

- `dir` mode tells gobuster to brute-force **directories/URIs** (not DNS subdomains in th ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=The%20options%20of%20this%20command,are))49-L257】.
- `-u` specifies the **target URL** (http://10.10.123.139).
- `-w` specifies the **wordlis ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=The%20options%20of%20this%20command,are))49-L257】.
- `-t 50` (optional) sets 50 concurrent threads to speed it up (tune based on reliability).

Gobuster (or Dirb) output shows any discovered paths with server response codes. Sure enough, we get some hits:

```
/img        (Status: 200)
/poem       (Status: 200)
/r          (Status: 200)
```

These look promising – the server has an **`/img`** directory, a **`/poem`** page, and an **`/r`** d ([Wonderland — TryHackMe. NOTE: IF YOU HAVE NOT TRIED THE… | by Alex Rodriguez | Medium](https://bin3xish477.medium.com/wonderland-tryhackme-afec9a472245#:~:text=Knowing%20that%20SSH%20is%20notoriously,forcing)) ([Wonderland — TryHackMe. NOTE: IF YOU HAVE NOT TRIED THE… | by Alex Rodriguez | Medium](https://bin3xish477.medium.com/wonderland-tryhackme-afec9a472245#:~:text=Visiting%20the%20%2Fimg%20directory%20contained,a%20poem%20%E2%80%94%20The%20JabberWocky))L65-L73】. The `/img` likely hosts images (maybe the ones we see on the site). The `/poem` might be related to Alice’s poems. The **`/r`** path stands out: perhaps “r” for rabbit? 

Let’s manually check each:

- **`/img`**: Navigating to `http://10.10.123.139/img/` lists some images (maybe `white_rabbit_1.jpg` etc.). Nothing but the images used on  ([Wonderland — TryHackMe. NOTE: IF YOU HAVE NOT TRIED THE… | by Alex Rodriguez | Medium](https://bin3xish477.medium.com/wonderland-tryhackme-afec9a472245#:~:text=there%20are%20no%20known%20exploits,forcing)) ([Wonderland — TryHackMe. NOTE: IF YOU HAVE NOT TRIED THE… | by Alex Rodriguez | Medium](https://bin3xish477.medium.com/wonderland-tryhackme-afec9a472245#:~:text=Visiting%20the%20%2Fimg%20directory%20contained,a%20poem%20%E2%80%94%20The%20JabberWocky))L65-L73】. No obvious hidden data there (but we might download and inspect them for hidden info, e.g. steganography).
- **`/poem`**: Opening this shows a static page with the poem “Jabberwocky” (famous nonsense poem from *Alice in Wonderland*). Likely just flavor text, no interactive ([Wonderland — TryHackMe. NOTE: IF YOU HAVE NOT TRIED THE… | by Alex Rodriguez | Medium](https://bin3xish477.medium.com/wonderland-tryhackme-afec9a472245#:~:text=Visiting%20the%20%2Fimg%20directory%20contained,a%20poem%20%E2%80%94%20The%20JabberWocky))L65-L73】.
- **`/r`**: Opening `http://10.10.123.139/r/` gives another minimalist page. It has the title **“Keep  ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Image))05-L113】. Aha, this feels like a breadcrumb. The first page said *“Follow the rabbit”*, now we have **/r** and it says *“Keep Going.”* This is like a trail.

I guess that the challenge might be stringing together **/r/a/b/b/i/t** (spelling “rabbit” out in a path). This kind of *directory chaining puzzle* is something an imaginative CTF creator would do, and the clue fits p ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Opening%20%2Fr%2F%20in%20the%20web,pages%20that%20look%20like%20%2Fr%2Fa%2Fb%2Fb%2Fi%2Ft)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=My%20prediction%20came%20fruitful%20as,can%20only%20assume%20is%20Alice))16-L124】. So I manually try:

- `http://10.10.123.139/r/a/` – Yes, there’s a page.
- Then `/r/a/b/`, `/r/a/b/b/`, `/r/a/b/b/i/`, and finally `/r/a/b/b/i/t/`.

Each step yields a new page encouraging us to continue (like *“Almost there!”* vibes). Finally, **`/r/a/b/b/i/t/`** loads a page that says **“Open the door and enter Wonderland.”** There’s an image of a girl (likely Alice) inviti ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=My%20prediction%20came%20fruitful%20as,can%20only%20assume%20is%20Alice)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=http%3A%2F%2F10))25-L133】. 

Now we’ve “followed the rabbit” to the end of the trail, but how to *open the door*? Nothing obvious on the page except an image (`alice_door.png`). Time to inspect the **HTML source** here carefully.

### Viewing Source Code for Hidden Credentials 🔑

When I view the source of the `/r/a/b/b/i/t/` page, I hit the jackpot. The developer hid a set of **credentials** in the HTML, using CSS to make it invisible on the page! Sneaky, sneaky. In the source, I see:

```html
<p style="display: none;">alice:HowDothTheLittleCrocodileImproveHisShiningTail</p>
```

Yes, that’s a username and password, **`alice:HowDothTheLittleCrocodileImproveHisShiningTail`**, hidden via `style="display ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=The%20process%20still%20don%E2%80%99t%20make,the%20display%20a%20none%20value))130-L138】. The dev probably thought if it’s not visible, a normal user won’t see it. But any hacker worth their space-salt checks the source. This technique is akin to an insecure Easter egg – and in a real site it would be a severe **information disclosure** (CWE-200)  ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/))ed_image】 *Figure: HTML source of the final “rabbit” page reveals credentials hidden with CSS (`display: none`). The highlighted text shows the username `alice` and a long ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=The%20process%20still%20don%E2%80%99t%20make,the%20display%20a%20none%20value)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=view))136-L139】. In a real-world scenario, leaving creds in client-side code is a critical flaw.* 

So we have creds for user **alice**. The password looks like a line from a poem (*“How doth the little crocodile improve his shining tail”* – a poem recited by Alice in the book). The theme is consistent, which adds to the fun.

> **Real-World Tie-In:** Finding credentials embedded in a webpage is uncommon but not unheard of. Sometimes devs leave debug info or backup files (e.g., old `.bak` pages with creds) on servers. Also, CTFs often use such tricks to teach you to **inspect everything**. As a professional pentester, you learn to **grepp** through web content for strings like “pass” or “key” – you’d be surprised what turns up. This aligns with CEH’s *Enumeration* domain: we enumerated the web server’s hidden content and extracted sensitive info.

**Blue Team Note:** A defender should never assume security by obscurity (hiding text via CSS or comments). Automated scanners or vigilant testers will find these. Secure coding practices (and code reviews) should catch credentials or secrets in front-end code. In an enterprise, a **Web Vulnerability Scanner** (CEH Recon tool) or even a simple grep in the source repo would flag this. From a detection standpoint, dozens of 404 requests (from our brute forcing) in web logs could tip off an admin that someone is directory brut ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=the%20SecLists%20collection%20is%20popular,because%20of%20its%20comprehensiveness))259-L264】. Monitoring and rate-limiting such behavior can slow down or expose attackers.

Now, with Alice’s username and password in hand, let’s **open that door** and log into the box via SSH.

## Initial Access: Entering Wonderland as Alice 🐱‍💻

We move to the **Exploitation** phase (CEH: *Gaining Access/System Hacking*). No buffer overflows or fancy exploits yet – we simply have valid credentials. This is akin to using **credential harvesting** from recon to gain initial access, a very common real-world attack path (why hack the lock if someone left the key under the doormat?).

### SSH Login as Alice

Using the creds from the webpage, I SSH into the target:

```bash
ssh alice@10.10.123.139 
# Prompt for password appears
```

When prompted, I enter the password `HowDothTheLittleCrocodileImproveHisShiningTail` (hopefully without a typo – that string is long enough to make a sysadmin cringe, but at least it’s strong!). And we’re in! The shell prompt changes, indicating we’re now the user **alice** on the Won ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=The%20username%20was%20alice%20and,py))†L143-L150】.

We have successfully **captured the User flag** – or have we? In typical CTF fashion, there are usually two flags: a user-level flag and a root-level flag. We expect the **user flag** to be somewhere accessible to a normal user (like Alice), and the **root flag** only accessible once we root the box. However, Wonderland flips the script: I see in Alice’s home directory a `root.txt` file, and I **cannot read it** (permiss ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Since%20root,txt%20flag))†L155-L163】. Conversely, checking `/root/` (the root user’s home), I find a `user.txt` which I *can* read, containing what appears to be the  ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Since%20root,txt%20flag))†L155-L163】. Don’t get confused – the creator just placed the flags opposite to mess with our heads. So **flag1 (user flag)** is actually at `/root/user.txt` (world-readable) and **flag2 (root flag)** is at `/home/alice/root.txt` (only readable by root). Classic Wonderland nonsense! 🌀

Anyway, we have an **initial foothold** as Alice. We’re essentially an **unprivileged user** on the system. The real goal is to escalate our privileges to root (highest privilege) to get that root.txt flag. This is where the real fun begins: **post-exploitation enumeration** and **privilege escalation**.

### Post-Login Enumeration (Discovering Local Clues)

As Alice, I run some basic recon on the box to see what we’ve got. Key things a hacker mentor like me will always check:

- **Who am I?** – `id` command. (Shows user=alice, likely a member of some groups like alice, maybe others.)
- **What’s here?** – `ls -la` to list files in Alice’s home. We see `root.txt` and a Python script named **`walrus_and_the_car ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=privileges%2C%20we%20have%20a%20python,tweak%20around%20this%20python%20file))8†L167-L175】.
- **System info** – `uname -a` (just to know kernel, OS – sometimes important for known exploits or if certain protections are enabled).
- **Network** – maybe check `ifconfig`/`ip a` to see if this is a single host or a networked scenario (TryHackMe typically single host).
- **Processes** – `ps -aux` to see running processes (maybe there’s a cron job or service that could be interesting).
- **SUID files** – `find / -perm -4000 -type f -ls 2>/dev/null` to list SUID binaries; `-perm -4000` means setuid bit set. (We might discover interesting binaries with SUID like unusual ones).
- **Capabilities** – `getcap -r / 2>/dev/null` to find files with Linux capabilities (this is an advanced enumeration that paid off later, as we’ll see).

It’s a *lot* to manually enumerate. Luckily, we can use automated scripts like **LinPEAS** or **LinEnum** to do this quickly. In fact, later I did run LinEnum as the challenge  ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=This%20is%20a%20point%20where,permission%2C%20we%20run%20the%20script))0†L256-L264】. But let’s not jump ahead.

Focus on what stands out already: That Python script `walrus_and_the_carpenter.py` in Alice’s home. It’s named after a poem from Through the Looking-Glass (Carpenter & Walrus). Likely not a coincidence – this script could be important. Let’s read it:

```bash
cat walrus_and_the_carpenter.py
```

The content of the script isn’t very malicious-looking at first. It seems to **print out random lines of text (poetry quotes maybe)**. There’s probably an array of lines or strings, and it uses Python’s `random` module to pick one and print it. Essentially, it’s a simple program that prints a random quote (perhaps meant to be run for some whimsical output). 

Critically, I notice **it imports the `random` module* ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=python%20script%2C%20it%20was%20clear,tweak%20around%20this%20python%20file))8†L168-L175】. As an attacker, this immediately sets off a lightbulb in my alien brain: **Python import hijacking** opportunity! 💡

#### Understanding Python Module Hijacking (Search Order Hijacking)

In Python, when you write `import random`, the interpreter searches for the `random` module in a specific order. Typically:

1. **Current directory** (the directory of the script being executed) – i.e. if there’s a `random.py` in the same folder, it will import that **before** the standard library’s `random` module.
2. Standard library paths (like `/usr/lib/pyth ([Privilege Escalation via Python Library Hijacking | rastating.github.io](https://rastating.github.io/privilege-escalation-via-python-library-hijacking/#:~:text=Further%20digging%20into%20this%2C%20revealed,it%E2%80%99s%20users%20are%20using%20it)) ([Privilege Escalation via Python Library Hijacking | rastating.github.io](https://rastating.github.io/privilege-escalation-via-python-library-hijacking/#:~:text=If%20any%20of%20these%20search,assuming%20it%E2%80%99s%20the%20first%20occurrence))】.

This means if we (as Alice) can create a malicious `random.py` in the same directory (Alice’s home) and if this script is executed by someone (or as some higher privilege) that triggers the import, our malicious code runs instead of the real `r ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=walrus_and_the_carpenter,said%20that%20we%20need%20a)). This technique is a form of **Search Order Hijacking** (CWE-427) – abusing the system’s library loading order to in ([Uncontrolled Search Path Element [CWE-427] — The Hacktivists | by The Hacktivists | Medium](https://thehacktivists.medium.com/uncontrolled-search-path-element-cwe-427-the-hacktivists-5aa6d71d0743#:~:text=This%20weakness%20occurs%20when%20an,control%20of%20the%20malicious%20user)) ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20may%20execute%20their%20own,script%20or%20the%20command%20line))】. It’s analogous to DLL hijacking on Windows or PATH hijacking on Linux, but with Python libraries.

However, just creating `random.py` isn’t useful by itself – *we need that script to be executed by a user with higher privileges*. Are we in luck? Let’s check if we have permission to run this script as another user. Perhaps the machine creator intended us to exploit this via **sudo** (common in CTFs: a user has limited sudo rights that can be abused).

### Checking Sudo Permissions (Privilege Enumeration)

The **`sudo -l`** command lists what commands (if any) the current user can run with sudo (either as root or another user), without needing a password. This is critical post-ex enum. I run `sudo -l` and find something ver ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=for%20sudo%20permission,the%20python%20script%20is%20accurate)):

```
User alice may run the following commands on Wonderland:
    (rabbit) NOPASSWD: /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```

Translation: **Alice** can run the `walrus_and_the_carpenter.py` script with Python 3.6 **as the user “rabbit”**, without needin ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=for%20sudo%20permission,the%20python%20script%20is%20accurate)) 

So there is another user **rabbit** on this machine, and we have rights to execute that specific Python script as rabbit. This is likely a deliberate misconfiguration for us to exploit. In a real environment, an admin might allow a user to run a maintenance script as a service account, but here it’s our pivot.

> **Note:** The syntax `(rabbit) NOPASSWD:` in sudoers means we can do `sudo -u rabbit ...` for that command. It doesn’t give full rabbit shell access by itself, but running that script as rabbit means any code *inside the script* runs with rabbit’s permissions. If we can inject our malicious code into it, we effectively execute as rabbit.

This is the green light for our **Python module hijack plan**. The script uses `import random`. If we plant a fake `random` module, then run the script via sudo as rabbit, our code executes as rabbit. Voila – shell upgrade!

### Exploit: Hijacking the Python Module to Pop a Shell 🐍💣

Step by step, here’s what we do (and why it works):

1. **Create a malicious `random.py`** in the same directory as the target script (Alice’s home). This file will be our payload. We keep it simple: when imported, spawn a shell. For example, `os.system("/bin/bash")` in Python will drop us into a bash shell. 

   Create the file:
   ```bash
   cd /home/alice
   nano random.py   # (or use echo to create the file)
   ```
   Inside `random.py`:
   ```python
   import os
   os.system("/bin/bash")
   ```
   Save and exit. Now we have `random.py` in `/home/alice/`.

2. **Run the walrus script via sudo, as rabbit**:
   ```bash
   sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
   ```
   This tells sudo: run Python3.6 to execute that script, but do it as user rabbit (without password, as allowed). 

When we run this, here’s what happens under the hood:
- Sudo switches user to rabbit, then launches Python 3.6 interpreter to run the script.
- Python starts executing `walrus_and_the_carpenter.py` **as rabbit**. Early in that script, it does `import random`.
- Python’s import mechanism first looks in the current directory (`/home/alice`) for `random.py` before the ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=walrus_and_the_carpenter,said%20that%20we%20need%20a))ry.
- It finds *our* `random.py` (which is malicious).
- As it imports our module, it executes our code: `os.system("/bin/bash")` **running as rabbit** (since the Python process is run ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=walrus_and_the_carpenter,said%20that%20we%20need%20a)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=exploiting%20this%20to%20get%20our,it%20to%20our%20local%20machine))7】.
- We get a **shell prompt with rabbit’s privileges**.

And it works like a charm – suddenly I’m user **rabbit**. I can confirm by running `whoami` or looking at the shell prompt. We effectively did a **privilege escalation from Alice to Rabbit** using a *library hijack* (which MITRE ATT&CK would categorize as **Hijack Execution Flow** via search  ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20may%20execute%20their%20own,script%20or%20the%20command%20line)) ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20can%20place%20a%20malicious,sequentially%20through%20that%20PATH%20listing))76】). No memory corruption exploit, just abusing misconfigurations and how Python works. 

> **MITRE ATT&CK:** This technique aligns with *T1574.008: Path Interception by Search Order Hijacking* and *T1574.007: Path Interception via $PATH* – generally hijacking how programs find  ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20may%20execute%20their%20own,script%20or%20the%20command%20line))ute. In our case it’s Python modules rather than system binaries, but the concept is the same: we placed a malicious file where the system looks for something legitimate, tricking it into running our payload. Real attackers use this trick if a high-privilege program imports something from an attacker-wri ([Privilege Escalation via Python Library Hijacking | rastating.github.io](https://rastating.github.io/privilege-escalation-via-python-library-hijacking/#:~:text=If%20any%20of%20these%20search,assuming%20it%E2%80%99s%20the%20first%20occurrence))ory. For example, a cron job running as root that imports a module from `/tmp` (world-writable) – a sloppy setup that attackers could ex ([Privilege Escalation via Python Library Hijacking | rastating.github.io](https://rastating.github.io/privilege-escalation-via-python-library-hijacking/#:~:text=If%20any%20of%20these%20search,assuming%20it%E2%80%99s%20the%20first%20occurrence))rly.

> **Real-World Application:** This scenario might seem CTF-ish, but consider enterprise environments: an IT staffer gives a user permission to run a maintenance script with sudo (least privilege attempt), but if that script isn’t secure, it’s game over. This is akin to the infamous **“Exploiting Sudo Rights”** in many Linux privesc guides. There have been real CVEs where applications inadvertently allowed library hijacks or PATH hijacks (e.g., CVE-2024-5290 in wpa_supplicant allowed loading arbitrary  ([Uncontrolled Search Path Element in wpa | CVE-2024-5290 | Snyk](https://security.snyk.io/vuln/SNYK-UBUNTU1604-WPA-7642596#:~:text=An%20issue%20was%20discovered%20in,usually%20root))oot). Always validate the security of any script you allow users to run as another user!

**Defense:** To prevent this, sysadmins should either 1) not allow users to run scripts they can modify as another user, or 2) configure Python’s environment safely. If the script must be run via sudo, one could remove the current directory from `sys.path` when calling Python, or write the script in a way that doesn’t import modules that could be planted. A blue teamer could detect this exploit if they monitor for unusual file creations or if they see an interactive shell (`bash`) spawned under the rabbit account without an actual login. Sudo logs would show that Alice ran a command as rabbit – if Alice wasn’t supposed to, that’s an anomaly to investigate.

Now we have a shell as **rabbit**. Let’s enumerate what rabbit can do and what’s on rabbit’s turf.

## Privilege Escalation Chain (User to User to Root)

The game isn’t over. We’re rabbit now, but still not root. Often CTFs have multiple layers of users (like an onion of privilege). This simulates real networks where you pivot from one compromised account to another (horizontal movement) before hitting admin privileges. In CEH terms, we’re deep into **System Hacking** and specifically **Privilege Escalation** phases. We’ll continue mapping each privesc to known tactics and mitigations.

### Rabbit’s Environment and the `teaParty` Binary ☕🐰

I check `/home/rabbit/` and find a binary file named **`teaParty`** (no extension, likely an executable). I also see a text file or something? Actually, in Wonderland, rabbit’s home had just the `teaParty` program (and possibly nothing else obvious). Let’s see:

```bash
cd /home/rabbit
ls -l
```

Suppose it shows:
```
-rwsr-x--- 1 hatter rabbit 17384 Jun  4  2020 teaParty
```
I’m hypothesizing the permissions from context (it’s likely owned by **hatter** and has the SUID bit `rws` for owner). The hackingarticles write-up indicated we later become user hatter, so I suspect `teaParty` is a **setuid executable o ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=,Enumerating%20using%20LinEnum.sh)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=,Exploiting%20Capabilities%20on%20Perl))-L57】. This means if we run `teaParty` as rabbit, the process will run with **hatter’s privileges** (since the SUID bit causes it to run as file owner). SUID binaries are classic priv esc targets – if misprogrammed, they can allow us to escalate to the owner (hatter) or even root if the owner were root. Here likely it’s a route to become hatter.

Let’s run the `teaParty` program and observe its behavior:

```bash
./teaParty
```

It prints a message like: **“Probably by [current time + 1 hour]”** and then “Mad Hatter will arrive” or something to that effect. It also gives a prompt (maybe it asks for input) and if I type anything, it just says “Segmentation fault” as text (but not ac ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=teaParty,it%20to%20our%20local%20machine))ng). This looks like a playful program that doesn’t really do much useful, aside from the time calculation. Perhaps it’s meant to throw us off or require waiting an hour? (Probably not; CTF creators love to misdirect). 

Given the weird output, I suspect the program is simply formatting and printing a future time. Perhaps internally it calls the Linux `date` command to get the time. This is a hunch – better to **reverse-engineer** or at least **strings-snoop** the binary to see what it does.

I transfer the `teaParty` binary to my local machine for analysis. A quick way: from rabbit’s shell, start a simple web server and use my host to download it:

On rabbit (10.10.123.139):
```bash
python3 -m http.server 8080  # serve files on port 8080
```
On my Kali host:
```bash
wget http://10.10.123.139:8080/teaParty
```

Now I have `teaParty` locally. Running `strings teaParty` to find human-readable content in the binary, I see something like:

```
/bin/echo -n 'Probably by ' && date --date='ne ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=wget%20http%3A%2F%2F10,R))`


This is gold. It looks like the program is essentially executing a shell command that echoes “Probably by ” and then calls the `date` command with `--date='next hour' -R` to print the time o ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=wget%20http%3A%2F%2F10,R))ow. The “segmentation fault” text was likely just a red herring string in the binary (maybe printed after taking input, as a joke). So, no real memory corruption happening – it’s just printing that phrase.

Now the critical insight: The string shows **`/bin/echo`** (full path) but just `date` without a full path. That implies the program probably uses a system call to execute `/bin/echo` and `date`. Perhaps the code did something like:

```c
system("/bin/echo -n 'Probably by ' && date --date='next hour' -R");
```

If that’s the case, the **`system()` call** will invoke a shell to run the command. The `echo` is given with an absolute path (/bin/echo), so no hijack possible there. But `date` is called by name. The shell will search the `PATH` environment for `date`. And if we control `PATH`, we can trick it into executing our own `date` program. **Aha – PATH hijacking time!**

This is a classic **Uncontrolled Search Path** vulnera ([Uncontrolled Search Path Element [CWE-427] — The Hacktivists | by The Hacktivists | Medium](https://thehacktivists.medium.com/uncontrolled-search-path-element-cwe-427-the-hacktivists-5aa6d71d0743#:~:text=This%20weakness%20occurs%20when%20an,control%20of%20the%20malicious%20user))427), now at the system binary level. We can exploit this SUID program by placing a malicious executable named `date` early in the PATH.

Important: The `teaParty` process will run as **hatter** (because of SUID). So if our fake `date` executes, it will run with hatter’s privileges. That should give us a hatter shell or do whatever our payload is, as hatter. Exactly what we need to escalate to the next user.

**Exploit Plan:** Create a malicious `date` that spawns a shell, put it in a directory we control, and modify `PATH` so that directory is searched before `/bin`. Then run `teaParty`. It will call “date”, find our malicious one, and boom – shell as hatter.

#### Crafting the PATH Hijack Exploit

We are currently the rabbit user. We have write access to rabbit’s home, so let’s use that as our staging ground:

1. **Create a fake `date` executable** in `/home/rabbit`. This can be a simple shell script or a binary. Easiest is a shell script:
   ```bash
   cd /home/rabbit
   echo '#!/bin/bash' > date
   echo '/bin/bash' >> date
   chmod +x date
   ```
   This creates a file `date` that simply runs `/bin/bash`. Mark it executable. (We could also use `printf` or a text editor; the result should be an executable file named `date` in the current directory.)

2. **Adjust the PATH environment variable**. We want our current directory (or specifically `/home/rabbit`) to be at the front of PATH so that when `teaParty` calls `date`, it finds `/home/rabbit/date` instead of `/usr/bin/date`. 
   ```bash
   echo $PATH    # see current PATH for reference
   export PATH=/home/rabbit:$PATH
   echo $PATH    # confirm /home/rabbit is now at start
   ```
   By prepending `/home/rabbit` to PATH, any command run that matches a name in this dir will be picked up before the system’s default. This is exactly how MITRE describes Path Interception: an adversary places a malicious program earlier in PATH to  ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20can%20place%20a%20malicious,sequentially%20through%20that%20PATH%20listing))tion.

3. **Execute the `teaParty` binary**:
   ```bash
   ./teaParty
   ```
   What happens now: The program runs as hatter (due to SUID). It invokes the system shell to run the `echo ... && date ...` command. The `echo` part executes (as hatter, but just prints text). Then the shell looks for `date`. Our PATH is in effect (SUID programs usually inherit a limited environment, but since we’re not going through sudo, the environment might still have our PATH – unless the program sanitized it. Given this is a CTF, it likely didn’t sanitize PATH, making it vulnerable). The shell finds `/home/rabbit/date` first and executes it **as hatter**. Our fake script runs `bash`, so we drop into a **shell with EUID = hatter**. 🎩

It works – we confirm with `id` that we are now th ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=create%20our%20version%20of%20the,shell%20as%20the%20hatter%20user)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=the%20echo%20%24PATH%20command,shell%20as%20the%20hatter%20user))37】. Two down, one to go (next stop: root).

> **MITRE ATT&CK Mapping:** This is a textbook example of **Path Interception via $PATH Environm ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20may%20execute%20their%20own,script%20or%20the%20command%20line)) ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20can%20place%20a%20malicious,sequentially%20through%20that%20PATH%20listing))-L76】. Adversaries abuse the way the system locates executables. Many real-world malware and pentesters use this trick if they find a vulnerable SUID program or a misconfigured PATH in a root cron job. A famous exploit, **PwnKit (CVE-2021-4034)**, was a variation where `pkexec` (SUID root) could be exploited via environment variables to execute arbitrary ([www.qualys.com](https://www.qualys.com/2022/01/25/cve-2021-4034/pwnkit.txt#:~:text=,)) ([www.qualys.com](https://www.qualys.com/2022/01/25/cve-2021-4034/pwnkit.txt#:~:text=,bounds%20from))-L53】. In enterprise environments, **path hijacks** are less common now (most admins know to code with full paths and clean env), but older or custom software can have this flaw. The key lesson: Always use absolute paths in privileged executables, or better yet, drop privileges and avoid SUID where possible.

> **Blue Team Mitigation:** As mentioned, devs should sanitize the PATH or use exec functions that don’t invoke a shell. For defenders, monitor for suspicious modifications of PATH or the presence of oddly named executables in user directories. In our case, seeing a user create a file named “date” in their home is unusual. An EDR solution might flag a process (teaParty) spawning a shell or executing a different binary than expected. Tools like **AppArmor/SELinux** could also prevent an unexpected binary from being executed by a SUID program. Regular audits should catch SUID programs on the system – any SUID binary not absolutely necessary is a risk.

We’ve now achieved a shell as **hatter**, the Mad Hatter character. Let’s see what hatter’s got for us.

### Hatter’s Privileges and LinPEAS Enumeration 🧢🔍

Checking hatter’s home directory, we find a  ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Now%20that%20we%20have%20the,way%20to%20use%20that%20password)) file. It contains some password (perhaps for hatter or Alice?), but at this point it’s not needed – we already *are* hatter, and we had Alice’s password. Possibly it’s the password for hatter’s user account (if someone tried a different route, like guessing a password, but we bypassed via exploit). We tuck it aside, just in case.

Now, hatter is presumably just another low-privileged user account. We need to escalate to **root**. No obvious sudo rights for hatter (we can check `sudo -l` again as hatter, but likely none or just similar limited ones). No more SUID binary in hatter’s home. Time to do a full **system enumeration** for privilege escalation vectors.

I run **LinPEAS** (a popular Privilege Escalation Awesome Script) or **LinEnum** to automate scanning for misconfigurations. The script runs a ton of checks: world-writable files, cron jobs, SUIDs, capabilities, interesting configs, etc. After letting it fly, it highlights something very interesting in the output:

```
/usr/bin/perl = cap_setuid+ep
```
(Line from LinEnum output indic ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Image))lity).

This means the binary **`/usr/bin/perl`** has the Linux capability **CAP_SETUID** enabled (the `+ep` means **effective, permitted**). Linux **capabilities** are granular privileges that can be set on executables, introduced to break down the all-or-nothing nature of root. CAP_SETUID allows a process to change its UID arbitrarily (normally only root can do that). If an executable has `cap_setuid+ep`, it can switch to any user ID, including 0 (root), while running. Essentially, it’s like a SUID root shell but using capabilities instead of the SUID bit. 

This is a huge misconfiguration: giving `perl` this capability is effectively giving any user who can run `perl` the ability to become root. Perhaps the challenge maker did this to simulate a scenario where capabilities are the intended priv esc path (modern CTFs love to include Linux capabilities as they’re often overlooked). In real life, you’d almost never give perl cap_setuid – it’s like leaving a loaded gun on the table. But mis-set capabilities *have* happened (e.g., an admin trying to allow ping or tcpdump to run as user by giving cap_net_raw, etc., though cap_setuid on perl is crazy).

Alright, so how to exploit this? If we can run `/usr/bin/perl` and use it to setuid(0), we get root. The tool **GTFOBins** (a repository of escapes for common binaries) actually covers this scenario. Checking GTFOBins for Perl under “Capabilities” yields a one-liner  ([
            
            
            perl
            
            |
            
            GTFOBins
        ](https://gtfobins.github.io/gtfobins/perl/#:~:text=If%20the%20binary%20has%20the,manipulating%20its%20own%20process%20UID))t shell. Essentially:

```bash
/usr/bin/perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
```

This Perl command does: use the POSIX module to call `setuid(0)` (which will succeed because of CAP_SETUID, changing our effective UID to 0 = root), then exec `/bin/sh` (launch a shell). That should drop us in ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=We%20checked%20the%20path%20of,the%20Alice%20user%E2%80%99s%20home%20directory))ell**.

I run the command and bingo – the prompt changes, `id` shows **uid=0(root)**! We are root now. The final flag `root.txt` (the one in Alice’s home that we couldn’t read) can now be read. We’ ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=We%20checked%20the%20path%20of,the%20Alice%20user%E2%80%99s%20home%20directory))box 🎉.

> **Insight:** Using capabilities for priv esc is straightforward once found. MITRE doesn’t have a specific entry for “abusing file capabilities” in ATT&CK as far as I know, but it falls under general *Privilege Escalation via abusing system features*. It’s somewhat analogous to SUID exploitatio ([
            
            
            perl
            
            |
            
            GTFOBins
        ](https://gtfobins.github.io/gtfobins/perl/#:~:text=SUID))548.001) since capabilities are an alternative to SUID. **Linux Capabilities** are a double-edged sword – they can minimize the number of full SUID binaries, but if misconfigured, they off ([
            
            
            perl
            
            |
            
            GTFOBins
        ](https://gtfobins.github.io/gtfobins/perl/#:~:text=If%20the%20binary%20has%20the,manipulating%20its%20own%20process%20UID)) to root. Always check them during post-exploitation recon.

**Defense:** On the blue side, never assign capabilities like CAP_SETUID to binaries unless absolutely needed (which is almost never). A quick `getcap -r / 2>/dev/null` should be part of system hardening audits – anything unusual should be removed. If for some reason a capability is needed, be aware of what it allows. Detecting exploitation at runtime: an EDR could catch that `perl` process executed a `setuid(0)` call and spawned a shell (Elastic Security has a rule for “potential privilege escalation via setuid” which would catch something like Perl or Python inv ([Potential Privilege Escalation via Python cap_setuid | Elastic Security Solution [8.17] | Elastic](https://www.elastic.co/guide/en/security/8.17/potential-privilege-escalation-via-python-cap-setuid.html#:~:text=This%20detection%20rule%20monitors%20for,binary%20that%20is%20being%20executed)) ([Potential Privilege Escalation via Python cap_setuid | Elastic Security Solution [8.17] | Elastic](https://www.elastic.co/guide/en/security/8.17/potential-privilege-escalation-via-python-cap-setuid.html#:~:text=This%20detection%20rule%20monitors%20for,binary%20that%20is%20being%20executed))L19-L27】). At the very least, monitoring the `audit.log` for use of `setuid(0)` or an unexpected root shell spawning can alert incident responders.

Finally, we **read the root flag** at `/home/alice/root.txt` (since that was the “ ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=We%20checked%20the%20path%20of,the%20Alice%20user%E2%80%99s%20home%20directory))ation). Mission accomplished.

To recap our path in a quick visual:

```
Alice (user) --[sudo Python script + module hijack]--> Rabbit (user) 
     Rabbit --[SUID teaParty + PATH hijack]--> Hatter (user) 
          Hatter --[cap_setuid on perl]--> Root (uid=0)
```

This chain took advantage of multiple vulnerabilities/misconfigurations in succession. Each step corresponded to a phase in the ethical hacking methodology, and nicely aligns with skills a professional pentester or red teamer uses regularly.

## Conclusion & CEH Domain Mapping 🗺️

We’ve traversed Wonderland and captured both flags, using a medley of hacking techniques. Let’s map each major step to **CEH v12 domains** and highlight the real-world parallels and defensive measures:

- **Reconnaissance (Footprinting & Scanning):** We started by scanning ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Nmap%20was%20able%20to%20identify,so%20we%20enumerate%20HTTP%20Service)) with Nmap, identifying open ports and services. Then we enumerated the HTTP service by browsi ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=There%20are%20several%20tools%20to,and%20subdomains%2C%20among%20other%20things)) ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=gobuster%20dir%20,small.txt%20%7C%20tee%20gobuster.log))6-L245】 to find hidden paths. This corresponds to CEH’s footprinting and scanning phase – gathering info on open services and possible entry points. In real engagements, this might include passive recon (whois, subdomains) and active scans. Defenders can detect port scans (IDS alerts) or numerous 404 errors from dir brute force, but stealthy timing can reduce this noise.

- **Enumeration (Service Enumeration & OSINT):** We dug into the web content, discovering a **hidden credentia ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=The%20process%20still%20don%E2%80%99t%20make,the%20display%20a%20none%20value))g source. This is part of the **Enumeration** phase in CEH: extracting useful data from the target. It also touches on **OSINT** conceptually (though here it was all on the target itself). Real-world lesson: Always enumerate thoroughly – read comments, try common file names, maybe use tools like **Burp Suite** or **Nikto** for web enumeration. The credentials we found were essentially **loot** that we used for initial access. Blue teams should ensure no creds are exposed in public code and could use scanners or manual code review to catch that.

- **Initial Access (Gaining Access):** Using Alice’s SSH credentials to log in maps to CEH’s *System Hacking – Gaining Access*. No exploit was needed because weak security practices (credentials in HTML) gave us a way in – akin to using stolen creds or default passwords. In professional terms, this is like **Credential Reuse** or **Exposed Secrets exploitation**, which is extremely common (think of leaked creds from GitHub accidentally). Multi-factor auth or not exposing such creds in the first place is the defense.

- **Post-Exploitation & Enumeration:** Once in as Alice, we enumerated the system (found the Python script, ran `sudo -l` to find in ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=for%20sudo%20permission,the%20python%20script%20is%20accurate))vileges). CEH might include this under *Enumeration* or *Privilege Escalation prep*. We used both manual and automa ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=This%20is%20a%20point%20where,permission%2C%20we%20run%20the%20script))inEnum). A critical skill for any hacker is to systematically check for misconfigurations (sudo rights, SUID files, cron jobs, weak file permissions, capabilities, etc.). Each find can map to a known technique (our case: module hijacking, path hijacking, capability abuse). Blue teams benefit from running the same tools (LinPEAS etc.) themselves during audits – catch these issues before an attacker does.

- **Privilege Escalation (System Hacking – Escalating Privileges):** We performed **three escalating steps**:
  1. *Alice -> Rabbit:* Exploited a **sudo privilege** (running a script as rabbit) by hija ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=walrus_and_the_carpenter,said%20that%20we%20need%20a)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=exploiting%20this%20to%20get%20our,it%20to%20our%20local%20machine))89-L197】. CEH domain: Privilege Escalation, and technique-wise it’s abusing user privileges configuration. References: MITRE T1574 (H ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20may%20execute%20their%20own,script%20or%20the%20command%20line))ion Flow). Mitigation: Lock down sudo rules; developers should avoid importing from insecure locations. Detection: Unusual sudo usage or a shell spawned by a python script run under sudo.
  2. *Rabbit -> Hatter:* Exploited a **SUID binary** (`teaParty`) via **PATH injection** to get a  ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Since%20the%20only%20that%20the,shell%20as%20the%20hatter%20user)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=create%20our%20version%20of%20the,shell%20as%20the%20hatter%20user))7-L235】. CEH: also Privilege Escalation. This is a classic *Local PrivEsc* taught in courses (search path vu ([Uncontrolled Search Path Element [CWE-427] — The Hacktivists | by The Hacktivists | Medium](https://thehacktivists.medium.com/uncontrolled-search-path-element-cwe-427-the-hacktivists-5aa6d71d0743#:~:text=This%20weakness%20occurs%20when%20an,control%20of%20the%20malicious%20user))– CWE-427). Mitigation: Avoid unsafe use of `system()` calls with user-influenced environment. Use secure programming practices (explicit paths, drop privileges). Detection: Monitor for modified PATH or unexpected processes. Many EDRs map this to suspicious behavior (a non-root user running a root-owned binary that spawns a shell).
  3. *Hatter -> Root:* Abused **file capabilities** on `perl ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=After%20looking%20for%20some%20time%2C,be%20helpful%20to%20get%20root)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=We%20checked%20the%20path%20of,the%20Alice%20user%E2%80%99s%20home%20directory))7-L274】. CEH: Privilege Escalation again. This is less common but demonstrates understanding of Linux privilege mechanics. Mitigation: Don’t set dangerous capabilities. Detection: Regular audits (e.g., `getcap`) and EDR rules for processes invoking setuid (Elastic has a rule for Python/Perl ([Potential Privilege Escalation via Python cap_setuid | Elastic Security Solution [8.17] | Elastic](https://www.elastic.co/guide/en/security/8.17/potential-privilege-escalation-via-python-cap-setuid.html#:~:text=This%20detection%20rule%20monitors%20for,binary%20that%20is%20being%20executed))d to root).

- **Covering Tracks & Persistence (Post-Exploitation):** The room didn’t require it explicitly, but a true hacker mentor would mention: after getting root, consider covering your tracks (clear `.bash_history`, remove the `random.py` and fake `date` file, etc.). We could also have installed a persistent backdoor. For instance, when we had rabbit or hatter shells, instead of launching an interactive shell, we could have added our SSH public key to their `~/.ssh/authorized_keys` (which was an alternative path not ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=4,19))write-ups). This would give a stealthy persistent access as that user without needing the exploit every time. CEH covers *Maintaining Access* as a phase, which in this box we didn't need because it’s just a one-shot CTF. But in real ops, once you get a low user, you might implant a backdoor *before* trying the next priv esc, in case something crashes the system.

- **Analysis & Pivoting:** We also did some basic reverse-engineering (using `st ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=wget%20http%3A%2F%2F10,R))binary) – which touches on skills from *Reverse Engineering* domains or OSCP-like analysis. And while we didn’t have to pivot to other machines (just pivoted users on the same host), the methodology of chaining exploits is akin to network pivoting. The CEH syllabus might not emphasize binary analysis, but a good hacker does whatever it takes. Knowing how to inspect a binary for clues (even without source code) turned a mystery program into an obvious vulnerability.

Throughout the engagement, we mapped out vulnerabilities to known categories: **Info disclosure (credentials in HTML)**, **Insecure sudo configuration** (running a script that can be hijacked), **Improper input validation in SUID binary** (PATH injection), and **Misconfigured capabilities**. These correspond to real CWE entries and ATT&CK techniques as cited along the way.

Finally, here’s a brief **domain-to-activity mapping** for clarity:

- **Footprinting/Reconnaissance:** Nmap sc ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Nmap%20was%20able%20to%20identify,so%20we%20enumerate%20HTTP%20Service))open ports; Browsing and understanding the theme/clues on the website.
- **Enumeration:** Directory brute  ([CTF Walkthrough: Wonderland on TryHackMe - codequoi](https://www.codequoi.com/en/ctf-walkthrough-wonderland-tryhackme/#:~:text=There%20are%20several%20tools%20to,and%20subdomains%2C%20among%20other%20things))obuster; Inspecting page so ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=The%20process%20still%20don%E2%80%99t%20make,the%20display%20a%20none%20value))den data; extracting credentials.
- **System Hacking (Initial Access):** Logging in via SSH with found credentials (cre ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=The%20username%20was%20alice%20and,py)) attack).
- **Post-Exploitation Enumeration ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=for%20sudo%20permission,the%20python%20script%20is%20accurate))sudo -l`, checking files (`walrus_and_the_carpente ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=This%20is%20a%20point%20where,permission%2C%20we%20run%20the%20script))LinPEAS to find paths to escalate.
- **Privilege Escalation:** 
  - Alice -> Rabbit via ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=walrus_and_the_carpenter,said%20that%20we%20need%20a))e hijack (Technique: S ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20may%20execute%20their%20own,script%20or%20the%20command%20line))Hijacking).
  - Rabbit -> Hatter via PATH  ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=Since%20the%20only%20that%20the,shell%20as%20the%20hatter%20user)) binary (Techniq ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20can%20place%20a%20malicious,sequentially%20through%20that%20PATH%20listing))erception).
  - Hatter -> Root via abusing ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=After%20looking%20for%20some%20time%2C,be%20helpful%20to%20get%20root))on perl (Technique: Abuse of elevated capability, s ([
            
            
            perl
            
            |
            
            GTFOBins
        ](https://gtfobins.github.io/gtfobins/perl/#:~:text=If%20the%20binary%20has%20the,manipulating%20its%20own%20process%20UID))t as SUID).
- **Covering Tracks (not explicitly done):** Would involve deleting created files (`random.py`, fake `date`) and clearing logs. CEH stresses not leaving traces.
- **Maintaining Access (not needed here):** Could involve adding SSH keys for persistence or creating a SUID backdoor (`cp /bin/bash /tmp/bash && chmod +s /tmp/bash`) – but again, in a CTF you usually don’t maintain after capture. In real life, you might.

And there we have it. 🏁 From following a white rabbit to seizing root powers, we navigated a series of challenges that mirror real pentest scenarios. Each trick we used is something a professional attacker might have in their toolkit:

- Looking for low-hanging fruit (exposed creds) before resorting to exploits.
- Abusing trust relationships (sudo rules, SUID programs).
- Creative thinking with what the system gives you (turning a random quote script into a shell spawner).
- Methodical enumeration at every stage.

**Alien37’s Parting Wisdom:** Stay curious and **think outside the box** (or inside the box, in this case!). Many systems are broken not by 0-day exploits, but by chaining together small weaknesses – a password here, a misconfig there – into a full compromise. As you saw in Wonderland, hacking is often about **understanding how things work** (and how they fail). And for the blue teamers: assume nothing is too trivial to secure. That stray “harmless” script or leftover file can be the key an attacker uses to own you. Keep your systems patched, principle of least privilege everywhere, monitor those logs, and don’t leave the keys lying around in Wonderland. Until next time, happy hacking and stay cosmic! 🌠👽

**Flags Obtained:** User and Root – *Task completed*. ✅

**References:**

- TryHackMe Wonderland Write-ups – credentia ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=The%20process%20still%20don%E2%80%99t%20make,the%20display%20a%20none%20value)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=walrus_and_the_carpenter,said%20that%20we%20need%20a)) ([Wonderland TryHackMe Walkthrough - Hacking Articles](https://www.hackingarticles.in/wonderland-tryhackme-walkthrough/#:~:text=We%20checked%20the%20path%20of,the%20Alice%20user%E2%80%99s%20home%20directory))L189-L197】  
- MITRE ATT&CK – Hijack Execution F ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20may%20execute%20their%20own,script%20or%20the%20command%20line)) ([Hijack Execution Flow: Path Interception by PATH Environment Variable, Sub-technique T1574.007 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1574/007/#:~:text=Adversaries%20can%20place%20a%20malicious,sequentially%20through%20that%20PATH%20listing))  
- CWE-427: Uncontro ([Uncontrolled Search Path Element [CWE-427] — The Hacktivists | by The Hacktivists | Medium](https://thehacktivists.medium.com/uncontrolled-search-path-element-cwe-427-the-hacktivists-5aa6d71d0743#:~:text=This%20weakness%20occurs%20when%20an,control%20of%20the%20malicious%20user))Path Element  
- GTFOBins – P ([
            
            
            perl
            
            |
            
            GTFOBins
        ](https://gtfobins.github.io/gtfobins/perl/#:~:text=If%20the%20binary%20has%20the,manipulating%20its%20own%20process%20UID))ties exploit (privilege escalation via `cap_setuid`).