import streamlit as st
from utils import apply_user_css
from google import genai
from dotenv import load_dotenv
import os
import re
from datetime import datetime

load_dotenv()

@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

# ──────────────────────────────────────────────
# PDF 리포트 생성
# ──────────────────────────────────────────────
_FONT_REG  = r"C:\Windows\Fonts\malgun.ttf"
_FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"

def _pdf_section(pdf, W, title, body):
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

def generate_care_pdf(age, income, asset, expense,
                      fin_risk, fin_cashflow, fin_risks, fin_sustain,
                      has_tx, tx_risk, tx_signals,
                      핵심_메시지, immediate, short_plan, long_strategy,
                      final_summary, confidence):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_margins(18, 18, 18)
    pdf.add_page()
    pdf.add_font("Malgun", "",  _FONT_REG)
    pdf.add_font("Malgun", "B", _FONT_BOLD)
    W = pdf.w - 2 * pdf.l_margin

    # 헤더
    pdf.set_fill_color(37, 99, 235)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Malgun", "B", 17)
    pdf.cell(W, 13, "안심케어 AI  종합 케어 리포트",
             fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Malgun", "", 9)
    pdf.set_fill_color(219, 234, 254)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(W, 7,
             f"분석 일시: {datetime.now().strftime('%Y년 %m월 %d일  %H:%M')}   |   JB금융그룹 Fin:AI Challenge",
             fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    # 고객 정보
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 9, "[ 고객 정보 ]", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(37, 99, 235)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Malgun", "", 11)
    pdf.cell(W / 2, 8, f"나이: {age}세", new_x="RIGHT", new_y="TOP")
    pdf.cell(W / 2, 8, f"금융 자산: {asset:,}만원", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(W / 2, 8, f"월 소득/연금: {income}만원", new_x="RIGHT", new_y="TOP")
    pdf.cell(W / 2, 8, f"월 생활비: {expense}만원", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # 재무 분석
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 9, "[ 재무 분석 결과 ]", new_x="LMARGIN", new_y="NEXT")
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
    pdf.ln(3)
    if "위험" in fin_risk:
        pdf.set_fill_color(254, 226, 226); pdf.set_text_color(185, 28, 28)
    elif "주의" in fin_risk:
        pdf.set_fill_color(254, 243, 199); pdf.set_text_color(180, 83, 9)
    else:
        pdf.set_fill_color(220, 252, 231); pdf.set_text_color(21, 128, 61)
    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 10, f"재무 위험도: {fin_risk}",
             fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(2)
    pdf.set_text_color(0, 0, 0)
    _pdf_section(pdf, W, "월 현금흐름", fin_cashflow)
    if fin_risks and fin_risks != "위험 요인 없음":
        _pdf_section(pdf, W, "핵심 위험 요인", fin_risks)
    _pdf_section(pdf, W, "자산 유지 예상", fin_sustain)

    # 거래 분석
    if has_tx:
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Malgun", "B", 12)
        pdf.cell(W, 9, "[ 거래 이상 분석 결과 ]", new_x="LMARGIN", new_y="NEXT")
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
        pdf.ln(3)
        if "높음" in tx_risk:
            pdf.set_fill_color(254, 226, 226); pdf.set_text_color(185, 28, 28)
        elif "보통" in tx_risk:
            pdf.set_fill_color(254, 243, 199); pdf.set_text_color(180, 83, 9)
        else:
            pdf.set_fill_color(220, 252, 231); pdf.set_text_color(21, 128, 61)
        pdf.set_font("Malgun", "B", 11)
        pdf.cell(W, 9, f"거래 위험도: {tx_risk}",
                 fill=True, new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(2)
        pdf.set_text_color(0, 0, 0)
        if tx_signals and tx_signals != "없음":
            _pdf_section(pdf, W, "위험 신호", tx_signals)

    # 케어 플랜
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 9, "[ 맞춤 케어 플랜 ]", new_x="LMARGIN", new_y="NEXT")
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
    pdf.ln(3)
    if 핵심_메시지:
        _pdf_section(pdf, W, "핵심 요약", 핵심_메시지)
    _pdf_section(pdf, W, "즉각 조치", immediate)
    _pdf_section(pdf, W, "단기 계획 (1~3개월)", short_plan)
    _pdf_section(pdf, W, "장기 전략 (6개월 이상)", long_strategy)

    # 종합
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Malgun", "B", 12)
    pdf.cell(W, 9, "[ 종합 케어 요약 ]", new_x="LMARGIN", new_y="NEXT")
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
    pdf.ln(3)
    _pdf_section(pdf, W, "", final_summary)
    pdf.set_font("Malgun", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(W, 6, f"분석 신뢰도: {confidence}", new_x="LMARGIN", new_y="NEXT")

    # 푸터
    pdf.ln(6)
    pdf.set_draw_color(210, 210, 210)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Malgun", "", 8)
    pdf.set_text_color(160, 160, 160)
    pdf.cell(W, 5, "본 리포트는 AI 분석 결과이며 실제 금융 상담을 대체하지 않습니다.",
             new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(W, 5, "JB금융그룹 Fin:AI Challenge  |  안심케어 AI",
             new_x="LMARGIN", new_y="NEXT", align="C")

    return bytes(pdf.output())


st.set_page_config(page_title="AI 종합 케어 에이전트", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.session_state.setdefault("profile_age", 70)
st.session_state.setdefault("profile_income", 80)
st.session_state.setdefault("profile_asset", 20000)
st.session_state.setdefault("profile_expense", 150)

user_type = st.session_state.get("user_type", "고령층")
apply_user_css(user_type)

st.html(f"""
<div style="width:100%;margin-bottom:20px;box-sizing:border-box;
  background:linear-gradient(135deg,#1E40AF 0%,#3B82F6 100%);
  border-radius:16px;padding:24px 32px 20px;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;">
  <div style="margin-bottom:14px;">
    <a href="/" style="color:rgba(255,255,255,0.75);text-decoration:none;font-size:13px;font-weight:500;">← 홈으로</a>
  </div>
  <div style="display:flex;align-items:center;gap:16px;">
    <div style="font-size:42px;line-height:1;">🤖</div>
    <div>
      <div style="font-size:{'28px' if user_type == '고령층' else '22px'};font-weight:800;color:white;line-height:1.2;">AI 종합 케어 에이전트</div>
      <div style="font-size:{'16px' if user_type == '고령층' else '13px'};color:rgba(255,255,255,0.82);margin-top:5px;line-height:1.6;">재무 상태, 거래 위험, 맞춤 케어 플랜까지 AI가 단계별로 분석해드립니다.</div>
    </div>
  </div>
</div>
""")

# ──────────────────────────────────────────────
# 입력
# ──────────────────────────────────────────────
st.markdown("### 📋 정보 입력")

_age = st.session_state.get("profile_age", 70)
_income = st.session_state.get("profile_income", 80)
_asset = st.session_state.get("profile_asset", 20000)
_expense = st.session_state.get("profile_expense", 150)
st.info(f"📋 홈 프로필 적용 중 — {_age}세 | 월 소득 {_income}만원 | 금융 자산 {_asset:,}만원 | 월 생활비 {_expense}만원")

with st.expander("✏️ 정보 수정하기", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        age     = st.number_input("나이", min_value=1, max_value=100, key="profile_age")
        income  = st.number_input("월 연금/소득 (만원)", min_value=0, step=5, key="profile_income")
    with col2:
        asset   = st.number_input("금융 자산 (만원)", min_value=0, step=100, key="profile_asset")
        expense = st.number_input("월 생활비 + 의료비 (만원)", min_value=0, step=5, key="profile_expense")

with st.expander("📂 최근 거래 내역 (선택 — 입력 시 이상거래 분석 추가)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚠️ 위험 거래 예시"):
            st.session_state["agent_tx_input"] = """2025-01-15 | 해외 송금 | 500만원 | 베트남 계좌
2025-01-15 | ATM 출금 | 200만원 | 강남역
2025-01-14 | 모르는 번호 송금 | 150만원 | 010-9999-1234
2025-01-13 | 온라인 쇼핑 | 8만원 | 쿠팡"""
            st.rerun()
    with col2:
        if st.button("✅ 정상 거래 예시"):
            st.session_state["agent_tx_input"] = """2025-01-15 | 마트 | 8만원 | 이마트
2025-01-14 | 병원비 | 3만원 | 서울성모병원
2025-01-13 | 편의점 | 1만원 | GS25
2025-01-12 | 약국 | 1만원 | 온누리약국"""
            st.rerun()

    transactions = st.text_area(
        "거래 내역",
        key="agent_tx_input",
        placeholder="날짜 | 항목 | 금액 | 수신처 형식으로 입력하세요.",
        height=150,
        label_visibility="collapsed"
    )

st.divider()

# ──────────────────────────────────────────────
# Rule Engine (Step 2)
# ──────────────────────────────────────────────
def rule_engine(fin_risk, monthly_shortage):
    decisions = []
    if "위험" in fin_risk:
        decisions.append(("⚡ 이상거래 즉시 점검", "재무 위험 상태 + 금융사기 피해 시 자산 급감 가능 → 거래 위험 최우선 분석"))
        decisions.append(("🚨 긴급 방어 플랜 수립", "위험도 높음 → 즉각적인 자산 보호 조치 필요"))
    elif "주의" in fin_risk:
        decisions.append(("🔍 거래 패턴 정밀 점검", "주의 단계 → 불필요한 지출·이상 거래 모니터링 강화"))
        decisions.append(("💡 지출 절감 방안 탐색", f"월 적자 구조 → 지출 항목 재검토 필요"))
    else:
        decisions.append(("✅ 안정 유지 전략 수립", "현재 안정 → 장기 목표 중심 계획 가능"))
        decisions.append(("🌟 버킷리스트 실현 계획 검토", "여유 자산 활용한 꿈 실현 계획 분석"))
    return decisions

# Extract helper
def extract(label, text):
    escaped = re.escape(label)
    pattern = rf"{escaped}:\s*(.*?)(?=\n[^\d\s][^\n]*:|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

# ──────────────────────────────────────────────
# 에이전트 실행
# ──────────────────────────────────────────────
if st.button("🤖 AI 에이전트 시작", type="primary"):
    monthly_shortage = expense - income
    has_tx = bool(transactions.strip())
    if monthly_shortage > 0 and asset > 0:
        _sm = int(asset / monthly_shortage)
        asset_sustain_str = f"약 {_sm // 12}년 {_sm % 12}개월 후 소진 예상"
    elif monthly_shortage > 0:
        asset_sustain_str = "자산 없음 — 즉시 위험"
    else:
        asset_sustain_str = "안정 (소득 ≥ 지출)"

    fin_risk = ""
    fin_cashflow = ""
    fin_risks = ""
    fin_sustain = ""
    tx_risk = "분석 없음"
    tx_signals = "없음"
    핵심_메시지   = ""
    immediate     = ""
    short_plan    = ""
    long_strategy = ""

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ① 판단: 재무 건전성 분석
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with st.status("재무 상태 분석 중...", expanded=False) as s1:
        prompt1 = f"""
당신은 노후 재무 분석 AI 에이전트입니다.
고령 고객의 재무 상태를 분석하여 위험도와 핵심 요인을 도출하세요.

고객 정보:
- 나이: {age}세 / 금융 자산: {asset:,}만원
- 월 소득/연금: {income}만원 / 월 지출: {expense}만원
- 월 현금흐름: {"적자 " + str(monthly_shortage) + "만원" if monthly_shortage > 0 else "흑자 " + str(abs(monthly_shortage)) + "만원"}
- 예상 자산 유지: {asset_sustain_str}

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
        try:
            r1 = client.models.generate_content(model="gemini-2.5-flash", contents=prompt1)
            fin_result = r1.text
        except Exception:
            st.error("⚠️ AI 서버에 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
            st.stop()

        fin_risk     = extract("재무위험도", fin_result)
        fin_cashflow = extract("월현금흐름", fin_result)
        fin_risks    = extract("핵심위험요인", fin_result)
        fin_sustain  = extract("자산유지예상", fin_result)

        s1.update(label=f"재무 상태 분석 완료 — 위험도: {fin_risk}", state="complete", expanded=True)

    if "위험" in fin_risk:
        st.error(f"재무 위험도: {fin_risk}")
    elif "주의" in fin_risk:
        st.warning(f"재무 위험도: {fin_risk}")
    else:
        st.success(f"재무 위험도: {fin_risk}")

    st.write(fin_cashflow)
    if fin_risks and fin_risks != "위험 요인 없음":
        st.warning(fin_risks)
    st.caption(fin_sustain)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ② 행동: Rule Engine 기반 방향 결정
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.markdown("---")
    st.markdown("**분석 방향 결정**")

    decisions = rule_engine(fin_risk, monthly_shortage)
    for title, reason in decisions:
        st.info(f"{title}  \n근거: {reason}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ③ 판단: 거래 이상 패턴 분석
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.markdown("---")
    if has_tx:
        with st.status("거래 이상 패턴 분석 중...", expanded=False) as s3:
            prompt3 = f"""
당신은 금융 이상거래 탐지 AI 에이전트입니다.
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
            try:
                r3 = client.models.generate_content(model="gemini-2.5-flash", contents=prompt3)
                tx_result = r3.text
            except Exception:
                st.error("⚠️ AI 서버에 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
                st.stop()

            tx_risk    = extract("거래위험도", tx_result)
            tx_signals = extract("위험신호", tx_result)
            tx_fraud   = extract("사기의심", tx_result)

            s3.update(label=f"거래 분석 완료 — 위험도: {tx_risk}", state="complete", expanded=True)

        if "높음" in tx_risk:
            st.error(f"거래 위험도: {tx_risk}")
        elif "보통" in tx_risk:
            st.warning(f"거래 위험도: {tx_risk}")
        else:
            st.success(f"거래 위험도: {tx_risk}")

        if tx_signals and tx_signals != "없음":
            st.warning(tx_signals)
    else:
        st.info("거래 내역 미입력 — 거래 분석을 생략합니다.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ④ 행동: 맞춤 케어 플랜 생성
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.markdown("---")
    with st.status("맞춤 케어 플랜 생성 중...", expanded=False) as s4:
        prompt4 = f"""
당신은 고령 고객 케어 플랜 생성 AI 에이전트입니다.
아래 분석 결과를 종합하여 고객 맞춤 행동 계획을 만드세요.

재무 분석 결과:
- 재무 위험도: {fin_risk}
- 월 현금흐름: {fin_cashflow}
- 핵심 위험 요인: {fin_risks}
- 예상 자산 유지: {asset_sustain_str}

거래 분석 결과:
- 거래 위험도: {tx_risk}
- 위험 신호: {tx_signals}

사용자 유형: {user_type}
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.
고객을 반드시 "고객님"으로만 호칭하세요.

반드시 아래 형식으로만 답하세요.

핵심메시지:
(고객님 재무 상황을 실제 수치 포함하여 한 문장으로. 예: "현재 월 30만원 적자로 약 8년 후 자산이 소진될 수 있습니다.")

즉각조치:
(지금 당장 해야 할 행동. 번호 목록 2~3가지)

단기계획:
(1~3개월 내 실천 계획. 번호 목록 2~3가지)

장기전략:
(6개월 이상 장기 관리 전략. 번호 목록 2가지)
"""
        try:
            r4 = client.models.generate_content(model="gemini-2.5-flash", contents=prompt4)
            care_plan = r4.text
        except Exception:
            st.error("⚠️ AI 서버에 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
            st.stop()

        핵심_메시지   = extract("핵심메시지", care_plan)
        immediate     = extract("즉각조치", care_plan)
        short_plan    = extract("단기계획", care_plan)
        long_strategy = extract("장기전략", care_plan)

        s4.update(label="맞춤 케어 플랜 생성 완료", state="complete", expanded=True)

    if 핵심_메시지:
        if "위험" in fin_risk or "높음" in tx_risk:
            st.error(f"📌 핵심 요약: {핵심_메시지}")
        elif "주의" in fin_risk:
            st.warning(f"📌 핵심 요약: {핵심_메시지}")
        else:
            st.success(f"📌 핵심 요약: {핵심_메시지}")
    st.markdown("**초안 케어 플랜**")
    tab1, tab2, tab3 = st.tabs(["⚡ 즉각 조치", "📅 단기 계획", "🔭 장기 전략"])
    with tab1:
        st.error(immediate)
    with tab2:
        st.warning(short_plan)
    with tab3:
        st.info(long_strategy)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ⑤ 검증/개선: 문제 발견 시 케어 플랜 재생성 후 재검증
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.markdown("---")

    MAX_RETRIES = 1
    retry_count = 0
    verify_status = ""
    corrections = ""
    final_summary = ""
    confidence = ""

    while retry_count <= MAX_RETRIES:
        is_retry = retry_count > 0
        status_label = (
            "최종 검토 중..."
            if not is_retry
            else "개선된 케어 플랜 최종 확인 중..."
        )

        with st.status(status_label, expanded=False) as s5:
            prompt5 = f"""
당신은 AI 에이전트의 검증 모듈입니다.
아래 분석 결과들이 서로 일관성이 있는지 검토하세요.
문제가 있으면 "수정 필요"로 판정하고 무엇이 문제인지 구체적으로 명시하세요.

[① 재무 분석 결과]
위험도: {fin_risk} / 현금흐름: {fin_cashflow}
핵심 위험: {fin_risks} / 자산 유지: {fin_sustain}

[③ 거래 분석 결과]
거래 위험도: {tx_risk} / 위험 신호: {tx_signals}

[④ 케어 플랜{"(개선됨)" if is_retry else ""}]
즉각 조치: {immediate}
단기 계획: {short_plan}
장기 전략: {long_strategy}

검증 항목:
1. 재무·거래 위험도와 케어 플랜이 일관성이 있는가?
2. 즉각 조치가 위험 수준에 비해 충분한가?
3. 중요한 위험 요소가 누락되지 않았는가?
4. 우선순위가 올바르게 설정되어 있는가?

고객을 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

검증결과: [일관성 있음/수정 필요]

수정사항:
(문제점과 수정 방향. 없으면 "없음")

최종종합:
(전체 분석 종합 요약. {user_type} 수준으로 3~4문장)

신뢰도: [높음/보통/낮음]
"""
            try:
                r5 = client.models.generate_content(model="gemini-2.5-flash", contents=prompt5)
                verify_result = r5.text
            except Exception:
                st.error("⚠️ AI 서버에 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
                st.stop()

            verify_status = extract("검증결과", verify_result)
            corrections   = extract("수정사항", verify_result)
            final_summary = extract("최종종합", verify_result)
            confidence    = extract("신뢰도", verify_result)

            needs_fix = ("수정 필요" in verify_status) and (retry_count < MAX_RETRIES)

            if needs_fix:
                s5.update(
                    label="케어 플랜 개선 중...",
                    state="running",
                    expanded=True
                )
                st.write(f"발견된 문제: {corrections}")

                # 케어 플랜 재생성 (종료 조건: 수정 완료 시 다음 루프에서 재검증)
                fix_prompt = f"""
AI 검증에서 아래 문제가 발견되었습니다. 이를 반영하여 케어 플랜을 개선하세요.

발견된 문제:
{corrections}

[재무 분석] 위험도: {fin_risk} / 핵심 위험: {fin_risks}
[거래 분석] 위험도: {tx_risk} / 위험 신호: {tx_signals}

사용자 유형: {user_type}
고객을 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

즉각조치:
(개선된 즉각 행동. 번호 목록 2~3가지)

단기계획:
(개선된 단기 계획. 번호 목록 2~3가지)

장기전략:
(개선된 장기 전략. 번호 목록 2가지)
"""
                try:
                    r_fix = client.models.generate_content(model="gemini-2.5-flash", contents=fix_prompt)
                    fixed = r_fix.text
                except Exception:
                    st.error("⚠️ AI 서버에 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
                    st.stop()

                new_immediate = extract("즉각조치", fixed)
                new_short     = extract("단기계획", fixed)
                new_long      = extract("장기전략", fixed)

                if new_immediate:
                    immediate = new_immediate
                if new_short:
                    short_plan = new_short
                if new_long:
                    long_strategy = new_long

                s5.update(
                    label="케어 플랜 개선 완료 — 재확인 진행",
                    state="complete",
                    expanded=True
                )
                retry_count += 1
            else:
                s5.update(
                    label=f"최종 검토 완료 — 신뢰도: {confidence}",
                    state="complete",
                    expanded=True
                )
                break

    # 개선이 이루어진 경우 최종 케어 플랜 표시
    if retry_count > 0:
        st.markdown("### ✨ 개선된 최종 케어 플랜")
        st.success("AI 검증을 통해 케어 플랜이 개선되었습니다.")
        tab1, tab2, tab3 = st.tabs(["⚡ 즉각 조치 (개선됨)", "📅 단기 계획 (개선됨)", "🔭 장기 전략 (개선됨)"])
        with tab1:
            st.error(immediate)
        with tab2:
            st.warning(short_plan)
        with tab3:
            st.info(long_strategy)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 종합 케어 리포트
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.divider()
    st.markdown("## 📋 종합 케어 리포트")

    if corrections and corrections != "없음":
        st.warning(f"검증 중 수정 사항: {corrections}")

    st.info(final_summary)

    col1, col2, col3 = st.columns(3)
    with col1:
        if "위험" in fin_risk:
            st.error(f"재무 위험도\n{fin_risk}")
        elif "주의" in fin_risk:
            st.warning(f"재무 위험도\n{fin_risk}")
        else:
            st.success(f"재무 위험도\n{fin_risk}")
    with col2:
        if "높음" in tx_risk:
            st.error(f"거래 위험도\n{tx_risk}")
        elif "보통" in tx_risk:
            st.warning(f"거래 위험도\n{tx_risk}")
        else:
            st.success(f"거래 위험도\n{tx_risk}")
    with col3:
        if "높음" in confidence:
            st.success(f"분석 신뢰도\n{confidence}")
        elif "보통" in confidence:
            st.warning(f"분석 신뢰도\n{confidence}")
        else:
            st.error(f"분석 신뢰도\n{confidence}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # JB금융그룹 연계 서비스 안내
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.divider()
    st.markdown("### 🏦 JB금융그룹 연계 서비스")

    is_urgent = ("위험" in fin_risk) or ("높음" in tx_risk)
    is_caution = ("주의" in fin_risk) or ("보통" in tx_risk)

    if is_urgent:
        st.error("긴급 상담이 필요합니다. 지금 바로 JB금융그룹 고객센터로 연락하세요.")
        jb_col1, jb_col2 = st.columns(2)
        with jb_col1:
            st.error("🚨 **전북은행 고객센터**\n☎ 1588-4477\n금융사기 신고 즉시 처리")
        with jb_col2:
            st.error("🚨 **광주은행 고객센터**\n☎ 1588-3388\n이상거래 즉시 정지 요청")
    elif is_caution:
        st.warning("JB금융그룹 전문 상담을 통해 재무 점검을 권장합니다.")
        jb_col1, jb_col2, jb_col3 = st.columns(3)
        with jb_col1:
            st.warning("**전북은행**\n☎ 1588-4477\n재무 설계 상담")
        with jb_col2:
            st.warning("**광주은행**\n☎ 1588-3388\n거래 모니터링 서비스")
        with jb_col3:
            st.warning("**JB우리캐피탈**\n☎ 1600-2266\n긴급 생활자금 대출")
    else:
        st.success("안정적인 재무 상태입니다. JB금융그룹 상품으로 노후를 더 풍요롭게 설계하세요.")
        jb_col1, jb_col2, jb_col3, jb_col4 = st.columns(4)
        with jb_col1:
            st.success("**전북은행**\nJB연금저축신탁\n세액공제 노후 준비")
        with jb_col2:
            st.success("**광주은행**\nKJ파킹통장\n여유자금 고금리 운용")
        with jb_col3:
            st.info("**JB자산운용**\nJB단기채권펀드\n안정적 수익 추구")
        with jb_col4:
            st.info("**JB우리캐피탈**\n시니어 생활안정\n대출 상품 안내")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PDF 리포트 다운로드
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.divider()
    try:
        pdf_bytes = generate_care_pdf(
            age=age, income=income, asset=asset, expense=expense,
            fin_risk=fin_risk, fin_cashflow=fin_cashflow,
            fin_risks=fin_risks, fin_sustain=fin_sustain,
            has_tx=has_tx, tx_risk=tx_risk, tx_signals=tx_signals,
            핵심_메시지=핵심_메시지, immediate=immediate,
            short_plan=short_plan, long_strategy=long_strategy,
            final_summary=final_summary, confidence=confidence,
        )
        _, dl_col, _ = st.columns([1, 2, 1])
        with dl_col:
            st.download_button(
                label="📥 케어 리포트 PDF 다운로드",
                data=pdf_bytes,
                file_name=f"안심케어_리포트_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
    except Exception as e:
        st.caption(f"PDF 생성 오류: {e}")
