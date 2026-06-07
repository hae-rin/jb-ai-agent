from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.gemini import generate, extract

router = APIRouter()


def tone(user_type: str) -> str:
    if user_type == "고령층":
        return "고객님은 고령층입니다. 매우 쉬운 말로 설명하고, 어려운 금융 용어는 반드시 일상 언어로 풀어서 설명하세요. 문장은 짧고 명확하게."
    elif user_type == "금융 초보자":
        return "고객님은 금융 초보자입니다. 금융 용어가 나올 때마다 괄호 안에 간단히 설명을 덧붙이세요. 친근하고 교육적인 톤으로."
    return "고객님은 일반 사용자입니다. 표준 금융 언어를 사용하되 핵심을 명확하게."


class VPRequest(BaseModel):
    content: str
    user_type: str = "일반 사용자"


@router.post("/voice-phishing")
def analyze(req: VPRequest):
    prompt = f"""당신은 금융 보이스피싱·스미싱 전문 탐지 AI입니다.
{tone(req.user_type)}

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
