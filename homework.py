import logging

...

PRACTICUM_TOKEN = ...
TELEGRAM_TOKEN = ...
CHAT_ID = ...

...

RETRY_TIME = 300
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена, в ней нашлись ошибки.'
}


def send_message(bot, message):
    ...


def get_api_answer(url, current_timestamp):
    ...


def parse_status(homework):
    verdict = ...
    ...

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_response(response):
    homeworks = response.get('homeworks')
    ...


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    ...
    while True:
        try:
            ...
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
            time.sleep(RETRY_TIME)
            continue


if __name__ == '__main__':
    main()
