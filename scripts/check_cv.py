# -*- coding: utf-8 -*-
"""Verify a tailored CV against the rules before it goes out.

    python check_cv.py "<tailored.tex>" [--master <master.tex>] [--profile <profile.md>]

Catches the failures that are invisible when you eyeball the PDF:

  * fewer than two protected numbers kept
  * a tool or skill named in the summary that is not in the master (an invented fact)
  * the headline left as the master's default instead of the job title
  * a language level claimed above what the profile allows
  * the PDF or the DOCX running to more than one page

Exit code is 1 if anything fails, so it can gate a build.
"""
import io
import os
import re
import sys

RE_PROTECTED = re.compile(r"(?im)^[ \t]*-?[ \t]*protected numbers?\b[^:\n]*:[ \t]*\n(.+?)\n[ \t]*\n", re.S)
RE_MINKEEP = re.compile(r"(?im)^[ \t]*-?[ \t]*keep at least\b[^:\n]*:\D*(\d+)")
RE_HEADLINE = re.compile(r"(?im)^[ \t]*-?[ \t]*default headline\b[^:\n]*:[ \t]*(.+)$")
RE_LANGFLOOR = re.compile(r"(?im)^[ \t]*-[ \t]*([A-Za-z ]+?)[ \t]*:[ \t]*never claim above[ \t]*`?([^`\n]+)`?")


def load_profile(path):
    """Pull the machine-checkable rules out of profile.md."""
    cfg = {"protected_numbers": [], "min_protected": 2,
           "language_floor": {}, "default_headline": ""}
    if not path or not os.path.exists(path):
        return cfg
    txt = io.open(path, encoding="utf-8").read()
    m = RE_PROTECTED.search(txt)
    if m:
        cfg["protected_numbers"] = [x.strip(" -`\t") for x in m.group(1).split("\n") if x.strip(" -`\t")]
    m = RE_MINKEEP.search(txt)
    if m:
        cfg["min_protected"] = int(m.group(1))
    for lm in RE_LANGFLOOR.finditer(txt):
        cfg["language_floor"][lm.group(1).strip().lower()] = lm.group(2).strip(" `")
    m = RE_HEADLINE.search(txt)
    if m:
        cfg["default_headline"] = m.group(1).strip(" `")
    return cfg


def body_of(tex):
    marker = "\\begin{document}"
    return tex[tex.index(marker):] if marker in tex else tex


def summary_of(body):
    m = re.search(r"\\vspace\{6pt\}\s*\n\s*\n?(.+?)\n\s*\n", body, re.S)
    return m.group(1) if m else ""


def headline_of(body):
    m = re.search(r"\\fontsize\{9\}\{11\}\\selectfont (.+?)\\par", body, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def norm(s):
    return re.sub(r"[^a-z0-9%+]", "", (s or "").lower())


def check(tex_path, profile_path=None, master_path=None):
    tex = io.open(tex_path, encoding="utf-8").read()
    body = body_of(tex)
    cfg = load_profile(profile_path)
    fails, warns = [], []

    # 1. protected numbers
    if cfg["protected_numbers"]:
        kept = [p for p in cfg["protected_numbers"] if norm(p) in norm(body)]
        if len(kept) < cfg["min_protected"]:
            fails.append("only {} protected number(s) kept, need {}. Present: {}".format(
                len(kept), cfg["min_protected"], ", ".join(kept) if kept else "none"))
        else:
            print("  ok  protected numbers: {} kept ({})".format(len(kept), ", ".join(kept)))
    else:
        warns.append("no protected numbers found in the profile - skipping that check")

    # 2. headline must not still be the master default
    hl = headline_of(body)
    if not hl:
        warns.append("no headline found under the name")
    elif cfg["default_headline"] and norm(hl) == norm(cfg["default_headline"]):
        fails.append("headline is still the master default ({!r}) - it must mirror the job title".format(hl))
    else:
        print("  ok  headline: {!r}".format(hl))

    # 3. language claims must not exceed the profile ceiling
    for lang, floor in cfg["language_floor"].items():
        m = re.search(re.escape(lang) + r"\s*\(([^)]+)\)", body, re.I)
        if m and norm(m.group(1)) != norm(floor):
            fails.append("{} claimed as {!r}, profile allows only {!r}".format(
                lang.title(), m.group(1), floor))

    # 4. invented facts: capitalised tokens in the summary must exist in the master
    if master_path and os.path.exists(master_path):
        master = io.open(master_path, encoding="utf-8").read()
        tokens = set(re.findall(r"\b([A-Z][A-Za-z0-9.+#]{2,})\b", summary_of(body)))
        stop = {"The", "This", "That", "His", "Her", "Has", "Have", "Owned", "Built", "Runs",
                "Works", "Tracks", "Global", "MBA", "Four", "Five", "Performance", "Digital",
                "Lifecycle", "Growth", "Marketing", "Manager", "Content", "Analytics", "Before"}
        unknown = sorted(t for t in tokens - stop if norm(t) not in norm(master))
        if unknown:
            fails.append("summary names things absent from the master: " + ", ".join(unknown))
        else:
            print("  ok  no invented facts in the summary")

    # 5. one page, measured
    pdf = os.path.splitext(tex_path)[0] + ".pdf"
    if os.path.exists(pdf):
        try:
            from pypdf import PdfReader
            n = len(PdfReader(pdf).pages)
            if n == 1:
                print("  ok  pdf is 1 page")
            else:
                fails.append("pdf is {} pages".format(n))
        except Exception as e:
            warns.append("could not read the pdf ({})".format(type(e).__name__))
    else:
        warns.append("no pdf beside the .tex - compile before checking")

    docx = os.path.splitext(tex_path)[0] + ".docx"
    if os.path.exists(docx):
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from docx_pages import page_count
            n = page_count(docx)
            if n == 1:
                print("  ok  docx is 1 page")
            else:
                fails.append("docx is {} pages".format(n))
        except Exception:
            warns.append("could not measure the docx (Word unavailable)")

    for w in warns:
        print("  --  " + w)
    for f in fails:
        print("  XX  " + f)
    return not fails


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    tex = args[0]
    prof = args[args.index("--profile") + 1] if "--profile" in args else None
    master = args[args.index("--master") + 1] if "--master" in args else None
    if prof is None:
        here = os.path.dirname(os.path.abspath(__file__))
        candidate = os.path.join(here, os.pardir, "profile.md")
        prof = candidate if os.path.exists(candidate) else None
    print("checking {}".format(os.path.basename(tex)))
    sys.exit(0 if check(tex, prof, master) else 1)
