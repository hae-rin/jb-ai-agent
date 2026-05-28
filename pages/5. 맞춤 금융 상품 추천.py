import streamlit as st
from utils import apply_user_css
from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

st.set_page_config(page_title="맞춤 금융 상품 추천", page_icon="💎", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

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

st.session_state.setdefault("profile_age", 70)
st.session_state.setdefault("profile_income", 80)
st.session_state.setdefault("profile_asset", 20000)
st.session_state.setdefault("profile_expense", 150)

user_type = st.session_state.get("user_type", "고령층")
apply_user_css(user_type)

st.html(f"""
<div style="width:100%;margin-bottom:20px;box-sizing:border-box;
  background:linear-gradient(135deg,#065F46 0%,#10B981 100%);
  border-radius:16px;padding:24px 32px 20px;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;">
  <div style="margin-bottom:14px;">
    <a href="/" style="color:rgba(255,255,255,0.75);text-decoration:none;font-size:13px;font-weight:500;">← 홈으로</a>
  </div>
  <div style="display:flex;align-items:center;gap:16px;">
    <div style="font-size:42px;line-height:1;">💎</div>
    <div>
      <div style="font-size:{'28px' if user_type == '고령층' else '22px'};font-weight:800;color:white;line-height:1.2;">맞춤 금융 상품 추천</div>
      <div style="font-size:{'16px' if user_type == '고령층' else '13px'};color:rgba(255,255,255,0.82);margin-top:5px;line-height:1.6;">나이, 자산, 목표에 따라 AI가 최적의 계좌와 투자 상품을 추천해드립니다.</div>
    </div>
  </div>
</div>
""")

# ──────────────────────────────────────────────
# 입력
# ──────────────────────────────────────────────
st.markdown("### 📋 기본 정보 입력")

_age = st.session_state.get("profile_age", 70)
_income = st.session_state.get("profile_income", 80)
_asset = st.session_state.get("profile_asset", 20000)
_expense = st.session_state.get("profile_expense", 150)
st.info(f"📋 홈 프로필 적용 중 — {_age}세 | 월 소득 {_income}만원 | 금융 자산 {_asset:,}만원 | 월 생활비 {_expense}만원")

with st.expander("👤 기본 정보", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        age    = st.number_input("나이", min_value=1, max_value=100, key="profile_age")
        income = st.number_input("월 소득 (만원)", min_value=0, step=10, key="profile_income")
    with col2:
        asset  = st.number_input("현재 금융 자산 (만원)", min_value=0, step=100, key="profile_asset")
        monthly_save = st.number_input("월 저축 가능 금액 (만원)", min_value=0, value=50, step=5)

with st.expander("🎯 재무 목표", expanded=False):
    goals = st.multiselect(
        "목표를 선택하세요 (복수 선택 가능)",
        ["단기 목돈 마련 (1~3년)", "장기 자산 증식 (3~10년)", "노후 준비 (은퇴 대비)", "안전한 자산 보관"],
        default=["노후 준비 (은퇴 대비)"]
    )
    risk_level = st.select_slider(
        "투자 성향",
        options=["매우 안전 추구", "안전 추구", "중립", "수익 추구", "적극 투자"],
        value="안전 추구"
    )

with st.expander("➕ 추가 정보 (선택)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        has_pension   = st.selectbox("국민연금 가입 여부", ["가입 중", "미가입", "수령 중"])
        has_irp       = st.selectbox("IRP/연금저축 보유 여부", ["없음", "IRP 보유", "연금저축 보유", "둘 다 보유"])
    with col2:
        tax_concern   = st.selectbox("세금 절약 관심도", ["관심 없음", "보통", "매우 관심 있음"])
        has_loan      = st.selectbox("대출 여부", ["없음", "있음 (소액)", "있음 (고액)"])

st.divider()

if st.button("💎 AI 맞춤 상품 추천 받기", type="primary"):
    if not goals:
        st.warning("재무 목표를 하나 이상 선택해주세요.")
    else:
        with st.spinner("AI가 맞춤 상품을 분석 중입니다..."):
            prompt = f"""
당신은 고령 고객 전문 자산관리 AI입니다.
사용자 유형: {user_type}
- 고령층: 아주 쉬운 말, 짧은 문장, 일상 비유 활용
- 일반 사용자: 핵심 위주 설명
- 금융 초보자: 금융 용어 쉽게 풀이

고객 정보:
- 나이: {age}세
- 월 소득: {income}만원
- 현재 금융 자산: {asset}만원
- 월 저축 가능 금액: {monthly_save}만원
- 재무 목표: {', '.join(goals)}
- 투자 성향: {risk_level}
- 국민연금: {has_pension}
- IRP/연금저축: {has_irp}
- 세금 절약 관심: {tax_concern}
- 대출: {has_loan}

고객의 목표와 상황에 맞는 JB금융그룹 계열사 상품을 우선 추천하세요.
각 추천 상품에 계열사명(전북은행/광주은행/JB우리캐피탈/JB자산운용)을 반드시 포함하고 쉽게 설명하세요.

JB금융그룹 참고 상품 목록:
{JB_PRODUCTS}

고객을 따님, 아드님 등 가족 호칭으로 절대 부르지 마세요. "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

종합평가:
(현재 재무 상태 한 줄 평가)

단기추천:
(1~3년 목표 상품 추천. 없으면 "해당 없음". 상품명과 이유 포함. 번호 목록)

장기추천:
(3~10년 목표 상품 추천. 없으면 "해당 없음". 상품명과 이유 포함. 번호 목록)

노후추천:
(노후 대비 상품 추천. 없으면 "해당 없음". 상품명과 이유 포함. 번호 목록)

세금절약:
(절세 가능한 상품/방법. 없으면 "해당 없음". 번호 목록)

쉬운설명:
(전체 추천을 {user_type} 수준으로 쉽게 3~4문장 요약)

우선순위행동:
(지금 당장 해야 할 행동. 번호 목록 3가지)
"""
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                result = response.text
            except Exception:
                st.error("⚠️ AI 서버에 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
                st.stop()

        def extract(label, text):
            escaped = re.escape(label)
            pattern = rf"{escaped}:\s*(.*?)(?=\n[^\d\s][^\n]*:|\Z)"
            match = re.search(pattern, text, re.DOTALL)
            return match.group(1).strip() if match else ""

        overall   = extract("종합평가", result)
        short     = extract("단기추천", result)
        long_term = extract("장기추천", result)
        retire    = extract("노후추천", result)
        tax       = extract("세금절약", result)
        easy      = extract("쉬운설명", result)
        actions   = extract("우선순위행동", result)

        st.divider()

        # 종합 평가
        st.markdown("### 📊 종합 평가")
        st.info(overall if overall else result)

        # 목표별 추천
        st.markdown("### 🎯 목표별 추천 상품")
        tab1, tab2, tab3 = st.tabs(["📅 단기 추천 (1~3년)", "📈 장기 추천 (3~10년)", "🏖️ 노후 추천 (은퇴 대비)"])
        with tab1:
            if short and short != "해당 없음":
                st.success(short)
            else:
                st.caption("해당 없음")
        with tab2:
            if long_term and long_term != "해당 없음":
                st.success(long_term)
            else:
                st.caption("해당 없음")
        with tab3:
            if retire and retire != "해당 없음":
                st.success(retire)
            else:
                st.caption("해당 없음")

        # 절세
        if tax and tax != "해당 없음":
            st.markdown("### 💰 절세 상품 추천")
            st.warning(tax)

        # 쉬운 설명
        st.markdown("### 💬 쉽게 말하면")
        st.write(easy if easy else result)

        # 우선순위 행동
        if actions:
            st.markdown("### 💡 지금 당장 해야 할 행동")
            st.success(actions)

        # JB금융그룹 상담 연결
        st.divider()
        st.markdown("### 🏦 JB금융그룹 상담 연결")
        st.info("AI 추천 상품에 대해 JB금융그룹 전문 상담사와 직접 상담하실 수 있습니다.")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.success("**전북은행**\n☎ 1588-4477")
        with col2:
            st.success("**광주은행**\n☎ 1588-3388")
        with col3:
            st.info("**JB우리캐피탈**\n☎ 1600-2266")
        with col4:
            st.info("**JB자산운용**\n홈페이지 방문")