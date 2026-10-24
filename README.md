# CERT-SCAN

**Status: DRAFT v0.3 (2026-10-23). Not for citation. Unverified rows are marked.**

CERT-SCAN is an open, yearly record of whether each U.S. state, the District of Columbia and Puerto Rico require cybersecurity knowledge for drinking water and wastewater operator certification. Every cell cites the law, rule, or agency document behind it.

## Why

The last national summary of operator certification programs, EPA 816-R-16-002 (March 2016, 131 pages), never uses the word "cyber." One state, Pennsylvania, did require a general system-security course. Since then, water systems have become a target for attackers, and a few states have begun writing cybersecurity into the operator's license. No one tracks those changes in one place. CERT-SCAN does.

## What the draft shows so far

- **Maryland was first to put it in law.** Md. Code, Environment § 9-2702(2) (2025 ch. 495) took effect October 1, 2025. The operator board had already required EPA cybersecurity training at renewal since July 1, 2025.
- **New York followed in regulation.** Drinking water: 10 NYCRR Appendix 5-E § 5-E.7, adopted March 11, 2026. Wastewater: 6 NYCRR Part 650, for renewals expiring on or after January 1, 2027.
- **Pennsylvania** has required a one-time system-security course since 2010; whether it covers cybersecurity is unconfirmed.
- **Texas, Massachusetts, Michigan, Montana and Maine (wastewater)** grant certification credit for cybersecurity training without requiring it.
- **Everywhere else, no provision was found** in the renewal rule or program page (one source read per state and program, listed in the table).
- **Exams:** the 2025 WPI exam outlines for water treatment (classes 1 to 4) list a cybersecurity task. Distribution, wastewater treatment and collection outlines do not. 33 drinking water programs use WPI exams.

![Tile map](paper/figures/fig1_tilemap.png)
![Timeline](paper/figures/fig2_timeline.png)

Final counts are generated in `paper/stats.json` and will be quoted from there after verification.

## How to run

```
python code/01_baseline_epa2016.py       # 2016 baseline scan
python code/02_extract_2016_profiles.py  # 2016 state program authorities
python code/02b_fill_sweep_rows.py       # adds unchecked rows (low confidence)
python code/02c_scan_state_sources.py    # reads each state's renewal rule, counts cyber terms
python code/02d_apply_state_checks.py    # applies the state checks to the table
python code/02e_exam_fields.py           # exam provider and exam cyber content
python code/03_build_dataset.py          # builds table, QA report, stats
python code/04_figures.py                # tile map and timeline (add --final after verification)
```

Needs Python 3, `pdfplumber`, and `pdftotext` (poppler).

## Files

- `data/processed/cert_scan_v1.csv`: the table
- `docs/CODEBOOK.md`: what every column means
- `docs/SEARCH_LOG.md`: how "no provision found" was established
- `docs/VERIFY_CHECKLIST.md`: the author's pre-release checks
- `data/raw/PROVENANCE.txt`: every downloaded source with its fingerprint

## Limitations

The table measures the policy lever, not operator skill or security outcomes. Rows marked `low` confidence rest on a nationwide search only. Agencies do not publish every course approval, so the "credited" level is undercounted. The 2016 baseline covers drinking water programs only.

## License and citation

Code: MIT. Data and documents: CC BY 4.0. Maintainer: Deborah Wale Ibinayo, Independent Researcher, Lawrenceville, Georgia. DOI: [assigned at v1.0 release].
