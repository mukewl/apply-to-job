# -*- coding: utf-8 -*-
"""Convert a tailored LaTeX CV into a matching .docx.

    python tex_to_docx.py "<path to tailored .tex>"

Writes the .docx beside the .tex. Used by the apply-to-job / tailor-cv flow, which
requires a Word copy alongside every PDF (many application forms reject or mangle PDFs).
It will not match the LaTeX pixel for pixel - it needs to be clean and one page.
"""
import io, os, re, sys

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def clean(t):
    t = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\textbf\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\textit\{([^}]*)\}", r"\1", t)
    for a, b in ((r"\textperiodcentered\ ", " \u00b7 "), (r"\textperiodcentered", "\u00b7"),
                 (r"\textendash\ ", "\u2013 "), (r"\textendash", "\u2013"),
                 (r"$\vert$", "|"), (r"$\times$", "x"), (r"\&", "&"), (r"\%", "%"),
                 (r"\csep", " \u00b7 "), (r"--", "\u2013"), (r"\,", " ")):
        t = t.replace(a, b)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", "", t)
    t = t.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s+", " ", t).strip()


def build(tex_path, trim=False):
    src = io.open(tex_path, encoding="utf-8").read()
    if trim:
        # last-resort cut, naming the entry profile.md marks as "Trim first"
        entry = ""
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import profile_io
            entry = profile_io.load().get("trim_first", "")
        except Exception:
            pass
        if entry:
            a = src.find("\\job{" + entry)
            b = src.find("% ---------------- PROJECTS", a) if a > -1 else -1
            if a > -1 and b > a:
                src = src[:a] + src[b:]
    body = src[src.index(r"\begin{document}"):]

    m = re.search(r"LARGE.{0,12}bfseries\s+([A-Z][A-Z .À-ž-]+?)\s*\}", body)
    name = clean(m.group(1)) if m else ""
    m = re.search(r"\\fontsize\{9\}\{11\}\\selectfont (.+?)\\par", body, re.S)
    headline = clean(m.group(1)) if m else ""
    m = re.search(r"\\fontsize\{8\.3\}\{10\}\\selectfont (.+?)\\par", body, re.S)
    contact = clean(m.group(1)) if m else ""

    after_rule = body[body.index(r"\hrule height 0.4pt"):]
    m = re.search(r"\\vspace\{6pt\}\s*\n\s*\n?(.+?)\n\s*\n", after_rule, re.S)
    summary = clean(m.group(1)) if m else ""
    m = re.search(r"\\textbf\{Core Competencies:\}(.+?)\n\s*\n", after_rule, re.S)
    comps = "Core Competencies: " + clean(m.group(1)) if m else ""

    doc = Document()
    sec = doc.sections[0]
    # python-docx defaults to US Letter, which is 18mm shorter than A4 - tuned for A4 and
    # rendered on Letter, the CV spills by about a line. Set it explicitly.
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(0.8)
    sec.left_margin = sec.right_margin = Cm(1.5)
    st = doc.styles["Normal"]
    st.font.name = "Arial"; st.font.size = Pt(9)
    # Word's Normal style is 1.15 line spacing by default; the LaTeX is 1.0
    st.paragraph_format.line_spacing = 1.0
    st.paragraph_format.space_after = Pt(3); st.paragraph_format.space_before = Pt(0)
    try:
        bl = doc.styles["List Bullet"]
        bl.font.name = "Arial"; bl.font.size = Pt(9)
        bl.paragraph_format.line_spacing = 1.0
        bl.paragraph_format.space_after = Pt(2); bl.paragraph_format.space_before = Pt(0)
    except KeyError:
        pass

    def para(text, size=9, bold=False, align=None, after=3, before=0):
        p = doc.add_paragraph()
        if align: p.alignment = align
        p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
        r = p.add_run(text); r.font.size = Pt(size); r.bold = bold; r.font.name = "Arial"

    def heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7); p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text.upper()); r.bold = True; r.font.size = Pt(10.5); r.font.name = "Arial"
        pb = p._p.get_or_add_pPr(); bdr = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
        bt.set(qn("w:val"), "single"); bt.set(qn("w:sz"), "6"); bt.set(qn("w:space"), "1")
        bt.set(qn("w:color"), "000000"); bdr.append(bt); pb.append(bdr)

    def jobline(left, right):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(18.0), WD_ALIGN_PARAGRAPH.RIGHT)
        r = p.add_run(left); r.bold = True; r.font.size = Pt(9); r.font.name = "Arial"
        r2 = p.add_run("\t" + right); r2.font.size = Pt(9); r2.font.name = "Arial"

    def bullet(text):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2); p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Cm(0.5); p.paragraph_format.first_line_indent = Cm(-0.25)
        r = p.add_run(text); r.font.size = Pt(9); r.font.name = "Arial"

    para(name, size=17, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=1)
    if headline:
        para(headline, size=9, align=WD_ALIGN_PARAGRAPH.CENTER, after=1)
    para(contact, size=8.3, align=WD_ALIGN_PARAGRAPH.CENTER, after=5)
    para(summary, after=4)
    para(comps, after=2)

    # walk the rest of the document in order
    rest = after_rule[after_rule.index(r"% ---------------- EXPERIENCE"):]
    for line in rest.splitlines():
        ls = line.strip()
        if not ls or ls.startswith("%") or ls.startswith(r"\begin{itemize}") \
           or ls.startswith(r"\end{itemize}") or ls.startswith(r"\end{document}"):
            continue
        m = re.match(r"\\section\*\{(.+?)\}", ls)
        if m:
            heading(clean(m.group(1))); continue
        m = re.match(r"\\job\{(.+)\}\{(.+?)\}\s*$", ls)
        if m:
            jobline(clean(m.group(1)), clean(m.group(2))); continue
        if ls.startswith(r"\item"):
            bullet(clean(ls[5:])); continue
        txt = clean(ls)
        if txt:
            para(txt, after=2)

    out = os.path.splitext(tex_path)[0] + ".docx"
    doc.save(out)
    return out


def build_one_page(tex_path):
    """Build, then ask Word how many pages it really is. If it spilled, drop the
    entry profile.md marks as "Trim first" and rebuild. python-docx cannot lay out a
    the only way to know."""
    out = build(tex_path)
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from docx_pages import page_count
    except Exception:
        print("  (Word not available - page count unverified)")
        return out, None
    try:
        n = page_count(out)
    except Exception as e:
        print("  (could not measure: %s)" % type(e).__name__)
        return out, None
    if n <= 1:
        return out, n
    print("  docx came to %d pages - trimming and rebuilding" % n)
    out = build(tex_path, trim=True)
    try:
        n = page_count(out)
    except Exception:
        n = None
    return out, n


if __name__ == "__main__":
    p, n = build_one_page(sys.argv[1])
    print("wrote {}{}".format(p, "" if n is None else "  ({} page)".format(n)))
