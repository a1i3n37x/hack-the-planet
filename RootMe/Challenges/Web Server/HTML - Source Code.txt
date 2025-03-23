# 🕵️ Root-Me Write-Up: Web-Server Challenge #1 – "HTML: Source Code"

## 🎯 Challenge Overview

- **Platform**: [Root-Me.org](https://www.root-me.org)
- **Category**: Web-Server  
- **Title**: HTML - Source Code  
- **Difficulty**: Beginner  
- **Objective**: Find the hidden information in the HTML source code of the webpage.

---

## 🧠 Why This Challenge Matters

This first web challenge might seem simple, but it teaches one of the *most critical habits* in cybersecurity and ethical hacking: **always check the source code**.

In web penetration testing, the front-end of a website (what you see in your browser) often hides juicy details just behind the scenes. Developers might accidentally leave comments, hidden forms, or sensitive information in the code that a regular user never sees—but a hacker knows to look for.

Understanding how to inspect and interpret HTML is a foundational skill that pays off throughout your journey.

---

## 🛠️ Tools You’ll Need

This challenge is beginner-friendly and requires only a browser. Optionally, you can enhance your setup with:

- **Any Web Browser** (Chrome, Firefox, Brave, etc.)
- **Developer Tools** (DevTools – Right-click → Inspect)
- *Optional*: **VS Code** or a text editor (for copying/pasting HTML)
- *Optional*: **Burp Suite** (for future web challenges)

---

## 🔍 Step-by-Step Walkthrough

### 1. Visit the Challenge Page

Go to:

> Challenges → Web-Server → HTML - Source Code

Launch the URL provided in the challenge. You'll see a simple page with a message like:

> *"Don’t search too far"*

That’s your clue.

---

### 2. View the Page Source

Right-click anywhere on the page and choose:

> `View Page Source`  
> *(Or use Ctrl+U / Command+U on most browsers)*

This shows you the raw HTML code of the page.

---

### 3. Find the Hidden Comment

You’ll likely see a line like this inside the HTML:

```html
<!-- The password is: hunter2 -->
```

This is what we’re looking for — the hidden flag or password!

---

### 4. Submit the Flag

Take the value you found (e.g. `hunter2`) and paste it into the flag box on the Root-Me challenge page.

Click **Submit** — and you’ve solved your first challenge!

✅ **Done!**

---

## 📚 Key Concepts You Just Learned

### 🔹 HTML Basics

HTML is the structure of the web. Comments in HTML look like this:

```html
<!-- This is a comment -->
```

They’re invisible on the page but visible in the source code.

---

### 🔹 Why Hackers Check the Source

Viewing the source is part of **reconnaissance**, the first phase of hacking.

Hackers check for:

- Comments containing sensitive info
- Hidden form inputs
- Debug or test code
- Unlinked files or directories

---

### 🔹 Real-World Examples of Info Leakage

In the real world, developers accidentally leave:

```html
<!-- TODO: Add login page -->
<!-- Admin panel: /admin_login -->
<!-- Credentials: admin / test123 -->
```

Finding this kind of info can help during pentests or bug bounty hunting.

---

## 🧭 Going Further (Bonus Practice)

- Open DevTools (F12) → Elements tab
- Inspect DOM elements and look for hidden attributes
- Explore the “Network” tab to see how data is sent/received
- Check for scripts or external files (`.js`, `.css`) that might contain clues

---

## 💡 Skills Reinforced

- Web Recon (Information Gathering)
- HTML Structure and Comments
- Basic Web Hacking Techniques
- Hacker Mindset & Curiosity

---

## ✅ Final Thoughts

This challenge is simple—but it sets the tone for every web challenge that follows.

Always start with the basics:
- Check the source
- Inspect the structure
- Think like a developer *and* a hacker

Let this be your first step in building solid web hacking instincts.

---

**Keep hacking. Keep learning.**  
💻👽 – *Alien37 / a1i3n37x*
