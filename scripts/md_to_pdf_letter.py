# -*- coding: utf-8 -*-
"""Turn a plain-text / Markdown cover letter into a one-page PDF matching the CV.

    python md_to_pdf_letter.py "<letter.md>" ["Optional Heading Line"]

Writes <letter>.tex and <letter>.pdf beside the source. The name and contact strip come
from profile.md, so nothing personal lives in this file.
"""
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import profile_io

PREAMBLE = r"""\documentclass[10pt,a4paper]{extarticle}
\usepackage[a4paper,top=1.4cm,bottom=1.4cm,left=2.0cm,right=2.0cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[hidelinks]{hyperref}
\usepackage{textcomp}
\usepackage{parskip}
\linespread{1.12}
\emergencystretch=1.2em
\setlength{\parskip}{7pt}
\pagestyle{empty}
\begin{document}
\begin{center}
    {\LARGE\bfseries @@NAME@@}\\[2pt]
    {\fontsize{8.6}{10}\selectfont @@CONTACT@@\par}
\end{center}
\vspace{2pt}
\hrule height 0.4pt
\vspace{12pt}
"""


def esc(t):
    for a, b in (("\\", r"\textbackslash "), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde "), ("^", r"\textasciicircum ")):
        t = t.replace(a, b)
    t = t.replace("’", "'").replace("‘", "'")
    t = t.replace("“", "``").replace("”", "''")
    t = t.replace("—", "---").replace("–", "--")
    return t


def build(md_path, heading=None, profile_path=None):
    who = profile_io.load(profile_path)
    if not who.get("name"):
        raise SystemExit("profile.md not found, or it has no Name - the letter header needs it")

    raw = io.open(md_path, encoding="utf-8").read()
    paras = [p.strip().replace("\n", " ") for p in raw.split("\n\n") if p.strip()]
    body = []
    if heading:
        body.append(r"\noindent\textbf{" + esc(heading) + "}\n")
    for p in paras:
        body.append(esc(re.sub(r"\s+", " ", p)) + "\n")

    head = (PREAMBLE
            .replace("@@NAME@@", esc(who["name"]).upper())
            .replace("@@CONTACT@@", esc(profile_io.contact_line(who))))
    tex = head + "\n".join(body) + "\n\\end{document}\n"

    base = os.path.splitext(md_path)[0]
    tex_path = base + ".tex"
    io.open(tex_path, "w", encoding="utf-8").write(tex)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", os.path.basename(tex_path)],
                   cwd=os.path.dirname(os.path.abspath(md_path)),
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for ext in (".aux", ".log", ".out"):
        stale = base + ext
        if os.path.exists(stale):
            os.remove(stale)
    return base + ".pdf"


if __name__ == "__main__":
    heading = sys.argv[2] if len(sys.argv) > 2 else None
    print("wrote", build(sys.argv[1], heading))
