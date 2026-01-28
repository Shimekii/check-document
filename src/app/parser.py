import json
from app.schemas.doc import Document, UserRequest

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
    return mrz_data == int(date)

def parse(request: UserRequest):
    line1, line2 = request.mrz.splitlines()

    # чтение первой строки
    doc_type = line1[0:2]
    country = line1[2:5]
    names = line1[5:44].strip('<').split('<<')
    last_name = names[0]
    first_name = names[1]
    middle_name = names[2]

    #чтение второй строки
    doc_number = line2[0:10]
    doc_check = line2[10]
    nationality = line2[11:14]
    birth_date = line2[14:20]
    birth_date_check = line2[20]
    sex = line2[21]
    expiry_date = line2[22:28]
    expiry_date_check = line2[28]
    personal_code = line2[29:42]
    personal_code = personal_code.replace('<', '0')
    personal_code_check = line2[42]
    end_check = line2[43]
    return Document(
        doc_type=doc_type, country=country, first_name=first_name, last_name=last_name, middle_name=middle_name,
        doc_number=doc_number, doc_number_check=doc_check, nationality=nationality, birth_date=birth_date,
        birth_date_check=birth_date_check, sex=sex, expiry_date=expiry_date, expiry_date_check=expiry_date_check,
        personal_code=personal_code, personal_code_check=personal_code_check, end_check=end_check
    )
