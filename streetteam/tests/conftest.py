import os
import sys
from django.test import Client
import pytest

sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    yield Client()
