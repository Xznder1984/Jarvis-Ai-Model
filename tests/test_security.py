from jarvis_app.security import SecureVault


def test_vault_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr("jarvis_app.security.CONFIG_DIR", tmp_path)
    monkeypatch.setattr("jarvis_app.security.SECRETS_PATH", tmp_path / "secrets.bin")

    vault = SecureVault("pass")
    vault.add_api_key("openai", "abc123")

    assert vault.get_api_key("openai") == "abc123"
