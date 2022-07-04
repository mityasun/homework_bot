class WrongResponseCode(Exception):
    """Неверный ответ API."""
    pass


class NotForSend(Exception):
    """Исключение не для пересылки в telegram."""
    pass
