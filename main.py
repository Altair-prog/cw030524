import json
from datetime import datetime

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
    return sorted(operations, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)

# Функция для форматированного вывода операции
def format_operation(operation):
    masked_from = mask_card_number(operation.get('from', ''))
    masked_to = mask_account_number(operation.get('to', ''))
    formatted_date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    return f"{formatted_date} {operation['description']}\n{masked_from} -> {masked_to}\n{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}\n"

# Функция для маскирования номера карты
def mask_card_number(card_info):
    if card_info:
        card_type, card_number = card_info.rsplit(' ', 1)
        card_number = card_number.replace(' ', '')  # Удаление пробелов из номера карты
        private_number = card_number[:6] + (len(card_number[6:-4]) * '*') + card_number[-4:]
        masked_number = ' '.join([private_number[i:i+4] for i in range(0, len(private_number), 4)])
        return f"{card_type} {masked_number}"
    else:
        return ''

# Функция для маскирования номера счета
def mask_account_number(account_info):
    if account_info:
        return f"Счет **{account_info[-4:]}"
    else:
        return ''

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
