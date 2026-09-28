---
name: apply-to-job
description: End-to-end prep for one job application - read the posting, produce a tailored one-page CV in the applicant's own formatting (PDF and DOCX), find real people worth contacting at that company, and draft the outreach for them to send by hand. Use when given a job URL or job description and asked to apply, prepare an application, tailor a CV for a role, or find who to reach out to about a job.
---

# Prepare one job application

Produce everything needed to apply by hand: a tailored CV, a shortlist of real people to
contact, and drafted messages.

**Nothing is ever sent automatically. No account is ever logged into. Nothing that costs
money is ever bought.**

## Before anything else

Read **`profile.md`** (path in `config.json`). It holds the applicant's identity, work
authorisation, language ceilings, CV masters, protected numbers and known gaps. Every
rule below depends on it. If it is missing, copy `profile.example.md` and ask them to
fill it in — do not guess at someone's work authorisation.

Read **`config.json`** for paths: CV masters, contacts workbook, output root, scripts.

Also read `reference/outreach-rules.md` before writing any message, and
`reference/lessons-learned.md` once — it is the list of things that fail silently.

Output folder: `<output_root>/<Company>/`. **Check whether that folder already exists**
before creating a new one; a company often has more than one role, and existing contacts
usually still apply.

---

## Step 1 — Read the posting

Fetch the URL. `WebFetch` first. If it 403s, open it in the browser and pull
`document.body.innerText`. If both fail, stop and ask for the pasted text.
**Never guess the role.**

Extract: company, exact title, location (city **and country**), contract type, years
required, responsibilities, must-have skills, language requirement, and any stated work
authorisation or nationality requirement.

Then run these four checks. Each one has ended an application that otherwise looked fine.

**1. Does the employer ban AI-assisted applications?** Grep the posting for
`AI-generated`, `use of AI`, `your own work`. Some state that any AI use in application
materials means disqualification. If so, **say so and stop writing.** Offer research and
honest assessment instead — those are advice to the applicant, not submitted material.

**2. Work authorisation, by country.** Compare the posting's country against the
profile's list. A national student or work permit does **not** travel across the EU: a
French permit does not cover Portugal, Poland or Malta. If the role needs sponsorship,
say so plainly in one or two sentences and keep going unless the profile forbids it.

**3. Language, beyond what the ad says.** The ad being in English is not enough. If the
job involves local content, local agencies or a local market, check whether the work
itself needs the language. Look at the team's own LinkedIn profiles: skills listed in the
local language, or "spoken English" listed as a *separate skill*, means the team works in
that language. Raise it, and make it a question in the outreach.

**4. Level and pay.** If the ad asks for materially fewer years than the applicant has,
or the stated package is junior, say so before building anything.

---

## Step 2 — Tailor the CV

`reference/tailor-cv.md` is the single source of truth for CV rules. Follow it exactly.

**Pick the master by market first,** from the profile's table. Sending the wrong regional
master is a silent failure: the document looks right and the phone number is unreachable.
Say which master you chose.

The essentials, which `tailor-cv.md` covers in full:

- **The headline always mirrors the posting's job title.** Every time, including the
  AI-first variant. Drop seniority words that overstate the applicant.
- The master is **read-only**. Invent nothing — no tool, employer, number or skill that
  is not already in it. If the JD wants something absent, it goes in the gaps report.
- Never claim a language above the profile's ceiling.
- Keep at least the profile's minimum number of **protected numbers** in the summary.
- Never touch the preamble, geometry, fonts or spacing.
- **One page**, verified from the LaTeX log (`Output written ... (1 page`).

**AI-first variant.** If the employer is an AI company, or the JD names LLM, MCP, agent,
Claude, GPT, prompt engineering or AI tooling, invert the emphasis: the AI building leads
the summary and competencies, paid media follows, experience stays untouched. A JD that
mentions AI *search visibility* (GEO) is not the same as one that wants AI tooling —
judge what the applicant would actually do.

**Then produce the `.docx`, every time:**

```
python <scripts_dir>/tex_to_docx.py "<tailored.tex>"
```

It converts the tailored `.tex`, so the two cannot drift. It sets A4 and 1.0 line
spacing explicitly, then asks Word for the real page count and trims if it spilled.

**Then verify, do not eyeball:**

```
python <scripts_dir>/check_cv.py "<tailored.tex>" --master "<master.tex>"
```

This catches too few protected numbers, invented facts in the summary, a headline left at
the master default, a language claim above the ceiling, and either file running long. Fix
anything it reports before handing over.

---

## Step 3 — Find 5–10 people worth contacting

Use the prospecting provider named in `config.json` (Explorium's vibe-prospecting MCP by
default). Load its tools with `ToolSearch` first — the names carry a session prefix.

### Absolute rules — money

- **Never call `export-to-csv` or `enrich-prospects`.** Search and preview are free;
  export is not, and enrich returns masked values that only unmask on export.
- Never confirm a credit-consuming action on the applicant's behalf. If a tool asks for
  confirmation to spend, stop and report.
- `cost_in_credits` in a response is an **export estimate, not a charge.**

### Procedure

1. **Find the company.** Use `match-business` with the company name and domain. It is far
   more reliable than keyword search, which returns name collisions. Confirm the returned
   business really is the employer.
2. **Fetch prospects** at that `business_id`, with `job_department: ["marketing"]` plus
   adjacent departments only when the JD calls for them, and `prospect_country_code` for
   the country the role sits in.
   - **Large company (1000+):** `["manager","senior manager","director"]`. The VP and
     C-suite layer is too far above a manager-level application.
   - **Small company (under ~200):** add `["founder","c-suite"]` — there the founder or
     Head of Marketing genuinely is the hiring manager.
3. **`show-sample`** with the returned `table_name` to unmask names, titles and LinkedIn
   URLs. This is free.
4. More names? Re-run step 2 with `exclude_key: "prospects"`, then `show-sample` again.

### When the database is thin — do not stop there

A zero or a weak result is a starting point, not an answer.

- **Check who posted the job.** A named recruiter on the posting is confirmed on the
  requisition and is usually the best first approach.
- **Search the web and trade press.** Hiring managers absent from prospect databases are
  often one search away. Verify anyone found this way, and say where they came from.
- **Check the company's own team and about pages.**
- **Verify titles are current.** People leave; databases lag. Sanity-check before
  building outreach around someone's employer.

Say plainly what you could not find. "One relevant name, and here is why" beats a padded
list.

### Reading the results

- Quote `records_available` as what you got. `records_matching_filters` is upstream
  headroom — never present it as data you have.
- Prospect fetches return **no email or phone values**. Do not imply otherwise and never
  guess an address.
- LinkedIn URLs come back obfuscated (`linkedin.com/in/ACoAA...`). They resolve in a
  logged-in browser. Always give the person's **name and title** too so they can just
  search.

Rank by closeness to the actual role: the team the job describes working with, then that
team's manager. Say which are relevant and which are noise.

**Never** log in to LinkedIn, search it while authenticated, send connection requests or
send InMail.

---

## Step 4 — Draft the outreach

Follow `reference/outreach-rules.md` in full: the connection note, the message format,
the never-ask-for-a-referral rule, and the AI-writing tells to check every draft against.

Append rows to the contacts workbook named in `config.json`, preserving existing rows and
formatting. Columns:

`Company | Role applied | Priority | Name | Title | Why them | LinkedIn | Connection note | Follow-up message | Status | Date sent | Notes`

Priority 1–3 = contact these, 4–5 = optional peers, 9 = surfaced but not relevant. Give
**every** person a row; write messages only for 1–3. Set `Status` to `Not sent`. Row
height ~205 where there is a message, ~45 otherwise, wrapping Title, Why them and both
message columns.

**Do not double-message a warm contact.** If someone already holds an unanswered message
about another role, note it and wait rather than sending a second.

**Give a send order** and the reason for it.

If the workbook is locked, say so and ask them to close it. Never silently write
elsewhere.

---

## Step 5 — Cover letter, when asked

Write it to `<output_root>/<Company>/Cover_Letter_<Company>_<Role>.md`, then:

```
python <scripts_dir>/md_to_pdf_letter.py "<letter.md>"
```

That produces a one-page PDF with the same header and font as the CV, so the two read as
one set.

Same voice rules as outreach: plain verbs, contractions, one idea per sentence, no
headed sections, no em dashes, no summarising flourish. Name the genuine gap in its own
short paragraph — it is stronger than burying it, and it controls how it lands.

---

## Step 6 — Deliver

Leave in `<output_root>/<Company>/`: the `.pdf`, the `.docx` and the `.tex`. Delete
`.aux`, `.log`, `.out`.

Then report **in chat**, briefly:

1. Output path, which master was used, and the **verified** page count for both files
2. What changed in the CV
3. The people found, ranked, each with a one-line note on why they are or are not
   relevant, and the send order
4. **The connection note and message in full, in copy-paste code blocks, with that
   person's LinkedIn URL above each one** — so nothing needs the workbook opened
5. **Gaps.** What the posting wants that the CV genuinely does not support. Be straight;
   this is what gets asked in a first-round call.

Offer to log the row in the tracker workbook.
