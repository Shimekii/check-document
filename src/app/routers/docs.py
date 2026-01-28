from fastapi import APIRouter, Body, status, HTTPException
from app.schemas.doc import UserRequest, CheckResponse, Document
from app.parser import compare_doc_number, compare_date, parse, build_document

router = APIRouter(
    prefix='/doc',
    tags=['doc']
)

@router.post('/check',
    response_model=CheckResponse,
    status_code=status.HTTP_200_OK,
    summary='Проверить документ',
    description='Проверяет корректность считанных данных')
def check_document(data: UserRequest = Body(...)) -> CheckResponse:
    mrz_metadata = parse(data)
    doc = build_document(mrz_metadata)
    is_valid = (
        compare_date(doc.birth_date, data.birth_date) and compare_doc_number(doc.doc_number, data.doc_number)
    )
    return CheckResponse(valid=is_valid)