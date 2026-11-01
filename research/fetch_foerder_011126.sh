#!/bin/sh
# Förder-Prüflauf 01.11.2026: Originalquellen frisch abrufen (Evidence-Belege).
set -e
EV=/Users/mac/agentic-business/barrierefrei-leads/research/evidence
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

curl -sS -A "$UA" -o "$EV/foerder-011126-sgb40.html"   "https://www.gesetze-im-internet.de/sgb_11/__40.html"
curl -sS -A "$UA" -o "$EV/foerder-011126-kfw455b.html" "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/"
curl -sS -A "$UA" -o "$EV/foerder-011126-kfw159.html"  "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-(159)"
curl -sS -A "$UA" -o "$EV/foerder-011126-kfw159-umlaut.html" "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/Förderprodukte/Altersgerecht-Umbauen-(159)"
curl -sS -A "$UA" -o "$EV/foerder-011126-bmg-zuschuss.html" "https://www.bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung"

ls -la "$EV" | grep foerder-011126
