from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    birth_date: str = Field(
        description='Дата рождения',
        examples=['22.08.1977'],
        pattern=r"\d{2}\.\d{2}\.\d{4}"
    )
    doc_number: str = Field(
        description='Номер документа',
        examples=['0525 185673']
    )
    mrz: str = Field(
        description='Машиночитаемая запись',
        examples=['PNRUSIVANOV<<IVAN<<IVANOVICH<<<<<<<<<<<<<<<<', '0521856730RUS7708220M4510220<<<<<<<<<<<<<<44']
    )

class CheckResponse(BaseModel):
    valid: bool

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

    doc_number_check: int = Field(
        description='Контрольное число для номера документа',
        examples=['0'],
    )

    nationality: str = Field(
        description='Гражданство',
        examples=['RUS'],
    )

    birth_date: int = Field(
        description='Дата рождения формата YYMMDD',
        examples=['770822']
    )

    birth_date_check: int = Field(
        description='Контрольное число для даты рождения',
        examples=['0']
    )

    sex: str = Field(
        description='Пол',
        examples=['M', 'F'],
        pattern=r'[MF<]'
    )

    expiry_date: int = Field(
        description='Дата окончания действия документа формата YYMMDD',
        examples=['451022']
    )

    expiry_date_check: int = Field(
        description='Контрольное число для даты окончания действия документа',
        examples=['0']
    )

    personal_code: int | None = Field(
        description='Персональный код, может быть пустым',
        examples=['', '1120322770122']
    )

    personal_code_check: int = Field(
        description='Контрольное число для персонального кода',
        examples=['0']
    )

    end_check: int = Field(
        description='Конечное контрольное число',
        examples=['0']
    )