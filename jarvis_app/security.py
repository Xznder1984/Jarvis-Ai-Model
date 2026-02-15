from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from hashlib import pbkdf2_hmac, sha256
from pathlib import Path
from typing import Any


CONFIG_DIR = Path.home() / ".jarvis"
SECRETS_PATH = CONFIG_DIR / "secrets.bin"


@dataclass
class SecretRecord:
    provider: str
    encrypted_key: str
    digest: str


class SecureVault:
    """Stores API keys in an encrypted binary file with random salt+hash digest."""

    def __init__(self, master_password: str) -> None:
        self.master_password = master_password.encode("utf-8")
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def _derive_key(self, salt: bytes) -> bytes:
        return pbkdf2_hmac("sha256", self.master_password, salt, 390000, dklen=32)

    @staticmethod
    def _xor_stream(data: bytes, key: bytes) -> bytes:
        return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

    def _encrypt(self, plaintext: str, salt: bytes) -> str:
        key = self._derive_key(salt)
        encrypted = self._xor_stream(plaintext.encode("utf-8"), key)
        return base64.b64encode(encrypted).decode("utf-8")

    def _decrypt(self, ciphertext: str, salt: bytes) -> str:
        key = self._derive_key(salt)
        raw = base64.b64decode(ciphertext)
        decrypted = self._xor_stream(raw, key)
        return decrypted.decode("utf-8")

    def _load_raw(self) -> dict[str, Any]:
        if not SECRETS_PATH.exists():
            return {"salt": None, "records": []}
        raw = SECRETS_PATH.read_bytes()
        return json.loads(raw.decode("utf-8"))

    def _save_raw(self, obj: dict[str, Any]) -> None:
        SECRETS_PATH.write_bytes(json.dumps(obj, indent=2).encode("utf-8"))

    def add_api_key(self, provider: str, api_key: str) -> None:
        blob = self._load_raw()
        salt_b64 = blob.get("salt")
        if not salt_b64:
            salt = os.urandom(16)
            blob["salt"] = base64.b64encode(salt).decode("utf-8")
        else:
            salt = base64.b64decode(salt_b64)

        encrypted = self._encrypt(api_key, salt)
        digest = sha256((provider + api_key).encode("utf-8") + os.urandom(8)).hexdigest()

        records = [r for r in blob.get("records", []) if r.get("provider") != provider]
        records.append({"provider": provider, "encrypted_key": encrypted, "digest": digest})
        blob["records"] = records
        self._save_raw(blob)

    def get_api_key(self, provider: str) -> str | None:
        blob = self._load_raw()
        if not blob.get("salt"):
            return None
        salt = base64.b64decode(blob["salt"])

        for record in blob.get("records", []):
            if record.get("provider") == provider:
                return self._decrypt(record["encrypted_key"], salt)
        return None
