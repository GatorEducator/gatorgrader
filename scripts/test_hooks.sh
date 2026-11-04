#!/usr/bin/env bash
# exercise the installed hooks in an isolated checkout, never this clone
set -euo pipefail
source_root=$(git rev-parse --show-toplevel)
test_root=$(mktemp -d)
trap 'rm -rf -- "$test_root"' EXIT
git -C "$source_root" checkout-index --all --prefix="$test_root/"
cd "$test_root"
unset VIRTUAL_ENV
git init -q
git config user.name 'Hook tests'
git config user.email 'hook-tests@example.invalid'
git config commit.gpgsign false
git add .
git commit -qm 'test: prepare hook fixture'
uv sync --locked
uv run task hooks-install
log_file="$test_root/.git/hook-test.log"

commit_passes() {
  if ! git commit --allow-empty -qm "$1" >"$log_file" 2>&1; then
    cat "$log_file"
    exit 1
  fi
}

commit_fails() {
  before=$(git rev-parse HEAD)
  if git commit --allow-empty -qm "$1" >"$log_file" 2>&1; then
    echo 'FAIL: a prohibited commit succeeded'
    exit 1
  fi
  test "$(git rev-parse HEAD)" = "$before"
  grep -Fq "$2" "$log_file" || { cat "$log_file"; exit 1; }
}

commit_fails 'fix typo' 'Conventional commit message'
commit_passes 'docs: accept a valid header'
commit_passes 'refactor!: describe a breaking change'
commit_passes $'refactor: describe a breaking change\n\nBREAKING CHANGE: supply an explicit file.'
echo 'PASS: malformed commit blocked; valid and breaking headers accepted'

printf '\nuv run task nonexistent-hook-test-task\n' >> CONTRIBUTING.md
git add CONTRIBUTING.md
# hide the staged error with clean working content to test staged-file checks
git show HEAD:CONTRIBUTING.md > CONTRIBUTING.md
commit_fails 'docs: test staged guide' 'Contributor commands'
git restore --source=HEAD --staged --worktree -- CONTRIBUTING.md
commit_passes 'docs: accept the corrected guide'
echo 'PASS: bad staged task blocked; corrected guide accepted'

mkdir -p docs
printf '# Hook smoke test\nMissing blank line.\n' > docs/hook-smoke.md
git add docs/hook-smoke.md
commit_fails 'docs: test Markdown' 'Markdown'
printf '# Hook smoke test\n\nA valid documentation change.\n' > docs/hook-smoke.md
git add docs/hook-smoke.md
commit_passes 'docs: accept valid Markdown'
echo 'PASS: malformed Markdown blocked; corrected Markdown accepted'

sed 's/^branch = true$/branch = false/' pyproject.toml > .git/changed.toml
mv .git/changed.toml pyproject.toml
git add pyproject.toml
commit_fails 'test: protect branch coverage' 'Contributor commands'
git restore --source=HEAD --staged --worktree -- pyproject.toml
commit_passes 'test: accept restored coverage settings'
echo 'PASS: disabled branch coverage blocked; restored settings accepted'


printf 'def broken(:\n' > tests/test_hook_smoke.py
git add tests/test_hook_smoke.py
commit_fails 'test: reject invalid Python' 'Existing project lint and tests'
git restore --staged -- tests/test_hook_smoke.py
rm -- tests/test_hook_smoke.py
commit_passes 'test: accept corrected Python'
echo 'PASS: invalid Python blocked; corrected checkout accepted'
