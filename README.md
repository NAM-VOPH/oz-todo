# OZ TODO

Interní nástroj pro obchodní zástupce MujOneShop — seznam odběratelů s prioritou návštěv,
poznámkami a reklamacemi. Statická stránka na GitHub Pages, data zašifrovaná AES-256-GCM.

**Web:** https://oz.mujoneshop.cz

## Struktura

```
index.html          celá aplikace (login, tabulky, sync s GitHub API)
config.js           OWNER / REPO / branch
keys.json           salt + zabalený datový klíč pro každého uživatele (veřejné, bez PINu k ničemu)
CNAME               oz.mujoneshop.cz
data/
  customers.json    zákazníci — generuje se denně ze XLSX, jen ke čtení    (zašifrováno)
  tasks.json        otevřené poznámky a reklamace — zapisuje aplikace       (zašifrováno)
  completed.json    dokončené úkoly                                         (zašifrováno)
  overrides.json    ruční změny obchodního zástupce                         (zašifrováno)
  files/            přílohy, ukládané jako <soubor>.enc                     (zašifrováno)
scripts/
  psc_okres.py      PSČ -> okres -> kraj
  build_db.py       XLSX -> customers.json (skupiny, priority, obraty)
  ozcrypto.py       šifrování, shodné se schématem v index.html
  init_crypto.py    jednorázové nastavení / změna PINu
  publish.py        denní aktualizace: přepočítá a nahraje customers.json
```

## Šifrování

Náhodný 256bitový datový klíč `K` šifruje všechna data v `data/`.
`K` je v `keys.json` uložen zvlášť pro každého uživatele, zabalený klíčem
`PBKDF2-SHA256(PIN, salt, 600 000)`. Přihlášení = rozbalení `K` PINem.
`K` v čitelné podobě existuje jen v `.oz-secrets/datakey.txt` mimo repozitář
(potřebuje ho denní skript) a v paměti prohlížeče po přihlášení.

## Denní aktualizace

```bash
export GITHUB_TOKEN=github_pat_...
python3 scripts/publish.py --owner yamem102 --repo oz-todo \
  --datakey "../.oz-secrets/datakey.txt" \
  --odberatele "../data odberatele.xlsx" \
  --prodeje    "../data prodeje.xlsx"
```

Návod pro uživatele: `../HUONG-DAN-OZ-TODO.md`
