#!/usr/bin/env python3
"""Automatically scans writeup directories for YAML frontmatter and updates the root README.md index table."""
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
README_FILE = ROOT_DIR / "README.md"
START_MARKER = "<!-- INDEX_START -->"
END_MARKER = "<!-- INDEX_END -->"

DIFFICULTY_COLORS = {
    "info": "lightgrey",
    "easy": "brightgreen",
    "medium": "yellow",
    "hard": "orange",
    "insane": "red",
}


def parse_frontmatter(content: str) -> dict:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    frontmatter = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            frontmatter[key.strip().lower()] = val.strip().strip("\"'")
    return frontmatter


def scan_writeups() -> list:
    entries = []
    for file_path in ROOT_DIR.glob("*/**/README.md"):
        if any(part.startswith(".") or part == "templates" for part in file_path.parts):
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        data = parse_frontmatter(content)
        if not data:
            continue
        rel_folder = file_path.parent.relative_to(ROOT_DIR)
        entries.append(
            {
                "platform": data.get("platform", "CTF"),
                "title": data.get("title", rel_folder.name.capitalize()),
                "os": data.get("os", "N/A"),
                "difficulty": data.get("difficulty", "N/A").capitalize(),
                "tags": data.get("tags", "General"),
                "date": data.get("date", "1970-01-01"),
                "link": f"./{rel_folder.as_posix()}/",
            }
        )
    entries.sort(key=lambda x: (x["date"], x["title"]), reverse=True)
    return entries


def generate_markdown_table(entries: list) -> str:
    if not entries:
        return "\n*No writeups detected with valid frontmatter metadata.*\n"
    headers = [
        "| Platform | Target / Room | OS | Difficulty | Key Concepts / Vectors | Documentation |",
        "| :--- | :--- | :---: | :---: | :--- | :---: |",
    ]
    rows = []
    for item in entries:
        diff_label = item["difficulty"]
        diff_color = DIFFICULTY_COLORS.get(diff_label.lower(), "blue")
        diff_badge = f"![{diff_label}](https://img.shields.io/badge/-{diff_label}-{diff_color})"
        os_code = f"`{item['os']}`" if item["os"] != "N/A" else "—"
        row = (
            f"| **{item['platform']}** "
            f"| {item['title']} "
            f"| {os_code} "
            f"| {diff_badge} "
            f"| {item['tags']} "
            f"| [Read Writeup]({item['link']}) |"
        )
        rows.append(row)
    return "\n" + "\n".join(headers + rows) + "\n"


def update_root_readme():
    if not README_FILE.exists():
        print(f"[-] Error: {README_FILE} not found.")
        return
    content = README_FILE.read_text(encoding="utf-8")
    if START_MARKER not in content or END_MARKER not in content:
        print(f"[-] Error: Could not find '{START_MARKER}' and '{END_MARKER}' in README.md.")
        return
    entries = scan_writeups()
    new_table = generate_markdown_table(entries)
    pattern = re.compile(
        f"({re.escape(START_MARKER)})(.*?)({re.escape(END_MARKER)})",
        re.DOTALL,
    )
    updated_content = pattern.sub(f"\\1{new_table}\\3", content)
    README_FILE.write_text(updated_content, encoding="utf-8")
    print(f"[+] Successfully indexed {len(entries)} writeup(s) into root README.md.")


if __name__ == "__main__":
    update_root_readme()
