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


@pytest.fixture
def api_url():
    return 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
