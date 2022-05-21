import json
import os

import requests
from tabulate import tabulate
from dotenv import load_dotenv
import matplotlib.pyplot as plt


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

    def _get_labels_and_values(self) -> tuple[list, list]:
        """
        Формирует два списка: названий покупок и их стоимости на основе данных от API
        """
        labels, values = [], []
        data, _ = self._get_data_from_api()

        for buy in data:
            labels.append(buy['name'])
            values.append(buy['cost'])

        return (labels, values)

    def create_expensive_costs_pie(self) -> None:
        """
        Создаёт диаграмму на основе 10 самых дорогих покупок
        """
        labels, values = self._get_labels_and_values()
        self._create_pie(labels[:10], values[:10], 'expensive')

    def create_cheap_costs_pie(self) -> None:
        """
        Создаёт диаграмму на основе 10 самых дешёвых покупок
        """
        labels, values = self._get_labels_and_values()
        self._create_pie(labels[-10:], values[-10:], 'cheap')

    def create_all_costs_pie(self) -> None:
        """
        Создаёт диаграмму на основе всех покупок
        """
        labels, values = self._get_labels_and_values()
        self._create_pie(labels, values, 'all')


    def _create_pie(self, labels: list, values: list, filename:str) -> None:
        """
        Создаёт диаграмму
        """
        myexplode = [0.2, 0.2, 0.1, 0.1] + [0]*(len(values)-4)
        plt.pie(values, labels=labels, startangle=90, explode=myexplode)

        plt.savefig(f'pie_images/{filename}.jpg')
        plt.close()


if __name__ == '__main__':
    service = Service()
    service.create_all_costs_pie()
    service.create_cheap_costs_pie()
    service.create_expensive_costs_pie()
