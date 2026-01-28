import json
from fastapi import HTTPException
from app.schemas.doc import Document, UserRequest
from pydantic import ValidationError

def mrz_checksum(data):
    weights = [7, 3, 1]
    total = 0

    for i, c in enumerate(data):
        if c.isdigit():
            v = int(c)
        else:
            v = 0
        total += v * weights[i % 3]
    return str(total % 10)

# сравнение даты выдачи документа из запроса и mrz
def compare_doc_number(mrz_doc, req_doc):
    return req_doc.replace(' ', '') == mrz_doc

# сравнение даты из запроса и mrz
def compare_date(mrz_data, req_data):
    data = req_data.split('.')
    date = data[2][2:4] + data[1] + data[0]
    return mrz_data == date

def parse(request: UserRequest):
    try:
        line1, line2 = request.mrz.splitlines()
    except ValueError:
        raise ValueError("MRZ должен состоять из двух строк с разделителем \\n")

    if len(line1) < 44 or len(line2) < 44:
        raise ValueError("Каждая строка MRZ должна содержать 44 символа")


    names = line1[5:44].strip('<').split('<<')
    if len(names) < 2:
        raise ValueError("Неверный формат ФИО в MRZ")

    return {
        "doc_type": line1[0:2],
        "country": line1[2:5],
        "last_name": names[0],
        "first_name": names[1],
        "middle_name": names[2] if len(names) > 2 else None,
        "doc_number": line2[0:10],
        "doc_number_check": line2[10],
        "nationality": line2[11:14],
        "birth_date": line2[14:20],
        "birth_date_check": line2[20],
        "sex": line2[21],
        "expiry_date": line2[22:28],
        "expiry_date_check": line2[28],
        "personal_code": line2[29:42].replace('<', '0'),
        "personal_code_check": line2[42],
        "end_check": line2[43]
    }

def build_document(data: dict) -> Document:
    try:
        return Document(**data)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    'field': '.'.join(map(str, err['loc'])),
                    'message': err['msg']
                }
                for err in e.errors()
            ]
        )