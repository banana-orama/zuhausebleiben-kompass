#!/bin/bash
# Direktprogramm-Scan 28.10.2026: Roh-HTML fuer alle Kandidaten abrufen (oeffentliche Seiten, kein Login).
set -u
D="/Users/mac/agentic-business/barrierefrei-leads/research/evidence/direct-partner-scan-281026"
mkdir -p "$D"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
fetch() {
  name="$1"; url="$2"
  code=$(curl -sL -A "$UA" --max-time 45 -o "$D/$name.html" -w "%{http_code}" "$url")
  size=$(wc -c < "$D/$name.html" | tr -d ' ')
  echo "$name $code ${size}B $url"
}
fetch hiro-affiliate            "https://hiro.de/affiliate/"
fetch hiro-partner              "https://hiro.de/partner/"
fetch adcell-hiro-lift          "https://www.adcell.de/partnerprogramme/hiro-lift"
fetch affmarketing-hiro         "https://www.affiliate-marketing.de/partnerprogramme/hiro.de"
fetch 100pp-hiro                "https://www.100partnerprogramme.de/p/hiro/"
fetch tke-partner               "https://www.tke-homesolutions.de/preise/partner/"
fetch fital-partner             "https://www.fital-treppenlifte.de/partner.html"
fetch aroundhome-affiliate      "https://www.aroundhome.de/affiliateprogramm/"
fetch acorn-partnerportal       "https://de.acornpartner.com/"
fetch handicare-partner         "https://handicare-treppenlifte.de/ueber-handicare/handicare-partner/"
fetch lotse-100pp               "https://www.100partnerprogramme.de/p/treppenlift-zentrum-de-18014/"
