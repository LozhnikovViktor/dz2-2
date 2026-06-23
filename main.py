import csv
import json


def read_csv(filename):
    """Читает CSV-файл и возвращает список словарей с данными о продажах."""
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Преобразуем числовые поля в нужный тип
            row['Price'] = float(row['Price'])
            row['Quantity'] = int(row['Quantity'])
            data.append(row)
    return data


def get_sales_by_date(data, target_date):
    """Фильтрует записи по указанной дате."""
    return [row for row in data if row['Date'] == target_date]


def find_top_store(sales):
    """
    Находит магазин с наибольшей выручкой за день.
    Выручка = Price * Quantity для каждой записи, суммируется по магазинам.
    """
    store_revenue = {}

    for row in sales:
        store = row['Store']
        revenue = row['Price'] * row['Quantity']

        if store in store_revenue:
            store_revenue[store] += revenue
        else:
            store_revenue[store] = revenue

    # Находим магазин с максимальной выручкой
    top_store = None
    max_revenue = -1

    for store, revenue in store_revenue.items():
        if revenue > max_revenue:
            max_revenue = revenue
            top_store = store

    return top_store, max_revenue


def generate_product_report(sales):
    """
    Генерирует отчёт: суммарное количество проданных единиц
    по каждому продукту за указанный день.
    """
    product_sales = {}

    for row in sales:
        product = row['Product']
        quantity = row['Quantity']

        if product in product_sales:
            product_sales[product] += quantity
        else:
            product_sales[product] = quantity

    # Формируем список словарей для JSON
    report = [
        {"product": product, "total_sales": total}
        for product, total in product_sales.items()
    ]

    return report


def save_report_to_json(report, target_date, filename):
    """Сохраняет итоговый отчёт в JSON-файл."""
    result = {target_date: report}

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    # 1. Чтение данных из CSV
    csv_filename = 'sales_data.csv'
    data = read_csv(csv_filename)

    # 2. Запрос даты у пользователя
    target_date = input("Введите дату для отчетности (формат YYYY-MM-DD): ")

    # 3. Фильтрация данных по дате
    daily_sales = get_sales_by_date(data, target_date)

    if not daily_sales:
        print(f"Нет данных за дату {target_date}")
        return

    # 4. Поиск магазина с наибольшими продажами (по выручке)
    top_store, max_revenue = find_top_store(daily_sales)

    # Выручка может быть дробной — выводим как целое, если нет остатка
    if max_revenue == int(max_revenue):
        max_revenue = int(max_revenue)

    print(f"Наибольшие продажи за {target_date}: {top_store} "
          f"с объёмом продаж {max_revenue}")

    # 5. Формирование отчёта по продуктам и сохранение в JSON
    product_report = generate_product_report(daily_sales)
    json_filename = 'sales_report.json'
    save_report_to_json(product_report, target_date, json_filename)

    print(f"Отчёт сохранён в файл {json_filename}")


if __name__ == '__main__':
    main()