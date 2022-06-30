import logging
import os
import sys
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляет сообщение в telegram."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logging.info('Отправлен статус работы в telegram')
    except Exception as error:
        raise Exception(error)


def get_api_answer(current_timestamp):
    """Отправляем запрос к API и получаем список домашних работ.
    Также проверяем, что эндпоинт отдает статус 200.
    """
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(
            ENDPOINT, headers=HEADERS, params=params
        )
        status = response.status_code
        if status != 200:
            raise ConnectionError(
                f'Ответ API не возвращает 200. Код ответа: {status}'
            )
        return response.json()
    except ConnectionError as error:
        raise ConnectionError(error)


def check_response(response):
    """Проверяет ответ API на корректность.
    В качестве параметра функция получает ответ API,
    приведенный к типам данных Python.
    Если ответ API соответствует ожиданиям,
    то функция должна вернуть список домашних работ (он может быть и пустым),
    доступный в ответе API по ключу 'homeworks'
    """
    if not isinstance(response, dict):
        raise TypeError('Ответ API не является dict')
    if 'homeworks' not in response or 'current_date' not in response:
        raise KeyError('Нет ключа homeworks в ответе API')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError('homeworks не является list')
    return homeworks


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус этой работы.
    В случае успеха, функция возвращает подготовленную для отправки
    в Telegram строку.
    """
    if 'homework_name' not in homework:
        raise KeyError('Нет ключа homework_name в ответе API')
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_STATUSES:
        raise ValueError(f'Неизвестный статус работы - {homework_status}')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяем, что есть все токены.
    Если нет хотя бы одного, то останавливаем бота.
    """
    logging.info('Все токены есть')
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    bot_logger = logging.getLogger(__name__)
    bot_logger.setLevel(logging.INFO)
    handler_console = logging.StreamHandler(stream=sys.stdout)
    handler_console.setFormatter(
        logging.Formatter('%(asctime)s, %(levelname)s, %(message)s, %(name)s')
    )
    bot_logger.addHandler(handler_console)
    if not check_tokens():
        raise SystemError('Отсутствует токен. Бот остановлен!')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    send_message(bot, 'Бот начал работу')
    logging.info('Бот начал работу')

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            for homework in homeworks:
                homework = homeworks[0]
                homework_status = parse_status(homework)
                send_message(bot, homework_status)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message, exc_info=True)
            send_message(bot, message)
            return message

        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='main.log',
        filemode='a',
        encoding='UTF-8',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    main()
