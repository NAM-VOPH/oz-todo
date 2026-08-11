# -*- coding: utf-8 -*-
"""
ozcrypto.py - sifrovani dat (musi presne odpovidat crypto casti v index.html).

Schema:
  K   = nahodny 256bit datovy klic (spolecny pro vsechna data)
  KEK = PBKDF2-SHA256(pin, salt_uzivatele, ITERS) -> AES-256
  keys.json obsahuje pro kazdeho uzivatele salt + K zasifrovany jeho KEK
  soubory dat = {"v":1,"iv":<b64>,"ct":<b64>} , AES-GCM(K)
"""
import base64, json, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERS = 600000
b64e = lambda b: base64.b64encode(b).decode()
b64d = lambda s: base64.b64decode(s)


def derive_kek(pin: str, salt: bytes, iters: int = ITERS) -> bytes:
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                      salt=salt, iterations=iters).derive(pin.encode())


def enc_bytes(data: bytes, key: bytes) -> dict:
    iv = os.urandom(12)
    return {"v": 1, "iv": b64e(iv), "ct": b64e(AESGCM(key).encrypt(iv, data, None))}


def dec_bytes(blob: dict, key: bytes) -> bytes:
    return AESGCM(key).decrypt(b64d(blob["iv"]), b64d(blob["ct"]), None)


def enc_json(obj, key: bytes) -> dict:
    return enc_bytes(json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode(), key)


def dec_json(blob: dict, key: bytes):
    return json.loads(dec_bytes(blob, key).decode())


def make_keys(datakey: bytes, users: dict, iters: int = ITERS) -> dict:
    """users = {"NAM": {"pin":"1002","role":"admin"}, ...} -> obsah keys.json"""
    out = {"v": 1, "kdf": "PBKDF2-SHA256", "iters": iters, "users": {}}
    for name, u in users.items():
        salt = os.urandom(16)
        kek = derive_kek(u["pin"], salt, iters)
        out["users"][name] = {"role": u.get("role", "oz"), "salt": b64e(salt),
                              "wrapped": enc_bytes(datakey, kek)}
    return out


def unwrap(keys: dict, name: str, pin: str) -> bytes:
    u = keys["users"][name]
    kek = derive_kek(pin, b64d(u["salt"]), keys.get("iters", ITERS))
    return dec_bytes(u["wrapped"], kek)
