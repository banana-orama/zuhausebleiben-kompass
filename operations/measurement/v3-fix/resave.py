#!/usr/bin/env python3
"""v3-fix: re-save tags 14/16 + triggers 9/15 in ZBK web workspace 3 via named gtm tools."""
import json, subprocess, sys

WS = "accounts/572865630/containers/267198165/workspaces/3"
EV = "operations/measurement/v3-fix"


def call(tool, args, confirm=False):
    cmd = ["gtm", "tool", "call", tool, "--args-json", json.dumps(args)]
    if confirm:
        cmd.append("--confirm")
    p = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/mac/agentic-business/barrierefrei-leads")
    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip()
    try:
        return json.loads(out), err
    except json.JSONDecodeError:
        return {"_raw": out, "_stderr": err}, err


def expect(resp, label, keys):
    data = resp.get("data") or {}
    missing = [k for k in keys if data.get(k) in (None, "")]
    err = resp.get("error")
    status = "OK" if not missing and not err else "FAIL"
    print(f"[{status}] {label}: " + json.dumps({k: data.get(k) for k in keys}) + (f" error={err}" if err else ""))
    if status == "FAIL":
        print("  raw:", json.dumps(resp)[:600])
    return status == "OK"


def main():
    ok = True
    # --- triggers: re-save with identical config ---
    for tid in ("9", "15"):
        t = json.load(open(f"{EV}/trigger-{tid}-before.json"))
        cfg = {"name": t["name"], "type": t["type"], "filter": t["filter"],
               "customEventFilter": t["customEventFilter"]}
        resp, _ = call("gtm_update_trigger", {"triggerPath": t["path"],
                                              "fingerprint": t["fingerprint"],
                                              "triggerConfig": cfg}, confirm=True)
        ok &= expect(resp, f"update trigger {tid}", ["triggerId", "fingerprint"])

    # --- tags: re-save with identical config ---
    for tid in ("14", "16"):
        t = json.load(open(f"{EV}/tag-{tid}-before.json"))
        cfg = {"name": t["name"], "type": t["type"], "parameter": t["parameter"],
               "firingTriggerId": t["firingTriggerId"]}
        resp, _ = call("gtm_update_tag", {"tagPath": t["path"],
                                          "fingerprint": t["fingerprint"],
                                          "tagConfig": cfg}, confirm=True)
        ok &= expect(resp, f"update tag {tid}", ["tagId", "fingerprint"])

    # --- readback verify ---
    for tid in ("14", "16"):
        resp, _ = call("gtm_get_tag", {"tagPath": f"{WS}/tags/{tid}"})
        d = resp.get("data") or {}
        json.dump(d, open(f"{EV}/tag-{tid}-after-resave.json", "w"), indent=1)
        ok &= expect(resp, f"readback tag {tid}", ["tagId", "fingerprint"])
    for tid in ("9", "15"):
        resp, _ = call("gtm_get_trigger", {"triggerPath": f"{WS}/triggers/{tid}"})
        d = resp.get("data") or {}
        json.dump(d, open(f"{EV}/trigger-{tid}-after-resave.json", "w"), indent=1)
        ok &= expect(resp, f"readback trigger {tid}", ["triggerId", "fingerprint"])

    print("RESAVE_RESULT:", "ALL_OK" if ok else "SOME_FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
