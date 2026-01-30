from fastapi import APIRouter, status, Depends
from app.schemas.doc import UserRequest, CheckResponse, Document
from app.parser import compare_doc_number, compare_date, parse, build_document, gen_redis_key
from app.dependencies.redis import get_redis


router = APIRouter(
    prefix='/doc',
    tags=['doc']
)

@router.post('/check',
    response_model=CheckResponse,
    status_code=status.HTTP_200_OK,
    summary='Проверить документ',
    description='Проверяет корректность считанных данных')
async def check_document(data: UserRequest, redis_client = Depends(get_redis)) -> CheckResponse:
    # получаем ключ сформированный из запроса
    key = gen_redis_key(data)
    value = await redis_client.get(key)
    if not value:
        mrz_metadata = parse(data)
        doc = build_document(mrz_metadata)
        await redis_client.set(key, doc.model_dump_json())
    else:
        doc = Document.model_validate_json(value)
    is_valid = (
        compare_date(doc.birth_date, data.birth_date) and compare_doc_number(doc.doc_number, data.doc_number)
    )
    return CheckResponse(result=is_valid)