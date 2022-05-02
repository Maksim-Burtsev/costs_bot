import json
import os

import requests
from tabulate import tabulate
from dotenv import load_dotenv


load_dotenv()
URL_GET = os.getenv('URL_GET')
URL_CREATE = os.getenv('URL_CREATE')


def _get_data_from_api(month=None, week_number=None) -> list:
    """
    Делает запрос к API и получает данные
    """
    if month:
        response = requests.get(f'{URL_GET}?month={month}')
    elif week_number:
        response = requests.get(f'{URL_GET}?week_number={week_number}')
    else:
        response = requests.get(URL_GET)

    data = json.loads(response.text)
    data = [i for i in sorted(data, key=lambda x:x['cost'], reverse=True)]

    total = _get_total_spent(data)

    return (data, total)


def _get_total_spent(data: list[dict]) -> int:
    """
    Считает общую сумму покупок
    """
    return sum([buy['cost'] for buy in data])


def _format_message(data: list, total: int) -> str:
    """
    Форматирует сообщение для отправки
    """

    data_list = [[i['name'], f"{i['cost']} руб."] for i in data]

    res = tabulate(data_list, tablefmt='tsv')

    res += '\n' + '—'*17 + f'\nИТОГ {total} руб.'
    return res


def get_static(month=None, week_number=None) -> str:
    """
    Возвращает список покупок за месяц и считает сумму
    """
    data, total = _get_data_from_api(month, week_number)

    return _format_message(data, total)


def add_buy(name: str, price: int) -> bool:
    """
    Делает запрос для добавления данных
    """

    data = {
        'name': name,
        'price': price
    }

    response = requests.post(URL_CREATE, json=data)
    if response.status_code == 201:
        return True
    return False


if __name__ == '__main__':
    print(get_static(week_number=17))
    add_buy('амилопептин', 500)
