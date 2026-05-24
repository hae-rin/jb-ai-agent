import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="맞춤 금융 상품 추천", page_icon="💎", layout="centered")

if "user_type" not in st.session_state:
    st.session_state.user_type = "고령층"

user_type = st.selectbox("사용자 유형", ["고령층", "일반 사용자", "금융 초보자"], key="user_type")

if user_type == "고령층":
    st.markdown("""
    <style>
    .stApp, .stApp p, .stApp div, .stApp label, .stApp span { font-size: 20px !important; }
    .stButton > button { font-size: 22px !important; height: 60px !important; width: 100% !important; }
    .stTextInput input, .stTextArea textarea, .stNumberInput input { font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 맞춤 금융 상품 추천")
st.caption("나이, 자산, 목표에 따라 AI가 최적의 계좌와 투자 상품을 추천해드립니다.")
st.divider()

# ──────────────────────────────────────────────
# 입력
# ──────────────────────────────────────────────
st.markdown("### 📋 기본 정보 입력")

with st.expander("👤 기본 정보", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        age    = st.number_input("나이", min_value=1, max_value=100, value=45)
        income = st.number_input("월 소득 (만원)", min_value=0, value=300, step=10)
    with col2:
        asset  = st.number_input("현재 금융 자산 (만원)", min_value=0, value=5000, step=100)
        monthly_save = st.number_input("월 저축 가능 금액 (만원)", min_value=0, value=50, step=5)

with st.expander("🎯 재무 목표", expanded=True):
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

고객의 목표와 상황에 맞는 금융 상품을 추천하세요.
각 목표별로 구체적인 상품을 추천하고 쉽게 설명하세요.

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
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            result = response.text

        def extract(label, text):
            escaped = re.escape(label)
            pattern = rf"{escaped}:\s*(.*?)(?=\n\S[^\n]*:|\Z)"
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
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**📅 단기 추천**\n(1~3년)")
            if short and short != "해당 없음":
                st.success(short)
            else:
                st.caption("해당 없음")
        with col2:
            st.markdown("**📈 장기 추천**\n(3~10년)")
            if long_term and long_term != "해당 없음":
                st.success(long_term)
            else:
                st.caption("해당 없음")
        with col3:
            st.markdown("**🏖️ 노후 추천**\n(은퇴 대비)")
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