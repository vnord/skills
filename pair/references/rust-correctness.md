# Rust review guidance for pairing code

Guidance for the tests, the standard solutions, and reviewing the user's code; not a checklist to recite. Raise the findings that matter to the current step.

## Semantics before style

Establish the invariant the change must preserve: exact representations, units, ordering, ownership, state transitions, or error behavior. Inspect how inputs are decoded and how outputs are consumed. Check nested and repeated cases, empty and malformed data, unknown values, integer widths and overflow, partial I/O, and whether a caller depends on the old behavior.

## Tests

Choose tests that distinguish a correct implementation from the old one and from plausible wrong implementations. Use independent fixtures when a round trip could hide a matching reader and writer bug. Compare structural meaning rather than incidental sizes. Exercise new validation and error branches as well as the happy path. When a legitimate test assumption changes, replace it with a stronger behavior-level check rather than weakening it.

## Solutions

- Prefer existing types, helpers, error conventions, and standard library facilities. Do not add an abstraction to demonstrate a Rust feature. Use the least code that fully preserves the required behavior.
- Reuse domain enums; do not treat an enum as bit flags unless the format says so.
- Keep borrows narrow. Scope a writer holding an exclusive borrow; collect owned metadata when a live iterator would block the next mutation. Do not clone large buffers just to silence the borrow checker; when an owned copy is justified, say why.
- Use `From`/`TryFrom` when they describe the conversion. Validate length, range, alignment, and byte order at input boundaries. A cast or invariant-based `expect` needs a reason established by the surrounding code.
- Use `Result` and the crate's error types for malformed data and I/O failures. `unwrap`/`expect` belongs in test setup or on an invariant the API proves. Do not turn malformed input into panics or silently discard meaningful data.
- Preserve validation, errors, and resource finalization when extracting helpers.
- Use private or `pub(crate)` visibility unless external callers need the API. Add only required generics, bounds, lifetimes, and dependencies.
- Do not disable a useful lint to accommodate an example.

## Validation claims

Inspect warnings rather than allowing them. Green checks do not establish correctness for untested invariants, unsafe code, concurrency, external formats, or interoperability; state those limits.
