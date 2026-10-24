#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: builds the data paper. It fills every number and list in
paper/manuscript_template.md from paper/stats.json and AUTHORS.json, writes
paper/manuscript.md, and converts it to paper/manuscript.docx with pandoc.
Nobody types a number into the paper by hand, so the paper cannot disagree
with the data. Without --final the paper carries a DRAFT banner.
Do you need to open it? No. Open paper/manuscript.docx.
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "paper"
FINAL = "--final" in sys.argv
NAMES = {"MD": "Maryland", "NY": "New York", "PA": "Pennsylvania", "TX": "Texas", "MA": "Massachusetts",
         "MI": "Michigan", "MT": "Montana", "ME": "Maine"}
NOTE = {("MA", "drinking_water"), ("ME", "wastewater"), ("TX", "drinking_water")}


def word(n):
    return ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"][n] if n <= 10 else str(n)


def join(abbrs, qualify=None):
    names = [NAMES.get(a, a) for a in abbrs]
    if qualify:
        names = [n + qualify.get(a, "") for n, a in zip(names, abbrs)]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def main():
    s = json.loads((P / "stats.json").read_text())
    a = json.loads((ROOT / "AUTHORS.json").read_text())["authors"][0]
    qa = (ROOT / "data/processed/qa_report.txt").read_text()
    qa_problems = int(qa.split("Problems:")[1].split()[0])
    req = s["jurisdictions_by_status"]["required"]
    cred = s["jurisdictions_by_status"]["credited_optional"]
    gen = s["jurisdictions_by_status"]["general_security_only"]
    progs = {}
    for r in s["positive_rows"]:
        progs.setdefault(r["abbr"], set()).add(r["program"])
    qual = {ab: (" (drinking water)" if p == {"drinking_water"} else
                 " (wastewater)" if p == {"wastewater"} else "") for ab, p in progs.items()}
    rows = [r for r in s["positive_rows"] if r["cyber_status"] == "required"]
    table = ["| State | Program | Hours per cycle | Effective | Citation |",
             "|---|---|---|---|---|"]
    for r in rows:
        h = r["hours"].replace(" by grade", "")
        cyc = f"{h} h{' by grade' if 'grade' in r['hours'] else ''} / {r['cycle_years']} yr"
        table.append(f"| {r['abbr']} | {'DW' if r['program'] == 'drinking_water' else 'WW'} | {cyc} "
                     f"| {r['effective_date']} | {r['citation']} |")
    table.append("")
    table.append("*DW = drinking water; WW = wastewater. Maryland's training length is set by the operator board, not the statute.*")
    sb = s["status_by_program"]
    fill = dict(
        author_name=a["name"], author_affiliation=a["affiliation"], author_orcid=a["orcid"],
        author_email=a["email"], version="1.0" if FINAL else "1.0 DRAFT", accessed="23 October 2026",
        draft_banner="" if FINAL else "**DRAFT. Not for citation or circulation. Numbers are generated from the dataset and will change if the data change.**",
        epa2016_pages=s["epa2016_pages"], epa2016_cyber=s["epa2016_term_counts"]["cyber"],
        epa2016_security=s["epa2016_term_counts"]["security"], epa2016_scada=s["epa2016_term_counts"]["scada"],
        n_rows=s["n_rows"], n_juris=s["n_jurisdictions"],
        n_req_juris=len(req), req_list=join(req),
        n_cred_juris=len(cred), cred_list=join(cred, qual),
        n_gen_juris=len(gen), gen_list=join(gen),
        n_req_juris_w=word(len(req)), n_req_juris_W=word(len(req)).capitalize(),
        n_cred_juris_W=word(len(cred)).capitalize(), n_gen_juris_W=word(len(gen)).capitalize(),
        n_none_dw=sb["drinking_water"].get("no_provision_found", 0),
        n_none_ww=sb["wastewater"].get("no_provision_found", 0),
        n_wpi_dw=s["n_wpi_dw_treatment"], table_required="\n".join(table),
        qa_problems=qa_problems, n_state_specific=s["n_rows_state_specific_source"],
        n_high=s["n_rows_primary_text_high"], n_verified=s["n_verified_by_author"],
        repo_url="[GITHUB URL PENDING]", doi="[DOI PENDING]")
    text = (P / "manuscript_template.md").read_text().format(**fill)
    (P / "manuscript.md").write_text(text)
    subprocess.run(["pandoc", "manuscript.md", "-o", "manuscript.docx", "--resource-path", "."],
                   cwd=P, check=True)
    print("wrote paper/manuscript.md and paper/manuscript.docx;", len(text.split()), "words")


if __name__ == "__main__":
    main()
