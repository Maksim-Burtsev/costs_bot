import csv
import time
from datetime import date, datetime
from collections import defaultdict


    
def _get_buying_dict(reader: list) -> defaultdict:
    """
    Формирует словарь на основе всех покупок
    """

    res = defaultdict(int)
    for row in reader:
        name = row[0].capitalize()
        price = int(row[3])

        res[name] += price

    return res


def _get_csv_in_list() -> list:
    """
    Распаковывает cvs-файл в виде списка и убирает из него название столбцов
    """

    with open('costs.csv', 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))[1:]

    return reader


def _make_formatted_str(buying_dict: defaultdict, total_spent: int) -> str:
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


def _get_week_byings(week_num: int) -> list:
    """
    Возвращает список всех покупок за указанную неделю из cvs-файла
    """

    reader = _get_csv_in_list()

    data = []
    for row in reader:
        buy_date = datetime.strptime(row[1], '%Y-%m-%d').date()
        buy_week_num = buy_date.isocalendar().week
        if buy_week_num == week_num:
            data.append(row)

    return data


def add_buy(name: str, price: int) -> None:
    """
    Добавляет покупку в csv-файл
    """
    date_now = date.today()
    unix_time_now = time.time()

    buy = [name, date_now, unix_time_now, price]

    with open('costs.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(buy)


def get_total_spent(reader=None) -> int:
    """
    Возвращает потраченную сумму на все покупки из csv-файла
    """
    if reader is None:
        reader = _get_csv_in_list()

    total = 0
    for row in reader:
        total += int(row[3])
    return total


def get_all_statics() -> str:
    """
    Возвращает ВЕСЬ список продуктов и сумму, потраченную в виде отформатированной строки
    """

    reader = _get_csv_in_list()

    buying_dict = _get_buying_dict(reader)
    total_spent = get_total_spent()

    res = _make_formatted_str(buying_dict, total_spent)
    return res


def get_week_statics(week_num: str) -> str:
    """
    Возвращает список продуктов за указанную неделю и сумму, потраченную в виде отформатированной строки
    """

    data = _get_week_byings(week_num)

    buying_dict = _get_buying_dict(data)
    total_spent = get_total_spent(data)

    res = _make_formatted_str(buying_dict, total_spent)

    return res


def refresh_csv_file():
    """
    Очищает csv-файл
    """

    name_of_columns = ['Название', 'Дата', 'Unix-время', 'Стоимость']
    with open('costs.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(name_of_columns)



def main():
    pass    

if __name__ == '__main__':
    main()
