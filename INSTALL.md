# Install

About fifteen minutes, most of it filling in your own details.

## 1. Prerequisites

**Claude Code**, in a folder you'll use for job applications.

**Python 3.10+** with:

```bash
pip install python-docx pypdf openpyxl
```

On Windows, add `pywin32` as well — it lets the skill ask Word for a real page count:

```bash
pip install pywin32
```

**A LaTeX distribution** for compiling the CV. On Windows:

```bash
winget install MiKTeX.MiKTeX
```

Then let it fetch packages on demand, or the first compile fails on a missing `.sty`:

```bash
initexmf --set-config-value=[MPM]AutoInstall=1
```

**A prospecting MCP server**, if you want contact finding. Built against Explorium's
vibe-prospecting. Without one, everything else still works and the skill will say it
couldn't find people.

**A LaTeX CV master**, one per market you apply in. The skill never edits it.

## 2. Drop the skill in

Copy this whole folder to `.claude/skills/apply-to-job/` in your project.

Copy the CV command so `/tailor-cv` works on its own:

```bash
cp reference/tailor-cv.md ../../commands/tailor-cv.md
```

Check Claude Code sees it — `apply-to-job` should appear in your skills list.

## 3. Fill in your profile

```bash
cp profile.example.md profile.md
```

Open it and be honest. Every rule the skill enforces reads from here.

The fields that matter most:

**Work authorisation.** List *countries*, not regions. A national student or work permit
does not travel across the EU — a French permit does not let you work in Portugal. Get
this wrong and you'll spend days on applications you can't accept.

**Language ceilings.** Write the highest level you'd defend in an interview. The skill
will never claim above it, which is the point.

**Protected numbers.** Two to four achievements that must survive tailoring, so the CV
never goes generic. Write them exactly as they appear in your master.

**Known gaps.** What you genuinely can't do. These show up in the report and, where
relevant, in outreach. Being caught overstating is worse than being under-qualified.

## 4. Point it at your files

```bash
cp config.example.json config.json
```

Set `output_root`, the `cv_masters` paths per market, and the contacts workbook path.
Use forward slashes, even on Windows.

The contacts workbook needs a sheet named `Contacts` with these headers in row 1:

```
Company | Role applied | Priority | Name | Title | Why them | LinkedIn |
Connection note | Follow-up message | Status | Date sent | Notes
```

An empty workbook with just that header row is fine — rows get appended.

## 5. Check it works

```bash
python scripts/tex_to_docx.py "path/to/your/master_cv.tex"
python scripts/check_cv.py "path/to/your/master_cv.tex"
```

The first should report `(1 page)`. The second will flag that the headline is still the
master default, which is correct — that's the check doing its job on an untailored file.

Then run it for real:

```
/apply-to-job <a job URL>
```

## Sharing this

`profile.md` and `config.json` are yours and hold personal data. Everything else is
generic. Share the folder without those two files, or replace them with the
`.example` versions.

Add to `.gitignore` if the folder is in a repo:

```
.claude/skills/apply-to-job/profile.md
.claude/skills/apply-to-job/config.json
```
