#!/bin/bash
# Region-Screen 271126 MV — Runde 2: LFI via Wayback (Host curl-blockiert; Browser-Daemon down)
set -u
MV="research/evidence/region-screen-271126/mv"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

fetch() {
  code=$(curl -sL -A "$UA" -o "$2/$3.tmp" -w "%{http_code}" --max-time 120 "$1" || echo "000")
  if [ "$code" = "200" ]; then mv "$2/$3.tmp" "$2/$3"; fi
  size=$(wc -c < "$2/$3" 2>/dev/null | tr -d ' ' || echo 0)
  echo "$3  HTTP $code  ${size}B"
}

# LFI-Produktseite (Snapshot 09.11.2026, id_ = Original-Bytes)
fetch "https://web.archive.org/web/20261109030126id_/https://www.lfi-mv.de/foerderfinder/personenaufzuege-und-lifte-barrierearmes-wohnen/" "$MV" "lfi-barrierearmes-wohnen.html"
# Richtlinie-Lesefassung inkl. Aenderungserlasse (Snapshot 08.11.2026)
fetch "https://web.archive.org/web/20261108122841id_/https://www.lfi-mv.de/export/sites/lfi/.galleries/personenaufzuege-und-lifte-barrierearmes-wohnen/lesefassung-richtlinie-inkl-aenderungserlasse.pdf" "$MV" "lfi-rl-lesefassung.pdf"
# Merkblatt (Snapshot 08.11.2026)
fetch "https://web.archive.org/web/20261108122841id_/https://www.lfi-mv.de/export/sites/lfi/.galleries/personenaufzuege-und-lifte-barrierearmes-wohnen/merkblatt-personenaufzuege-lifte-barrierearmes-wohnen.pdf" "$MV" "lfi-merkblatt.pdf"

file "$MV/lfi-rl-lesefassung.pdf" "$MV/lfi-merkblatt.pdf" 2>/dev/null
echo "--- Runden-Check Treppenlift im LFI-HTML:"
grep -c -i "treppenlift" "$MV/lfi-barrierearmes-wohnen.html" || true
echo "--- Ministerium-PM + Wohnraumfoerderung: Wayback-Snapshots vorhanden?"
curl -sL --max-time 30 "https://archive.org/wayback/available?url=regierung-mv.de/Landesregierung/im/Aktuell%3Fid%3D219369" | head -c 500; echo
curl -sL --max-time 30 "https://archive.org/wayback/available?url=regierung-mv.de/Landesregierung/im/Bau/wohnen/wohnraumf%C3%B6rderung" | head -c 500; echo
