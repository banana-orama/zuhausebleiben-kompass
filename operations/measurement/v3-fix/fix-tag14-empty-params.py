#!/usr/bin/env python3
"""Restore tag 14 config including explicit empty-string page_referrer/page_title rows."""
import json, subprocess, sys

WS = "accounts/572865630/containers/267198165/workspaces/3"
EV = "operations/measurement/v3-fix"


def call(tool, args, confirm=False):
    cmd = ["gtm", "tool", "call", tool, "--args-json", json.dumps(args)]
    if confirm:
        cmd.append("--confirm")
    p = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/mac/agentic-business/barrierefrei-leads")
    try:
        return json.loads((p.stdout or "").strip())
    except json.JSONDecodeError:
        return {"_raw": p.stdout, "_stderr": p.stderr}


def settings_row(parameter, parameterValue):
    m = [{"type": "template", "key": "parameter", "value": parameter}]
    m.append({"type": "template", "key": "parameterValue", "value": parameterValue})
    return {"type": "map", "map": m}


def main():
    cur = call("gtm_get_tag", {"tagPath": f"{WS}/tags/14"})
    fp = cur.get("fingerprint")
    assert fp and fp != "1792143575557", f"unexpected fingerprint: {fp}"
    parameter = [
        {"type": "template", "key": "tagId", "value": "G-5738T8FHWW"},
        {"type": "list", "key": "configSettingsTable", "list": [
            settings_row("send_page_view", "true"),
            settings_row("page_location", "https://zuhausebleiben-kompass.de/"),
            settings_row("page_referrer", ""),
            settings_row("page_title", ""),
        ]},
    ]
    resp = call("gtm_update_tag", {
        "tagPath": f"{WS}/tags/14", "fingerprint": fp,
        "tagConfig": {"name": cur.get("name"), "type": "googtag",
                      "parameter": parameter, "firingTriggerId": ["9"]},
    }, confirm=True)
    entity = resp if resp.get("tagId") else (resp.get("data") or {})
    if not entity:
        print("[FAIL] update:", json.dumps(resp)[:500])
        return 1
    json.dump(entity, open(f"{EV}/tag-14-after-resave.json", "w"), indent=1)

    rb = call("gtm_get_tag", {"tagPath": f"{WS}/tags/14"})
    rb = rb if rb.get("tagId") else (rb.get("data") or {})
    json.dump(rb, open(f"{EV}/tag-14-after-resave.json", "w"), indent=1)
    rows = []
    for param in rb.get("parameter", []):
        if param.get("key") == "configSettingsTable":
            for row in param.get("list", []):
                m = row.get("map", [])
                k = next((e.get("value") for e in m if e.get("key") == "parameter"), None)
                v = next((e.get("value") for e in m if e.get("key") == "parameterValue"), None)
                rows.append((k, "" if v is None else v))
        else:
            rows.append((param.get("key"), param.get("value")))
    print("tag 14 rows:", json.dumps(rows))
    expected = [["tagId", "G-5738T8FHWW"], ["send_page_view", "true"],
                ["page_location", "https://zuhausebleiben-kompass.de/"],
                ["page_referrer", ""], ["page_title", ""]]
    print("RESTORED:", rows == expected, "| new fingerprint:", rb.get("fingerprint"))
    return 0 if rows == expected else 1


if __name__ == "__main__":
    sys.exit(main())
