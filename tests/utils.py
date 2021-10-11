from inspect import signature
from types import ModuleType


def check_function(scope: ModuleType, func_name: str, params_qty: int = 0):
    """Checks if scope has a function with specific name and params with qty"""
    assert hasattr(scope, func_name), (
        f'Не найдена функция `{func_name}`. '
        'Не удаляйте и не переименовывайте её.'
    )

    func = getattr(scope, func_name)

    assert callable(func), (
        f'`{func_name}` должна быть функцией'
    )

    sig = signature(func)
    assert len(sig.parameters) == params_qty, (
        f'Функция `{func_name}` должна принимать '
        'количество аргументов: {params_qty}'
    )
