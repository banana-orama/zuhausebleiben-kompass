#!/bin/bash
# Region-Screen 271126 — Runde 3: PSP/EGH/PM-Belege MV+RP
set -u
MV="research/evidence/region-screen-271126/mv"
RP="research/evidence/region-screen-271126/rheinland-pfalz"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

fetch() {
  code=$(curl -sL -A "$UA" -o "$2/$3.tmp" -w "%{http_code}" --max-time 60 "$1" || echo "000")
  if [ "$code" = "200" ]; then mv "$2/$3.tmp" "$2/$3"; fi
  size=$(wc -c < "$2/$3" 2>/dev/null | tr -d ' ' || echo 0)
  echo "$3  HTTP $code  ${size}B"
}

# === MV: offizielle PMs via Presseportal (ots-Distribution IM-MV) ===
fetch "https://www.presseportal.de/blaulicht/pm/108531/6257916" "$MV" "mv-pm-183-2026-presseportal.html"
fetch "https://www.presseportal.de/blaulicht/pm/108531/6331780" "$MV" "mv-pm-aufstockung-1208-2026-presseportal.html"
# MV PSP: gemeinsamer Träger-Portal + Ministerium via Wayback
fetch "https://psp-mv.de/" "$MV" "mv-psp.html"
curl -sL --max-time 30 "https://archive.org/wayback/available?url=regierung-mv.de/Landesregierung/sm/Soziales/Pflege/Pflegest%C3%BCtzpunkte" | head -c 400; echo " <- PSP-ministerium wayback"
curl -sL --max-time 30 "https://archive.org/wayback/available?url=regierung-mv.de/Landesregierung/sm/Soziales/Eingliederungshilfe" | head -c 400; echo " <- EGH-ministerium wayback"
curl -sL --max-time 30 "https://archive.org/wayback/available?url=regierung-mv.de/Landesregierung/sm/Soziales" | head -c 400; echo " <- sm-Soziales wayback"

# === RP: LSJV (Landesamt) PSP + EGH ===
fetch "https://lsjv.rlp.de/themen/pflege/menschen-mit-pflegebedarf/pflegestuetzpunkte" "$RP" "rp-lsjv-pflegestuetzpunkte.html"
fetch "https://lsjv.rlp.de/themen/inklusion/eingliederungshilfe" "$RP" "rp-lsjv-egh.html"
fetch "https://service.rlp.de/detail?pstId=13702216" "$RP" "rp-serviceportal-psp.html"
