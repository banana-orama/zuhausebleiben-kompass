#!/usr/bin/env python3
# 23.11.2026: Eingerückte BGBl-Quellenblöcke (10 Leerzeichen) auf 6 Leerzeichen normalisieren.
import os
BASE = os.path.join(os.path.dirname(__file__), "..", "content-ready")
FILES = ["hilfsmittel-dusch-wc-uebernahme.json", "hilfsmittel-pflegekasse-uebernahme.json",
         "rollator-auswahl-passform-kosten.json"]
for fn in FILES:
    p = os.path.join(BASE, fn)
    t = open(p, encoding="utf-8").read()
    old_block = (
        '    {\n'
        '          "title": "Bundesgesetzblatt Teil I: GKV-Beitragssatzstabilisierungsgesetz vom 24. Juli 2026 (BGBl. 2026 I Nr. 228, Art. 1 Nr. 23 – neuer § 61 SGB V)",\n'
        '          "url": "https://www.recht.bund.de/bgbl/1/2026/228/VO.html",\n'
        '          "checked_at": "2026-11-23"\n'
        '    }'
    )
    new_block = (
        '    {\n'
        '      "title": "Bundesgesetzblatt Teil I: GKV-Beitragssatzstabilisierungsgesetz vom 24. Juli 2026 (BGBl. 2026 I Nr. 228, Art. 1 Nr. 23 – neuer § 61 SGB V)",\n'
        '      "url": "https://www.recht.bund.de/bgbl/1/2026/228/VO.html",\n'
        '      "checked_at": "2026-11-23"\n'
        '    }'
    )
    assert t.count(old_block) == 1, f"{fn}: Block nicht (einmalig) gefunden"
    import json
    t = t.replace(old_block, new_block)
    json.loads(t)
    open(p, "w", encoding="utf-8").write(t)
    print(fn, "normalisiert, Parse OK")
