#!/usr/bin/env bash
# CI-Wait für Prüflauf 16.11.2026 — wartet bis alle Runs des Commits completed sind.
# Lesson 09.11.: gh liefert status lowercase → Vergleich case-insensitive via tr.
set -u
cd /Users/mac/agentic-business/barrierefrei-leads
SHA=$(git rev-parse HEAD)
echo "Warte auf CI für $SHA"
for i in $(seq 1 40); do
  sleep 15
  R=$(gh run list --commit "$SHA" --json status,conclusion,databaseId --limit 5 2>/dev/null)
  [ -z "$R" ] && continue
  [ "$R" = "[]" ] && continue
  PENDING=$(echo "$R" | python3 scripts/_ci_pending.py)
  if [ "$PENDING" = "0" ]; then
    echo "$R" | python3 scripts/_ci_print.py
    exit 0
  fi
done
echo "TIMEOUT nach 10min — letzter Stand: $R"
exit 1
