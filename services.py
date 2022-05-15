import json
import os

import requests
from tabulate import tabulate
from dotenv import load_dotenv


class Service:

    def __init__(self) -> None:
        load_dotenv()
        self.URL_GET = os.getenv('URL_GET')
        self.URL_CREATE = os.getenv('URL_CREATE')

    def _get_data_from_api(self, month=None, week_number=None) -> tuple[list, int]:
        """
        Делает запрос к API и возвращает отсортированные данные с общей суммой
        """
        if month:
            response = requests.get(f'{self.URL_GET}?month={month}')
        elif week_number:
            response = requests.get(
                f'{self.URL_GET}?week_number={week_number}')
        else:
            response = requests.get(self.URL_GET)

        data = json.loads(response.text)
        data = [i for i in sorted(data, key=lambda x:x['cost'], reverse=True)]

        total = self._get_total_spent(data)

        return (data, total)

    def _get_total_spent(self, data: list[dict]) -> int:
        """
        Считает общую сумму покупок
        """
        return sum([buy['cost'] for buy in data])

    def _format_message(self, data: list, total: int) -> str:
        """
        Форматирует сообщение для отправки
        """
        data_list = [[i['name'], f"{i['cost']} руб."] for i in data]

        res = tabulate(data_list, tablefmt='tsv')

        res += '\n' + '—'*17 + f'\nИТОГ {total} руб.'
        return res

    def get_static(self, month=None, week_number=None) -> str:
        """
        Возвращает список покупок за месяц и считает сумму
        """
        data, total = self._get_data_from_api(month, week_number)

        return self._format_message(data, total)

    def add_buy(self, name: str, price: int) -> bool:
        """
        Делает запрос для добавления данных
        """
        data = {
            'name': name,
            'price': price
        }

        response = requests.post(self.URL_CREATE, json=data)
        if response.status_code == 201:
            return True
        return False
