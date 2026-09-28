# -*- coding: utf-8 -*-
"""Read the applicant's details out of profile.md.

Keeps every personal fact in one gitignored file, so the scripts themselves stay
generic and shareable.
"""
import io
import os
import re

_FIELDS = {
    "name": r"name",
    "location": r"based in",
    "email": r"email",
    "portfolio": r"portfolio(?: / site)?",
    "linkedin": r"linkedin",
    "phone": r"phone",
}


def find_profile(start=None):
    """profile.md sits one level above scripts/."""
    here = os.path.dirname(os.path.abspath(start or __file__))
    for candidate in (os.path.join(here, os.pardir, "profile.md"),
                      os.path.join(here, "profile.md")):
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return None


def load(path=None):
    """Return {name, location, email, portfolio, linkedin, phone, languages, trim_first}."""
    path = path or find_profile()
    out = {k: "" for k in _FIELDS}
    out["languages"] = []
    out["trim_first"] = ""
    if not path or not os.path.exists(path):
        return out
    txt = io.open(path, encoding="utf-8").read()

    for key, label in _FIELDS.items():
        m = re.search(r"(?im)^[ \t]*-[ \t]*" + label + r"[ \t]*:[ \t]*`?([^`\n]+)`?", txt)
        if m:
            out[key] = m.group(1).strip(" `")

    for m in re.finditer(r"(?im)^[ \t]*-[ \t]*([A-Za-z ]+?)[ \t]*:[ \t]*never claim above[ \t]*`?([^`\n]+)`?", txt):
        out["languages"].append((m.group(1).strip(), m.group(2).strip(" `")))

    m = re.search(r"(?im)^[ \t]*-?[ \t]*trim first\b[^:\n]*:[ \t]*`?([^`\n]+)`?", txt)
    if m:
        out["trim_first"] = m.group(1).strip(" `")
    return out


def contact_line(p, sep=" · "):
    """The one-line contact strip used under the name."""
    bits = [p.get("location"), p.get("phone"), p.get("email"),
            p.get("portfolio"), p.get("linkedin")]
    bits += ["{} ({})".format(l, lvl) for l, lvl in p.get("languages", [])]
    return sep.join(b for b in bits if b)
