import os
import sys
from os.path import abspath, dirname

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

os.environ['PRAKTIKUM_TOKEN'] = ''
os.environ['TELEGRAM_TOKEN'] = ''
os.environ['TELEGRAM_CHAT_ID'] = ''
os.environ['CHAT_ID'] = ''

pytest_plugins = [
    'tests.fixtures.fixture_data'
]
