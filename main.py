import datetime
from decimal import Decimal
import re


def add(items, title, amount, expiration_date=None):
    if expiration_date is not None:
        expiration_date = datetime.date.fromisoformat(expiration_date)

    amount = Decimal(amount)

    if title in items:
        items[title].append({'amount': amount, 'expiration_date': expiration_date})
    else:
        items[title] = [{'amount': amount, 'expiration_date': expiration_date}]


def add_by_note(items, note):
    pattern = r'\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b'
    match = re.search(pattern, note)

    if match:
        date_str = match.group(0)
        note = note.replace(date_str, '', 1).strip()
    else:
        date_str = None

    note = note.split()

    quantity = None
    for word in note:
        if word.isdigit():
            quantity = int(word)
            note.remove(word)
            break

    note = ' '.join(note)

    if quantity:
        add(items, note, quantity, date_str)
    else:
        add(items, note, Decimal('1'), date_str)


def find(items, needle):
    needle = needle.lower()
    found = []
    for title, data in items.items():
        if needle in title.lower():
            found.append(title)
    return found if found else "Ничего не найдено"


def amount(items, needle):
    needle = needle.lower()
    found = []
    for title, data in items.items():
        if needle in title.lower():
            found.append(sum([item['amount'] for item in data]))
    return found if found else "Ничего не найдено"


def expire(items, in_advance_days=0):
    today = datetime.date.today()
    found = []
    if in_advance_days:
        for title, data in items.items():
            for item in data:
                if item['expiration_date'] is not None:
                    if item['expiration_date'] - today <= datetime.timedelta(days=in_advance_days) \
                            and item['expiration_date'] > today:
                        found.append(title)
                        break

    else:
        for title, data in items.items():
            for item in data:
                if item['expiration_date'] is not None:
                    if item['expiration_date'] < today:
                        found.append(title)

    return list(set(found)) if found else "Ничего не найдено"


goods = {
    'Пельмени Универсальные': [
        # Первая партия продукта 'Пельмени Универсальные':
        {'amount': Decimal('0.5'), 'expiration_date': datetime.date(2023, 7, 15)},
        # Вторая партия продукта 'Пельмени Универсальные':
        {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 1)},
    ],
    'Вода': [
        {'amount': Decimal('1.5'), 'expiration_date': None}
    ],
}


def main():
    print("Сегодняшняя дата:", datetime.date.today())
    print("Список продуктов:", goods)

    print(find(goods, "пельмени"))
    add(goods, "Фарш", Decimal('1'), "2025-07-20")
    print(find(goods, "ФАРШ"))
    add_by_note(goods, "Молоко 1 2023-07-15")
    print(find(goods, "Молоко"))
    print(amount(goods, "Молоко"))
    print(amount(goods, "пЕльмЕни"))
    print(expire(goods, 0))


if __name__ == '__main__':
    main()