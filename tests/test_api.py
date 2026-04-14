from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]


def load_module(module_name: str, file_path: Path):
    parent = str(file_path.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    for transient in ("schemas", "client", "memory", "models", "security", "database", "bootstrap"):
        sys.modules.pop(transient, None)
    spec = spec_from_file_location(module_name, file_path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_register_and_login_flow():
    auth_main = load_module("auth_service_main", ROOT / "services" / "auth-service" / "main.py")
    client = TestClient(auth_main.app)

    register_response = client.post(
        "/register",
        json={"email": "integration@example.com", "password": "password123"},
    )
    assert register_response.status_code in (200, 400)

    login_response = client.post(
        "/login",
        json={"email": "integration@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_gateway_rejects_missing_token():
    gateway_main = load_module("gateway_service_main", ROOT / "services" / "api-gateway" / "main.py")
    client = TestClient(gateway_main.app)
    response = client.post("/chat", json={"message": "hello"})
    assert response.status_code == 401
