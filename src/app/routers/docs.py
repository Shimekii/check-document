from fastapi import APIRouter, Response, status
from app.schemas.doc import UserRequest, CheckResponse
from app.parser import compare_doc_number, compare_date, parse

router = APIRouter(
    prefix='/doc',
    tags=['doc']
)

@router.post('/check',
    response_model=CheckResponse,
    status_code=status.HTTP_200_OK,
    summary='Проверить документ',
    description='Проверяет корректность считанных данных')
def check_document(data: UserRequest) -> CheckResponse:
    doc = parse(data)
    is_valid = (
        compare_date(doc.birth_date, data.birth_date) and compare_doc_number(doc.doc_number, data.doc_number)
    )
    return CheckResponse(valid=is_valid)