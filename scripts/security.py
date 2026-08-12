#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security.py - sprava zamku prihlaseni (data/security.json).

Soubor NENI sifrovany - aplikace ho musi precist jeste pred prihlasenim.
Proto obsahuje jen SHA-256 otisky zarizeni a IP, nikdy citelne udaje.

Uzivatel, ktery je zamceny, vidi na obrazovce kod typu "A1B2-C3".
Ten kod staci predat NAMovi.

  # odemknout zarizeni podle kodu z obrazovky
  python3 scripts/security.py unlock --code A1B2-C3

  # trvale zablokovat zarizeni (i kdyby si smazalo localStorage)
  python3 scripts/security.py block --code A1B2-C3 --note "ztraceny telefon"

  # zrusit trvalou blokaci
  python3 scripts/security.py allow --code A1B2-C3

  # vypsat stav
  python3 scripts/security.py list

  # zmenit pocet povolenych pokusu
  python3 scripts/security.py limit --max 5

Pridanim --push se soubor rovnou nahraje na GitHub (potrebuje GITHUB_TOKEN).
"""
import argparse, base64, json, os, sys, urllib.request, urllib.error
from datetime import datetime, timezone

API = "https://api.github.com"
PATH = "data/security.json"
DEFAULT = {"updated_at": None, "max_attempts": 5, "blocked": [], "cleared": []}


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm(code):
    return code.upper().replace("-", "").replace(" ", "").strip()


def load(repo_dir):
    p = os.path.join(repo_dir, PATH)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        for k, v in DEFAULT.items():
            d.setdefault(k, v)
        return d
    return dict(DEFAULT, blocked=[], cleared=[])


def save(repo_dir, d):
    d["updated_at"] = now()
    p = os.path.join(repo_dir, PATH)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("Zapsano:", p)


def push(owner, repo, branch, repo_dir):
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        sys.exit("Chybi GITHUB_TOKEN - nelze nahrat na GitHub.")
    body_path = os.path.join(repo_dir, PATH)
    content = base64.b64encode(open(body_path, "rb").read()).decode()

    def gh(method, url, payload=None):
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
            raise RuntimeError("GitHub %s -> %s %s" % (method, e.code, e.read().decode()[:200]))

    cur = gh("GET", "%s/repos/%s/%s/contents/%s?ref=%s" % (API, owner, repo, PATH, branch))
    payload = {"message": "security %s" % now(), "branch": branch, "content": content}
    if cur:
        payload["sha"] = cur["sha"]
    gh("PUT", "%s/repos/%s/%s/contents/%s" % (API, owner, repo, PATH), payload)
    print("Nahrano na GitHub:", PATH)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["list", "unlock", "block", "allow", "limit"])
    ap.add_argument("--code", help='kod z obrazovky uzivatele, napr. A1B2-C3')
    ap.add_argument("--ip", help='misto --code lze blokovat/odemknout podle IP')
    ap.add_argument("--note", default="")
    ap.add_argument("--max", type=int)
    ap.add_argument("--repo-dir", default=".")
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--owner", default="NAM-VOPH")
    ap.add_argument("--repo", default="oz-todo")
    ap.add_argument("--branch", default="main")
    a = ap.parse_args()

    d = load(a.repo_dir)

    if a.action == "list":
        print("Povoleno pokusu:", d.get("max_attempts", 5))
        print("Trvale zablokovana zarizeni:", len(d["blocked"]))
        for b in d["blocked"]:
            print("   %-9s %-6s %s  %s" % (b.get("code", "?"), b.get("user", ""),
                                           b.get("at", ""), b.get("note", "")))
        print("Odemknuti:", len(d["cleared"]))
        for c in d["cleared"][-10:]:
            print("   %-9s %s" % (c.get("code", "?"), c.get("at", "")))
        return

    if a.action == "limit":
        if not a.max:
            sys.exit("Zadejte --max")
        d["max_attempts"] = a.max
        print("Pocet povolenych pokusu:", a.max)
    else:
        if not a.code and not a.ip:
            sys.exit("Zadejte --code (kod z obrazovky uzivatele) nebo --ip")

        ent = {"at": now()}
        if a.code:
            code = norm(a.code)
            if len(code) != 6:
                sys.exit("Kod ma mit 6 znaku, napr. A1B2-C3")
            ent["code"] = code[:3] + "-" + code[3:]
            ent["prefix"] = code.lower()
        if a.ip:
            import hashlib
            ent["ip"] = hashlib.sha256(a.ip.strip().encode()).hexdigest()
            ent.setdefault("code", "IP:" + a.ip.strip())
        label = ent["code"]
        same = lambda x: x.get("code") == label

        if a.action == "unlock":
            d["blocked"] = [b for b in d["blocked"] if not same(b)]
            d["cleared"] = [c for c in d["cleared"] if not same(c)] + [ent]
            print("Odemknuto:", label, "- uzivatel da F5 nebo klikne 'Thu lai'.")
        elif a.action == "block":
            ent["note"] = a.note
            d["blocked"] = [b for b in d["blocked"] if not same(b)] + [ent]
            d["cleared"] = [c for c in d["cleared"] if not same(c)]
            print("Trvale zablokovano:", label)
        elif a.action == "allow":
            d["blocked"] = [b for b in d["blocked"] if not same(b)]
            d["cleared"].append(ent)
            print("Blokace zrusena:", label)

    save(a.repo_dir, d)
    if a.push:
        push(a.owner, a.repo, a.branch, a.repo_dir)


if __name__ == "__main__":
    main()
