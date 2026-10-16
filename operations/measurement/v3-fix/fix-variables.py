#!/usr/bin/env python3
"""Root-cause fix: add dataLayerVersion=2 to variables 11/12/13 (measurement.*) in ws5."""
import json, subprocess, sys

WS = "accounts/572865630/containers/267198165/workspaces/5"
EV = "operations/measurement/v3-fix"
VARS = {"11": "measurement.content_id", "12": "measurement.event_name", "13": "measurement.cta_id"}


def call(tool, args, confirm=False):
    cmd = ["gtm", "tool", "call", tool, "--args-json", json.dumps(args)]
    if confirm:
        cmd.append("--confirm")
    p = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/mac/agentic-business/barrierefrei-leads")
    try:
        return json.loads((p.stdout or "").strip())
    except json.JSONDecodeError:
        return {"_raw": p.stdout, "_stderr": p.stderr}


def main():
    ok = True
    for vid, name in VARS.items():
        cur = call("gtm_get_variable", {"variablePath": f"{WS}/variables/{vid}"})
        fp = cur.get("fingerprint")
        assert fp, f"no fingerprint for {vid}"
        cfg = {
            "name": cur.get("name"),
            "type": "v",
            "parameter": [
                {"type": "integer", "key": "dataLayerVersion", "value": "2"},
                {"type": "template", "key": "name", "value": name},
            ],
        }
        resp = call("gtm_update_variable", {"variablePath": f"{WS}/variables/{vid}",
                                            "fingerprint": fp, "variableConfig": cfg}, confirm=True)
        ent = resp if resp.get("variableId") else (resp.get("data") or {})
        new_fp = ent.get("fingerprint")
        # verify readback
        rb = call("gtm_get_variable", {"variablePath": f"{WS}/variables/{vid}"})
        params = {p.get("key"): p.get("value") for p in rb.get("parameter", [])}
        good = params.get("dataLayerVersion") == "2" and params.get("name") == name
        status = "OK" if good else "FAIL"
        print(f"[{status}] variable {vid} ({name}): dlv={params.get('dataLayerVersion')} name={params.get('name')} fp {fp}->{new_fp}")
        if not good:
            print("   ", json.dumps(rb)[:300])
        ok &= good
    print("VARIABLE_FIX:", "ALL_OK" if ok else "SOME_FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
