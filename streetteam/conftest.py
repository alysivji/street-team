import pytest
from apps.users.tests.factories import UserFactory


@pytest.fixture
def login_user(client):
    def _login_user(user=None):
        user = user if user else UserFactory()
        client.force_login(user)
        return user

    yield _login_user


@pytest.fixture
def patcher(monkeypatch):
    """Helper to patch in the correct spot"""

    def _patcher(module_to_test, *, namespace, replacement):
        namespace_to_patch = f"{module_to_test}.{namespace}"
        monkeypatch.setattr(namespace_to_patch, replacement)
        return replacement

    yield _patcher
