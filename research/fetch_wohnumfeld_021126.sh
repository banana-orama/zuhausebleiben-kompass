#!/bin/bash
# Batch: Briefing 15 — Wohnumfeld-Zuschuss beantragen (02.11.2026)
# Zieht alle Belege frisch in research/evidence/wohnumfeld-021126/
set -u
D="research/evidence/wohnumfeld-021126"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

fetch() { # fetch <url> <outfile>
  code=$(curl -sL -A "$UA" -o "$D/$2" -w "%{http_code}" --max-time 45 "$1")
  size=$(wc -c < "$D/$2" | tr -d ' ')
  echo "$2  HTTP $code  ${size}B"
}

fetch "https://www.gesetze-im-internet.de/sgb_11/__40.html" sgb40.html
fetch "https://www.bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung" bmg-wohnung.html
fetch "https://www.verbraucherzentrale.de/sites/default/files/2021-09/wohnumfeldverbessernde_massnahmen_bevollmaechtigter.pdf" vz-musterbrief.pdf
fetch "https://www.meine-pflegekasse.de/fileadmin/Dokumente/Formulare/Pflege/antrag-pflege-wohnumfeldmassnahme-mkk.pdf" mkk-formular.pdf
fetch "https://www.gkv-spitzenverband.de/media/dokumente/krankenversicherung_1/hilfsmittel/fortschreibungen_aktuell/12_2025/2025_12_11_Produktgruppe_33_Toilettenhilfen.pdf" gkv-pg33.pdf
fetch "https://www.rehadat-gkv.de/produkt/index.html?prod=bidet&s3f=s3f&reloaded&produktId=33.40.05.0006" rehadat-334005.html
fetch "https://www.pflege.de/pflegekasse-pflegefinanzierung/pflegeleistungen/wohnraumanpassung/" pflegede.html
fetch "https://verwaltung.bund.de/leistungsverzeichnis/de/leistung/99106013080001" bundportal.html
fetch "https://www.dak.de/dak/ihr-anliegen/pflege/wohnraumanpassung/wie-stelle-ich-einen-antrag-auf-wohnraumanpassung_21390" dak.html
fetch "https://www.aok.de/pk/pflegeleistungen/wohnraumanpassungen-und-barrierefreiheit/" aok.html

# Textextraktion
for f in vz-musterbrief mkk-formular gkv-pg33; do
  pdftotext -enc UTF-8 "$D/$f.pdf" "$D/$f.txt" 2>/dev/null && echo "$f.txt $(wc -c < $D/$f.txt | tr -d ' ')B"
done
