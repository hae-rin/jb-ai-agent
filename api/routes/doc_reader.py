import base64
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
from api.gemini import generate, generate_with_file, extract

router = APIRouter()

def tone(user_type: str) -> str:
    if user_type == "고령층":
        return "고객님은 고령층입니다. 매우 쉬운 말로 설명하고, 어려운 금융 용어는 반드시 일상 언어로 풀어서 설명하세요. 문장은 짧고 명확하게."
    elif user_type == "금융 초보자":
        return "고객님은 금융 초보자입니다. 금융 용어가 나올 때마다 괄호 안에 간단히 설명을 덧붙이세요. 친근하고 교육적인 톤으로."
    return "고객님은 일반 사용자입니다. 표준 금융 언어를 사용하되 핵심을 명확하게."


SYSTEM_PROMPT_TEMPLATE = """당신은 금융 문서 해설 AI입니다.
{user_tone}

문서 유형: {doc_type}

문서 유형: {doc_type}

고객을 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

한줄요약:
(문서 전체를 한 문장으로 요약)

쉬운설명:
(쉽게 말하면 형식으로. 3~5문장. 일상 비유 활용)

핵심내용:
(꼭 알아야 할 내용. 번호 목록 3~5가지)

주의사항:
(조심해야 할 내용. 없으면 "특별한 주의사항 없음". 번호 목록)"""


@router.post("/doc-reader")
async def analyze(
    doc_type: str = Form("보험 약관"),
    user_type: str = Form("일반 사용자"),
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(doc_type=doc_type, user_tone=tone(user_type))
    try:
        if file:
            file_bytes = await file.read()
            b64 = base64.standard_b64encode(file_bytes).decode("utf-8")
            contents = [
                {"inline_data": {"mime_type": file.content_type, "data": b64}},
                system_prompt,
            ]
            result = generate_with_file(contents)
        elif text:
            result = generate(system_prompt + f"\n\n분석할 문서:\n{text}")
        else:
            raise HTTPException(status_code=400, detail="파일 또는 텍스트를 제공해주세요.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "summary": extract("한줄요약", result),
        "easy":    extract("쉬운설명", result),
        "key":     extract("핵심내용", result),
        "caution": extract("주의사항", result),
    }
