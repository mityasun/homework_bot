import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import WrongResponseCode

load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляет сообщение в telegram."""
    try:
        logging.info('Начало отправки статуса в telegram')
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
    except telegram.error.TelegramError(message) as error:
        raise Exception(error)


def get_api_answer(current_timestamp):
    """Отправляем запрос к API и получаем список домашних работ.
    Также проверяем, что эндпоинт отдает статус 200.
    """
    timestamp = current_timestamp or int(time.time())
    params_request = {
        'url': ENDPOINT,
        'headers': HEADERS,
        'params': {'from_date': timestamp},
    }
    logging.info('Начало запроса к API')
    try:
        response = requests.get(**params_request)
        if response.status_code != HTTPStatus.OK:
            raise WrongResponseCode(
                f'Ответ API не возвращает 200. '
                f'Код ответа: {response.status_code}.Причина: {response.reason}.'
            )
        return response.json()
    except Exception as error:
        raise WrongResponseCode(error)


def check_response(response):
    """Проверяет ответ API на корректность.
    В качестве параметра функция получает ответ API,
    приведенный к типам данных Python.
    Если ответ API соответствует ожиданиям,
    то функция должна вернуть список домашних работ (он может быть и пустым),
    доступный в ответе API по ключу 'homeworks'
    """
    logging.info('Проверка ответа API на корректность')
    if not isinstance(response, dict):
        raise TypeError('Ответ API не является dict')
    if 'homeworks' not in response or 'current_date' not in response:
        raise KeyError('Нет ключа homeworks в ответе API')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise KeyError('homeworks не является list')
    return homeworks


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус этой работы.
    В случае успеха, функция возвращает подготовленную для отправки
    в Telegram строку.
    """
    logging.info('Проводим проверки и извлекаем статус работы')
    if 'homework_name' not in homework:
        raise KeyError('Нет ключа homework_name в ответе API')
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(f'Неизвестный статус работы - {homework_status}')
    return ('Изменился статус проверки работы "{homework_name}". {verdict}'
            ).format(homework_name=homework_name,
                     verdict=HOMEWORK_VERDICTS[homework_status]
                     )


def check_tokens():
    """Проверяем, что есть все токены.
    Если нет хотя бы одного, то останавливаем бота.
    """
    logging.info('Проверка наличия всех токенов')
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        message = 'Отсутствует токен. Бот остановлен!'
        logging.critical(message)
        sys.exit(message)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    send_message(bot, 'Бот начал работу')
    logging.info('Бот начал работу')
    current_report = {}
    prev_report = {}

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            current_timestamp = response.get(current_timestamp)
            for homework in homeworks:
                homework_status = parse_status(homeworks[0])
                send_message(bot, homework_status)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message, exc_info=True)
            send_message(bot, message)

        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='main.log',
        filemode='a',
        encoding='UTF-8',
        format='%(asctime)s, %(levelname)s, %(funcName)s, '
               '%(lineno)s, %(message)s, %(name)s'
    )
    handler_console = logging.StreamHandler(stream=sys.stdout)
    handler_console.setFormatter(
        logging.Formatter('%(asctime)s, %(levelname)s, %(funcName)s, '
                          '%(lineno)s, %(message)s, %(name)s')
    )
    main()
