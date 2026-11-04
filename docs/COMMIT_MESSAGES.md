# Commit message standards

Use [Conventional Commits 1.0.0][spec] for each commit in a PR.
PR titles do not need a prefix such as `docs:`, `fix:`, or `feat:`; use a
clear, descriptive title.

## Format

```text
type(scope)!: description

Optional body.

Optional footers.
```

Type, colon-space, and description are required; scope and ! are optional.
Types are nouns; scopes name codebase sections. Bodies allow multiple
paragraphs. Separate header, body, and footers with blank lines.

- `fix`: bug fix; PATCH.
- `feat`: feature; MINOR.
- Other types are allowed and imply no version bump without a breaking change.

## Breaking changes

Any type can mark a breaking change using ! immediately before the colon,
or an uppercase `BREAKING CHANGE: description` footer, or both.
`BREAKING-CHANGE:` is synonymous. With ! alone, describe the break in the
header. Breaking changes correspond to MAJOR.

```text
refactor(checks)!: require explicit file paths
```

A footer works without !:

```text
refactor(checks): remove the default file path

BREAKING CHANGE: callers must supply --file explicitly.
```

## Footers and case

Footer names use hyphens instead of spaces, except BREAKING CHANGE.
Use colon-space or space-# separators; values may span lines until the next
footer. Other fields accept any case; breaking-change tokens stay uppercase.

```text
Refs: #123
Reviewed-by: contributor
```

For reverts, prefer revert and reference commit SHAs.

## Project rules and verification

For substantial AI assistance, describe the contribution and actual
verification in the commit body, then add a trailer such as:

```text
AI-Assisted: Codex
```

The developer owns commits unless they authorize an agent to commit.
Our minimal commitlint configuration validates headers, including !. Human
review must check body/footer formatting, truthful verification, the chosen
type, and unmarked breaking changes. It does not require both breaking
markers or impose type lists, letter case, or length limits.

Release mappings explain the convention; they do not publish a release or
change package versions automatically. Maintainers handle releases.

[spec]: https://www.conventionalcommits.org/en/v1.0.0/
