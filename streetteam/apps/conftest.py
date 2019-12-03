from django.test import RequestFactory
import pytest


# TODO this is not being used properly
# test client is slow... this is fast, but requires us to test view
# so we have to do it a bit differently
@pytest.fixture(name="request_factory")
def client():
    """Django Test Client"""
    yield RequestFactory()


@pytest.fixture
def patcher(monkeypatch):
    """Helper to patch in the correct spot"""

    def _patcher(module_to_test, *, namespace, replacement):
        namespace_to_patch = f"{module_to_test}.{namespace}"
        monkeypatch.setattr(namespace_to_patch, replacement)
        return replacement

    yield _patcher
