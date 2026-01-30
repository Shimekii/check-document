# /healthz/live

async def test_health_returns_ok(async_client):
    responce = await async_client.get('/healthz/live')

    assert responce.status_code == 200
    assert responce.json() == {'status': 'ok'}

# /doc/check
# проверка с корректными данными
async def test_docs_check_correct_data(async_client):
    example_data = {
        "birth_date": "22.08.1977",
        "doc_number": "0525 185673",
        "mrz": "PNRUSIVANOV<<IVAN<<IVANOVICH<<<<<<<<<<<<<<<<\n05251856730RUS7708220M4510220<<<<<<<<<<<<<44"
    }
    responce = await async_client.post('/doc/check', json=example_data)

    assert responce.status_code == 200
    assert responce.json() == {'result': True}

# проверка с ошибкой в номере докумета в строке МЧЗ
async def test_docs_check_incorrect_doc_number(async_client):
    example_data = {
        "birth_date": "22.08.1977",
        "doc_number": "0525 185673",
        "mrz": "PNRUSIVANOV<<IVAN<<IVANOVICH<<<<<<<<<<<<<<<<\n052518w6730RUS7708220M4510220<<<<<<<<<<<<<44"
    }
    responce = await async_client.post('/doc/check', json=example_data)
    assert responce.status_code == 422
    resp = responce.json()
    detail = resp['detail']
    val_err = 'В номере документа должны быть только цифры. Позиции с 1 по 10. Позиция: 7'
    assert detail[0]['field'] == 'doc_number'
    assert val_err in detail[0]['message']

# проверка с ошибкой в дате рождения в строке МЧЗ
async def test_docs_check_incorrect_date_birth(async_client):
    example_data = {
        "birth_date": "22.08.1977",
        "doc_number": "0525 185673",
        "mrz": "PNRUSIVANOV<<IVAN<<IVANOVICH<<<<<<<<<<<<<<<<\n05251856730RUS7ф08220M4510220<<<<<<<<<<<<<44"
    }
    responce = await async_client.post('/doc/check', json=example_data)
    assert responce.status_code == 422
    resp = responce.json()
    detail = resp['detail']
    val_err = 'В дате рождения должны быть только цифры. Позиция с 15 по 20. Позиция с ошибкой: 16'
    assert detail[0]['field'] == 'birth_date'
    assert val_err in detail[0]['message']

# проверка с ошибкой в дате окончания действия документа в строке МЧЗ
async def test_docs_check_incorrect_expiry_date(async_client):
    example_data = {
        "birth_date": "22.08.1977",
        "doc_number": "0525 185673",
        "mrz": "PNRUSIVANOV<<IVAN<<IVANOVICH<<<<<<<<<<<<<<<<\n05251856730RUS7708220M45++220<<<<<<<<<<<<<44"
    }
    responce = await async_client.post('/doc/check', json=example_data)
    assert responce.status_code == 422
    resp = responce.json()
    detail = resp['detail']
    val_err = 'В дате окончания срока должны быть только цифры. Позиция с 23 по 28. Позиция c ошибкой: 25'
    assert detail[0]['field'] == 'expiry_date'
    assert val_err in detail[0]['message']

# проверка с ошибкой в дате окончания действия документа в строке МЧЗ
async def test_docs_check_incorrect_personal_code(async_client):
    example_data = {
        "birth_date": "22.08.1977",
        "doc_number": "0525 185673",
        "mrz": "PNRUSIVANOV<<IVAN<<IVANOVICH<<<<<<<<<<<<<<<<\n05251856730RUS7708220M4510220<<<<<<_<<<<<<44"
    }
    responce = await async_client.post('/doc/check', json=example_data)
    assert responce.status_code == 422
    resp = responce.json()
    detail = resp['detail']
    val_err = 'В личном коде должны быть только цифры. Позиция с 30 по 42. Позиция с ошибкой: 36'
    assert detail[0]['field'] == 'personal_code'
    assert val_err in detail[0]['message']