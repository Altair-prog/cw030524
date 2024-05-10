import pytest
from main import *
from main import mask_card_number, mask_account_number
from main import load_operations_from_json



# Mock данные
OPERATIONS = [
    {'date': '2024-05-01T00:00:00.000', 'state': 'EXECUTED', 'description': 'Перевод', 'from': '1234567890123456', 'to': '9876543210', 'operationAmount': '1000 руб.'},
    {'date': '2024-04-30T00:00:00.000', 'state': 'CANCELED', 'description': 'Покупка', 'from': '', 'to': '5432109876', 'operationAmount': '500 руб.'},
    {'date': '2024-04-29T00:00:00.000', 'state': 'EXECUTED', 'description': 'Перевод', 'from': '9876543210987654', 'to': '1234567890', 'operationAmount': '2000 руб.'},
    {'date': '2024-04-28T00:00:00.000', 'description': 'Пополнение', 'from': '', 'to': '1234567890', 'operationAmount': '3000 руб.'},
    {'date': '2024-04-27T00:00:00.000', 'state': 'EXECUTED', 'description': 'Платеж', 'from': '1111222233334444', 'to': '', 'operationAmount': '1500 руб.'}
]



# Тесты
def test_load_operations_from_json(tmp_path):
    # Создание временного JSON файла
    file_path = tmp_path / "test_operations.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(OPERATIONS, file)

    # Тестирование функции
    operations = load_operations_from_json(file_path)
    assert len(operations) == len(OPERATIONS)
    assert operations == OPERATIONS

def test_filter_executed_operations():
    # Тестирование функции
    filtered_operations = filter_executed_operations(OPERATIONS)
    assert len(filtered_operations) == 3
    assert all(operation['state'] == 'EXECUTED' for operation in filtered_operations)

def test_sort_operations_by_date():
    # Тестирование функции
    sorted_operations = sort_operations_by_date(OPERATIONS)
    assert sorted_operations[0]['date'][:10] == '2024-05-01'
    assert sorted_operations[-1]['date'][:10] == '2024-04-27'

def test_format_operation():
    # Тестирование функции
    operation = OPERATIONS[0]
    formatted_output = format_operation(operation)
    expected_date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')  # Приводим к ожидаемому формату даты
    assert formatted_output.startswith(expected_date)


def test_mask_card_number():
    # Тестирование функции
    card_number = '1234567890123456'
    masked_number = mask_card_number(card_number)
    assert masked_number == '123456******3456'  # Updated expected result


def test_mask_account_number():
    # Тестирование функции
    account_number = '1234567890'
    masked_number = mask_account_number(account_number)
    assert masked_number == '**7890'