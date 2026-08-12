#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
set_token.py - ulozi GitHub token do repa v ZASIFROVANE podobe (data/tokens.json).

Diky tomu se uzivatel prihlasi jen PINem a token uz nemusi nikam zadavat.
Token je sifrovany stejnym klicem jako ostatni data - kdo nezna PIN, neprecte ho.

  python3 scripts/set_token.py \
      --datakey "../.oz-secrets/datakey.txt" \
      --token-file "../.oz-secrets/github_token.txt"

Volitelne:
  --user NAM        ulozit token jen pro jednoho uzivatele (jinak spolecny pro vsechny)
  --token ghp_...   zadat token primo misto souboru
  --remove NAM      smazat token daneho uzivatele
  --show            vypsat, pro koho je token ulozen (bez odhaleni hodnoty)

POZOR: nikdy neukladejte token do repa v citelne podobe - GitHub secret scanning
ho automaticky zrusi. Zasifrovana forma tento problem nema.
"""
import argparse, base64, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ozcrypto import enc_json, dec_json  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datakey", required=True)
    ap.add_argument("--repo-dir", default=".")
    ap.add_argument("--token-file")
    ap.add_argument("--token")
    ap.add_argument("--user", default="*", help='jmeno uzivatele nebo "*" pro vsechny')
    ap.add_argument("--remove")
    ap.add_argument("--show", action="store_true")
    a = ap.parse_args()

    key = base64.b64decode(open(a.datakey).read().strip())
    path = os.path.join(a.repo_dir, "data", "tokens.json")

    store = {}
    if os.path.exists(path):
        blob = json.load(open(path, encoding="utf-8"))
        if isinstance(blob, dict) and blob.get("v") == 1 and "ct" in blob:
            store = dec_json(blob, key)

    if a.show:
        for k, v in store.items():
            who = "vsichni uzivatele" if k == "*" else k
            print("  %-22s token %s…%s (%d znaku)" % (who, v[:10], v[-4:], len(v)))
        if not store:
            print("  (zadny token neni ulozen)")
        return

    if a.remove:
        store.pop(a.remove, None)
        print("Odstranen token pro:", a.remove)
    else:
        tok = (a.token or (open(a.token_file).read() if a.token_file else "")).strip()
        if not tok:
            sys.exit("Chybi --token nebo --token-file.")
        if not tok.startswith(("github_pat_", "ghp_", "gho_")):
            print("!! Varovani: token nezacina github_pat_ ani ghp_ - opravdu spravny?")
        store[a.user] = tok
        print("Ulozen token pro:", "vsechny uzivatele" if a.user == "*" else a.user)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(enc_json(store, key), open(path, "w", encoding="utf-8"))
    print("Zapsano (zasifrovano):", path)
    print("-> nahrajte tento jeden soubor na GitHub, pak staci prihlaseni PINem.")


if __name__ == "__main__":
    main()
