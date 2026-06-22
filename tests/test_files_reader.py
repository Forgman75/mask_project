from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
import pytest

from src.files_reader import load_transactions_csv, load_transactions_excel


@patch('src.files_reader.pd.read_csv')
def test_load_csv_success(mock_read_csv):
    """Проверяет успешное чтение CSV-файла."""
    # Создаём мок DataFrame
    mock_df = pd.DataFrame({
        'id': [1, 2],
        'state': ['EXECUTED', 'CANCELED'],
        'description': ['Перевод', 'Открытие вклада']
    })
    mock_read_csv.return_value = mock_df

    result = load_transactions_csv('test.csv')

    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[0]['state'] == 'EXECUTED'
    assert result[1]['description'] == 'Открытие вклада'
    mock_read_csv.assert_called_once_with('test.csv', encoding='utf-8', sep=',')


@patch('src.files_reader.pd.read_csv')
def test_load_csv_empty(mock_read_csv):
    """CSV файл существует, но не содержит данных"""

    mock_df = MagicMock()
    mock_df.empty = True
    mock_read_csv.return_value = mock_df

    result = load_transactions_csv('data/empty.csv')
    assert result == []


@patch('src.files_reader.pd.read_csv')
def test_load_csv_error(mock_read_csv):
    """Ошибка при чтении CSV (файл не найден)"""
    mock_read_csv.side_effect = FileNotFoundError("Файл отсутствует")
    result = load_transactions_csv('data/missing.csv')
    assert result == []


@patch('src.files_reader.pd.read_csv')
def test_load_csv_with_missing_values(mock_read_csv):
    """Проверяет обработку пропущенных значений (NaN -> None)."""
    # DataFrame с NaN значениями
    mock_df = pd.DataFrame({
        'id': [1, 2],
        'state': ['EXECUTED', np.nan],
        'description': [np.nan, 'Открытие вклада']
    })
    mock_read_csv.return_value = mock_df

    result = load_transactions_csv('test.csv')

    assert len(result) == 2
    assert result[0]['state'] == 'EXECUTED'
    assert result[0]['description'] is None  # NaN заменён на None
    assert result[1]['state'] is None  # NaN заменён на None
    assert result[1]['description'] == 'Открытие вклада'


@patch('src.files_reader.pd.read_csv')
def test_load_csv_with_semicolon_separator(mock_read_csv):
    """Проверяет чтение CSV с разделителем ';'."""
    mock_df = pd.DataFrame({
        'id': [1, 2],
        'state': ['EXECUTED', 'CANCELED']
    })
    mock_read_csv.return_value = mock_df

    result = load_transactions_csv('test.csv', sep=';')

    assert len(result) == 2
    mock_read_csv.assert_called_once_with('test.csv', encoding='utf-8', sep=';')


@patch('src.files_reader.pd.read_csv')
def test_load_csv_with_tab_separator(mock_read_csv):
    """Проверяет использование табуляции как разделителя."""
    mock_df = pd.DataFrame({'id': [1]})
    mock_read_csv.return_value = mock_df

    load_transactions_csv('test.csv', sep='\t')

    mock_read_csv.assert_called_once_with('test.csv', encoding='utf-8', sep='\t')


@patch('src.files_reader.pd.read_csv')
def test_load_csv_parser_error(mock_read_csv):
    """Проверяет обработку ошибки парсинга."""
    mock_read_csv.side_effect = pd.errors.ParserError("Parser error")

    result = load_transactions_csv('invalid.csv')

    assert result == []

@patch('src.files_reader.pd.read_csv')
def test_load_csv_generic_exception(mock_read_csv):
    """Проверяет обработку непредвиденной ошибки."""
    mock_read_csv.side_effect = Exception("Unexpected error")

    result = load_transactions_csv('test.csv')

    assert result == []

@patch('src.files_reader.pd.read_csv')
def test_load_csv_with_pd_na(mock_read_csv):
    """Проверяет замену pd.NA на None."""
    mock_df = pd.DataFrame({
        'id': [1, 2],
        'state': ['EXECUTED', pd.NA]
    })
    mock_read_csv.return_value = mock_df

    result = load_transactions_csv('test.csv')

    assert result[1]['state'] is None

@patch('src.files_reader.pd.read_csv')
def test_load_csv_custom_encoding(mock_read_csv):
    """Проверяет использование кастомной кодировки."""
    mock_df = pd.DataFrame({'id': [1]})
    mock_read_csv.return_value = mock_df

    load_transactions_csv('test.csv', encoding='cp1251')

    mock_read_csv.assert_called_once_with('test.csv', encoding='cp1251', sep=',')


@patch('src.files_reader.pd.read_excel')
def test_load_excel_success(mock_read_excel):
    """Успешное чтение Excel: возвращает список словарей"""
    expected = [{'id': 2, 'amount': 500.0, 'currency': 'USD'}]
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.replace.return_value.to_dict.return_value = expected
    
    # Настраиваем len() чтобы возвращал правильное значение
    mock_df.__len__ = MagicMock(return_value=len(expected))

    mock_read_excel.return_value = mock_df

    result = load_transactions_excel('data/test.xlsx')
    assert result == expected
    mock_read_excel.assert_called_once_with('data/test.xlsx')


@patch('src.files_reader.pd.read_excel')
def test_load_excel_empty(mock_read_excel):
    """Excel файл существует, но не содержит данных"""
    mock_df = MagicMock()
    mock_df.empty = True
    mock_read_excel.return_value = mock_df

    result = load_transactions_excel('data/empty.xlsx')
    assert result == []



def test_load_csv_real_file_with_comma(tmp_path):
        """Тест с реальным CSV-файлом (запятая)."""
        csv_file = tmp_path / "ops.csv"
        csv_file.write_text(
            "id,state,description\n"
            "1,EXECUTED,Перевод\n"
            "2,CANCELED,Открытие вклада\n",
            encoding="utf-8",
        )

        result = load_transactions_csv(str(csv_file))

        assert len(result) == 2
        assert result[0]['state'] == 'EXECUTED'

def test_load_csv_real_file_with_semicolon(tmp_path):
    """Тест с реальным CSV-файлом (точка с запятой)."""
    csv_file = tmp_path / "ops.csv"
    csv_file.write_text(
        "id;state;description\n"
        "1;EXECUTED;Перевод\n"
        "2;CANCELED;Открытие вклада\n",
        encoding="utf-8",
    )

    # Для pandas версии
    result = load_transactions_csv(str(csv_file), sep=';')
        
    assert len(result) == 2


def test_load_csv_with_missing_values_does_not_raise(tmp_path):
    """
    Проверяет, что функция НЕ падает с ошибкой:
    'ValueError: Must specify a fill value or method'
    когда в CSV есть пустые ячейки.
    """
    csv_file = tmp_path / "ops.csv"
    # Пустые ячейки между запятыми — pandas прочитает их как NaN
    csv_file.write_text(
        "id,state,date,description,amount\n"
        "1,EXECUTED,2019-12-08,Перевод,100\n"
        "2,EXECUTED,,Перевод организации,\n"   # ← пустые date и amount
        "3,,2019-11-12,,500\n"                 # ← пустые state и description
        ",CANCELED,2019-10-01,Открытие вклада,200\n",  # ← пустой id
        encoding="utf-8",
    )

    # Если функция содержит fillna(None) — здесь упадёт ValueError
    result = load_transactions_csv(str(csv_file))

    # Проверяем, что данные прочитаны
    assert len(result) == 4
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)


import pytest
import pandas as pd
from src.files_reader import load_transactions_excel


def test_load_excel_with_missing_values_does_not_raise(tmp_path):
    """
    Проверяет, что функция НЕ падает с ошибкой:
    'ValueError: Must specify a fill value or method'
    когда в Excel есть пустые ячейки.
    """
    excel_file = tmp_path / "ops.xlsx"
    
    # Создаём DataFrame с пустыми значениями (NaN)
    df = pd.DataFrame({
        "id": [1, 2, 3, None],
        "state": ["EXECUTED", "EXECUTED", None, "CANCELED"],
        "date": ["2019-12-08", None, "2019-11-12", "2019-10-01"],
        "description": ["Перевод", "Перевод организации", None, "Открытие вклада"],
        "amount": [100, None, 500, 200],
    })
    
    # Сохраняем в Excel-файл
    df.to_excel(str(excel_file), index=False, engine="openpyxl")
    
    # Если функция содержит fillna(None) — здесь упадёт ValueError
    result = load_transactions_excel(str(excel_file))
    
    # Проверяем, что данные прочитаны
    assert len(result) == 4
    assert isinstance(result, list)
    assert all(isinstance(row, dict) for row in result)
    
    # Проверяем, что пустые значения превратились в None
    assert result[1]["date"] is None
    assert result[1]["amount"] is None
    assert result[2]["state"] is None
    assert result[2]["description"] is None
    assert result[3]["id"] is None