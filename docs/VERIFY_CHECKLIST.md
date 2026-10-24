# Your verification checklist (DRAFT v0.2)

*Nothing is published until you have done these checks yourself. Your name goes on this data permanently. Open `data/processed/cert_scan_v1.csv` in Excel or Google Sheets alongside this list.*

## Part A. The headline rows (about 60 minutes)

These six rows carry the project's main claims. Check each one against its source.

1. **Maryland (both rows).** Open https://mgaleg.maryland.gov/2025RS/Chapters_noln/CH_495_sb0871t.pdf. On page 3, find section 9-2702, item (2). It should say the department shall include cybersecurity awareness components for all new and renewing operator and superintendent certifications. On the last page you should see "this Act shall take effect October 1, 2025" and "Approved by the Governor, May 13, 2025." If both match, the Maryland `effective_date` (2025-10-01) is correct.
2. **New York drinking water.** Open the adopted rule PDF in the `citation_url` column. Find section 5-E.7. Confirm it requires one hour of cybersecurity training every three years for operators certified under Subpart 5-4. Confirm the adoption date of March 11, 2026 from the State Register notice or the DOH page. Fix the cell if it differs.
3. **New York wastewater.** Open the DEC page in `citation_url`. Confirm 2 hours (grades 1/1A, 2/2A) and 4 hours (grades 3/3A, 4/4A) per five-year renewal, for certificates expiring on or after January 1, 2027. Then find the date DEC adopted the 6 NYCRR Part 650 amendments and replace "2026-03 [VERIFY adoption date]".
4. **Pennsylvania (both rows).** Read 25 Pa. Code 302.804 at the link. Then email or call PA DEP's operator certification office and ask one question: "Does the SEC01 system security course include cybersecurity or control-system security content?" Their answer decides whether PA stays `general_security_only` or becomes `required`. Note who answered and the date.

## Part B. Judgment calls only you can make (15 minutes)

5. **Texas.** Since April 1, 2024, Texas requires resiliency training, and cybersecurity is allowed but not required inside it. We coded this `credited_optional`. Keep that, or create a separate level? Keeping it is simpler. A separate level would show that Texas sits closer to "required" than Michigan does.
6. **Maryland's statute directs the agency rather than the operator.** The law tells MDE to "include" cyber components, and MDE does so at renewal. We coded it `required` with instrument `statute`. Agree?
7. **The exam column.** The February 2025 WPI Water Treatment Class III outline lists "Perform cyber security according to industry standards" as one of about twenty tasks in a thirteen-question domain. Should states that adopted this exam count as "testing cybersecurity"? Our suggestion: record it in `exam_cyber_content`, but never let it change `cyber_status`.

## Part C. The five remaining low-confidence rows (30 minutes)

8. **Louisiana (both rows).** Open LAC 48:V, Chapter 73 (the renewal section) on the Louisiana Administrative Code site and search for "cyber" and "security." If nothing turns up, set confidence to `medium` and paste the URL into `citation_url`.
9. **Mississippi drinking water.** Find the MSDH waterworks operator renewal rule or form and do the same search.
10. **District of Columbia (both rows).** No DC operator certification program was found, and DC has no primacy under the Safe Drinking Water Act (EPA Region 3 runs the program). Decide how DC should appear: (a) keep it as `no_provision_found` with the note, (b) mark it "no certification program," or (c) drop DC and report 51 jurisdictions. Option (b) is the most accurate.

## Part C2. New judgment calls from Checkpoint 4 (10 minutes)

11. **Maine wastewater and Montana (both programs)** are coded `credited_optional` from agency guidance that names cybersecurity as an acceptable topic for credit. Agree?
12. **Colorado** revised its mandatory regulatory training curriculum on January 1, 2025. The curriculum guide was not readable. Worth one email to the Colorado board asking whether it includes cybersecurity.
13. **Exam column wording.** 33 drinking water programs belong to WPI, whose 2025 water treatment outlines (classes 1 to 4) list a cybersecurity task. Distribution, wastewater treatment and collection outlines do not. Membership doesn't prove a state has switched to the 2025 outlines. Keep the wording "yes_treatment_only (... adoption unconfirmed)"?

## Part D. Reproduce (10 minutes)

10. Run `python code/01_baseline_epa2016.py`. The screen should end with `"cyber": 0` and list three hits (pages 77, 82, 115).
11. Run `python code/03_build_dataset.py`. Compare `paper/stats.json` with the numbers in the README.

## Part E. Your words

12. Rewrite the README summary in your own voice. The claims must match the table.

When every box is done, tell Claude "verification complete" and the DRAFT stamps come off.

## Part F. The data paper (60 to 90 minutes)

Open `paper/manuscript.docx`. Every number in it was filled in from the data, so do not edit numbers in Word; tell Claude and the paper is rebuilt.

14. **Read it end to end.** Mark anything you would not say, or could not defend if asked.
15. **Check two sentences Claude wrote from background knowledge, not from a source read this session:**
    - Background, paragraph 1: under SDWA section 1419, a state without a compliant operator certification program loses part of its Drinking Water State Revolving Fund allotment. Confirm on EPA's operator certification page and note the exact share.
    - Reference 2: confirm the title and Federal Register page of EPA's 1999 operator certification guidelines.
16. **Rewrite the abstract and the "Testing ahead of training" paragraph in your own voice.** Claude can work through it with you line by line. The claims must stay the same.
17. **Approve the AI-use statement**, or change it so it stays true.
