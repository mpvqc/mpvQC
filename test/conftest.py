import pytest

from mpvqc.application import MpvqcApplication
from mpvqc.services import TypeMapperService


@pytest.fixture(scope="session")
def type_mapper() -> TypeMapperService:
    return TypeMapperService()


@pytest.fixture
def qt_app() -> MpvqcApplication:
    app = MpvqcApplication([])
    yield app
    app.shutdown()
