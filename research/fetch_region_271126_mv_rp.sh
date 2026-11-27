#!/bin/bash
# Region-Screen 271126: MV + RP — Runde 1 (Kernprogramme)
set -u
MV="research/evidence/region-screen-271126/mv"
RP="research/evidence/region-screen-271126/rheinland-pfalz"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

fetch() { # fetch <url> <outdir> <outfile>
  code=$(curl -sL -A "$UA" -o "$2/$3" -w "%{http_code}" --max-time 60 "$1")
  size=$(wc -c < "$2/$3" | tr -d ' ')
  echo "$3  HTTP $code  ${size}B"
}

# === MV: LFI-Produktseite + Richtlinie + Merkblatt ===
fetch "https://www.lfi-mv.de/foerderfinder/personenaufzuege-und-lifte-barrierearmes-wohnen" "$MV" "lfi-barrierearmes-wohnen.html"
fetch "http://www.lfi-mv.de/export/sites/lfi/.galleries/personenaufzuege-und-lifte-barrierearmes-wohnen/lesefassung-richtlinie-inkl-aenderungserlasse.pdf" "$MV" "lfi-rl-lesefassung.pdf"
fetch "http://www.lfi-mv.de/export/sites/lfi/.galleries/personenaufzuege-und-lifte-barrierearmes-wohnen/merkblatt-personenaufzuege-lifte-barrierearmes-wohnen.pdf" "$MV" "lfi-merkblatt.pdf"
# === MV: Ministerium (PM 18.04.2026 + Wohnraumfoerderungs-Overview) ===
fetch "https://www.regierung-mv.de/Landesregierung/im/Aktuell?id=219369&processor=processor.sa.pressemitteilung" "$MV" "mv-pm-183-2026.html"
fetch "https://www.regierung-mv.de/Landesregierung/im/Bau/wohnen/wohnraumf%C3%B6rderung" "$MV" "mv-ministerium-wohnraumfoerderung.html"

# === RP: ISB-Produktseite 505 + VV-PDF (Ministerium) + Foerderdatenbank ===
fetch "https://isb.rlp.de/foerderung/505.html" "$RP" "isb-505.html"
fetch "https://mkbwk.rlp.de/fileadmin/07/Bilder/Themen/Bauen_und_Wohnen/Wohnraumfoerderung/Soziale_Wohnraumfoerderung/Foerderung_selbst_genutzten_Wohnraums/VV_Modernisierung_selbstgenutzter_Wohnraum__konsolidierte_Arbeitsfassung__gueltig_ab_1._Oktober_2025_.pdf" "$RP" "vv-modernisierung-505.pdf"
fetch "https://www.foerderdatenbank.de/FDB/Content/DE/Foerderprogramm/Land/Rheinland-Pfalz/wohnraumfoerderung-isb-darlehen-modernisierung.html" "$RP" "fdb-isb-modernisierung.html"

# === Bundesrecht (je 1x, wird in beide Evidenz-Ordner kopiert) ===
fetch "https://www.gesetze-im-internet.de/sgb_11/__40.html" "$MV" "sgb11-40.html"
fetch "https://www.gesetze-im-internet.de/sgb_9/__113.html" "$MV" "sgb9-113.html"
fetch "https://www.gesetze-im-internet.de/sgb_9/__77.html" "$MV" "sgb9-77.html"
fetch "https://www.gesetze-im-internet.de/bgb/__554.html" "$MV" "bgb-554.html"

echo "--- exit ok ---"
