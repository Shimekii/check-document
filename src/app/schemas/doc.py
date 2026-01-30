from pydantic import BaseModel, Field, field_validator

class UserRequest(BaseModel):
    birth_date: str = Field(
        description='Дата рождения',
        examples=['22.08.1977'],
        pattern=r"\d{2}\.\d{2}\.\d{4}"
    )
    doc_number: str = Field(
        description='Номер документа',
        examples=['0525 185673'],
        pattern=r"\d{4} \d{6}"
    )
    mrz: str = Field(
        description='Машиночитаемая запись',
        examples=['PNRUSIVANOV<<IVAN<<IVANOVICH<<<<<<<<<<<<<<<<\n05251856730RUS7708220M4510220<<<<<<<<<<<<<44'],
        min_length=89,
        max_length=90
    )

class CheckResponse(BaseModel):
    result: bool

class Document(BaseModel):
    doc_type: str = Field(
        description="Тип документа",
        examples=['PN'],
    )

    country: str = Field(
        description='Страна',
        examples=['RUS'],
    )

    first_name: str = Field(
        description="Имя",
        examples=['IVAN']
    )

    last_name: str = Field(
        description='Фамилия',
        examples=['IVANOV']
    )

    middle_name: str | None = Field(
        description='Отчество',
        examples=['IVANOV']
    )

    doc_number: str = Field(
        description='Номер документа',
        examples=['0525185673'],
    )

    @field_validator('doc_number')
    @classmethod
    def symbols_included_in_doc_number(cls, number: str) -> str:
        for i, num in enumerate(number):
            if not num.isdigit():
                raise ValueError(f'В номере документа должны быть только цифры. Позиции с 1 по 10. Позиция: {i+1}')
        return number

    doc_number_check: int = Field(
        description='Контрольное число для номера документа',
        examples=['0'],
    )

    nationality: str = Field(
        description='Гражданство',
        examples=['RUS'],
    )

    birth_date: str = Field(
        description='Дата рождения формата YYMMDD',
        examples=['770822']
    )

    @field_validator('birth_date')
    @classmethod
    def symbols_included_in_birth_date(cls, date: str):
        for i, sym in enumerate(date):
            if not sym.isdigit():
                raise ValueError(f"В дате рождения должны быть только цифры. Позиция с 15 по 20. Позиция с ошибкой: {i+15}")
        return date

    birth_date_check: int = Field(
        description='Контрольное число для даты рождения',
        examples=['0']
    )

    sex: str = Field(
        description='Пол',
        examples=['M', 'F'],
        pattern=r'[MF<]'
    )

    expiry_date: str = Field(
        description='Дата окончания действия документа формата YYMMDD',
        examples=['451022']
    )

    @field_validator('expiry_date')
    @classmethod
    def symbols_included_in_expiry_date(cls, date: str):
        for i, sym in enumerate(date):
            if not sym.isdigit():
                raise ValueError(f"В дате окончания срока должны быть только цифры. Позиция с 23 по 28. Позиция c ошибкой: {i+23}")
        return date

    expiry_date_check: int = Field(
        description='Контрольное число для даты окончания действия документа',
        examples=['0']
    )

    personal_code: str | None = Field(
        description='Персональный код, может быть пустым',
        examples=['', '1120322770122']
    )

    @field_validator('personal_code')
    @classmethod
    def symbols_included_in_personal_code(cls, date: str | None):
        if date is None:
            return date
        for i, sym in enumerate(date):
            if not sym.isdigit():
                raise ValueError(f"В личном коде должны быть только цифры. Позиция с 30 по 42. Позиция с ошибкой: {i+30}")
        return date

    personal_code_check: int = Field(
        description='Контрольное число для персонального кода',
        examples=['0']
    )

    end_check: int = Field(
        description='Конечное контрольное число',
        examples=['0']
    )