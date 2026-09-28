---
description: Tailor the master LaTeX CV to one job posting and compile a one-page PDF and DOCX that keep the original formatting
argument-hint: "<job-url | pasted JD text> [--out <folder>]"
---

# Tailor CV to a job

Produce ONE tailored, one-page CV for the job in `$ARGUMENTS`, in the master's exact
formatting. **Never invent anything.**

## Inputs

- **Profile:** `.claude/skills/apply-to-job/profile.md` — the applicant's details, CV
  masters per market, language ceilings, protected numbers, and which experience entries
  may be trimmed. Read it first; every rule below depends on it.
- **Master (read-only, never edit):** the `.tex` named in the profile for this posting's
  market. Sending the wrong regional master is a silent failure — the document looks
  right and the phone number is unreachable.
- **Argument:** a job URL, or pasted job-description text. URL → fetch it. If the fetch
  fails, stop and ask for the text. **Do not guess the role.**
- Optional `--out <folder>`. Default: `<output_root>/<Company>/`.

## Step 1 — Read the JD

Extract: company, exact role title, must-have skills, responsibilities, seniority,
location, language requirement, and any stated work-authorisation or nationality
requirement.

**Stop and warn before doing any work if** the JD requires a language above the
profile's ceiling, requires the right to work in a country the profile does not cover,
or requires citizenship or clearance. Say so plainly and ask whether to continue.

## Step 2 — Tailor the content

Copy the master to a working file, then edit only these parts:

0. **Headline** (the line under the name) — **always** replace it with the posting's own
   job title, verbatim where it reads naturally. A CV headed with the exact role clears
   keyword screens and reads as a deliberate application. Drop seniority words that
   overstate the applicant ("Senior", "Lead", "Head of") and any employer-specific
   prefix. This applies to every CV, including the AI-first variant below.
1. **Summary paragraph** (the block after the header rule) — retarget to this role.
   Maximum 3 sentences. Third person, matching the master's voice. Never "I", "my".
2. **Core Competencies line** — reorder so what this JD asks for comes first. You may
   drop items to save space. **You may not add a competency absent from the master.**
3. **Experience bullets** — reword to lead with the outcome this JD cares about.
4. **Section order** — only if the JD clearly calls for it.

### Hard rules — not negotiable

- **No new facts.** Every number, date, employer, job title, tool and scope must already
  appear in the master. If the JD wants a tool the master does not have, it does not go
  in. Say what is missing in the summary report instead.
- **Never claim a language above the profile's ceiling.** The header language line stays
  as it is.
- **Never remove** the degree, or more than allows the profile's "Keep at least" number
  of protected achievements.
- **Do not touch** the preamble, `\documentclass`, geometry, fonts, `\titleformat`,
  spacing or the header block. Formatting fidelity is the whole point of this command.
- Rewording is allowed; upgrading scope ("managed" → "owned") only where the job title in
  the master already carries that authority.

### AI-first variant — when the JD leads with AI

Invert the emphasis when the employer is an AI company, or the JD asks for LLM, MCP,
agent, prompt-engineering or AI-tooling familiarity, or names AI in the job title, or
asks for an MBA alongside technical fluency.

1. **Summary** → open with the AI building, named concretely. The degree comes second.
   The marketing achievements come last; they still appear, they just stop leading.
2. **Core Competencies** → AI tooling first, automation second, the rest after.
3. **Projects** → order by what this JD values, strongest first. Drop the weakest if the
   page runs long.
4. **Experience stays exactly where it is.** Every role, every bullet, unchanged order.

A JD that mentions AI *search visibility* (GEO) is not the same as one that wants AI
tooling. Judge by what the applicant would actually do.

Inverting emphasis is allowed; inventing technical experience is not.

### To fit one page

In this order: tighten the summary → trim the Core Competencies list → shorten the
weakest bullets → drop the entry the profile marks as **Trim first**. Never drop an
entry the profile marks as **Never drop**. Never shrink the font or margins.

## Step 3 — Compile and verify

```bash
cd "<output folder>" && pdflatex -interaction=nonstopmode "<working>.tex"
grep "Output written" "<working>.log"
```

It must say `(1 page`. If it says 2, go back to Step 2's fit list and cut more. Do not
hand over a 2-page CV.

Then build the Word copy **from the same `.tex`**, so the two cannot drift:

```bash
python ".claude/skills/apply-to-job/scripts/tex_to_docx.py" "<tailored.tex>"
```

It sets A4 and 1.0 line spacing explicitly — python-docx defaults to US Letter, which is
18mm shorter and spills by about a line on the reader's machine, and Word's Normal style
is 1.15 spacing where the LaTeX is 1.0. It then asks Word for the real page count and
trims if it spilled.

**Then run the checker. Do not skip it and do not eyeball these.**

```bash
python ".claude/skills/apply-to-job/scripts/check_cv.py" "<tailored.tex>" --master "<master.tex>"
```

It catches what reading the PDF does not: too few protected numbers kept, a tool or skill
in the summary that is absent from the master, a headline left at the master default, a
language claim above the ceiling, and either file running long. A CV once went out with
only one protected number and looked completely fine. Exit code 1 means fix it first.

## Step 4 — Deliver

- Name the files `<Name>_CV_<Company>_<Role>.pdf` and `.docx` (no spaces).
- Keep the `.tex` beside them so it can be re-edited later.
- Delete the `.aux`, `.log` and `.out` files.

If `pdflatex` is missing, stop and say to run `winget install MiKTeX.MiKTeX`, then
reopen the terminal.
