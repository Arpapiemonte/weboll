import datetime

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient


# Fixture for monkeypatch the date
@pytest.fixture
def freeze(monkeypatch):
    """Now() manager patches datetime return a fixed, settable, value
    (freezes time)

    source: https://stackoverflow.com/a/28073449
    """

    original = datetime.datetime
    FAKE_TIME = datetime.datetime(2023, 2, 22, 12, 00, 00)

    class FreezeMeta(type):
        def __instancecheck__(self, instance):
            if type(instance) == original or type(instance) == Freeze:
                return True

    class Freeze(datetime.datetime):
        __metaclass__ = FreezeMeta

        frozen: datetime.datetime

        @classmethod
        def freeze(cls, val):
            cls.frozen = val

        @classmethod
        def now(cls):
            return cls.frozen

        @classmethod
        def today(cls):
            return cls.frozen

    monkeypatch.setattr(datetime, "datetime", Freeze)
    Freeze.freeze(FAKE_TIME)
    return Freeze
