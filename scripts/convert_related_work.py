#!/usr/bin/env python3
"""Convert related_work.md to LaTeX \\section{Related Work} for paper.tex.

Strategy:
1. Read related_work.md
2. Convert ## H.1 → \\subsection{}
3. Convert **bold** → \\textbf{}
4. Convert italics *text* → \\textit{}
5. Convert (Author, year) → \\citep{<bibkey>} ONLY when we have a verified
   BibTeX key in the per-paper slice. Otherwise leave as plain text.
6. Convert markdown bullets (- or *) → itemize/enumerate (when needed)
7. Insert at the right position in paper.tex (after Introduction, before Method)

Usage:
  python3 convert_related_work.py <paper_id>

The script reads:
  papers/drafts/<paper_id>/related_work.md
  papers/drafts/<paper_id>/paper.tex
  papers/drafts/<paper_id>/references.bib
And modifies paper.tex in-place by inserting a new \\section{Related Work}.
"""

import os
import re
import sys

REPO_ROOT = '/opt/data/work/satellite-paraguay'


def get_paper_keys(paper_id):
    """Read all BibTeX keys from the per-paper references.bib."""
    bib_path = os.path.join(REPO_ROOT, 'papers', 'drafts', paper_id, 'references.bib')
    with open(bib_path) as f:
        content = f.read()
    return set(re.findall(r'@\w+\{([^,\s]+)\s*,', content))


def build_author_year_to_key(content):
    """For each entry in the bib, extract (surname, year) → key mapping.

    Surname is the first author's family name (lowercase, first 6 chars).
    """
    mapping = {}
    for m in re.finditer(r'@\w+\{([^,\s]+)\s*,\s*\n(.*?)(?=\n@|\n%|\Z)', content, re.DOTALL):
        key = m.group(1)
        entry = m.group(2)
        # Get author field
        author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry)
        if not author_match:
            continue
        author_text = author_match.group(1)
        # First surname
        first_author = author_text.split(',')[0].strip()
        surname = first_author.lower().replace('{', '').replace('}', '')[:6]
        # Get year
        year_match = re.search(r'year\s*=\s*\{?(\d{4})', entry)
        if not year_match:
            continue
        year = year_match.group(1)
        mapping[(surname, year)] = key
    return mapping


def convert_prose_to_latex(text, key_map):
    """Convert markdown prose to LaTeX, substituting \\citep{} where applicable."""
    # Bold: **text** → \textbf{text}
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text, flags=re.DOTALL)
    # Italics: *text* → \textit{text}
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\textit{\1}', text, flags=re.DOTALL)
    # Code: `text` → \texttt{text}
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)

    # (Author, year) → \citep{key} when key exists
    def replace_cite(match):
        author = match.group(1).strip()
        year = match.group(2)
        # First surname = first word (it's the lead author; "et al." comes after)
        surname = author.split()[0]
        surname_clean = surname.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace('ß','ss')[:6]
        key = key_map.get((surname_clean, year))
        if key:
            return f'\\citep{{{key}}}'
        return match.group(0)  # leave as-is

    # Author and Author (year), Author et al. (year), Author (year)
    # Use DOTALL to allow line breaks within "et al." (e.g. "Hansen et\nal. (2013)")
    text = re.sub(
        r'([A-Z][\w\-\']+(?:\s+et\s+al\.)?(?:\s+and\s+[A-Z][\w\-\']+)?)\s*\((\d{4}[a-z]?)\)',
        replace_cite, text, flags=re.DOTALL
    )

    return text


def md_section_to_latex(section_lines):
    """Convert markdown body to LaTeX.

    Skips top-level H1 (# ...) — the caller wraps in \\section{...}.
    Converts H2 (## ...) → \\subsection, H3 (### ...) → \\subsubsection.
    Continuation lines after a bullet item stay INSIDE the itemize block.
    """
    out = []
    in_itemize = False

    def close_itemize():
        nonlocal in_itemize
        if in_itemize:
            out.append('\\end{itemize}')
            out.append('')
            in_itemize = False

    for line in section_lines:
        if line.startswith('### '):
            close_itemize()
            title = line[4:].strip()
            out.append(f'\\subsubsection{{{title}}}')
            out.append('')
        elif line.startswith('## '):
            close_itemize()
            title = line[3:].strip()
            # Strip R.X prefix
            title = re.sub(r'^R\.\d+\s+', '', title)
            out.append(f'\\subsection{{{title}}}')
            out.append('')
        elif line.startswith('# '):
            # Skip — caller wraps with \section{}
            continue
        elif line.startswith('- ') or line.startswith('* '):
            if not in_itemize:
                out.append('\\begin{itemize}')
                in_itemize = True
            out.append('  \\item ' + line[2:].rstrip())
        elif line.strip() == '':
            if in_itemize:
                out.append('')
            else:
                out.append('')
        else:
            # Regular text line: if inside itemize, this is item body;
            # if not, this is a paragraph. Either way, just emit it.
            out.append(line.rstrip())

    close_itemize()
    return '\n'.join(out)


def insert_related_work_section(paper_tex_path, latex_section):
    """Insert (or REPLACE) the \\section{Related Work} block in paper.tex.

    Strategy:
    1. If a \\section{Related Work} block already exists, REPLACE it.
    2. Else, insert before \\section{Methodology} (or \\section{Data}).
    3. Else, insert before \\bibliography{}.
    4. Else, append at end.
    """
    with open(paper_tex_path) as f:
        content = f.read()

    # 1. Try to REPLACE existing \section{Related Work} block.
    #    Use a function-style replacement so the LaTeX string is inserted as-is
    #    (re.sub treats backslashes specially in string replacement mode).
    pattern_replace = re.compile(
        r'\\section\{Related Work\}.*?(?=\\section\{|\\bibliography|\\end\{document\})',
        re.DOTALL
    )
    match = pattern_replace.search(content)
    if match:
        new_content = content[:match.start()] + latex_section + content[match.end():]
        with open(paper_tex_path, 'w') as f:
            f.write(new_content)
        return 'REPLACED existing Related Work block'

    # 2. Insert before \section{Methodology/Methods/Data}
    patterns = [
        r'\\section\{Methodology\}',
        r'\\section\{Methods?\}',
        r'\\section\{Data\}',
        r'\\section\{Materials\s+and\s+Methods\}',
    ]
    for pat in patterns:
        m = re.search(pat, content)
        if m:
            insert_pos = m.start()
            content = content[:insert_pos] + latex_section + '\n\n' + content[insert_pos:]
            with open(paper_tex_path, 'w') as f:
                f.write(content)
            return f'INSERTED before {pat}'

    # 3. Insert before \bibliography{}
    bib_match = re.search(r'\\bibliography', content)
    if bib_match:
        content = content[:bib_match.start()] + latex_section + '\n\n' + content[bib_match.start():]
        with open(paper_tex_path, 'w') as f:
            f.write(content)
        return 'INSERTED before bibliography'

    # 4. Append at end
    content = content.rstrip() + '\n\n' + latex_section
    with open(paper_tex_path, 'w') as f:
        f.write(content)
    return 'APPENDED at end'


def main():
    if len(sys.argv) < 2:
        print("Usage: convert_related_work.py <paper_id>")
        sys.exit(1)
    paper_id = sys.argv[1]

    md_path = os.path.join(REPO_ROOT, 'papers', 'drafts', paper_id, 'related_work.md')
    tex_path = os.path.join(REPO_ROOT, 'papers', 'drafts', paper_id, 'paper.tex')
    bib_path = os.path.join(REPO_ROOT, 'papers', 'drafts', paper_id, 'references.bib')

    with open(md_path) as f:
        md = f.read()
    with open(bib_path) as f:
        bib_content = f.read()

    print(f"\n{'='*60}")
    print(f"Paper: {paper_id}")
    print(f"MD: {md_path} ({len(md.splitlines())} lines, {len(md.split())} words)")

    # Build (surname, year) → key mapping from bib
    key_map = build_author_year_to_key(bib_content)
    print(f"Bib: {len(key_map)} (surname, year) → key mappings")

    # Convert prose citations in md to LaTeX with \citep{}.
    # Process the WHOLE md (DOTALL) so "Hansen et\nal. (2013)" matches across line breaks.
    converted_md = convert_prose_to_latex(md, key_map)

    # Track which citations got converted
    citations_resolved = re.findall(r'\\citep\{([^}]+)\}', converted_md)
    citations_unresolved = []
    # Find all (Author, year) that did NOT become \citep{}
    for m in re.finditer(
        r'([A-Z][\w\-\']+(?:\s+et\s+al\.)?(?:\s+and\s+[A-Z][\w\-\']+)?)\s*\((\d{4}[a-z]?)\)',
        converted_md
    ):
        author = m.group(1).strip()
        year = m.group(2)
        surname = author.split()[0].lower()[:6]
        if (surname, year) not in key_map:
            citations_unresolved.append((author, year))

    # Convert markdown structure to LaTeX
    latex_section = md_section_to_latex(converted_md.split('\n'))

    # Wrap in \section{Related Work}
    full_section = f"""% --- Related Work section (auto-generated from related_work.md) ---
\\section{{Related Work}}
{latex_section}
% --- end Related Work ---
"""

    # Insert into paper.tex
    inserted = insert_related_work_section(tex_path, full_section)

    print(f"\n  Inserted into paper.tex: {inserted}")
    print(f"  Citations resolved to \\citep{{}}: {len(citations_resolved)}")
    if citations_resolved:
        print(f"    Keys: {sorted(set(citations_resolved))}")
    print(f"  Citations left as prose (no bib key): {len(citations_unresolved)}")
    if citations_unresolved:
        unique = sorted(set(citations_unresolved))
        print(f"    First 10: {unique[:10]}")
    print(f"  New LaTeX section length: {len(full_section.splitlines())} lines")

    return 0


if __name__ == '__main__':
    sys.exit(main())
