# CERT-SCAN Codebook (v1.0)

*Plain-language header: this file defines every column in the CERT-SCAN table and the rules used to fill it in. Open it when you want to know exactly what a cell means. You will need it during verification.*

## Unit of observation

One row per **jurisdiction x program**. Jurisdictions: 50 states, District of Columbia, Puerto Rico (52). Programs: `drinking_water`, `wastewater`. Where one board certifies both under one rule, there are still two rows, with identical citations, so counts by program are always out of 52.

## Decisions fixed by the author (2026-10-23)

1. Five-level status, not yes/no.
2. **Board practice without a written rule does NOT count as "required."** It is recorded in `practice_beyond_rule` and coded no higher than the codified rule supports.
3. Exam content IS in scope (columns `exam_*`).
4. DC and Puerto Rico included.

## Status levels (`cyber_status`)

Coded on the **codified** instrument only (statute, regulation, or emergency rule). Highest applicable level wins.

| Code | Meaning | Test |
|---|---|---|
| `required` | A statute or regulation requires cybersecurity-specific training, coursework or demonstrated knowledge to obtain or renew operator certification | The text names cybersecurity (or cyber, IT/OT security, control-system security) AND makes it a condition of certification |
| `credited_optional` | Cybersecurity is explicitly eligible for certification credit, but not required | Rule or official program document names cybersecurity as an eligible CE topic, or the certifying body has approved at least one cybersecurity-titled course for credit |
| `general_security_only` | A codified security-training condition exists, but its cyber content is not established | Example: PA 25 Pa. Code 302.804 |
| `no_provision_found` | Searched; nothing found | Never "none": absence of evidence after a documented search |
| `unknown` | Could not be determined (sources unreachable or contradictory) | |

## Columns

| Column | Definition |
|---|---|
| `jurisdiction`, `abbr`, `program` | As above |
| `certifying_body` | Agency or board that issues the certificate |
| `program_authority_citation` | The rule chapter governing certification (statute; regulation). From EPA 816-R-16-002 for drinking water where unchanged, re-checked against the current code |
| `cyber_status` | See levels above |
| `mechanism` | `new_and_renewal_training` / `renewal_mandatory_hours` / `one_time_course` / `ce_eligible` / `cyber_optional_within_mandatory_category` / `none` |
| `hours`, `cycle_years`, `recurring` | As stated in the source |
| `applies_to` | Operator classes covered |
| `effective_date` | ISO date the codified provision took effect |
| `instrument_type` | `statute` / `regulation` / `emergency_rule` / `board_practice` / `guidance` / `none` |
| `citation` | Exact section supporting `cyber_status` |
| `citation_url` | Link to that text |
| `practice_beyond_rule` | What the agency does in practice that the codified rule does not show (author decision 2) |
| `exam_provider` | Who writes/administers the certification exam (ABC, WPI, state, other) |
| `exam_cyber_content` | Whether the exam's published content outline includes cybersecurity: `yes` / `no` / `not_published` |
| `evidence_note` | Short paraphrase of the source; no long quotes |
| `sources_searched` | Queries/pages checked, so a "no_provision_found" can be audited |
| `accessed` | Date sources were read |
| `confidence` | `high` (primary legal text read) / `medium` (official agency page) / `low` (secondary or inferred) |
| `verified_by_author` | `yes` only after Deborah checks it against the source |

## Known measurement limits

- `credited_optional` depends on what agencies publish online; boards approve courses that never appear on the web. It undercounts.
- The 2016 EPA baseline covers drinking water programs only. There is no wastewater baseline.
- "Required" measures the policy lever, not operator competence or security outcomes.
