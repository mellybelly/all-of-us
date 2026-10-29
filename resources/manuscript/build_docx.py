#!/usr/bin/env python3
"""Render the manuscript (outline.md) + references (references-seed.md) to a .docx
with headings, tables, bullets, inline bold/links/code, and clickable DOI hyperlinks."""
import re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.shared import OxmlElement, qn
from docx.oxml.ns import qn as nsqn

def add_hyperlink(p, url, text):
    part = p.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), r_id)
    r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
    c = OxmlElement('w:color'); c.set(qn('w:val'), '1155CC'); rPr.append(c)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rPr.append(u)
    r.append(rPr)
    t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); r.append(t)
    h.append(r); p._p.append(h)

TOKEN = re.compile(r'\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)]+)\)|`([^`]+)`|\*(.+?)\*')
def render(p, text, size=11):
    pos = 0
    for m in TOKEN.finditer(text):
        if m.start() > pos:
            run = p.add_run(text[pos:m.start()]); run.font.size = Pt(size)
        if m.group(1) is not None:
            run = p.add_run(m.group(1)); run.bold = True; run.font.size = Pt(size)
        elif m.group(2) is not None:
            add_hyperlink(p, m.group(3), m.group(2))
        elif m.group(4) is not None:
            run = p.add_run(m.group(4)); run.font.name = 'Consolas'; run.font.size = Pt(size - 0.5)
        elif m.group(5) is not None:
            run = p.add_run(m.group(5)); run.italic = True; run.font.size = Pt(size)
        pos = m.end()
    if pos < len(text):
        run = p.add_run(text[pos:]); run.font.size = Pt(size)

doc = Document()
doc.styles['Normal'].font.name = 'Calibri'
doc.styles['Normal'].font.size = Pt(11)

def add_table(doc, rows):
    # rows: list of lists (header first), separator already dropped
    tbl = doc.add_table(rows=len(rows), cols=len(rows[0]))
    tbl.style = 'Light Grid Accent 1'
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            para = tbl.cell(ri, ci).paragraphs[0]
            render(para, cell, size=9.5)
            if ri == 0:
                for run in para.runs:
                    run.bold = True

def split_row(line):
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    return cells

def emit(path):
    lines = [l.rstrip('\n') for l in open(path)]
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s or s == '---':
            i += 1; continue
        if s.startswith('|'):                      # table block
            block = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                block.append(lines[i]); i += 1
            rows = [split_row(b) for b in block]
            rows = [r for r in rows if not all(set(c) <= set('-: ') for c in r)]  # drop separator
            add_table(doc, rows); doc.add_paragraph()
            continue
        if s.startswith('> '):                     # blockquote callout
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(0.3)
            render(p, s[2:]);
            for r in p.runs: r.italic = True
            i += 1; continue
        if s.startswith('# '):
            doc.add_heading(re.sub(r'[*`]', '', s[2:]), 0)
        elif s.startswith('## '):
            doc.add_heading(re.sub(r'[*`]', '', s[3:]), 1)
        elif s.startswith('### '):
            doc.add_heading(re.sub(r'[*`]', '', s[4:]), 2)
        elif s.startswith('- '):
            render(doc.add_paragraph(style='List Bullet'), s[2:])
        elif re.match(r'^\d+\.\s', s):
            render(doc.add_paragraph(style='List Number'), re.sub(r'^\d+\.\s', '', s))
        else:
            render(doc.add_paragraph(), s)
        i += 1

SECTION_LABELS = {
    'anchor seeds': "Anchor references (author's prior work)",
    '1. introduction': 'Introduction',
    '2. the': 'Research landscape',
    '3. benchmarking': 'Peer biobanks',
    '4. emerging': 'Emerging frontiers',
    '5. the analysis': 'Platform: Researcher Workbench',
    '6. recommendations': 'Recommendations: responsible AI',
    'committee-sourced': 'Committee-sourced (All of Us program papers, 2026)',
}
def clean_label(h):
    low = h.lower()
    for k, v in SECTION_LABELS.items():
        if low.startswith(k) or k in low:
            return v
    return re.sub(r'\s*[-:].*$', '', h).strip()

def render_references(path):
    """Clean, de-annotated reference list grouped by section: author/title/journal/year + DOI link."""
    skip = False
    for raw in open(path):
        s = raw.rstrip('\n').strip()
        if s.startswith('## ') or s.startswith('### '):
            head = re.sub(r'[*`]', '', s.lstrip('# ').strip())
            if head.lower().startswith('caveats'):
                skip = True; continue
            skip = False
            doc.add_heading(clean_label(head), 2)
            continue
        if skip or not s.startswith('- ['):
            continue
        m = re.match(r'- \[([^\]]+)\]\(([^)]+)\)(.*)', s)
        if not m:
            continue
        label, main_url, rest = m.group(1).strip(), m.group(2).strip(), m.group(3)
        dm = re.search(r'\*\*DOI:\*\*\s*\[([^\]]+)\]\(([^)]+)\)', rest)
        if dm:
            doi_text, doi_url = dm.group(1), dm.group(2)
        elif 'doi.org/' in main_url:
            doi_url = main_url; doi_text = main_url.split('doi.org/', 1)[1]
        else:
            doi_url = main_url; doi_text = None
        tag = ' [preprint]' if '[preprint]' in rest or 'preprint' in label.lower() else ''
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
        r = p.add_run(label.rstrip('.') + '.'); r.bold = True; r.font.size = Pt(10)
        if tag:
            tr = p.add_run(tag); tr.italic = True; tr.font.size = Pt(9)
        p.add_run('  ').font.size = Pt(10)
        add_hyperlink(p, doi_url, ('DOI: ' + doi_text) if doi_text else 'link')

emit('outline.md')
doc.add_page_break()
doc.add_heading('References', 0)
n = doc.add_paragraph()
rr = n.add_run('Verified reference list, grouped to match the sections above. Every entry resolves to the exact paper; DOIs resolved via NCBI E-utilities. Preprints are tagged and should be upgraded to their journal versions before submission. Spot-check each DOI on import.')
rr.italic = True; rr.font.size = Pt(9.5)
render_references('references-seed.md')

out = 'AoU_Roadmap_Refresh_Manuscript_Outline.docx'
doc.save(out)
print('wrote', out)
