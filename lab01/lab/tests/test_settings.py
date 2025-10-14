from pydantic import ValidationError

from src.settings import Settings
from src.main import export_secrets
import pytest


def test_settings_load():
    export_secrets()
    settings = Settings()
    assert settings.ENVIRONMENT == "test"
    assert settings.APP_NAME == "MyApp (Test)"
    # Not a good practice to check for real secrets in tests, but for demonstration:
    assert settings.FAKE_API_KEY == "super-secret-api-key-123"


def test_settings_load_without_secret(monkeypatch):
    monkeypatch.delenv("FAKE_API_KEY", raising=False)
    with pytest.raises(ValidationError):
        Settings()
