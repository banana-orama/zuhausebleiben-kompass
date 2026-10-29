#!/bin/bash
# Zitat-Link-Rot-Audit: HTTP-Status jeder externen Quellen-URL (Final-URL nach Redirects)
cd /Users/mac/agentic-business/barrierefrei-leads
OUT=research/linkrot-291026-status.tsv
python3 - <<'PYEOF'
import json, html
data = json.load(open("research/linkrot-291026-urls.json"))
with open("research/linkrot-291026-checklist.txt", "w") as f:
    for item in data["urls"]:
        u = item["url"].replace("&amp;", "&")
        f.write(u + "\t" + ",".join(item["articles"]) + "\n")
print("checklist geschrieben")
PYEOF
cat research/linkrot-291026-checklist.txt | cut -f1 | while read -r u; do
  code=$(curl -sS -o /dev/null -w '%{http_code}\t%{url_effective}' -L --max-time 30 \
    --retry 1 --retry-delay 2 \
    -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' \
    -H 'Accept: text/html,application/xhtml+xml,application/pdf,*/*;q=0.8' \
    "$u" 2>/dev/null || printf 'ERR\tCURL_FAIL')
  printf '%s\t%s\n' "$code" "$u"
done > "$OUT" &
BGPID=$!
wait $BGPID
echo "=== FERTIG. Verteilung: ==="
cut -f1 "$OUT" | sort | uniq -c | sort -rn
echo "=== Nicht-200: ==="
awk -F'\t' '$1 != "200" {print}' "$OUT"
