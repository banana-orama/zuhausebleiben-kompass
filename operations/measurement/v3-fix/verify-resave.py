#!/usr/bin/env python3
"""Re-fetch readbacks of tags 14/16 + triggers 9/15 (top-level entity response) and diff vs before."""
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


def main():
    ok = True
    for kind, tid in (("trigger", "9"), ("trigger", "15"), ("tag", "14"), ("tag", "16")):
        path = f"{WS}/{kind}s/{tid}"
        resp = call(f"gtm_get_{kind}", {f"{kind}Path": path})
        entity = resp if resp.get(f"{kind}Id") else (resp.get("data") or {})
        json.dump(entity, open(f"{EV}/{kind}-{tid}-after-resave.json", "w"), indent=1)
        if not entity:
            print(f"[FAIL] {kind} {tid}: empty readback", json.dumps(resp)[:300])
            ok = False
            continue
        old = json.load(open(f"{EV}/{kind}-{tid}-before.json"))
        cfg_keys = ("name", "type", "parameter", "firingTriggerId", "filter", "customEventFilter")
        same = all(old.get(k) == entity.get(k) for k in cfg_keys)
        new_fp = entity.get("fingerprint")
        changed = new_fp and new_fp != old.get("fingerprint")
        status = "OK" if (same and changed) else "WARN"
        print(f"[{status}] {kind} {tid}: config_identical={same} fingerprint {old.get('fingerprint')} -> {new_fp}")
        if not same:
            for k in cfg_keys:
                if old.get(k) != entity.get(k):
                    print(f"    DIFF in {k}:\n      before={json.dumps(old.get(k))[:400]}\n      after ={json.dumps(entity.get(k))[:400]}")
    print("READBACK_RESULT:", "ALL_OK" if ok else "SOME_FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
