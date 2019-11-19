from django.test import RequestFactory
import pytest


@pytest.fixture
def client():
    yield RequestFactory()
