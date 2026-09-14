#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
push_files.py - nahraje soubory z disku primo na GitHub tak, jak jsou.

Nesifruje ani nic neprepocitava - jen zkopiruje obsah souboru do repa.
Pouziva se, kdyz se rucne menil index.html, keys.json, skripty nebo uz
zasifrovane soubory v data/.

  set GITHUB_TOKEN=github_pat_...
  python scripts/push_files.py --owner NAM-VOPH --repo oz-todo \
      --message "popis zmeny" index.html keys.json data/customers.json

Cesty se zadavaji relativne ke koreni repa (= adresar oz-todo).
Soubor, ktery je na GitHubu uz stejny, se preskoci.
"""
import argparse, base64, hashlib, json, os, sys, urllib.request, urllib.error

API = "https://api.github.com"


def gh(url, token, method="GET", payload=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    data = json.dumps(payload).encode() if payload is not None else None
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise RuntimeError("GitHub %s %s -> %s %s"
                           % (method, url, e.code, e.read().decode()[:300]))


def blob_sha(raw):
    """SHA-1 tak, jak ji pocita git - kvuli porovnani s GitHubem."""
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(raw))
    h.update(raw)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--branch", default="main")
    ap.add_argument("--message", default="rucni aktualizace")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("paths", nargs="+", help="cesty relativne ke koreni repa")
    a = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token and not a.dry_run:
        sys.exit("Chybi GITHUB_TOKEN.")

    changed = skipped = 0
    for p in a.paths:
        rel = p.replace("\\", "/").lstrip("./")
        if not os.path.exists(rel):
            print("!! neexistuje:", rel)
            continue
        raw = open(rel, "rb").read()
        mine = blob_sha(raw)
        if a.dry_run:
            print("   %-28s %8d B  sha=%s" % (rel, len(raw), mine[:8]))
            continue
        url = "%s/repos/%s/%s/contents/%s" % (API, a.owner, a.repo, rel)
        cur = gh(url + "?ref=" + a.branch, token)
        if cur and cur.get("sha") == mine:
            print("   %-28s beze zmeny" % rel)
            skipped += 1
            continue
        body = {"message": a.message, "branch": a.branch,
                "content": base64.b64encode(raw).decode()}
        if cur:
            body["sha"] = cur["sha"]
        gh(url, token, "PUT", body)
        print("   %-28s nahrano (%d B)" % (rel, len(raw)))
        changed += 1

    if not a.dry_run:
        print("Hotovo: %d zmeneno, %d beze zmeny." % (changed, skipped))


if __name__ == "__main__":
    main()
