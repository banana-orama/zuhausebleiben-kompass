#!/bin/bash
# Fetch-Skript zuschuss-refresh 18.11.2026: alle Quellen der geplanten Ampel-Tabelle live holen (Retry 1x bei transientem Fehler).
set -u
D=research/evidence/zuschuss-refresh-181126
mkdir -p "$D"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
fetch () {
  local name="$1"; local url="$2"; local enc="${3:-}"
  local out="$D/$name"
  for attempt in 1 2; do
    code=$(curl -sSL --fail -A "$UA" -o "$out" -w '%{http_code}' "$url" 2>"$D/$name.err")
    if [ "$code" = "200" ] && [ -s "$out" ]; then echo "PASS $name $code"; return 0; fi
    sleep 3
  done
  # zweiter Versuch mit prozent-encodierter URL (Fallback für Umlaut-Pfade)
  if [ -n "$enc" ]; then
    code=$(curl -sSL --fail -A "$UA" -o "$out" -w '%{http_code}' "$enc" 2>>"$D/$name.err")
    if [ "$code" = "200" ] && [ -s "$out" ]; then echo "PASS $name $code (encoded-retry)"; return 0; fi
  fi
  echo "FAIL $name code=$code"; return 1
}
fetch sgb11-40.html "https://www.gesetze-im-internet.de/sgb_11/__40.html"
fetch kfw-455b.html "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/" "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-%28455%29/"
fetch kfw-159.html "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-(159)/" "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-%28159%29/"
fetch nrwbank-barrierefrei.html "https://www.nrwbank.de/de/privatpersonen/wohneigentum-gestalten/barrierefrei-umbauen"
fetch stmb-bayern-barrierefrei.html "https://www.stmb.bayern.de/wohnen/wohnraum_nutzen/barrierefreieswohnen/"
fetch live-zuschuss.html "https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html"
fetch live-region-nrw.html "https://zuhausebleiben-kompass.de/region/nordrhein-westfalen.html"
fetch live-region-bayern.html "https://zuhausebleiben-kompass.de/region/bayern.html"
echo "--- done ---"
