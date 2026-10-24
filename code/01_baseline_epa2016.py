#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: downloads EPA's 2016 50-state summary of operator
certification programs (EPA 816-R-16-002) and searches every page for
security-related words. It writes the hits, with page numbers, to
data/processed/baseline_2016_hits.csv. This is the evidence behind the
"2016 baseline" sentence in the README and paper.
Do you need to open it? No. You only need to look at the output CSV.

Run: python code/01_baseline_epa2016.py
Needs: pdftotext (poppler-utils) on the PATH.
"""
import csv, json, re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
URL = "https://www.epa.gov/system/files/documents/2025-01/summary_of_state_operator_certification_programs.pdf"
PDF = RAW / "EPA_816-R-16-002.pdf"

# Terms searched. Kept broad on purpose: the claim "no cybersecurity content"
# should survive a search for adjacent words, not just the word "cyber".
TERMS = ["cyber", "scada", "security", "computer", "information technology",
         "operational technology", "network", "hacker", "malware", "ransomware"]


def main():
    RAW.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    if not PDF.exists():
        urllib.request.urlretrieve(URL, PDF)
        subprocess.run([sys.executable, str(ROOT / "code" / "provenance.py"), str(PDF), URL,
                        "--log", str(RAW / "PROVENANCE.txt"),
                        "--note", "EPA re-hosted the 2016 PDF under a 2025-01 path; 2016 original at 19january2021snapshot.epa.gov"],
                       check=True)
    n_pages = int(re.search(r"Pages:\s+(\d+)",
                            subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True).stdout).group(1))
    rows, counts = [], {t: 0 for t in TERMS}
    for p in range(1, n_pages + 1):
        txt = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), str(PDF), "-"],
                             capture_output=True, text=True).stdout
        for line in txt.splitlines():
            low = line.lower()
            for t in TERMS:
                if t in low:
                    counts[t] += 1
                    rows.append({"pdf_page": p, "term": t, "line": " ".join(line.split())[:200]})
    with open(OUT / "baseline_2016_hits.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pdf_page", "term", "line"]); w.writeheader(); w.writerows(rows)
    stats = {"epa2016_pages": n_pages, "epa2016_term_counts": counts}
    (OUT / "baseline_2016_stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=2))
    for r in rows:
        print(f"p.{r['pdf_page']:>3}  [{r['term']}]  {r['line']}")


if __name__ == "__main__":
    main()
