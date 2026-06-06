from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from api.gemini import generate, extract

router = APIRouter()

JB_PRODUCTS = """
[전북은행]
- JB다이렉트 정기예금: 비대면 전용 고금리 정기예금 / 안전한 자산 보관, 단기 목돈 운용
- JB행복적금: 자동이체 시 우대금리 / 월 저축을 통한 목돈 마련
- JB연금저축신탁: 연간 400만원 세액공제 혜택 / 노후 연금 준비
- JB개인형퇴직연금(IRP): 퇴직금 + 추가 납입 가능, 연 900만원 세액공제 / 은퇴 대비

[광주은행]
- KJ파킹통장: 수시입출 가능 고금리 통장 / 긴급 생활자금 보관
- KJ정기적금: 우대금리 최대 연 4%대 / 단기 목돈 마련
- KJ연금저축: 세제혜택 연금 상품 / 노후 소득 준비

[JB우리캐피탈]
- 시니어 생활안정 대출: 고령층 특화, 연금 담보 / 일시적 생활자금 필요 시
- 주택담보대출: 부동산 자산 활용 자금 조달 / 목돈 필요 시

[JB자산운용]
- JB단기채권펀드: 안정적 단기 채권 투자, 원금 손실 가능성 낮음 / 안전 투자
- JB글로벌자산배분펀드: 글로벌 분산투자 / 장기 자산 증식 목표
"""


class ProductRequest(BaseModel):
    age: int
    income: int
    asset: int
    monthly_save: int = 50
    goals: List[str]
    risk_level: str = "안전 추구"
    has_pension: str = "가입 중"
    has_irp: str = "없음"
    tax_concern: str = "보통"
    has_loan: str = "없음"


@router.post("/products")
def recommend(req: ProductRequest):
    prompt = f"""당신은 고령 고객 전문 자산관리 AI입니다.

고객 정보:
- 나이: {req.age}세
- 월 소득: {req.income}만원
- 현재 금융 자산: {req.asset}만원
- 월 저축 가능 금액: {req.monthly_save}만원
- 재무 목표: {', '.join(req.goals)}
- 투자 성향: {req.risk_level}
- 국민연금: {req.has_pension}
- IRP/연금저축: {req.has_irp}
- 세금 절약 관심: {req.tax_concern}
- 대출: {req.has_loan}

고객의 목표와 상황에 맞는 JB금융그룹 계열사 상품을 우선 추천하세요.
각 추천 상품에 계열사명(전북은행/광주은행/JB우리캐피탈/JB자산운용)을 반드시 포함하고 쉽게 설명하세요.

JB금융그룹 참고 상품 목록:
{JB_PRODUCTS}

고객을 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

종합평가:
(현재 재무 상태 한 줄 평가)

단기추천:
(1~3년 목표 상품 추천. 없으면 "해당 없음". 상품명과 이유 포함. 번호 목록)

장기추천:
(3~10년 목표 상품 추천. 없으면 "해당 없음". 번호 목록)

노후추천:
(노후 대비 상품 추천. 없으면 "해당 없음". 번호 목록)

세금절약:
(절세 가능한 상품/방법. 없으면 "해당 없음". 번호 목록)

쉬운설명:
(전체 추천을 쉽게 3~4문장 요약)

우선순위행동:
(지금 당장 해야 할 행동. 번호 목록 3가지)
"""
    try:
        text = generate(prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "overall":   extract("종합평가", text),
        "short":     extract("단기추천", text),
        "long_term": extract("장기추천", text),
        "retire":    extract("노후추천", text),
        "tax":       extract("세금절약", text),
        "easy":      extract("쉬운설명", text),
        "actions":   extract("우선순위행동", text),
    }
