#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish.py - denni aktualizace zasifrovane databaze na GitHubu.

Co dela:
  1. stahne z GitHubu data/overrides.json (rucni zmeny OZ), data/completed.json a
     data/customers.json a desifruje je datovym klicem
  2. znovu spocita customers.json z "data odberatele.xlsx" + "data prodeje.xlsx"
  3. pokud se neco zmenilo, zasifruje a nahraje novy customers.json zpet na GitHub
  4. vypise souhrn: novi zakaznici, zmeny skupiny, po termínu, hotove ukoly za 24 h

Pouziti:
  export GITHUB_TOKEN=github_pat_...
  python3 scripts/publish.py --owner NAM-VOPH --repo oz-todo \
      --datakey "/cesta/.oz-secrets/datakey.txt" \
      --odberatele "/cesta/data odberatele.xlsx" --prodeje "/cesta/data prodeje.xlsx"

Volby:
  --dry-run   jen spocita a vypise souhrn, nic nenahraje
"""
import argparse, base64, json, os, subprocess, sys, tempfile, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ozcrypto import enc_json, dec_json  # noqa: E402

API = "https://api.github.com"


def gh(url, token, method="GET", payload=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise RuntimeError("GitHub %s %s -> %s %s" % (method, url, e.code, e.read().decode()[:300]))


def get_file(owner, repo, branch, path, token, key):
    j = gh("%s/repos/%s/%s/contents/%s?ref=%s" % (API, owner, repo, path, branch), token)
    if not j:
        return None, None
    blob = json.loads(base64.b64decode(j["content"]).decode())
    data = dec_json(blob, key) if isinstance(blob, dict) and blob.get("v") == 1 and "ct" in blob else blob
    return data, j["sha"]


def put_file(owner, repo, branch, path, obj, msg, sha, token, key):
    enc = enc_json(obj, key)
    body = {"message": msg, "branch": branch,
            "content": base64.b64encode(json.dumps(enc).encode()).decode()}
    if sha:
        body["sha"] = sha
    gh("%s/repos/%s/%s/contents/%s" % (API, owner, repo, path), token, "PUT", body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--branch", default="main")
    ap.add_argument("--datakey", required=True, help="cesta k datakey.txt")
    ap.add_argument("--odberatele", required=True)
    ap.add_argument("--prodeje", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token and not a.dry_run:
        sys.exit("Chybi GITHUB_TOKEN.")
    key = base64.b64decode(open(a.datakey).read().strip())

    here = os.path.dirname(os.path.abspath(__file__))
    tmp = tempfile.mkdtemp()

    # 1) stahnout stav z GitHubu -------------------------------------------
    old, old_sha, overrides, done = None, None, {}, []
    if token:
        old, old_sha = get_file(a.owner, a.repo, a.branch, "data/customers.json", token, key)
        ov, _ = get_file(a.owner, a.repo, a.branch, "data/overrides.json", token, key)
        overrides = (ov or {}).get("obchodni_zastupce", {})
        dn, _ = get_file(a.owner, a.repo, a.branch, "data/completed.json", token, key)
        done = (dn or {}).get("tasks", [])

    ov_path = os.path.join(tmp, "overrides.json")
    with open(ov_path, "w", encoding="utf-8") as f:
        json.dump({"obchodni_zastupce": overrides}, f, ensure_ascii=False)

    # predchozi databaze -> zachova prirazeni obchodniho zastupce
    prev_path = os.path.join(tmp, "previous.json")
    if old:
        with open(prev_path, "w", encoding="utf-8") as f:
            json.dump(old, f, ensure_ascii=False)

    # dokoncene ukoly -> navstevy, resetuji termin navstevy
    done_path = os.path.join(tmp, "completed.json")
    with open(done_path, "w", encoding="utf-8") as f:
        json.dump({"tasks": done}, f, ensure_ascii=False)

    # 2) prepocitat ---------------------------------------------------------
    out = os.path.join(tmp, "customers.json")
    cmd = [sys.executable, os.path.join(here, "build_db.py"),
           "--odberatele", a.odberatele, "--prodeje", a.prodeje,
           "--out", out, "--overrides", ov_path, "--completed", done_path]
    if old:
        cmd += ["--previous", prev_path]
    subprocess.run(cmd, check=True)
    new = json.load(open(out, encoding="utf-8"))

    # 3) souhrn -------------------------------------------------------------
    print("\n=== SOUHRN ===")
    oldm = {c["id"]: c for c in (old or {}).get("customers", [])}
    newm = {c["id"]: c for c in new["customers"]}
    added = [c for i, c in newm.items() if i not in oldm]
    moved = [(oldm[i]["skupina_label"], c["skupina_label"], c["firma"])
             for i, c in newm.items()
             if i in oldm and oldm[i]["skupina_label"] != c["skupina_label"]]
    over = sorted([c for c in new["customers"] if (c.get("po_terminu_dni") or 0) > 0],
                  key=lambda c: -c["po_terminu_dni"])

    print("Zakazniku celkem: %d (+%d novych)" % (len(newm), len(added)))
    for c in added[:40]:
        print("  + %-40s %-22s %s" % (c["firma"][:40], c["okres"], c["obchodni_zastupce"]))
    if moved:
        print("Zmena skupiny (%d):" % len(moved))
        for o, n, f in moved[:40]:
            print("  ~ %-40s %s -> %s" % (f[:40], o, n))
    print("Po termínu navstevy: %d" % len(over))
    for c in over[:20]:
        print("  ! %-40s %-18s %3d dni  %s" % (c["firma"][:40], c["skupina_label"],
                                               c["po_terminu_dni"], c["obchodni_zastupce"]))
    since = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    fresh = [t for t in done if (t.get("done_at") or "") >= since]
    print("Ukoly dokoncene za 24 h: %d" % len(fresh))
    for t in fresh[:30]:
        print("  ✓ %-30s %-10s %s" % (t["firma"][:30], t["type"], (t["text"] or "")[:60]))

    # 4) nahrat -------------------------------------------------------------
    if a.dry_run:
        print("\n(dry-run: nic nenahrano)")
        return
    if old:
        strip = lambda p: json.dumps([{k: v for k, v in c.items()} for c in p["customers"]],
                                     ensure_ascii=False, sort_keys=True)
        if strip(old) == strip(new):
            print("\nZadna zmena dat - customers.json nechan beze zmeny.")
            return
    put_file(a.owner, a.repo, a.branch, "data/customers.json", new,
             "denní aktualizace %s" % datetime.now().strftime("%Y-%m-%d %H:%M"),
             old_sha, token, key)
    print("\ncustomers.json (zasifrovany) nahran na GitHub.")


if __name__ == "__main__":
    main()
