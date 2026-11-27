#!/bin/bash
# Region-Screen 271126 MV+RP — Runde 1 (nur erreichbare Quellen; LFI via Browser nachgezogen)
set -u
MV="research/evidence/region-screen-271126/mv"
RP="research/evidence/region-screen-271126/rheinland-pfalz"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

fetch() { # fetch <url> <outdir> <outfile>
  code=$(curl -sL -A "$UA" -o "$2/$3.tmp" -w "%{http_code}" --max-time 45 "$1" || echo "000")
  if [ "$code" = "200" ]; then mv "$2/$3.tmp" "$2/$3"; fi
  size=$(wc -c < "$2/$3" 2>/dev/null | tr -d ' ' || echo 0)
  echo "$3  HTTP $code  ${size}B"
}

fetch "https://www.regierung-mv.de/Landesregierung/im/Aktuell?id=219369&processor=processor.sa.pressemitteilung" "$MV" "mv-pm-183-2026.html"
fetch "https://www.regierung-mv.de/Landesregierung/im/Bau/wohnen/wohnraumf%C3%B6rderung" "$MV" "mv-ministerium-wohnraumfoerderung.html"
fetch "https://isb.rlp.de/foerderung/505.html" "$RP" "isb-505.html"
fetch "https://mkbwk.rlp.de/fileadmin/07/Bilder/Themen/Bauen_und_Wohnen/Wohnraumfoerderung/Soziale_Wohnraumfoerderung/Foerderung_selbst_genutzten_Wohnraums/VV_Modernisierung_selbstgenutzter_Wohnraum__konsolidierte_Arbeitsfassung__gueltig_ab_1._Oktober_2025_.pdf" "$RP" "vv-modernisierung-505.pdf"
fetch "https://www.foerderdatenbank.de/FDB/Content/DE/Foerderprogramm/Land/Rheinland-Pfalz/wohnraumfoerderung-isb-darlehen-modernisierung.html" "$RP" "fdb-isb-modernisierung.html"
fetch "https://www.gesetze-im-internet.de/sgb_11/__40.html" "$MV" "sgb11-40.html"
fetch "https://www.gesetze-im-internet.de/sgb_9/__113.html" "$MV" "sgb9-113.html"
fetch "https://www.gesetze-im-internet.de/sgb_9/__77.html" "$MV" "sgb9-77.html"
fetch "https://www.gesetze-im-internet.de/bgb/__554.html" "$MV" "bgb-554.html"
# gesetze auch nach RP kopieren (Bundesrecht identisch)
cp "$MV/sgb11-40.html" "$MV/sgb9-113.html" "$MV/sgb9-77.html" "$MV/bgb-554.html" "$RP/" 2>/dev/null
echo done
