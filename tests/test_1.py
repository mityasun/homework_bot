from inspect import signature
import requests
import telegram


class MockResponseGET:

    def __init__(self, url, params=None, random_sid=None, **kwargs):
        assert url.startswith('https://praktikum.yandex.ru/api/user_api/homework_statuses'), \
            'Проверьте, что вы делаете запрос на правильный ресурс API для запроса статуса домашней работы'
        assert 'headers' in kwargs, 'Проверьте, что вы передали загаловки `headers` для запроса статуса домашней работы'
        assert 'Authorization' in kwargs['headers'], \
            'Проверьте, что в параметрах `headers` для запроса статуса домашней работы добавили Authorization'
        assert kwargs['headers']['Authorization'].startswith('OAuth '), \
            'Проверьте,что в параметрах `headers` для запроса статуса домашней работы Authorization начинается с OAuth'
        assert params is not None, \
            'Проверьте, что передали параметры `params` для запроса статуса домашней работы'
        assert 'from_date' in params, \
            'Проверьте, что в параметрах `params` для запроса статуса домашней работы `from_date`'
        assert params['from_date'] == 234435234,\
            'Проверьте, что в параметрах `params` для запроса статуса домашней работы `from_date` передаете timestamp'
        self.random_sid = random_sid

    def json(self):
        data = {
            "homeworks": [],
            "current_date": self.random_sid
        }
        return data


class MockTelegramBot:

    def __init__(self, token=None, random_sid=None, **kwargs):
        assert token is not None, 'Проверьте, что вы передали токен бота Telegram'
        self.random_sid = random_sid

    def send_message(self, chat_id=None, text=None, **kwargs):
        assert chat_id is not None, 'Проверьте, что вы передали chat_id= при отправки сообщения ботом Telegram'
        assert text is not None, 'Проверьте, что вы передали text= при отправки сообщения ботом Telegram'
        return self.random_sid


class TestHomework:

    def test_send_message(self, monkeypatch, random_sid):

        def mock_telegram_bot(*args, **kwargs):
            return MockTelegramBot(*args, random_sid=random_sid, **kwargs)

        monkeypatch.setattr(telegram, "Bot", mock_telegram_bot)

        import homework

        assert hasattr(homework, 'send_message'), 'Функция `send_message()` не существует. Не удаляйте её.'
        assert hasattr(homework.send_message, '__call__'), 'Функция `send_message()` не существует. Не удаляйте её.'
        assert len(signature(homework.send_message).parameters) == 1, \
            'Функция `send_message()` должна быть с одним параметром.'

        result = homework.send_message('Test_message_check')
        assert result == random_sid, \
            'Проверьте, что вы возвращаете в функции send_message() отправленное сообщение ботом bot.send_message()'

    def test_get_homework_statuses(self, monkeypatch, random_sid):

        def mock_response_get(*args, **kwargs):
            return MockResponseGET(*args, random_sid=random_sid, **kwargs)

        monkeypatch.setattr(requests, 'get', mock_response_get)

        import homework

        assert hasattr(homework, 'get_homework_statuses'), \
            'Функция `get_homework_statuses()` не существует. Не удаляйте её.'
        assert hasattr(homework.get_homework_statuses, '__call__'), \
            'Функция `get_homework_statuses()` не существует. Не удаляйте её.'
        assert len(signature(homework.get_homework_statuses).parameters) == 1, \
            'Функция `get_homework_statuses()` должна быть с одним параметром.'

        result = homework.get_homework_statuses(234435234)
        assert type(result) == dict, \
            'Проверьте, что из функции get_homework_statuses() возвращается словарь'
        assert 'homeworks' in result, \
            'Проверьте, что из функции get_homework_statuses() возвращается словарь содержащий ключ homeworks'
        assert 'current_date' in result, \
            'Проверьте, что из функции get_homework_statuses() возвращается словарь содержащий ключ current_date'
        assert result['current_date'] == random_sid, \
            'Проверьте, что из функции get_homework_statuses() возращаете ответ API homework_statuses'

    def test_parse_homework_status(self, random_sid):
        test_data = {
            "id": 123,
            "status": "approved",
            "homework_name": str(random_sid),
            "reviewer_comment": "Всё нравится",
            "date_updated": "2020-02-13T14:40:57Z",
            "lesson_name": "Итоговый проект"
        }

        import homework

        assert hasattr(homework, 'parse_homework_status'), \
            'Функция `parse_homework_status()` не существует. Не удаляйте её.'
        assert hasattr(homework.parse_homework_status, '__call__'), \
            'Функция `parse_homework_status()` не существует. Не удаляйте её.'
        assert len(signature(homework.parse_homework_status).parameters) == 1, \
            'Функция `parse_homework_status()` должна быть с одним параметром.'

        result = homework.parse_homework_status(test_data)
        assert result.startswith(f'У вас проверили работу "{random_sid}"'), \
            'Проверьте, что возвращаете название домашней работы в возврате функции parse_homework_status()'
        assert result.endswith(f'Ревьюеру всё понравилось, можно приступать к следующему уроку.'), \
            'Проверьте, что возвращаете правильный вердикт для статуса approved ' \
            'в возврате функции parse_homework_status()'

        test_data['status'] = 'rejected'
        result = homework.parse_homework_status(test_data)
        assert result.startswith(f'У вас проверили работу "{random_sid}"'), \
            'Проверьте, что возвращаете название домашней работы в возврате функции parse_homework_status()'
        assert result.endswith(f'К сожалению в работе нашлись ошибки.'), \
            'Проверьте, что возвращаете правильный вердикт для статуса rejected ' \
            'в возврате функции parse_homework_status()'
