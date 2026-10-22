#!/usr/bin/env python3
"""Create document files without editing Rust, applying patches, or using Git."""

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--title', required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--description', required=True)
    parser.add_argument('--baseline', default='')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error('Output must be a new or empty directory; existing files are not overwritten.')
    if not all(value.strip() for value in (args.title, args.project, args.description)):
        parser.error('Title, project, and description must not be blank.')
    assets = Path(__file__).resolve().parents[1] / 'assets/tutorial-site'
    output.mkdir(parents=True, exist_ok=True)
    for name in ('build.py', 'template.html', 'style.css', 'tutorial.js'):
        shutil.copy2(assets / name, output / name)
    for name in ('snippets', 'assets'):
        (output / name).mkdir()
    identity = '\0'.join((args.project, args.title, args.baseline))
    config = {
        'title': args.title, 'project': args.project, 'description': args.description,
        'baseline': args.baseline, 'date': date.today().isoformat(),
        'id': hashlib.sha256(identity.encode()).hexdigest()[:16],
    }
    (output / 'tutorial.json').write_text(json.dumps(config, indent=2) + '\n')
    source = f'# {args.title}\n\n{args.description}\n'
    if args.baseline:
        source += f'\n## Starting revision\n\n`{args.baseline}`\n'
    (output / 'tutorial.source.md').write_text(source)
    print(f'Created document files in {output}')
    print('Write the tutorial, validated snippets, and diagrams before delivery.')
    print(f'Rebuild with: python3 {output / "build.py"}')


if __name__ == '__main__':
    main()
