#!/usr/bin/env bash
# Evals for the publish skill's verification script (hack/verify-publish.sh).
#
# Builds minimal public/ fixtures in temp dirs and asserts pass/fail behavior:
#   eval 1  all assets and links present          -> exit 0, "VERIFY: OK"
#   eval 2  one static/img asset missing          -> exit 1, "MISSING asset"
#   eval 3  one internal link target missing      -> exit 1, "MISSING link"
#   eval 4  page file itself missing              -> exit 1, "page not found"
#   eval 5  external URLs must NOT be checked     -> exit 0 even when unreachable
#
# Run from anywhere:  bash .agents/skills/publish/evals/run-evals.sh

set -u

ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
VERIFY="$ROOT/hack/verify-publish.sh"
[ -f "$VERIFY" ] || { echo "FATAL: $VERIFY not found"; exit 2; }

PAGE='public/2026/10/demo/index.html'
passed=0
failed=0

make_fixture() {
  local d
  d="$(mktemp -d)"
  mkdir -p "$d/public/2026/10/demo" "$d/public/img/202610" "$d/public/2026/01/old"
  cat > "$d/$PAGE" <<'HTML'
<img src="https://en.blog.alswl.com/img/202610/a.png" alt="a">
<img src="/img/202610/a.png" alt="b">
<a href="https://en.blog.alswl.com/2026/01/old/">prev</a>
<a href="/2026/10/demo/#section">self</a>
<a href="https://github.com/alswl/guides">external</a>
HTML
  : > "$d/public/img/202610/a.png"
  : > "$d/public/2026/01/old/index.html"
  echo "$d"
}

# expect_ok <name> <dir>
expect_ok() {
  if (cd "$2" && bash "$VERIFY" "$PAGE" >/dev/null 2>&1); then
    echo "PASS $1"; passed=$((passed + 1))
  else
    echo "FAIL $1 (expected exit 0)"; failed=$((failed + 1))
  fi
}

# expect_fail <name> <dir> <grep pattern in output>
expect_fail() {
  local out
  out="$(cd "$2" && bash "$VERIFY" "$PAGE" 2>&1)"
  local rc=$?
  if [ "$rc" -ne 0 ] && echo "$out" | grep -q "$3"; then
    echo "PASS $1"; passed=$((passed + 1))
  else
    echo "FAIL $1 (rc=$rc, expected non-zero + '$3'); output: $out"
    failed=$((failed + 1))
  fi
}

# eval 1: happy path
d="$(make_fixture)"; expect_ok "eval1-happy-path" "$d"; rm -rf "$d"

# eval 2: missing image in static/img copy
d="$(make_fixture)"; rm "$d/public/img/202610/a.png"; expect_fail "eval2-missing-asset" "$d" "MISSING asset"; rm -rf "$d"

# eval 3: missing internal link target
d="$(make_fixture)"; rm "$d/public/2026/01/old/index.html"; expect_fail "eval3-missing-link" "$d" "MISSING link"; rm -rf "$d"

# eval 4: page itself missing
d="$(make_fixture)"
if (cd "$d" && bash "$VERIFY" public/2026/10/nope/index.html >/dev/null 2>&1); then
  echo "FAIL eval4-missing-page (expected exit 1)"; failed=$((failed + 1))
else
  echo "PASS eval4-missing-page"; passed=$((passed + 1))
fi
rm -rf "$d"

# eval 5: external URL unreachable must be ignored
d="$(make_fixture)"
sed -i '' 's#https://github.com/alswl/guides#https://unreachable.invalid/nope#' "$d/$PAGE" 2>/dev/null \
  || sed -i 's#https://github.com/alswl/guides#https://unreachable.invalid/nope#' "$d/$PAGE"
expect_ok "eval5-external-ignored" "$d"; rm -rf "$d"

echo "----"
echo "evals: $passed passed, $failed failed"
[ "$failed" -eq 0 ]
