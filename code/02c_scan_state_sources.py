#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: downloads each state's renewal rule or program page
listed in data/coding/state_sources.csv, converts it to text, and counts
cybersecurity-related words. Results go to data/processed/state_scan.csv,
with a short snippet around every hit so a person can judge it.
A page that could not be read (blocked, empty, or a "verify you are human"
page) is marked unreadable, never treated as "no cyber content".
Do you need to open it? No. Open data/processed/state_scan.csv.
"""
import csv, hashlib, html, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/coding/state_sources.csv"
OUT = ROOT / "data/processed/state_scan.csv"
CACHE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/raw/state_pages"
CYBER = re.compile(r"cyber|scada|control system|operational technology|ransomware|malware|network secur|information secur", re.I)
SEC = re.compile(r"\bsecurity\b", re.I)
BLOCK = re.compile(r"just a moment|enable javascript and cookies|access denied|please enable js|captcha", re.I)


def fetch(url, dest):
    subprocess.run(["curl", "-sSL", "-m", "45", "-A", "Mozilla/5.0", "-o", str(dest), url],
                   capture_output=True)
    if not dest.exists() or dest.stat().st_size == 0:
        return ""
    head = dest.read_bytes()[:5]
    if head.startswith(b"%PDF"):
        r = subprocess.run(["pdftotext", "-layout", str(dest), "-"], capture_output=True, text=True)
        return r.stdout
    if head.startswith(b"PK"):
        return ""
    t = dest.read_text(errors="ignore")
    t = re.sub(r"(?s)<(script|style|nav|header|footer).*?</\1>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    rows = []
    for s in csv.DictReader(open(SRC, encoding="utf-8")):
        name = hashlib.sha1(s["url"].encode()).hexdigest()[:12]
        text = fetch(s["url"], CACHE / name)
        words = len(text.split())
        readable = words > 150 and not BLOCK.search(text[:3000])
        hits = [m for m in CYBER.finditer(text)]
        snippets = " | ".join(" ".join(text[max(0, m.start() - 120): m.end() + 120].split()) for m in hits[:4])
        rows.append({**s, "words": words, "readable": "yes" if readable else "no",
                     "cyber_hits": len(hits), "security_hits": len(SEC.findall(text)),
                     "snippets": snippets})
        print(f"{s['abbr']:3} {s['program']:15} words={words:6} readable={'Y' if readable else 'N'} "
              f"cyber={len(hits):3} security={rows[-1]['security_hits']:3}")
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
