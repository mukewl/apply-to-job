# Usage

## Running it

```
/apply-to-job https://example.com/jobs/growth-manager
```

A pasted job description works too, if the URL is behind a login.

Takes a few minutes. Most of it is fetching the posting, compiling the CV twice and
running prospect searches.

## What you get

**In `<output_root>/<Company>/`:**

- `<Name>_CV_<Company>_<Role>.pdf` — one page, verified from the LaTeX log
- the same as `.docx` — A4, page count measured through Word
- the `.tex`, so it can be re-edited later

**In your contacts workbook:** one row per person, with the connection note and message
for anyone worth contacting.

**In the chat:** the messages in copy-paste blocks with LinkedIn URLs, a send order, and
an honest list of gaps.

## Read the gaps section first

It's the most useful part. It tells you what you'll be asked in the first call and
whether the role is worth the time at all.

The skill is told to be blunt. If it says the job is a level below you, or that it needs
SEO you don't have, that isn't pessimism — it's the check working. Two or three real
applications beat fifteen hopeful ones.

## Before you send anything

**Verify the people.** LinkedIn URLs come back obfuscated (`linkedin.com/in/ACoAA...`)
and resolve when you're logged in. If one doesn't open, search the name and title —
both are given for that reason. Titles go stale; a database saying someone works
somewhere doesn't mean they still do.

**Read the messages aloud.** They're checked against a list of AI-writing tells, but
you're the last filter. If a line doesn't sound like you, change it. Say so and the rule
gets written into `reference/outreach-rules.md` so it doesn't come back.

**Check the send order.** Usually the named recruiter first — lowest friction, and their
read on a hard requirement tells you how hard to push. Then the person doing the job.
Then the hiring manager.

## Asking for changes

The skill improves by being corrected. Useful things to say:

- *"This reads like AI"* — the specific tell gets added to the reference file
- *"Don't ask for an introduction"* — becomes a hard rule
- *"I do actually know Tableau"* — goes into your master CV and profile, so it stops
  being listed as a gap
- *"Lead with the AI work for roles like this"* — becomes a variant rule

Changes to how the skill behaves belong in `SKILL.md` or the `reference/` files, not just
the conversation. **A rule agreed in chat and never written down only exists in that
chat** — a fresh session won't know about it, which is how two sessions start producing
different output from the same skill.

## Cover letters

Ask for one after the CV is built. It's written to Markdown, then:

```bash
python scripts/md_to_pdf_letter.py "<letter.md>"
```

which produces a one-page PDF with the same header and font as the CV.

## Checking a CV by hand

```bash
python scripts/check_cv.py "<tailored.tex>" --master "<master.tex>"
```

Reports too few protected numbers, invented facts in the summary, a headline left at the
master default, an inflated language claim, and either file running to two pages. Exit
code 1 if anything fails, so you can gate a build on it.

## When something goes wrong

**The PDF is two pages.** The tailoring got longer than the master. Tighten the summary
and the bullets you reworded. Never shrink the font or margins.

**The DOCX spills but the PDF doesn't.** Page size or line spacing. `tex_to_docx.py` sets
A4 and 1.0 spacing explicitly and re-measures — if you've edited it, check those first.

**No contacts found.** Small companies are poorly covered. Check the posting byline for a
named recruiter, the company's own team page, and the trade press. The skill is told to
do this, and to tell you when it came up empty rather than padding the list.

**The posting won't fetch.** Some boards block fetchers. Paste the text instead — the
skill won't guess at a role it hasn't read.
