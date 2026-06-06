from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.gemini import generate, extract

router = APIRouter()


class SimRequest(BaseModel):
    age: int
    health_status: str = "양호"
    asset_financial: int
    income: int
    monthly_expense: int
    medical: int = 30
    asset_real: str = ""
    has_family: str = "없음"
    has_loan: str = "없음"
    family_contact: str = "연락 가능"


@router.post("/simulation")
def simulate(req: SimRequest):
    monthly_total = req.monthly_expense + req.medical
    shortage = monthly_total - req.income

    if shortage > 0 and req.asset_financial > 0:
        sustain_months = int(req.asset_financial / shortage)
        sustain_years  = sustain_months // 12
        sustain_remain = sustain_months % 12
        sustain_str    = f"약 {sustain_years}년 {sustain_remain}개월"
    elif shortage > 0:
        sustain_months = 0
        sustain_years  = 0
        sustain_str    = "즉시 위험"
    else:
        sustain_months = 9999
        sustain_years  = 99
        sustain_str    = "안정 (소득 ≥ 지출)"

    # 30년 자산 변화 계산
    assets = []
    remaining = float(req.asset_financial)
    for y in range(31):
        assets.append(round(max(remaining, 0), 1))
        annual_net = (req.income - req.monthly_expense - req.medical * (1.03 ** y)) * 12
        remaining += annual_net

    prompt = f"""당신은 고령 고객 전문 노후 재무 설계 AI입니다.

고객 정보:
- 나이: {req.age}세 / 건강 상태: {req.health_status}
- 금융 자산: {req.asset_financial}만원
- 부동산 자산: {req.asset_real}
- 월 연금/소득: {req.income}만원
- 월 생활비: {req.monthly_expense}만원
- 월 의료비/보험료: {req.medical}만원
- 부양 가족: {req.has_family} / 대출: {req.has_loan} / 보호자 연락: {req.family_contact}
사전 계산 결과:
- 월 현금흐름: {"적자 " + str(shortage) + "만원" if shortage > 0 else "흑자 " + str(abs(shortage)) + "만원"}
- 자산 유지 가능 기간: {sustain_str}

마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.
고객을 반드시 "고객님"으로만 호칭하세요.

반드시 아래 형식으로만 답하세요.

노후안정도: [안정/주의/위험]

월현금흐름:
(월 수입·지출 현황과 부족/잉여액을 쉽게 설명. 2문장)

미래예측_현재~5년:
(현재부터 5년간 생활 전망. 2문장)

미래예측_5년~10년:
(5년~10년 사이 예상 변화. 2문장)

미래예측_10년이후:
(10년 이후 장기 리스크. 2문장)

추천행동:
(실천 가능한 행동 3가지. 번호 목록)

핵심인사이트:
(가장 중요한 사실 한 문장. 실제 연수·금액 포함)

쉬운설명:
(쉽게 말하면 형식으로 3~4문장. 어르신도 바로 이해할 수 있게)
"""
    try:
        text = generate(prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "risk":       extract("노후안정도", text),
        "cashflow":   extract("월현금흐름", text),
        "pred_5":     extract("미래예측_현재~5년", text),
        "pred_10":    extract("미래예측_5년~10년", text),
        "pred_after": extract("미래예측_10년이후", text),
        "actions":    extract("추천행동", text),
        "insight":    extract("핵심인사이트", text),
        "easy":       extract("쉬운설명", text),
        "monthly_shortage": shortage,
        "sustain_years":    sustain_years if shortage > 0 else None,
        "assets_over_time": assets,
    }
