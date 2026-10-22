#!/usr/bin/env python3
"""Build a Rust tutorial as Markdown and offline HTML using Python's standard library.

This is a small renderer for the Markdown subset used by this document, not a
general Markdown implementation. It never runs Rust, applies patches, or uses Git.
"""

from html import escape
from pathlib import Path
import json
import re
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent


def inline(text):
    pattern = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)]+)\)")
    result, offset = [], 0
    for match in pattern.finditer(text):
        result.append(escape(text[offset:match.start()]))
        if match.group(1) is not None:
            result.append('<code>' + escape(match.group(1)) + '</code>')
        elif match.group(2) is not None:
            result.append('<strong>' + inline(match.group(2)) + '</strong>')
        else:
            result.append('<a href="' + escape(match.group(4), quote=True) + '">' + inline(match.group(3)) + '</a>')
        offset = match.end()
    result.append(escape(text[offset:]))
    return ''.join(result)


def slug(text):
    ascii_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', ascii_text.lower()).strip('-')


def highlight(code, language):
    if language != 'rust':
        return escape(code)
    token = re.compile(r'//[^\n]*|r"[^"]*"|"(?:\\.|[^"\\])*"|\b(?:pub|crate|fn|let|mut|if|else|match|return|impl|for|in|use|mod|struct|static|const|type|as|true|false|where|trait)\b|\b(?:Result|Vec|String|Option|Some|None|Ok|Err|Self|Path|Cursor|PathBuf|Arc|Mutex|Box|Read|Seek|Write|RefCell|Once)\b|\b(?:0x[0-9a-fA-F_]+|\d[\d_]*(?:_u\d+)?)\b')
    parts, offset = [], 0
    for match in token.finditer(code):
        parts.append(escape(code[offset:match.start()]))
        value = match.group()
        kind = 'comment' if value.startswith('//') else 'string' if '"' in value else 'number' if value[0].isdigit() else 'type' if value[0].isupper() else 'keyword'
        parts.append('<span class="tok-' + kind + '">' + escape(value) + '</span>')
        offset = match.end()
    parts.append(escape(code[offset:]))
    return ''.join(parts)


def render(markdown):
    lines = markdown.splitlines()
    result, toc = [], []
    heading_ids = set()
    i, code_number, checkbox_number, figure_number = 0, 0, 0, 0
    while i < len(lines):
        text = lines[i]
        if not text.strip():
            i += 1
            continue
        if text.startswith('```'):
            language = text[3:].strip() or 'text'
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError('Unclosed code fence')
            code_number += 1
            highlighted = '\n'.join('<span class="code-line">' + highlight(line, language) + '</span>' for line in block)
            code_id = f'code-{code_number}'
            result.append(f'<div class="code-block"><div class="code-toolbar"><span>{escape(language.upper())}</span><button type="button" class="copy" data-code="{code_id}" aria-label="Copy code block {code_number}">Copy code</button></div><pre><code id="{code_id}">{highlighted}</code></pre></div>')
            i += 1
            continue
        image = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', text)
        if image:
            asset = ROOT / image.group(2)
            ET.parse(asset)
            svg = asset.read_text()
            figure_number += 1
            prefix = f"figure-{figure_number}"
            svg = svg.replace('aria-labelledby="title desc"', f'aria-labelledby="{prefix}-title {prefix}-desc"')
            for old in ('title', 'desc', 'arrow'):
                svg = svg.replace(f'id="{old}"', f'id="{prefix}-{old}"').replace(f'url(#{old})', f'url(#{prefix}-{old})')
            result.append('<figure><div class="diagram">' + svg + '</div><figcaption>' + inline(image.group(1)) + '</figcaption></figure>')
            i += 1
            continue
        heading = re.fullmatch(r'(#{1,4})\s+(.+)', text)
        if heading:
            level, title = len(heading.group(1)), heading.group(2)
            ident = slug(title)
            base, suffix = ident, 2
            while ident in heading_ids:
                ident = f'{base}-{suffix}'
                suffix += 1
            heading_ids.add(ident)
            result.append(f'<h{level} id="{ident}">' + inline(title) + f'</h{level}>')
            if level == 2:
                toc.append((ident, title))
            i += 1
            continue
        if text.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [cell.strip() for cell in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', cell) for cell in cells):
                    rows.append(cells)
                i += 1
            head = '<thead><tr>' + ''.join('<th scope="col">' + inline(cell) + '</th>' for cell in rows[0]) + '</tr></thead>'
            body = '<tbody>' + ''.join('<tr>' + ''.join('<td>' + inline(cell) + '</td>' for cell in row) + '</tr>' for row in rows[1:]) + '</tbody>'
            result.append('<div class="table-wrap"><table>' + head + body + '</table></div>')
            continue
        if text.startswith('> '):
            quote = []
            while i < len(lines) and lines[i].startswith('> '):
                quote.append(lines[i][2:])
                i += 1
            result.append('<aside class="callout">' + inline(' '.join(quote)) + '</aside>')
            continue
        if re.match(r'(?:- |\d+\. )', text):
            ordered = bool(re.match(r'\d+\. ', text))
            tag = 'ol' if ordered else 'ul'
            items = []
            while i < len(lines) and re.match(r'(?:- |\d+\. )', lines[i]):
                value = re.sub(r'^(?:- |\d+\. )', '', lines[i])
                if value.startswith('[ ] '):
                    checkbox_number += 1
                    items.append(f'<li class="checkpoint"><label><input type="checkbox" data-checkpoint="checkpoint-{checkbox_number}"><span>' + inline(value[4:]) + '</span></label></li>')
                else:
                    items.append('<li>' + inline(value) + '</li>')
                i += 1
            result.append('<' + tag + '>' + ''.join(items) + '</' + tag + '>')
            continue
        paragraph = [text]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(?:#{1,4} |```|!\[|\||> |- |\d+\. )', lines[i]):
            paragraph.append(lines[i])
            i += 1
        result.append('<p>' + inline(' '.join(paragraph)) + '</p>')
    return '\n'.join(result), toc, code_number, checkbox_number


def build():
    source = (ROOT / 'tutorial.source.md').read_text()

    def include(match):
        name = match.group(1)
        code = (ROOT / 'snippets' / (name + '.rs.txt')).read_text().rstrip()
        return '```rust\n' + code + '\n```'

    markdown = re.sub(r'^\{\{snippet:([a-z0-9-]+)\}\}$', include, source, flags=re.MULTILINE)
    (ROOT / 'tutorial.md').write_text(markdown)
    article, toc, code_count, checks = render(markdown)
    config = json.loads((ROOT / 'tutorial.json').read_text())
    nav = ['<a href="#' + ident + '">' + escape(title) + '</a>' for ident, title in toc]
    template = (ROOT / 'template.html').read_text()
    baseline = str(config.get('baseline', ''))
    replacements = {
        'STYLE': (ROOT / 'style.css').read_text(),
        'SCRIPT': (ROOT / 'tutorial.js').read_text(),
        'NAV': '\n'.join(nav),
        'ARTICLE': article,
        'CHECKS': str(checks),
        'TITLE': escape(str(config['title'])),
        'PROJECT': escape(str(config['project'])),
        'DESCRIPTION': escape(str(config['description']), quote=True),
        'ID': escape(str(config['id']), quote=True),
        'BASELINE_LABEL': escape(f'Baseline: {baseline}' if baseline else 'Rust implementation tutorial'),
    }
    # Substitute only the template once. Code containing template-like text is literal.
    template = re.sub(r'\{\{([A-Z_]+)\}\}', lambda match: replacements[match.group(1)], template)
    (ROOT / 'index.html').write_text(template)
    print(f'Built {ROOT / "index.html"}')
    print(f'Expanded Markdown: {ROOT / "tutorial.md"}')
    print(f'{len(toc)} chapters · {code_count} code blocks · {checks} checkpoints')


if __name__ == '__main__':
    build()
