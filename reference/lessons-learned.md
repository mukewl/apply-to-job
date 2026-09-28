# Lessons learned

Things that cost real time to discover. Each one is here because it failed silently —
the output looked correct and was wrong.

---

## Job postings

**An ad written in English does not mean the job is done in English.** A GROHE France
posting was in flawless English and never named a language requirement. Every person on
that team listed their skills in French, one with "Anglais parlé" as a *separate skill*.
The job involved creating local content for the France site. Read the team's own
profiles before trusting the ad.

**Some employers ban AI-assisted applications.** Air Apps: *"Any use of AI in
application materials, assessments, or interviews will result in disqualification."*
Always grep the posting for this before writing anything. If it is there, say so and do
not ghost-write the application — help them think instead.

**Check who posted the job.** The named recruiter on the posting is a confirmed contact
on the requisition, and is usually the lowest-friction first approach. Easy to skip and
easy to find.

**Check the posting date.** Job boards differ enormously. One audit found hiring.cafe and
instahyre recycling roles one to six months old while iimjobs carried roles five to
twelve days old. Never assume a listing is live.

**Most listings on some boards hide the employer.** On iimjobs, 81% were posted by
recruitment consultancies with the real company undisclosed. That breaks contact
research entirely — there is no company to look up. Flag it rather than guessing.

**Flag level and pay mismatch.** An ad asking for 1–2 years, with a meal allowance and a
variable bonus and no base salary stated, is a junior seat. Say so before building
anything, especially for someone with an MBA and five years behind them.

---

## Contacts

**`match-business` beats keyword search.** Looking a company up by name and domain is far
more reliable than `website_keywords`, which returns name collisions and unrelated firms.

**When the data provider has nothing, the web usually does.** A Marketing Director who
owned a hire was absent from the prospect database and findable in French trade press in
one search. "Not in the database" is not "does not exist" — check the company's own
pages, the posting byline, and the press before giving up.

**Verify that a title is current.** A CFO listed at the company on both LinkedIn and the
prospect database had already left, which he said himself in his reply. Titles go stale.
Sanity-check before building outreach around someone's employer.

**A zero result can be a wrong query, not an empty market.** LinkedIn geocodes the
location `"Malta"` to Malta, **Ohio** and returns US jobs, which a country filter then
silently discards. It reads as "no jobs in Malta". Use `"Valletta, Malta"`. Check raw
pre-filter counts before believing a zero.

---

## Documents

**python-docx defaults to US Letter.** That is 18mm shorter than A4, so a CV laid out for
A4 spills by about a line on the reader's machine while looking fine on yours. Set the
page size explicitly.

**Word's Normal style is 1.15 line spacing.** LaTeX is 1.0. Set it explicitly too.

**Never trust a .docx page count you have not measured.** python-docx cannot lay out a
page. Ask Word through COM (`scripts/docx_pages.py`), and if it spilled, cut something
and rebuild.

**Verify the rules, do not eyeball them.** A CV shipped with only one protected number in
the summary when the rule required two. It looked completely fine.
`scripts/check_cv.py` exists because of that.

**Build the .docx from the tailored .tex,** never by hand alongside it. Two
hand-maintained copies drift.

---

## Process

**Reuse the company folder.** Check whether the company already has one before creating a
second. Contacts already gathered for one role at a company are usually still good for
the next one.

**Do not double-message a warm contact.** If someone already has an unanswered message
about one role, sending a second about another role within days reads as scattershot.
Wait for the reply and raise it in that conversation.

**Rank the send order.** Recruiter first when there is one, since they are lowest
friction and their read on a hard requirement tells you how hard to push. Then the peer
who does the job. Then the hiring manager.

**Say what you could not find.** "Only one relevant name surfaced and here is why" is
more useful than padding a list with people who do not matter.
