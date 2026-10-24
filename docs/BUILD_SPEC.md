# Build spec: CERT-SCAN v1.0 (DRAFT)

*Plain-language header: this is the one-page plan the whole build follows. If the project changes, this file changes first.*

```
PROJECT:        CERT-SCAN. Archetypes: open dataset (1) + annual report (5) + data descriptor paper (8).
QUESTION:       In each U.S. state, does the drinking water and/or wastewater operator certification
                program require, credit, or test cybersecurity knowledge, and under what legal instrument?
SOURCES:        EPA 816-R-16-002 (Mar 2016, 131 pp; baseline); state administrative codes and registers;
                state board notices, renewal forms, minutes; EPA/ASDWA/ABC materials for context.
                All accessed with date, URL, SHA-256 in data/raw/PROVENANCE.txt.
UNIT:           State x program (drinking water; wastewater). Combined programs coded once with program =
                drinking_water_and_wastewater. Target: 50 states (+DC, PR if author chooses).
MEASURES:       cyber_status (required / credited_optional / general_security_only / none / unknown)
                requirement_mechanism (initial exam content / new-cert training / renewal mandatory hours /
                  one-time course / CE-eligible only)
                cyber_specific (yes / no / unknown), hours, cycle_years, recurring, applies_to,
                effective_date, instrument_type (statute / regulation / emergency rule /
                  board administrative practice / guidance), citation, citation_url, evidence_note,
                accessed, confidence, verified_by_author.
OUTPUTS:        data/processed/cert_scan_v1.csv; docs/CODEBOOK.md; figures/ (state map, timeline);
                paper/ data descriptor; docs/STATE_BRIEF.pdf (one page); CITATION.cff.
VENUES:         GitHub + Zenodo DOI (v1.0); data paper preprint; ASDWA / AWWA / state program managers;
                annual versioned release on Zenodo (same concept DOI).
VERIFY POINTS:  (1) definition of "embeds cybersecurity"; (2) how PA's 2010 security course is coded;
                (3) whether board practice without a codified rule counts as "required";
                (4) the "first state" sentence; (5) every "required" row checked against its source.
LICENSE:        Code MIT; data and docs CC BY 4.0.
ASSUMPTIONS:    50 states only, DC/territories later; exam content (ABC need-to-know) out of scope for v1.0.
```
