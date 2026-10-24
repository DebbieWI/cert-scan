#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: builds the preprint PDF.
  1. Writes paper/preprint/stats.tex: every number the preprint quotes, as a
     LaTeX command, taken from paper/stats.json and the release table.
  2. Writes the generated tables (required provisions, credited provisions,
     exam outline matrix, and the full 52-jurisdiction appendix) from
     data/processed/cert_scan_v1.csv and the archived exam outlines.
  3. Copies the Power BI-style figures in and compiles
     paper/preprint/cert_scan_preprint.tex with pdflatex.
The text of the preprint never contains a typed number from the data; it uses
the commands from stats.tex. Without --final it prints a pre-release line.
Do you need to open it? No. Open paper/preprint/cert_scan_preprint.pdf.
"""
import csv, json, re, shutil, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "paper/preprint"
FIG = ROOT / "paper/figures"
NTK = ROOT / "data/raw/exam_ntk/2025"
FINAL = "--final" in sys.argv
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def tex(s):
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\^{}")]:
        s = s.replace(a, b)
    s = s.replace("§", r"\S{}").replace("–", "--")
    return re.sub(r"\[VERIFY[^\]]*\]", "", s).strip()


NAMES = {"MD": "Maryland", "NY": "New York", "PA": "Pennsylvania", "TX": "Texas", "MA": "Massachusetts",
         "MI": "Michigan", "MT": "Montana", "ME": "Maine"}


def join(abbrs):
    n = sorted(NAMES.get(a, a) for a in abbrs)
    return n[0] if len(n) == 1 else (" and ".join(n) if len(n) == 2 else ", ".join(n[:-1]) + ", and " + n[-1])


def macro(name, val):
    return f"\\newcommand{{\\{name}}}{{{val}}}\n"


def main():
    PP.mkdir(parents=True, exist_ok=True)
    s = json.loads((ROOT / "paper/stats.json").read_text())
    authors = json.loads((ROOT / "AUTHORS.json").read_text())["authors"]
    a, co = authors[0], authors[1]
    rows = list(csv.DictReader(open(ROOT / "data/processed/cert_scan_v1.csv", encoding="utf-8")))
    qa = int((ROOT / "data/processed/qa_report.txt").read_text().split("Problems:")[1].split()[0])
    sb = s["status_by_program"]
    jb = s["jurisdictions_by_status"]
    pos = [r for r in rows if r["cyber_status"] != "no_provision_found"]
    inst = Counter(r["instrument_type"] for r in pos)
    def n(pg, k): return sb[pg].get(k, 0)
    wpi_dw_other = sum(1 for r in rows if r["program"] == "drinking_water" and not r["exam_provider"].startswith("WPI"))
    wpi_ww_other = sum(1 for r in rows if r["program"] == "wastewater" and not r["exam_provider"].startswith("WPI"))
    m = ""
    for k, v in {
        "nJuris": s["n_jurisdictions"], "nRows": s["n_rows"],
        "nReqJuris": len(jb["required"]), "nReqJurisW": WORDS[len(jb["required"])],
        "nCredJuris": len(jb["credited_optional"]), "nCredJurisW": WORDS[len(jb["credited_optional"])],
        "nGenJuris": len(jb["general_security_only"]), "nGenJurisW": WORDS[len(jb["general_security_only"])],
        "nAnyJuris": s["n_jurisdictions_any_provision"], "nAnyJurisW": WORDS[s["n_jurisdictions_any_provision"]],
        "nNoneJuris": s["n_jurisdictions"] - s["n_jurisdictions_any_provision"],
        "dwReq": n("drinking_water", "required"), "dwCred": n("drinking_water", "credited_optional"),
        "dwGen": n("drinking_water", "general_security_only"), "dwNone": n("drinking_water", "no_provision_found"),
        "wwReq": n("wastewater", "required"), "wwCred": n("wastewater", "credited_optional"),
        "wwGen": n("wastewater", "general_security_only"), "wwNone": n("wastewater", "no_provision_found"),
        "nWPIdw": s["n_wpi_dw_treatment"], "nWPIww": s["n_wpi_ww"],
        "nOtherExamDW": wpi_dw_other, "nOtherExamWW": wpi_ww_other,
        "nHigh": s["confidence"].get("high", 0), "nMedium": s["confidence"].get("medium", 0),
        "nLow": s["confidence"].get("low", 0), "nVerified": s["n_verified_by_author"],
        "nStateSpecific": s["n_rows_state_specific_source"], "nQA": qa,
        "nPositive": len(pos), "nInstStatute": inst["statute"], "nInstReg": inst["regulation"],
        "nInstGuidance": inst["guidance"], "nInstBoard": inst["board_practice"],
        "epaPages": s["epa2016_pages"], "epaCyber": s["epa2016_term_counts"]["cyber"],
        "epaSecurity": s["epa2016_term_counts"]["security"], "epaScada": s["epa2016_term_counts"]["scada"],
        "nReqJurisCap": WORDS[len(jb["required"])].capitalize(),
        "nCredJurisCap": WORDS[len(jb["credited_optional"])].capitalize(),
        "reqList": join(jb["required"]), "credList": join(jb["credited_optional"]),
        "nWPIdwNoReq": sum(1 for r in rows if r["program"] == "drinking_water"
                           and r["exam_cyber_content"].startswith("yes") and r["cyber_status"] != "required"),
        "nNonCodified": inst["guidance"] + inst["board_practice"],
        "accessDate": "23 October 2026", "authorName": a["name"], "authorOrcid": a["orcid"],
        "authorEmail": a["email"], "authorAffil": a["affiliation"],
        "coName": co["name"], "coOrcid": co["orcid"], "coEmail": co["email"],
        "coRoles": ", ".join(r.lower() for r in co["roles"]),
        "repoURL": "[GitHub URL assigned at release]", "doiText": "[DOI assigned at release]",
    }.items():
        m += macro(k, v)
    m += "\\newif\\iffinal\n" + ("\\finaltrue\n" if FINAL else "\\finalfalse\n")
    (PP / "stats.tex").write_text(m)

    # Table: required provisions
    req = [r for r in pos if r["cyber_status"] == "required"]
    t = ""
    for r in req:
        prog = "DW" if r["program"] == "drinking_water" else "WW"
        mech = {"new_and_renewal_training": "New and renewal training",
                "renewal_mandatory_hours": "Renewal hours (within CE total)"}.get(r["mechanism"], tex(r["mechanism"]))
        h = tex(r["hours"]).replace(" by grade", "")
        t += (f"{tex(r['jurisdiction'])} & {prog} & {mech} & {h}{' by grade' if 'grade' in r['hours'] else ''} "
              f"& {tex(r['cycle_years'])} & {tex(r['effective_date'])} & {tex(r['instrument_type']).capitalize()} "
              f"& {tex(r['citation'])} \\\\\n")
    (PP / "tab_required.tex").write_text("\\newcommand{\\tabRequired}{" + t + "}\n")

    # Table: credited provisions
    mech = {"cyber_optional_within_mandatory_category": "Cyber optional within mandatory resiliency hours",
            "ce_eligible": "Cyber eligible for CE credit"}
    inst_name = {"guidance": "Agency guidance", "board_practice": "Board course approvals"}
    t = ""
    for r in sorted((r for r in pos if r["cyber_status"] == "credited_optional"),
                    key=lambda r: (r["jurisdiction"], r["program"])):
        prog = "DW" if r["program"] == "drinking_water" else "WW"
        t += (f"{tex(r['jurisdiction'])} & {prog} & {mech.get(r['mechanism'], tex(r['mechanism']))} & "
              f"{inst_name.get(r['instrument_type'], tex(r['instrument_type']))} & {tex(r['effective_date'])} & "
              f"{tex(r['citation'])} \\\\\n")
    (PP / "tab_credited.tex").write_text("\\newcommand{\\tabCredited}{" + t + "}\n")

    # Table: exam outline matrix
    areas = [("Water treatment", "Water-Treatment-Class-{}_mh-fin.txt"),
             ("Water distribution", "WaterDistribution---Class-{}_mh-fin.txt"),
             ("Wastewater treatment", "WastewaterTreatment---Class-{}_mh-fin.txt"),
             ("Wastewater collection", "Collection---Class-{}_final.txt")]
    t = ""
    for name, pat in areas:
        cells = []
        for c in range(1, 5):
            txt = (NTK / pat.format(c)).read_text(errors="ignore")
            cells.append("Listed" if re.search("cyber", txt, re.I) else "--")
        t += f"{name} & " + " & ".join(cells) + " \\\\\n"
    (PP / "tab_exam.tex").write_text("\\newcommand{\\tabExam}{" + t + "}\n")

    # Appendix: all jurisdictions
    code = {"required": "R", "credited_optional": "C", "general_security_only": "G", "no_provision_found": "--"}
    exam = lambda r: ("WPI+" if r["exam_cyber_content"].startswith("yes") else
                      "WPI" if r["exam_provider"].startswith("WPI") else "Other")
    by = {}
    for r in rows:
        by.setdefault(r["jurisdiction"], {})[r["program"]] = r
    t = ""
    for j in sorted(by):
        dw, ww = by[j]["drinking_water"], by[j]["wastewater"]
        src = tex(dw["program_authority_citation"])
        if ww["program_authority_citation"] != dw["program_authority_citation"]:
            src += "; WW: " + tex(ww["program_authority_citation"])
        if not src:
            src = "No independent District program identified; confirmation requested"
        conf = "/".join(sorted({dw["confidence"][0].upper(), ww["confidence"][0].upper()}))
        t += (f"{tex(j)} & {code[dw['cyber_status']]} & {code[ww['cyber_status']]} & {exam(dw)} & {exam(ww)} "
              f"& {conf} & {src} \\\\\n")
    (PP / "tab_appendix.tex").write_text("\\newcommand{\\tabAppendix}{" + t + "}\n")

    for f in FIG.glob("pbi_*.png"):
        shutil.copy(f, PP / f.name)
    for _ in range(3):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "cert_scan_preprint.tex"],
                           cwd=PP, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-3000:]); sys.exit(1)
    warn = [l for l in r.stdout.splitlines() if "undefined" in l.lower() or "Overfull" in l]
    pages = re.search(r"\((\d+) pages", r.stdout)
    print("built paper/preprint/cert_scan_preprint.pdf;", pages.group(1) if pages else "?", "pages;",
          len(warn), "warnings")
    for w in warn[:12]:
        print("  ", w)


if __name__ == "__main__":
    main()
