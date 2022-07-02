class WrongResponseCode(Exception):
    """Неверный ответ API."""
    def __init__(self, text):
        self.txt = text
