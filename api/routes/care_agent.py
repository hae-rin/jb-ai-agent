from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
from api.gemini import generate, extract

router = APIRouter()


class CareRequest(BaseModel):
    age: int
    income: int
    asset: int
    expense: int
    transactions: Optional[str] = None


def _fin_prompt(age, income, asset, expense, shortage, sustain_str):
    return f"""당신은 노후 재무 분석 AI 에이전트입니다.
고령 고객의 재무 상태를 분석하여 위험도와 핵심 요인을 도출하세요.

고객 정보:
- 나이: {age}세 / 금융 자산: {asset:,}만원
- 월 소득/연금: {income}만원 / 월 지출: {expense}만원
- 월 현금흐름: {"적자 " + str(shortage) + "만원" if shortage > 0 else "흑자 " + str(abs(shortage)) + "만원"}
- 예상 자산 유지: {sustain_str}

위의 수치를 직접 인용하여 구체적으로 설명하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.
고객을 반드시 "고객님"으로만 호칭하세요.

반드시 아래 형식으로만 답하세요.

재무위험도: [안정/주의/위험]

월현금흐름:
(월 수입·지출 금액을 직접 언급하며 현황 설명. 1~2문장)

핵심위험요인:
(구체적 수치 포함하여 위험 요인 설명. 번호 목록 2~3가지. 없으면 "위험 요인 없음")

자산유지예상:
(몇 년 후까지 자산이 유지될지 구체적으로. 1문장)
"""


def _tx_prompt(age, income, expense, transactions):
    return f"""당신은 금융 이상거래 탐지 AI 에이전트입니다.
아래 거래 내역에서 위험 패턴을 탐지하세요.

고객 정보: 나이 {age}세, 월 소득 {income}만원, 월 지출 {expense}만원

거래 내역:
{transactions}

마크다운(**볼드**, *이탤릭*) 절대 금지. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

거래위험도: [낮음/보통/높음]

위험신호:
(발견된 이상 패턴. 없으면 "없음". 번호 목록)

사기의심: [있음/없음]
"""


def _care_prompt(fin_risk, fin_cashflow, fin_risks, sustain_str, tx_risk, tx_signals):
    return f"""당신은 고령 고객 케어 플랜 생성 AI 에이전트입니다.
아래 분석 결과를 종합하여 고객 맞춤 행동 계획을 만드세요.

재무 분석 결과:
- 재무 위험도: {fin_risk}
- 월 현금흐름: {fin_cashflow}
- 핵심 위험 요인: {fin_risks}

거래 분석 결과:
- 거래 위험도: {tx_risk}
- 위험 신호: {tx_signals}

마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.
고객을 반드시 "고객님"으로만 호칭하세요.

반드시 아래 형식으로만 답하세요.

핵심메시지:
(고객님 재무 상황을 실제 수치 포함하여 한 문장으로)

즉각조치:
(지금 당장 해야 할 행동. 번호 목록 2~3가지)

단기계획:
(1~3개월 내 실천 계획. 번호 목록 2~3가지)

장기전략:
(6개월 이상 장기 관리 전략. 번호 목록 2가지)
"""


def _verify_prompt(fin_risk, fin_cashflow, fin_risks, tx_risk, tx_signals,
                   immediate, short_plan, long_strategy, is_retry=False):
    return f"""당신은 AI 에이전트의 검증 모듈입니다.

[재무 분석] 위험도: {fin_risk} / 현금흐름: {fin_cashflow} / 핵심 위험: {fin_risks}
[거래 분석] 위험도: {tx_risk} / 위험 신호: {tx_signals}
[케어 플랜{"(개선됨)" if is_retry else ""}]
즉각 조치: {immediate} / 단기 계획: {short_plan} / 장기 전략: {long_strategy}

검증 항목:
1. 재무·거래 위험도와 케어 플랜이 일관성이 있는가?
2. 즉각 조치가 위험 수준에 비해 충분한가?
3. 중요한 위험 요소가 누락되지 않았는가?

고객을 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

검증결과: [일관성 있음/수정 필요]

수정사항:
(문제점과 수정 방향. 없으면 "없음")

최종종합:
(전체 분석 종합 요약. 3~4문장)

신뢰도: [높음/보통/낮음]
"""


@router.post("/care-agent")
def care_agent(req: CareRequest):
    shortage = req.expense - req.income
    if shortage > 0 and req.asset > 0:
        sm = int(req.asset / shortage)
        sustain_str = f"약 {sm // 12}년 {sm % 12}개월 후 소진 예상"
    elif shortage > 0:
        sustain_str = "자산 없음 — 즉시 위험"
    else:
        sustain_str = "안정 (소득 ≥ 지출)"

    try:
        # ① 재무 분석
        fin_text     = generate(_fin_prompt(req.age, req.income, req.asset, req.expense, shortage, sustain_str))
        fin_risk     = extract("재무위험도", fin_text)
        fin_cashflow = extract("월현금흐름", fin_text)
        fin_risks    = extract("핵심위험요인", fin_text)
        fin_sustain  = extract("자산유지예상", fin_text)

        # ② 거래 분석
        has_tx = bool(req.transactions and req.transactions.strip())
        tx_risk = "분석 없음"
        tx_signals = "없음"
        if has_tx:
            tx_text    = generate(_tx_prompt(req.age, req.income, req.expense, req.transactions))
            tx_risk    = extract("거래위험도", tx_text)
            tx_signals = extract("위험신호", tx_text)

        # ③ 케어 플랜
        care_text     = generate(_care_prompt(fin_risk, fin_cashflow, fin_risks, sustain_str, tx_risk, tx_signals))
        핵심_메시지   = extract("핵심메시지", care_text)
        immediate     = extract("즉각조치", care_text)
        short_plan    = extract("단기계획", care_text)
        long_strategy = extract("장기전략", care_text)

        # ④ 검증 (최대 1회 재생성)
        verify_text  = generate(_verify_prompt(fin_risk, fin_cashflow, fin_risks, tx_risk, tx_signals,
                                               immediate, short_plan, long_strategy))
        verify_status = extract("검증결과", verify_text)
        corrections   = extract("수정사항", verify_text)
        final_summary = extract("최종종합", verify_text)
        confidence    = extract("신뢰도", verify_text)

        if "수정 필요" in verify_status and corrections and corrections != "없음":
            fix_text = generate(f"""AI 검증에서 아래 문제가 발견되었습니다. 이를 반영하여 케어 플랜을 개선하세요.

발견된 문제: {corrections}
[재무] 위험도: {fin_risk} / 핵심 위험: {fin_risks}
[거래] 위험도: {tx_risk} / 위험 신호: {tx_signals}

고객을 반드시 "고객님"으로만 호칭하세요.
마크다운 절대 금지. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

즉각조치:
(개선된 즉각 행동. 번호 목록 2~3가지)

단기계획:
(개선된 단기 계획. 번호 목록 2~3가지)

장기전략:
(개선된 장기 전략. 번호 목록 2가지)
""")
            immediate     = extract("즉각조치", fix_text) or immediate
            short_plan    = extract("단기계획", fix_text) or short_plan
            long_strategy = extract("장기전략", fix_text) or long_strategy

            verify2      = generate(_verify_prompt(fin_risk, fin_cashflow, fin_risks, tx_risk, tx_signals,
                                                   immediate, short_plan, long_strategy, is_retry=True))
            final_summary = extract("최종종합", verify2) or final_summary
            confidence    = extract("신뢰도", verify2) or confidence

    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "fin_risk":      fin_risk,
        "fin_cashflow":  fin_cashflow,
        "fin_risks":     fin_risks,
        "fin_sustain":   fin_sustain,
        "has_tx":        has_tx,
        "tx_risk":       tx_risk,
        "tx_signals":    tx_signals,
        "핵심_메시지":   핵심_메시지,
        "immediate":     immediate,
        "short_plan":    short_plan,
        "long_strategy": long_strategy,
        "corrections":   corrections,
        "final_summary": final_summary,
        "confidence":    confidence,
    }


@router.post("/care-agent/pdf")
def download_pdf(req: dict):
    from fpdf import FPDF

    FONT_REG  = r"C:\Windows\Fonts\malgun.ttf"
    FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"

    pdf = FPDF()
    pdf.set_margins(18, 18, 18)
    pdf.add_page()
    pdf.add_font("Malgun", "",  FONT_REG)
    pdf.add_font("Malgun", "B", FONT_BOLD)
    W = pdf.w - 2 * pdf.l_margin

    def section(title, body):
        if not body:
            return
        if title:
            pdf.set_font("Malgun", "B", 10)
            pdf.set_text_color(55, 65, 81)
            pdf.cell(W, 7, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Malgun", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(W, 6, body.strip())
        pdf.ln(2)

    # 헤더
    pdf.set_fill_color(37, 99, 235)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Malgun", "B", 17)
    pdf.cell(W, 13, "Slowfit  종합 케어 리포트",
             fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Malgun", "", 9)
    pdf.set_fill_color(219, 234, 254)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(W, 7,
             f"분석 일시: {datetime.now().strftime('%Y년 %m월 %d일  %H:%M')}   |   JB금융그룹 Fin:AI Challenge",
             fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 9, "[ 고객 정보 ]", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(37, 99, 235); pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y()); pdf.ln(3)
    pdf.set_font("Malgun", "", 11)
    age     = req.get("age", "")
    income  = req.get("income", "")
    asset   = req.get("asset", "")
    expense = req.get("expense", "")
    pdf.cell(W / 2, 8, f"나이: {age}세",             new_x="RIGHT", new_y="TOP")
    pdf.cell(W / 2, 8, f"금융 자산: {asset:,}만원" if isinstance(asset, int) else f"금융 자산: {asset}만원",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(W / 2, 8, f"월 소득/연금: {income}만원", new_x="RIGHT", new_y="TOP")
    pdf.cell(W / 2, 8, f"월 생활비: {expense}만원",   new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 9, "[ 재무 분석 결과 ]", new_x="LMARGIN", new_y="NEXT")
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y()); pdf.ln(3)
    fin_risk = req.get("fin_risk", "")
    if "위험" in fin_risk:
        pdf.set_fill_color(254, 226, 226); pdf.set_text_color(185, 28, 28)
    elif "주의" in fin_risk:
        pdf.set_fill_color(254, 243, 199); pdf.set_text_color(180, 83, 9)
    else:
        pdf.set_fill_color(220, 252, 231); pdf.set_text_color(21, 128, 61)
    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 10, f"재무 위험도: {fin_risk}", fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(2); pdf.set_text_color(0, 0, 0)
    section("월 현금흐름",    req.get("fin_cashflow", ""))
    section("핵심 위험 요인", req.get("fin_risks", ""))
    section("자산 유지 예상", req.get("fin_sustain", ""))

    if req.get("has_tx"):
        tx_risk = req.get("tx_risk", "")
        pdf.set_font("Malgun", "B", 12)
        pdf.cell(W, 9, "[ 거래 이상 분석 결과 ]", new_x="LMARGIN", new_y="NEXT")
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y()); pdf.ln(3)
        if "높음" in tx_risk:
            pdf.set_fill_color(254, 226, 226); pdf.set_text_color(185, 28, 28)
        elif "보통" in tx_risk:
            pdf.set_fill_color(254, 243, 199); pdf.set_text_color(180, 83, 9)
        else:
            pdf.set_fill_color(220, 252, 231); pdf.set_text_color(21, 128, 61)
        pdf.set_font("Malgun", "B", 11)
        pdf.cell(W, 9, f"거래 위험도: {tx_risk}", fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(2); pdf.set_text_color(0, 0, 0)
        section("위험 신호", req.get("tx_signals", ""))

    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 9, "[ 맞춤 케어 플랜 ]", new_x="LMARGIN", new_y="NEXT")
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y()); pdf.ln(3)
    section("핵심 요약",          req.get("핵심_메시지", ""))
    section("즉각 조치",          req.get("immediate", ""))
    section("단기 계획 (1~3개월)", req.get("short_plan", ""))
    section("장기 전략 (6개월+)",  req.get("long_strategy", ""))

    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 9, "[ 종합 케어 요약 ]", new_x="LMARGIN", new_y="NEXT")
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y()); pdf.ln(3)
    section("", req.get("final_summary", ""))
    pdf.set_font("Malgun", "", 9); pdf.set_text_color(120, 120, 120)
    pdf.cell(W, 6, f"분석 신뢰도: {req.get('confidence', '')}", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_draw_color(210, 210, 210); pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y()); pdf.ln(2)
    pdf.set_font("Malgun", "", 8); pdf.set_text_color(160, 160, 160)
    pdf.cell(W, 5, "본 리포트는 AI 분석 결과이며 실제 금융 상담을 대체하지 않습니다.",
             new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(W, 5, "JB금융그룹 Fin:AI Challenge  |  Slowfit",
             new_x="LMARGIN", new_y="NEXT", align="C")

    pdf_bytes = bytes(pdf.output())
    from urllib.parse import quote
    filename = f"안심케어_리포트_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    disposition = f"attachment; filename=\"report.pdf\"; filename*=UTF-8''{quote(filename)}"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": disposition},
    )
