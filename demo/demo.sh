#!/usr/bin/env bash
# Real audit.py run on a sample ban-bloated CLAUDE.md, then an illustrative /rethink pass
# (the skills themselves run inside Claude Code; audit.py is the real, stdlib-only meter).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AUDIT="$ROOT/skills/rethink/audit.py"
SBX="$(mktemp -d)"; trap 'rm -rf "$SBX"' EXIT
say(){ printf '\033[1;36m$ %s\033[0m\n' "$1"; sleep .5; }
p(){ printf '%b\n' "$1"; sleep "${2:-.5}"; }

cat > "$SBX/CLAUDE.md" <<'P'
- Never edit config files without asking.
- Don't touch the production database.
- Never commit without running the tests first.
- Do not modify the config schema.
- Never push directly to main.
- Don't change environment variables in prod.
- Avoid editing config without confirmation.
- Never delete migration files.
- Do not refactor config during a feature task.
- Never hardcode secrets in config.
- Don't edit the config loader.
- Must not skip the config review step.
- Never overwrite the config defaults.
- Do not auto-format the config file.
P
echo; printf '\033[1mDon'\''t add another "never do that" rule. Fix the cause.\033[0m\n'; sleep 1.1; echo
say 'python3 audit.py CLAUDE.md     # how feverish is the rulebook?'
python3 "$AUDIT" "$SBX/CLAUDE.md" 2>&1 | head -10
sleep 1.2
p '\033[2m/rethink — instead of adding ban #15:\033[0m'
p '  symptom:    edited the wrong config file again'
p '  root cause: there is no "confirm the target before editing" step'
p '  \033[32m→ positive gate:\033[0m "Before editing, name the file & why, confirm it matches the target."'
p '  one gate kills the whole family — not just this one file.' 1.6
echo
printf '\033[2millustrative — /rethink & /deusex run inside Claude Code; audit.py above is real.\033[0m\n'; sleep 2
