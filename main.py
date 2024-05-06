import json

# Функция для чтения данных из файла JSON
def load_operations_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Функция для фильтрации операций по статусу EXECUTED
def filter_executed_operations(operations):
    return [operation for operation in operations if operation.get('state') == 'EXECUTED']

# Функция для сортировки операций по дате
def sort_operations_by_date(operations):
    return sorted(operations, key=lambda x: x['date'], reverse=True)

# Функция для форматированного вывода операции
def format_operation(operation):
    masked_from = mask_card_number(operation.get('from', ''))
    masked_to = mask_account_number(operation.get('to', ''))
    return f"{operation['date']} {operation['description']}\n{masked_from} -> {masked_to}\n{operation['operationAmount']}\n"

# Функция для маскирования номера карты
def mask_card_number(card_number):
    return f"{' '.join(card_number[:6])} XX** **** {' '.join(card_number[-4:])}" if card_number else ''

# Функция для маскирования номера счета
def mask_account_number(account_number):
    return f"**{account_number[-4:]}" if account_number else ''

# Основная функция
def main():
    # Загрузка данных из файла JSON
    operations = load_operations_from_json('operations.json')

    # Фильтрация и сортировка операций
    executed_operations = filter_executed_operations(operations)
    sorted_operations = sort_operations_by_date(executed_operations)

    # Вывод последних пяти операций:
    for operation in sorted_operations[:5]:
        print(format_operation(operation))

if __name__ == "__main__":
    main()
