import csv
import time
from datetime import date, datetime
from collections import defaultdict


class Service:

    def __init__(self) -> None:
        self.name_of_colums = ['Название', 'Дата', 'Unix-время', 'Стоимость']
        self.filename = 'costs.csv'

    def add_buy(self, name: str, price: int) -> None:
        """
        Добавляет покупку в csv-файл
        """
        date_now = date.today()
        unix_time_now = time.time()

        buy = [name, date_now, unix_time_now, price]

        with open(self.filename, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(buy)

    def get_total_spent(self, reader=None) -> int:
        """
        Возвращает потраченную сумму на все покупки из csv-файла
        """
        if reader is None:
            reader = self._get_csv_in_list()

        total = 0
        for row in reader:
            total += int(row[3])
        return total

    def get_all_statics(self) -> str:
        """
        Возвращает ВЕСЬ список продуктов и сумму, потраченную в виде отформатированной строки
        """

        data_list = self._get_csv_in_list()

        buying_dict = self._get_buying_dict(data_list)
        total_spent = self.get_total_spent()

        res = self._make_formatted_str(buying_dict, total_spent)
        return res

    def refresh_csv_file(self):
        """
        Очищает csv-file
        """
        with open(self.filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.name_of_columns)

    def get_week_statics(self, week_num: str) -> str:
        """
        Возвращает список продуктов за указанную неделю и сумму, потраченную в виде отформатированной строки
        """

        data = self._get_week_byings(week_num)

        buying_dict = self._get_buying_dict(data)
        total_spent = self.get_total_spent(data)

        res = self._make_formatted_str(buying_dict, total_spent)

        return res

    def _get_csv_in_list(self) -> list:
        """
        Распаковывает cvs-файл в виде списка и убирает из него название столбцов
        """

        with open(self.filename, 'r', encoding='utf-8') as f:
            reader = list(csv.reader(f))[1:]

        return reader

    def _get_buying_dict(self, data: list) -> defaultdict:
        """
        Формирует словарь на основе всех покупок
        """

        res = defaultdict(int)
        for row in data:
            name = row[0].capitalize()
            price = int(row[3])

            res[name] += price

        return res

    def _make_formatted_str(self, buying_dict: defaultdict, total_spent: int) -> str:
        """
        Формирует из словаря и о отформатированную строку с отчётом о покупках
        """

        res = ''
        for name, cost in sorted(buying_dict.items(),
                                 key=lambda item: item[1], reverse=True):
            res += f'{name:12} {str(cost):>5} руб.\n'

        res += '—'*23 + '\n'
        res += f'{"Всего":12} {str(total_spent):>5} руб.'

        return res

    def _get_week_byings(self, week_num: int) -> list:
        """
        Возвращает список всех покупок за указанную неделю из cvs-файла
        """

        reader = self._get_csv_in_list()

        data = []
        for row in reader:
            buy_date = datetime.strptime(row[1], '%Y-%m-%d').date()
            buy_week_num = buy_date.isocalendar().week
            if buy_week_num == week_num:
                data.append(row)

        return data

if __name__ == '__main__':
    service = Service()
    print(service.get_week_statics(date.today().isocalendar().week))