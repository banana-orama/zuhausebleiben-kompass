#!/usr/bin/env python3
"""Delete tags 14/16 + triggers 9/15, recreate with identical parameters (v2 JSON as source of truth)."""
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
    # --- delete tags then triggers ---
    for kind, tid in (("tag", "14"), ("tag", "16"), ("trigger", "9"), ("trigger", "15")):
        r = call(f"gtm_delete_{kind}", {f"{kind}Path": f"{WS}/{kind}s/{tid}", "confirm": True}, confirm=True)
        data = r.get("data") or {}
        gone = data.get("deleted") is True or r.get("ok") is True
        print(f"[{'OK' if gone else 'FAIL'}] delete {kind} {tid}: {json.dumps(data)[:120]}")
        ok &= gone

    st = call("gtm_get_workspace_status", {"workspacePath": WS})
    print("workspace after delete:", json.dumps(st.get("data") or st))
    print("DELETE_RESULT:", "ALL_OK" if ok else "SOME_FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
