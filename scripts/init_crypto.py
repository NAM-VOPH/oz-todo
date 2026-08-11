#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_crypto.py - jednorazove nastaveni sifrovani (nebo zmena PINu).

  python3 scripts/init_crypto.py --users "NAM:1002:admin,AHUY:1972:oz" \
      --repo-dir . --secret-dir "/cesta/k/.oz-secrets"

Vytvori:
  <repo>/keys.json                 -> jde na GitHub (verejne, bez nej se nic nedesifruje)
  <secret>/datakey.txt             -> NIKDY na GitHub! potrebuje ho denni skript
a zasifruje data/*.json na misto (customers, tasks, completed, overrides).

ZMENA PINu: spustte znovu s --keep-key (zachova datovy klic, jen prebali PINy).
"""
import argparse, base64, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ozcrypto import make_keys, enc_json, dec_json, b64e, b64d, ITERS  # noqa: E402

DATA = ["customers.json", "tasks.json", "completed.json", "overrides.json"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", required=True,
                    help='napr. "NAM:1002:admin,AHUY:1972:oz"')
    ap.add_argument("--repo-dir", default=".")
    ap.add_argument("--secret-dir", required=True)
    ap.add_argument("--keep-key", action="store_true",
                    help="zachovat existujici datakey.txt (zmena PINu bez presifrovani dat)")
    ap.add_argument("--iters", type=int, default=ITERS)
    a = ap.parse_args()

    os.makedirs(a.secret_dir, exist_ok=True)
    keyfile = os.path.join(a.secret_dir, "datakey.txt")

    if a.keep_key and os.path.exists(keyfile):
        K = b64d(open(keyfile).read().strip())
        print("Pouzit existujici datovy klic.")
    else:
        K = os.urandom(32)
        open(keyfile, "w").write(b64e(K))
        os.chmod(keyfile, 0o600)
        print("Novy datovy klic ulozen do", keyfile)

    users = {}
    for part in a.users.split(","):
        bits = part.strip().split(":")
        if len(bits) < 2:
            sys.exit("Spatny format --users")
        users[bits[0]] = {"pin": bits[1], "role": bits[2] if len(bits) > 2 else "oz"}
        if len(bits[1]) < 6:
            print("!! POZOR: PIN '%s' ma jen %d znaku. Doporuceno 6-8 cislic."
                  % (bits[0], len(bits[1])))

    keys = make_keys(K, users, a.iters)
    kp = os.path.join(a.repo_dir, "keys.json")
    json.dump(keys, open(kp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Zapsan", kp, "- uzivatele:", ", ".join(users))

    if a.keep_key:
        print("(--keep-key: data nebyla znovu sifrovana)")
        return

    for name in DATA:
        p = os.path.join(a.repo_dir, "data", name)
        if not os.path.exists(p):
            continue
        raw = json.load(open(p, encoding="utf-8"))
        if isinstance(raw, dict) and raw.get("v") == 1 and "ct" in raw:
            print("  ", name, "- uz zasifrovano, preskoceno")
            continue
        json.dump(enc_json(raw, K), open(p, "w", encoding="utf-8"))
        print("  ", name, "- zasifrovano")


if __name__ == "__main__":
    main()
