#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: reads the 2016 EPA report and pulls out, for each state,
(a) the "Authorization" column (the laws and rules the program ran under in 2016)
and (b) who administered the certification exam. Output:
data/processed/epa2016_state_profiles.csv. These are STARTING POINTS only:
every 2016 citation is re-checked against the current code before use.
Do you need to open it? No.
"""
import csv, re
from pathlib import Path
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "data/raw/EPA_816-R-16-002.pdf"
OUT = ROOT / "data/processed/epa2016_state_profiles.csv"

def clean(x):
    return re.sub(r"\s+", " ", (x or "")).strip()


def main():
    pdf = pdfplumber.open(PDF)
    rows = []
    for i, page in enumerate(pdf.pages[:-1]):
        t = page.extract_tables()
        if not t or len(t[0]) < 2 or t[0][0][:2] != ["State", "Authorization"]:
            continue
        a = t[0][1]
        b_tab = pdf.pages[i + 1].extract_tables()
        b = b_tab[0][1] if b_tab and len(b_tab[0]) > 1 else [""] * 5
        resources = clean(b[1])
        m = re.search(r"((?:The )?[Ee]xams? (?:is|are)[^.]*\.)", resources)
        rows.append({"pdf_page": i + 1, "state": clean(a[0]),
                     "authorization_2016": clean(a[1]),
                     "renewal_2016": clean(a[5]),
                     "exam_admin_2016": clean(m.group(1)) if m else "",
                     "resources_2016": resources})
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), "profiles")


if __name__ == "__main__":
    main()
