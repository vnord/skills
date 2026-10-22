#!/usr/bin/env python3
"""Check document structure and code fidelity; does not execute Rust or a browser."""

import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlparse


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.code, self.remote = [], [], [], []
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'code' and attrs.get('id', '').startswith('code-'):
            self.current = ''
        if tag in ('script', 'link', 'img', 'iframe', 'image', 'use'):
            for key in ('src', 'href', 'xlink:href'):
                if urlparse(attrs.get(key, '')).scheme in ('http', 'https'):
                    self.remote.append(attrs[key])

    def handle_data(self, data):
        if self.current is not None:
            self.current += data

    def handle_endtag(self, tag):
        if tag == 'code' and self.current is not None:
            self.code.append(self.current)
            self.current = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    root = args.output.expanduser().resolve()
    document = Document()
    document.feed((root / 'index.html').read_text())
    errors = []
    duplicates = [value for value, count in Counter(document.ids).items() if count > 1]
    if duplicates:
        errors.append(f'Duplicate IDs: {duplicates}')
    for link in document.links:
        parsed = urlparse(link)
        if parsed.scheme:
            continue
        if parsed.path and not (root / unquote(parsed.path)).exists():
            errors.append(f'Missing local link: {link}')
        elif not parsed.path and parsed.fragment and unquote(parsed.fragment) not in document.ids:
            errors.append(f'Missing anchor: {link}')
    markdown = (root / 'tutorial.md').read_text()
    blocks = re.findall(r'^```[^\n]*\n(.*?)^```\s*$', markdown, re.M | re.S)
    if [block.rstrip('\n') for block in blocks] != document.code:
        errors.append('Rendered/copyable code differs from the expanded Markdown.')
    if re.search(r'^\{\{snippet:', markdown, re.M):
        errors.append('Unexpanded snippet include.')
    if document.remote:
        errors.append(f'Remote runtime assets: {document.remote}')
    if errors:
        parser.exit(1, '\n'.join(errors) + '\n')
    print(f'Passed: {len(document.ids)} unique IDs, local links/anchors, {len(blocks)} faithful code blocks, and local runtime assets.')
    print('Rust correctness, executed test results, and browser appearance require their own checks.')


if __name__ == '__main__':
    main()
