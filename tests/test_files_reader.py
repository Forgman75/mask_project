from unittest.mock import MagicMock, patch

import pytest

from src.files_reader import load_transactions_csv, load_transactions_excel


@patch('src.files_reader.pd.read_csv')
def test_load_csv_success(mock_read_csv):
    """Успешное чтение CSV: возвращает список словарей"""
    expected = [{'id': 1, 'amount': 1000.0, 'currency': 'RUB'}]
    # Создаём мок DataFrame
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.fillna.return_value.replace.return_value.to_dict.return_value = expected
    mock_read_csv.return_value = mock_df

    result = load_transactions_csv('data/test.csv')
    assert result == expected
    mock_read_csv.assert_called_once_with('data/test.csv', encoding='utf-8')


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


@patch('src.files_reader.pd.read_excel')
def test_load_excel_success(mock_read_excel):
    """Успешное чтение Excel: возвращает список словарей"""
    expected = [{'id': 2, 'amount': 500.0, 'currency': 'USD'}]
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.fillna.return_value.replace.return_value.to_dict.return_value = expected
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
