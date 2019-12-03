from django.test import Client
import pytest


# TODO: use RequestFactory
# test client is slow... this is fast, but requires us to test view
# so we have to do it a bit differently
@pytest.fixture
def client():
    """Django Test Client"""
    yield Client()


@pytest.fixture
def patcher(monkeypatch):
    """Helper to patch in the correct spot"""

    def _patcher(module_to_test, *, namespace, replacement):
        namespace_to_patch = f"{module_to_test}.{namespace}"
        monkeypatch.setattr(namespace_to_patch, replacement)
        return replacement

    yield _patcher
