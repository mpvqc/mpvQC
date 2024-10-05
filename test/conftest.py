import pytest

from mpvqc.application import MpvqcApplication


@pytest.fixture
def qt_app() -> MpvqcApplication:
    app = MpvqcApplication([])
    yield app
    app.shutdown()
