# -*- coding: utf-8 -*-
"""Count the real page count of a .docx by asking Word, not by guessing.

    python docx_pages.py "<file.docx>" [more.docx ...]

python-docx cannot lay out a page, so a generated CV can look fine in code and still
spill to a second page when opened. Word is installed on this machine, so ask it.
"""
import os, sys

WD_STAT_PAGES = 2


def page_count(path):
    import win32com.client
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    try:
        doc = word.Documents.Open(os.path.abspath(path), ReadOnly=True,
                                  AddToRecentFiles=False, Visible=False)
        try:
            doc.Repaginate()
            return int(doc.ComputeStatistics(WD_STAT_PAGES))
        finally:
            doc.Close(False)
    finally:
        word.Quit()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        try:
            print("{:2} page(s)  {}".format(page_count(p), os.path.basename(p)))
        except Exception as e:
            print("  ERROR {}: {}".format(os.path.basename(p), e))
