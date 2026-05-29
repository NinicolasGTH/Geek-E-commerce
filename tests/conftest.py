import pytest
from fastapi.testclient import TestClient

import main

@pytest.fixture
def banco_temporario(tmp_path, monkeypatch):
    caminho_banco = tmp_path / "test.db"

    monkeypatch.setenv("DB_PATH", str(caminho_banco))
    main.DB_PATH = str(caminho_banco)
    main.init_db()

    yield caminho_banco

    if caminho_banco.exists():
        caminho_banco.unlink()

@pytest.fixture
def client(banco_temporario):
    main.app.dependency_overrides.clear()
    with TestClient(main.app) as test_client:
        yield test_client
    main.app.dependency_overrides.clear()
