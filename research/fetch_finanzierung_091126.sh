#!/bin/bash
# Fetch alle Primärquellen für Briefing 20 (treppenlift-finanzierung) — Roh-HTML bewusst uncommitted
D="research/evidence/finanzierung-091126"
mkdir -p "$D"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

fetch() {
  local name="$1"; local url="$2"
  curl -sL --compressed -A "$UA" --max-time 45 -o "$D/$name.html" "$url"
  local code=$(curl -sL -A "$UA" --max-time 45 -o /dev/null -w "%{http_code}" "$url")
  echo "$name $code $(wc -c < "$D/$name.html" | tr -d ' ') bytes"
}

fetch tke-finanzierung "https://www.tke-homesolutions.de/preise/treppenlift-finanzierung/"
fetch lifta-finanzierung "https://www.lifta.de/treppenlift-preise/finanzierung"
fetch lifta-home "https://www.lifta.de/"
fetch hiro-home "https://www.hiro.de/"
fetch hiro-finanzierung "https://www.hiro.de/finanzierung/"
fetch liftteam-ratenkauf "https://nord-ostsee-liftteam.de/treppenlifte/ratenkauf/"
fetch der-tl-ratenzahlung "https://www.der-treppenlift.de/treppenlift-kosten/ratenzahlung/"
fetch ideal-tl-ratenzahlung "https://www.ideal-treppenlift.de/treppenlift-ratenzahlung/"
fetch gebrauchtl-finanzieren "https://www.gebraucht-treppenlifte.de/preise/treppenlift-finanzieren/"

# Gesetze: gesetze-im-internet (ISO-8859-1 + Entities — Strip passiert im Strip-Skript)
fetch bgb-491 "https://www.gesetze-im-internet.de/bgb/__491.html"
fetch bgb-492 "https://www.gesetze-im-internet.de/bgb/__492.html"
fetch bgb-495 "https://www.gesetze-im-internet.de/bgb/__495.html"
fetch bgb-500 "https://www.gesetze-im-internet.de/bgb/__500.html"
fetch bgb-502 "https://www.gesetze-im-internet.de/bgb/__502.html"
fetch bgb-312g "https://www.gesetze-im-internet.de/bgb/__312g.html"
fetch bgb-356b "https://www.gesetze-im-internet.de/bgb/__356b.html"

echo "--- HIRO Finanzierungs-Links auf der Startseite ---"
grep -o -i 'href="[^"]*finanzier[^"]*"' "$D/hiro-home.html" | head -5
echo "--- Lifta: 0%-Mentionen auf eigener Seite ---"
grep -c -i "0 %\|0%\|zinsfrei\|zinslos" "$D/lifta-finanzierung.html"
