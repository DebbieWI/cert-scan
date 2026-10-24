#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: fills the two exam columns for every row. It uses the WPI
(Water Professionals International, formerly the ABC exam service) regulatory
member list read on 2026-10-23 and the 2025 WPI exam outlines
(data/raw/exam_ntk/2025). In those outlines, only Water Treatment classes 1-4
list a cybersecurity task; Distribution, Wastewater Treatment and Collection
do not. Membership shows a state uses WPI exams; it does not prove the state
has switched to the 2025 version, so 'yes' is worded with that caveat.
Do you need to open it? No.
"""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CODING = ROOT / "data/coding/coding.csv"

# Programs each state's regulatory member body lists (WT/Dist = drinking water; WWT/Coll = wastewater)
WPI_DW_WT = set("AL AK AZ AR CO CT GA HI ID IA KS ME MD MA MN MS MT NV NH NJ NY OH OK OR RI SC SD TN VT VA WA WV WY".split())
WPI_DW_DIST_ONLY = {"NM"}          # NM member lists Dist but not WT
WPI_WW = set("AL AK AZ AR CO CT DE GA HI ID IA KS ME MD MA MS MT NE NJ NM NY OH OK OR SC SD TN UT VT VA WA WV WY MO".split())
NOTE_WW_ASSOC = {"NV": "Nevada WEA (association) is a WPI member for wastewater; NDEP exam source not confirmed"}

rows = list(csv.DictReader(open(CODING, newline="", encoding="utf-8")))
cols = list(rows[0])
for r in rows:
    ab, pg = r["abbr"], r["program"]
    if pg == "drinking_water":
        if ab in WPI_DW_WT:
            r["exam_provider"] = "WPI"
            r["exam_cyber_content"] = "yes_treatment_only (WPI 2025 WT 1-4 outline lists a cyber task; state adoption of 2025 version unconfirmed)"
        elif ab in WPI_DW_DIST_ONLY:
            r["exam_provider"] = "WPI (distribution only)"
            r["exam_cyber_content"] = "no (WPI 2025 distribution outline has no cyber task)"
        else:
            r["exam_provider"] = "state or other (not a WPI regulatory member)"
            r["exam_cyber_content"] = "not_published"
    else:
        if ab in WPI_WW:
            r["exam_provider"] = "WPI"
            r["exam_cyber_content"] = "no (WPI 2025 wastewater treatment and collection outlines have no cyber task)"
        else:
            r["exam_provider"] = NOTE_WW_ASSOC.get(ab, "state or other (not a WPI regulatory member)")
            r["exam_cyber_content"] = "not_published"
with open(CODING, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
from collections import Counter
print(Counter((r["program"], r["exam_cyber_content"].split(" ")[0]) for r in rows))
