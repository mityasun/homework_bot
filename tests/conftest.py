import sys
import os
from os.path import dirname
from os.path import abspath


root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

os.environ['PRACTICUM_TOKEN'] = ''
os.environ['TELEGRAM_TOKEN'] = ''
os.environ['TELEGRAM_CHAT_ID'] = ''

pytest_plugins = [
    'tests.fixtures.fixture_data'
]
