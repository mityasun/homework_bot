## Telegram bot для проверки статуса домашней работы на ЯндексПрактикуме.

### Возможности бота:
- Раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы.
- При обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram.
- Логгирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.

### Технологии
- Python 3.9.8<br>
- Telegram API<br>
- API

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/mityasun/homework_bot.git
```

```
cd homework_bot/
```

Создать файл .env в этой директории и укажите собственные токены:

```
PRACTICUM_TOKEN = токен Яндекс практикум.
TELEGRAM_TOKEN = токен вашего бота Telegram полученный от BotFather.
TELEGRAM_CHAT_ID = id вашего чата в Telegram.
```

Cоздать образ из Docker файла:

```
docker build -t homework_bot .
```

Запустите Docker контейнер:

```
docker run --name homework_bot homework_bot
```

### Получаем токены:

Зарегистрируйте бота в BotFather:<br>
<a href="https://t.me/BotFather" target="_blank">Регистрация бота и получение токена</a>

Получите токен в ЯндексПрактикум:<br>
<a href="https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a" target="_blank">Получить токен</a>

Получите id своего чата у бота Userinfobot:<br>
<a href="https://t.me/userinfobot" target="_blank">Получить свой id</a>


### Автор проекта:
Петухов Артем [Github](https://github.com/mityasun)