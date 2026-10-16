#!/usr/bin/env python3
"""Touch `notes` on tags 14/16 and triggers 9/15 (minimal real change forcing v3 regeneration)."""
import json, subprocess, sys

WS = "accounts/572865630/containers/267198165/workspaces/3"
EV = "operations/measurement/v3-fix"
NOTES = {
    "14": "ZBK client-side GA4 (consent-gated). Resaved 2026-10-16 to regenerate v3 runtime (v2 never fired).",
    "16": "ZBK cta_click GA4 (consent-gated). Resaved 2026-10-16 to regenerate v3 runtime (v2 never fired).",
}
TRIGGER_NOTES = {
    "9": "Fires on zbk_measurement page_view, 7 consent predicates. Resaved 2026-10-16 to regenerate v3 runtime.",
    "15": "Fires on zbk_measurement cta_click, 7 consent predicates. Resaved 2026-10-16 to regenerate v3 runtime.",
}


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
    for tid in ("9", "15"):
        t = call("gtm_get_trigger", {"triggerPath": f"{WS}/triggers/{tid}"})
        fp = t.get("fingerprint")
        resp = call("gtm_update_trigger", {"triggerPath": f"{WS}/triggers/{tid}", "fingerprint": fp,
                                           "triggerConfig": {"notes": TRIGGER_NOTES[tid]}}, confirm=True)
        ent = resp if resp.get("triggerId") else (resp.get("data") or {})
        new_fp = ent.get("fingerprint")
        status = "OK" if new_fp and new_fp != fp else "FAIL"
        print(f"[{status}] trigger {tid}: fp {fp} -> {new_fp}")
        if status == "FAIL":
            print("  ", json.dumps(resp)[:300])
        ok &= status == "OK"

    for tid in ("14", "16"):
        t = call("gtm_get_tag", {"tagPath": f"{WS}/tags/{tid}"})
        fp = t.get("fingerprint")
        resp = call("gtm_update_tag", {"tagPath": f"{WS}/tags/{tid}", "fingerprint": fp,
                                       "tagConfig": {"notes": NOTES[tid]}}, confirm=True)
        ent = resp if resp.get("tagId") else (resp.get("data") or {})
        new_fp = ent.get("fingerprint")
        status = "OK" if new_fp and new_fp != fp else "FAIL"
        print(f"[{status}] tag {tid}: fp {fp} -> {new_fp}")
        if status == "FAIL":
            print("  ", json.dumps(resp)[:300])
        ok &= status == "OK"

    st = call("gtm_get_workspace_status", {"workspacePath": WS})
    print("workspace status:", json.dumps(st.get("data") or st))
    print("TOUCH_RESULT:", "ALL_OK" if ok else "SOME_FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
