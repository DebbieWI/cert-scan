# Release verification: the short list (about 90 minutes)
*Plain-language header: verifying all 104 rows one by one is not needed for a responsible release. This list covers every record with a provision that you have not yet checked, plus a random sample of 10 'no provision found' records chosen by a fixed seed (20261023), so anyone can see the sample was not hand-picked. If all 10 match, say so in the paper; if any does not, tell Claude and the whole category is re-checked.*
## A. Records with a provision not yet verified by you
- [ ] **Massachusetts (drinking water)**: coded `credited_optional`. Open https://www.mass.gov/doc/dw-agenda-3-13-26/download and confirm: Board approved six cybersecurity courses for training contact hours (March 2026); MassDEP offers free 1-TCH cybersecurity course (Aug 2026 newsletter)
- [ ] **Michigan (drinking water)**: coded `credited_optional`. Open https://www.michigan.gov/egle/outreach/water-operator-training-courses/cybersecurity-for-the-water-sector-webinar-series and confirm: EGLE cybersecurity webinar series approved for operator CE credit
- [ ] **Michigan (wastewater)**: coded `credited_optional`. Open https://www.michigan.gov/egle/outreach/water-operator-training-courses/cybersecurity-for-the-water-sector-webinar-series and confirm: Same webinar approved for wastewater credit
- [ ] **Texas (drinking water)**: coded `credited_optional`. Open https://www.tceq.texas.gov/downloads/licensing/occupational/publications/rg-637-resiliency-requirements-for-water-operators-and-training-providers.pdf and confirm: Resiliency training mandatory (2 hr overview for new/upgrade; 2 hr per renewal cycle); cybersecurity is a permitted element of the critical-components topic but not required

## B. Random sample of 10 'no provision found' records

For each: open the link, search the page for "cyber" and "security". Confirm there is no cybersecurity requirement or credit provision.
- [ ] **Kentucky (drinking water)**: https://apps.legislature.ky.gov/law/kar/titles/401/011/001/
- [ ] **Kentucky (wastewater)**: https://apps.legislature.ky.gov/law/kar/titles/401/011/001/
- [ ] **Illinois (wastewater)**: https://ilga.gov/ftp/JCAR/AdminCode/035/035003800G07150R.html
- [ ] **South Carolina (drinking water)**: https://llr.sc.gov/env/PDF_Files/Regulations_4410.pdf
- [ ] **Nebraska (wastewater)**: https://dwee.nebraska.gov/surface-water/wastewater/wastewater-treatment-facility-operator-certification-program
- [ ] **Kansas (drinking water)**: https://www.kdhe.ks.gov/DocumentCenter/View/5187/Continuing-Education-Training-Credit-PDF
- [ ] **Tennessee (wastewater)**: https://www.law.cornell.edu/regulations/tennessee/Tenn-Comp-R-Regs-0400-49-01-.09
- [ ] **Nevada (drinking water)**: https://ndep.nv.gov/water/operator-certification/drinking-water
- [ ] **Alaska (drinking water)**: https://dec.alaska.gov/media/11157/2016-01-continuing-education-unit.pdf
- [ ] **New Mexico (drinking water)**: https://www.env.nm.gov/drinking_water/certification-renewal-requirements/

## C. Two confirmations from earlier

- [ ] Louisiana and Mississippi: you opened the documents yourself (not only another tool's summary).
- [ ] You have read `paper/preprint/cert_scan_preprint.pdf` end to end and would defend every sentence.

## D. Then

Tell Claude "verification complete". Claude marks the sampled rows verified, adds one sentence on the sample to the Technical Validation section, rebuilds with `--final` (removing the pre-release line and figure stamps), and runs the publish gate.
