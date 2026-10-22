# Authoring and building a Rust tutorial

## Files

The initializer copies page assets and writes `tutorial.json`. Author:

- `tutorial.source.md`: prose and exact edit instructions.
- `snippets/<name>.rs.txt`: validated Rust, kept outside Cargo's target discovery.
- `assets/*.svg`: diagrams for this implementation.
- Optional `steps/*.patch` and `validation/`: complete stage diffs and actual check results when they help the reader.

Run `python3 <output>/build.py` to create expanded `tutorial.md` and standalone `index.html` with CSS, JavaScript, and SVGs embedded. Configuration supplies title, project, description, baseline, date, and a browser-storage namespace. Rebuilding does not execute examples.

Include Rust on its own line:

```text
{{snippet:regression-test}}
```

This loads `snippets/regression-test.rs.txt`. Use ordinary fenced `bash` blocks for shell commands and Markdown images for SVGs:

```markdown
![Which fields survive the header conversion.](assets/header-conversion.svg)
```

The renderer supports headings, paragraphs, single-level lists/checklists, blockquotes, simple tables, links, inline code, fenced code, and SVG figures. It does not support raw HTML, nested Markdown lists, or complex inline Markdown. Avoid literal pipes in table cells; explain Rust or-patterns outside tables. The expanded Markdown can go through another compiler instead.

## Content and explanations

Start with the current baseline and remaining commits, then the domain representation needed to understand the edits. Cover each commit's motivation, changes, interesting Rust lines, and verification. End with results and actual limits. Add a glossary only when recurring unfamiliar concepts warrant it. Do not impose a chapter count or reproduce a TDD primer; this reader knows the workflow.

Explain what changes decisions or prevents mistakes:

- Which value owns data, which operation borrows it, and where that borrow ends.
- Why a read may need `&mut self`, why a writer's scope matters, and why a collected iterator can unblock mutation.
- What trait bounds, lifetimes, and visibility allow here; do not add abstraction to create a lesson.
- How patterns, guards, `Option`, and `Result` represent this behavior, including a valid absence versus corrupt input.
- What conversions do to width, signedness, byte order, and ownership, and what makes them safe here.
- Why `?` propagates an error, a test `unwrap` signals bad setup, and a specific expected message isolates the regression.
- What iterator items become and why materialization or flattening is needed.

Explain a construct when it becomes relevant, then refer back. Do not repeatedly narrate `.unwrap()` or semicolons. A larger fixture can deserve more explanation than a small fix if it prevents false confidence in that fix.

## Synchronize code with prose

Validate complete stage changes in the isolated copy and export actual snippets/diffs. Recheck code changed during editing or formatting. Follow the plan's test/fix sequence; enable behavior only after its regression is present. Each independent expected failure needs its own test, not a loop hidden behind the first panic. Check assertions that become reachable only after the fix.

Record the starting revision, commands, passed/failed/ignored results, and synthetic versus real input coverage. Never copy previous validation counts into a new tutorial. Keep code execution, browser preview, performance, and external interoperability claims separate. Link primary sources near format/API claims.

## Presentation

Use readable type, sufficient contrast, restrained color, accurate line numbering, and accessible SVG captions. Keep narrow-screen code and tables scrollable, and printed code legible. Titles and navigation describe the topic and steps. There is no slogan area or invented visual brand.

Run `python3 <skill-directory>/scripts/check_tutorial.py <output>` for include expansion, unique IDs, local links, exact code after HTML decoding, and local runtime assets. This does not prove Rust correctness or browser layout. If a browser is available, inspect desktop/mobile layouts and copy, navigation, theme, checkpoint, and print behavior. If not, report that limit. Do not install a browser or publish a document solely for optional preview.
