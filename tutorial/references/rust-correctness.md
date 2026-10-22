# Review the Rust examples

This is author guidance, not a required tutorial chapter. Read the relevant code and callers before writing or validating snippets. Explain the findings that matter to the change, not a generic Rust checklist to the learner.

## Semantics before style

Establish the invariant the change must preserve: exact representations, units, ordering, ownership, state transitions, or error behavior. Inspect how inputs are decoded and how outputs are consumed. Check nested and repeated cases, empty and malformed data, unknown values, integer widths and overflow, partial I/O, and whether a caller depends on the old behavior.

Choose tests that can distinguish a correct implementation from the old one and plausible wrong implementations. Use independent fixtures when a round trip could conceal a shared mistake. Compare structural meaning rather than incidental allocation size when appropriate. Exercise new validation/error branches as well as the happy path. Keep compatibility controls that the plan calls for.

## Idioms that affect these tutorials

- Reuse domain enums and types when they already exist; do not treat an enum value as bit flags unless the format specifies that. Do not add a new abstraction just to avoid every numeric constant.
- Keep borrows narrow. Scope a writer that holds an exclusive borrow; collect owned metadata when a live iterator would prevent the next mutation. Do not clone large buffers only to silence the borrow checker without understanding the ownership boundary.
- Use `From`/`TryFrom` when they describe the conversion. Validate length, range, alignment, and byte order before interpreting input. A representation-specific cast can be appropriate, but document its established invariant rather than presenting truncation as universally safe.
- Use `Result` and the crate's error types for malformed data or I/O failures. `unwrap`/`expect` belongs in deterministic test setup or on an internal invariant proven by the API. A panic based on an unchecked external assumption is not such an invariant.
- Preserve validation, errors, and resource finalization when extracting helpers. Do not suppress useful diagnostics for malformed ordinary inputs while accommodating a legitimate absence case.
- Prefer standard iterator and slice operations when they clarify intent. An expression that saves two lines at the cost of hiding widths, offsets, or ownership is not the better teaching example.
- Use private or `pub(crate)` helpers when external callers do not need an API. Add only required generics, trait bounds, lifetimes, and dependencies. Follow the repository's formatting and conventions.

## Validation claims

Run `cargo fmt`, relevant tests, and the repository's Clippy command after meaningful changes. Validate each stage, not only the final implementation. Run the full required checks where feasible; distinguish unavailable datasets and integration environments from passing checks.

Inspect warnings rather than automatically allowing them. Green checks do not establish correctness for untested invariants, unsafe code, concurrency, external formats, or interoperability. State those limits and use additional targeted checks when the proposed change makes them material.
