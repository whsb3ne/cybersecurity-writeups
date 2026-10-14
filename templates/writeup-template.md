---
platform: TryHackMe
title: Room Name
os: Linux
difficulty: Easy
tags: Web Exploitation, Enumeration, Privilege Escalation
date: YYYY-MM-DD
---

# [Platform] - [Room Name] ([Difficulty])

**Date:** YYYY-MM-DD  
**Platform:** TryHackMe / HackTheBox / CTF  
**OS:** Linux / Windows  
**Focus Areas:** Web Exploitation, Misconfiguration, Traffic Analysis  

## 1. Executive Summary

Write a 2–3 sentence overview describing the target, the primary vulnerability that allowed the initial foothold, and the misconfiguration that led to `root` or `SYSTEM` access.

## 2. Attack Chain Summary

| Phase | Vector / Technique | Tool / Artifact |
| :--- | :--- | :--- |
| **Reconnaissance** | TCP Port Scanning & Web Directory Busting | `nmap`, `gobuster` |
| **Initial Access** | Describe initial exploitation vector | Tool / payload used |
| **Lateral Movement** | Describe credential or pivot technique | Tool / artifact used |
| **Privilege Escalation** | Describe misconfiguration or binary abuse | Binary / script path |

## 3. Walkthrough

### Phase 1: Reconnaissance & Enumeration

- **Port Scanning:** Detail open ports, service banners, and reasoning for choosing specific scan flags.
  ```bash
  nmap -sC -sV -oN nmap_initial.txt <TARGET_IP>
  ```
- **Service Enumeration:** Show what you inspected on each port (e.g., anonymous FTP, `robots.txt`, SMB shares, virtual host fuzzing).

### Phase 2: Initial Foothold

- **Vulnerability Identification:** Explain *why* the service or endpoint was vulnerable.
- **Exploitation:** Show payload crafting, execution, and establishing the reverse listener.
- **Proof:** Include initial user shell output (`whoami`, `id`, hostname).

### Phase 3: Lateral Movement / Privilege Escalation

- **Internal Enumeration:** Detail what tools or manual checks were run (`linpeas.sh`, `winPEAS`, `sudo -l`, SUID binaries, cron jobs, packet captures).
- **Exploit / Privilege Abuse:** Explain how the weak permission, credential, or binary was leveraged.
- **Root Shell & Flags:** Show terminal snippet confirming `uid=0(root)` or `nt authority\system` (redact full flag strings where required by platform rules).

## 4. Key Takeaways & Real-World Remediation

*What would a defender, SOC analyst, or systems administrator do to prevent or detect this in production?*

1. **Remediation Control 1:** Specific configuration fix (e.g., disable anonymous write access, patch service, enforce parameterized queries).
2. **Remediation Control 2:** Principle of least privilege fix (e.g., file permissions, `sudoers` restrictions, service account hardening).
3. **Detection / Monitoring Opportunity:** Relevant log source, Sysmon Event ID, or Sigma/SIEM detection rule idea.

## 5. Quality & Formatting Checklist

- [ ] **Crop screenshots tightly:** Capture only the active terminal window or browser section showing the vulnerability.
- [ ] **Use fenced code blocks:** Format commands and terminal output using ` ```bash ` rather than screenshots of plain text.
- [ ] **Redact sensitive data:** Obfuscate private tokens, VPN IPs if sensitive, and full flag values `[REDACTED]`.
- [ ] **Draft LinkedIn summary:**
  - **1. The Hook (1–2 lines):** Machine name, difficulty, and core security concept.
  - **2. The Bottleneck (1 paragraph):** The hardest pivot or deceptive rabbit hole and how you solved it.
  - **3. The Defensive Angle (2–3 bullets):** Real-world hardening and detection takeaways.
  - **4. The CTA / Link:** Link to the writeup folder on GitHub.
