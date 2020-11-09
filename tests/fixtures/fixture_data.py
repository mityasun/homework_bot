import random
import string
from datetime import datetime

import pytest


def random_string(string_length=15):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(string_length))


@pytest.fixture
def random_sid():
    return random_string()


@pytest.fixture
def current_timestamp():
    return datetime.now().timestamp()
