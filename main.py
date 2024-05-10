import json
from datetime import datetime

def load_operations_from_json(file_path):
    """Читает данные из файла JSON."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def filter_executed_operations(operations):
    """Фильтрует операции по статусу EXECUTED."""
    return [operation for operation in operations if operation.get('state') == 'EXECUTED']

def sort_operations_by_date(operations):
    """Сортирует операции по дате и времени."""
    return sorted(operations, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)

def format_operation(operation):
    """Форматирует операцию для вывода."""
    masked_from = mask_card_number(operation.get('from', ''))
    masked_to = mask_account_number(operation.get('to', ''))
    formatted_date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    amount = operation.get('operationAmount', {})
    if isinstance(amount, dict):
        formatted_amount = f"{amount.get('amount', '')} {amount.get('currency', {}).get('name', '')}"
    else:
        formatted_amount = amount
    return f"{formatted_date} {operation['description']}\n{masked_from} -> {masked_to}\n{formatted_amount}\n"

def mask_card_number(card_info):
    """Маскирует номер карты."""
    if card_info:
        if ' ' in card_info:
            card_type, card_number = card_info.rsplit(' ', 1)
            card_number = card_number.replace(' ', '')
            private_number = card_number[:6] + '*' * (len(card_number) - 10) + card_number[-4:]
            masked_number = ' '.join([private_number[i:i+4] for i in range(0, len(private_number), 4)])
            return f"{card_type} {masked_number}"
        else:
            return card_info[:6] + '*' * (len(card_info) - 10) + card_info[-4:]
    else:
        return ''

def mask_account_number(account_info):
    """Маскирует номер счета."""
    if account_info:
        return f"**{account_info[-4:]}"
    else:
        return ''

def main():
    """Основная функция."""
    operations = load_operations_from_json('operations.json')
    executed_operations = filter_executed_operations(operations)
    sorted_operations = sort_operations_by_date(executed_operations)
    for operation in sorted_operations[:5]:
        print(format_operation(operation))

if __name__ == "__main__":
    main()
