#!/bin/bash
# Batch: Briefing 16 — Mobiler Hausnotruf (04.11.2026)
# Zieht alle Belege frisch in research/evidence/hausnotruf-mobil-041126/
set -u
D="research/evidence/hausnotruf-mobil-041126"
mkdir -p "$D"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

fetch() { # fetch <url> <outfile>
  code=$(curl -sL -A "$UA" -o "$D/$2" -w "%{http_code}" --max-time 45 "$1")
  size=$(wc -c < "$D/$2" | tr -d ' ')
  echo "$2  HTTP $code  ${size}B"
}

fetch "https://www.malteser.de/hausnotruf.html" malteser-hausnotruf.html
fetch "https://www.malteser.de/hausnotruf/faq.html" malteser-faq.html
fetch "https://www.gesetze-im-internet.de/sgb_11/__39.html" sgb39.html
fetch "https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/hausnotrufsysteme-erklaert-so-helfen-sie-im-notfall-funktionen-vorteile-kosten-10566" vz-hausnotruf.html
fetch "https://www.pflege.net/mobiler-hausnotruf-mit-gps/" pflegenet-mobil.html
fetch "https://www.pflege.net/ratgeber/hausnotruf-fuer-unterwegs/" pflegenet-unterwegs.html
fetch "https://www.pflege-panorama.de/ratgeber/mobiler-hausnotruf/" panorama-mobil.html
fetch "https://www.hausnotruf-kosten.de/mobiler-hausnotruf/" hnrkosten-mobil.html
fetch "https://www.hausnotruf-kosten.de/hausnotruf-ohne-festnetz/" hnrkosten-festnetz.html
fetch "https://pflegekompass.de/magazin/ratgeber/hausnotruf-mobil-gps" kompass-mobil.html
fetch "https://www.bewo-telehealthcare.com/ratgeber/hausnotruf-basis-vs-mobiler-notruf" bewo-basis-vs-mobil.html
fetch "https://sanivia.de/ratgeber/notrufsysteme-fuer-senioren/" sanivia-systeme.html
fetch "https://www.zqp.de/themen/technische-hilfen-im-alltag/" zqp-hilfen.html
