from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from api.gemini import generate, extract

router = APIRouter()


class BucketItem(BaseModel):
    name: str
    cost: int
    years: int


class BucketRequest(BaseModel):
    age: int
    income: int
    asset: int
    expense: int
    items: List[BucketItem]


@router.post("/bucket-list")
def analyze(req: BucketRequest):
    monthly_savings = req.income - req.expense
    items_text = "\n".join([
        f"{i+1}. {item.name} — 예상 비용 {item.cost}만원, 목표 시기 {item.years}년 후"
        for i, item in enumerate(req.items)
    ])

    # 달성 가능성 사전 계산
    item_results = []
    for item in req.items:
        months = item.years * 12
        total_available = req.asset + max(monthly_savings, 0) * months
        if total_available >= item.cost:
            status = "달성 가능"
        elif total_available >= item.cost * 0.7:
            status = "노력 필요"
        else:
            status = "어려움"
        item_results.append({
            "name":   item.name,
            "cost":   item.cost,
            "years":  item.years,
            "status": status,
        })

    prompt = f"""당신은 고령 고객의 꿈을 재무 계획으로 연결해주는 AI 노후 코치입니다.

고객 정보:
- 나이: {req.age}세
- 현재 금융 자산: {req.asset}만원
- 월 소득/연금: {req.income}만원
- 월 생활비: {req.expense}만원
- 월 저축 가능: {monthly_savings}만원 ({"흑자" if monthly_savings >= 0 else "적자"})

버킷리스트:
{items_text}

고객을 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

종합평가:
(현재 재무 상황과 꿈 실현 가능성 전반 평가. 2문장)

꿈분석:
(각 꿈별로 "꿈 이름: 달성 가능/노력 필요/어려움 — 이유 — 월 필요 저축액" 형식. 번호 목록)

우선순위:
(먼저 이루어야 할 꿈 순서와 이유. 번호 목록)

실천계획:
(지금 당장 시작할 수 있는 구체적 행동 3가지. 번호 목록)

응원메시지:
(고객님의 꿈을 응원하는 따뜻하고 짧은 메시지. 2문장)
"""
    try:
        text = generate(prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "overall":      extract("종합평가", text),
        "analysis":     extract("꿈분석", text),
        "priority":     extract("우선순위", text),
        "plan":         extract("실천계획", text),
        "cheer":        extract("응원메시지", text),
        "item_results": item_results,
    }
