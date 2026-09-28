# apply-to-job

A Claude Code skill that prepares one job application end to end: it reads the posting,
tailors a one-page CV in your own LaTeX formatting, produces a matching Word copy, finds
real people worth contacting at that company, and drafts the outreach.

**You send everything by hand.** It never logs into an account, never sends a message,
and never spends money.

```
/apply-to-job https://example.com/jobs/growth-manager
```

Out the other end: a tailored PDF and DOCX, rows appended to a contacts workbook, and
copy-paste messages in the chat with an honest list of where you fall short.

---

## Why it exists

Tailoring a CV, finding the right five people and writing messages that don't read like
spam takes 40 minutes a role. It is also where applications quietly go wrong — you send
the CV with the wrong country's phone number, or claim a language you don't speak, or
discover after applying that the job is done in Dutch.

This encodes the checks so they happen every time.

## What it does

**Reads the posting and runs four checks first.** Whether the employer bans AI-assisted
applications, whether your permit actually covers that country, whether the job needs a
local language the ad never mentions, and whether the level and pay are beneath you.
Each of these has killed an application that otherwise looked fine.

**Tailors the CV without inventing anything.** Your master `.tex` is read-only. The
headline mirrors the posting's job title. Protected achievements survive. Language levels
can't be inflated. Output is verified one page, from the LaTeX log and from Word — not
assumed.

**Finds people and says when it can't.** Company lookup by name and domain, prospects
filtered by department and seniority, ranked by closeness to the actual role. When the
database is thin it checks the posting byline, trade press and the company's own pages
rather than padding the list.

**Drafts outreach that asks instead of selling.** A connection note under 300 characters,
a message under 140 words, no metrics, and never a request for a referral. Every draft is
checked against a list of AI-writing tells before you see it.

## What's in the box

| File | What it is |
|---|---|
| `SKILL.md` | The skill itself. Claude reads this. |
| `profile.example.md` | Template for your details. Copy to `profile.md`. |
| `config.example.json` | Template for paths. Copy to `config.json`. |
| `reference/tailor-cv.md` | CV rules. Also installs as a `/tailor-cv` command. |
| `reference/outreach-rules.md` | Message format, the referral rule, AI-writing tells. |
| `reference/lessons-learned.md` | Things that fail silently. Worth reading once. |
| `scripts/tex_to_docx.py` | Tailored `.tex` → `.docx`, A4, page-verified. |
| `scripts/docx_pages.py` | Real page count, via Word. |
| `scripts/check_cv.py` | Verifies a CV against your rules before it goes out. |
| `scripts/md_to_pdf_letter.py` | Cover letter Markdown → PDF matching the CV. |

See `INSTALL.md` to set it up and `USAGE.md` for running it day to day.

## Honest limits

**It needs a LaTeX CV.** The formatting fidelity is the point — a tailored copy that
looks nothing like your CV is worse than no tailoring. If you don't have one, this isn't
for you yet.

**Contact finding needs a prospecting provider.** It's built against Explorium's
vibe-prospecting MCP on the free search-and-preview tier. Coverage of small companies is
poor, and the skill is told to fall back to the web and to say when it found nothing.

**It doesn't apply for you.** No form filling, no auto-send. That's deliberate: the
messages need your judgment, and most of these rules exist because sending the wrong
thing is worse than sending nothing.

**Word page verification is Windows-only.** It drives Word through COM. Elsewhere the
`.docx` still builds, it just isn't measured.

**It will tell you a role is a bad fit.** The gaps section is the most useful part and
the least comfortable. If it says the job needs SEO and you don't have SEO, that's the
feature working.
