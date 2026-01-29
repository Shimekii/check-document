import pytest

from app.parser import compare_date, compare_doc_number, parse
from app.schemas.doc import UserRequest

@pytest.mark.parametrize(
        "mrz,req,answer",
        [
            ('990101', '01.01.1999', True),     # проверка с корректными данными
            ('990101', '01.01.1199', False),    # проверка с некорректными данными
            ('990101', '01.10.1999', False)     # проверка с несовпадением
        ]
)
def test_compare_date(mrz, req, answer):
    assert compare_date(mrz, req) == answer

@pytest.mark.parametrize(
        'mrz,req,answer',
        [
            ('0525185673', '0525 185673', True),    # проверка с корректными данными
            ('0525185673', '0525185673', True),     # проверка с корректными данными без пробела
            ('525185673', '0525 185673', False)     # проверка на пропущенное значение
        ]
)
def test_compare_doc_number(mrz, req, answer):
    """Проверка при корректных данных с пробелом"""
    assert compare_doc_number(mrz, req) == answer


def test_parsing():
    example_data = {
        "birth_date": "22.08.1977",
        "doc_number": "0525 185673",
        "mrz": "PNRUSIVANOV<<IVAN<<IVANOVICH<<<<<<<<<<<<<<<<\n05251856730RUS7708220M4510220<<<<<<<<<<<<<44"
    }
    parse_text = parse(UserRequest(**example_data))
    check = {
        "doc_type": "PN",
        "country": "RUS",
        "last_name": "IVANOV",
        "first_name": "IVAN",
        "middle_name": "IVANOVICH",
        "doc_number": "0525185673",
        "doc_number_check": "0",
        "nationality": "RUS",
        "birth_date": "770822",
        "birth_date_check": "0",
        "sex": "M",
        "expiry_date": "451022",
        "expiry_date_check": "0",
        "personal_code": "0000000000000",
        "personal_code_check": "4",
        "end_check": "4"
    }
    assert parse_text == check