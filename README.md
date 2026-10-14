# 🛡️ Cybersecurity Writeups & Lab Journal

A documented archive of hands-on security challenges, CTFs, and lab machines covering penetration testing, network traffic analysis, and system defense.

## 📑 Lab & Machine Index

<!-- INDEX_START -->
| Platform | Target / Room | OS | Difficulty | Key Concepts / Vectors | Documentation |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **TryHackMe** | Startup | `Linux` | ![Easy](https://img.shields.io/badge/-Easy-brightgreen) | Anonymous FTP, PCAP Analysis, Cron PrivEsc | [Read Writeup](./tryhackme/startup/) |
<!-- INDEX_END -->

## 📂 Repository Architecture

```text
cybersecurity-writeups/
├── README.md                        <-- Dynamic index table & portfolio overview
├── generate_index.py                <-- Auto-updates README index from YAML frontmatter
├── .github/workflows/
│   └── update-index.yml             <-- GitHub Action to refresh index on every push
├── templates/
│   └── writeup-template.md          <-- Modular writeup & LinkedIn post blueprint
├── tryhackme/
│   ├── startup/
│   │   ├── README.md                <-- TryHackMe Startup walkthrough
│   │   └── assets/                  <-- Cropped terminal & browser screenshots
│   └── picklerick/
│       └── assets/
├── hackthebox/
│   └── legacy/
│       └── assets/
└── ctf-events/
```

## 🎯 Repository Roadmap

- [x] TryHackMe - Startup (FTP Abuse & Traffic Analysis)
- [ ] TryHackMe - Kenobi (Samba & SUID Exploitation)
- [ ] PicoCTF - Forensics & Cryptography Tracks

## ⚡ Adding a New Writeup

1. Create a folder for the room and its screenshots:
   ```powershell
   mkdir -Force tryhackme/<room-name>/assets
   cp templates/writeup-template.md tryhackme/<room-name>/README.md
   ```
2. Fill in the YAML frontmatter at the top of `tryhackme/<room-name>/README.md` (`platform`, `title`, `os`, `difficulty`, `tags`, `date`).
3. Run the index generator (or push directly to let the GitHub Action update the table):
   ```powershell
   python generate_index.py
   git add .
   git commit -m "docs: add writeup for TryHackMe <room-name>"
   git push origin main
   ```
