from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.gemini import generate, extract

router = APIRouter()


class VPRequest(BaseModel):
    content: str


@router.post("/voice-phishing")
def analyze(req: VPRequest):
    prompt = f"""당신은 금융 보이스피싱·스미싱 전문 탐지 AI입니다.

아래 내용이 보이스피싱·스미싱·금융사기인지 판단하세요.

내용:
{req.content}

판단 기준:
1. 긴급성·공포감 조성 (즉시, 동결, 수사, 체포, 미처리시 등)
2. 개인정보·금융정보 요구 (주민등록번호, 카드번호, 비밀번호 등)
3. 출처 불명 링크 포함 여부
4. 공공기관·금융기관 사칭 (검찰, 경찰, 금감원, 국민은행 등)
5. 계좌 이체·ATM 이용 유도
6. 가족에게 비밀로 하라는 요구
7. 실제 공식 기관이 절대 하지 않는 요청

고객을 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

판정: [사기/정상/주의]

위험도: [높음/보통/낮음]

발견된위험신호:
(사기 징후. 없으면 "이상 없음". 번호 목록)

쉬운설명:
(고령층도 바로 이해할 수 있는 쉬운 설명. 2~3문장)

지금해야할행동:
(지금 당장 해야 할 행동. 번호 목록)
"""
    try:
        text = generate(prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "verdict": extract("판정", text),
        "risk":    extract("위험도", text),
        "signals": extract("발견된위험신호", text),
        "easy":    extract("쉬운설명", text),
        "actions": extract("지금해야할행동", text),
    }
