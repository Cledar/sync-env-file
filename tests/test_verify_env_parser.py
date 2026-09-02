import importlib.util
from pathlib import Path

import pytest

_VERIFY_ENV = Path(__file__).resolve().parents[1] / "examples" / "minimal-consumer" / "verify_env.py"


@pytest.fixture
def parse_dotenv():
    spec = importlib.util.spec_from_file_location("verify_env", _VERIFY_ENV)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_dotenv


def test_parse_dotenv_reads_fixture(parse_dotenv) -> None:
    fixture = Path(__file__).resolve().parent / "fixtures" / "sample.env"
    values = parse_dotenv(fixture)
    assert values["APP_API_BASE_URL"] == "https://api.example.com"
    assert values["APP_DATABASE_PASSWORD"] == "secret"
    assert "SharedAccessKey=a+b=c" in values["APP_EVENTHUB_CONNECTION_STRING"]
