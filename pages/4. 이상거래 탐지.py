import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="이상거래 탐지", page_icon="🔍", layout="centered")

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

st.title("🔍 이상거래 탐지")
st.caption("최근 거래 내역을 입력하면 AI가 위험 패턴을 분석합니다.")
st.divider()

# ──────────────────────────────────────────────
# 고객 기본 정보
# ──────────────────────────────────────────────
st.markdown("### 📋 기본 정보")

with st.expander("👤 고객 정보", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name   = st.text_input("이름", placeholder="홍길동")
        income = st.number_input("월 소득 / 연금 (만원)", min_value=0, value=80, step=5,
                                 help="평소 거래 규모 파악에 사용됩니다.")
    with col2:
        age    = st.number_input("나이", min_value=1, max_value=100, value=70)
        avg_expense = st.number_input("평소 월 지출 (만원)", min_value=0, value=100, step=5,
                                      help="평소 대비 이상 지출 탐지에 사용됩니다.")

# ──────────────────────────────────────────────
# 거래 내역 입력
# ──────────────────────────────────────────────
st.markdown("### 📂 최근 거래 내역")
st.caption("날짜 | 항목 | 금액 | 수신처 형식으로 입력하면 더 정확하게 분석됩니다.")

# 예시 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button("⚠️ 위험 거래 예시 불러오기"):
        st.session_state.tx_example = """2025-01-15 | 해외 송금 | 500만원 | 베트남 계좌
2025-01-15 | ATM 출금 | 200만원 | 강남역
2025-01-14 | 모르는 번호 송금 | 150만원 | 010-9999-1234
2025-01-13 | 온라인 쇼핑 | 8만원 | 쿠팡
2025-01-12 | 편의점 | 1만원 | GS25"""
with col2:
    if st.button("✅ 정상 거래 예시 불러오기"):
        st.session_state.tx_example = """2025-01-15 | 마트 | 8만원 | 이마트
2025-01-14 | 병원비 | 3만원 | 서울성모병원
2025-01-13 | 편의점 | 1만원 | GS25
2025-01-12 | 약국 | 1만원 | 온누리약국
2025-01-11 | 경로당 | 0.5만원 | 강남경로당"""

transaction = st.text_area(
    "거래 내역 입력",
    value=st.session_state.get("tx_example", ""),
    placeholder="예)\n2025-01-15 | 해외 송금 | 500만원 | 베트남 계좌\n2025-01-14 | ATM 출금 | 200만원 | 강남역",
    height=200,
    label_visibility="collapsed"
)

st.divider()

# ──────────────────────────────────────────────
# 분석 버튼
# ──────────────────────────────────────────────
if st.button("🔍 AI 이상거래 분석 시작", type="primary"):
    if not transaction.strip():
        st.warning("거래 내역을 입력해주세요.")
    elif not name:
        st.warning("이름을 입력해주세요.")
    else:
        with st.spinner("AI가 거래 패턴을 분석 중입니다..."):
            prompt = f"""
당신은 고령 고객을 보호하는 금융 이상거래 탐지 AI입니다.
사용자 유형: {user_type}
- 고령층: 아주 쉬운 말, 짧은 문장
- 일반 사용자: 핵심 위주 설명
- 금융 초보자: 금융 용어 쉽게 풀이

고객 정보:
- 이름: {name} / 나이: {age}세
- 월 소득/연금: {income}만원
- 평소 월 지출: {avg_expense}만원

최근 거래 내역:
{transaction}

아래 항목을 기준으로 이상거래를 탐지하세요.
1. 평소 대비 과도한 금액 지출
2. 고액 송금 (월 소득 대비 큰 금액)
3. 해외 송금
4. 모르는 번호/계좌로 송금
5. 보이스피싱 의심 패턴 (급하게 큰돈 이동 등)

고객을 따님, 아드님 등 가족 호칭으로 절대 부르지 마세요. 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

위험도: [낮음/보통/높음]

탐지된패턴:
(발견된 위험 패턴. 없으면 "특이사항 없음". 번호 목록)

위험거래:
(가장 위험한 거래 1~2개 구체적으로. 없으면 "해당 없음")

쉬운설명:
(고객님께 쉽게 설명. 2~3문장. {user_type} 수준으로)

추천행동:
(지금 당장 해야 할 행동. 번호 목록 2~3가지)

가족알림필요: [필요/불필요]
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            result = response.text

        # ── 파싱
        def extract(label, text):
            escaped = re.escape(label)
            pattern = rf"{escaped}:\s*(.*?)(?=\n\S[^\n]*:|\Z)"
            match = re.search(pattern, text, re.DOTALL)
            return match.group(1).strip() if match else ""

        risk     = extract("위험도", result)
        patterns = extract("탐지된패턴", result)
        danger   = extract("위험거래", result)
        easy     = extract("쉬운설명", result)
        actions  = extract("추천행동", result)
        notify   = extract("가족알림필요", result)

        st.divider()

        # ① 위험도 배너
        if "높음" in risk:
            st.error("🔴 위험도: 높음 — 이상거래가 감지되었습니다!")
        elif "보통" in risk:
            st.warning("🟡 위험도: 보통 — 주의가 필요한 거래가 있습니다.")
        else:
            st.success("🟢 위험도: 낮음 — 정상적인 거래로 보입니다.")

        # ② 위험 거래
        if danger and danger != "해당 없음":
            st.markdown("### ⚠️ 위험 거래")
            st.error(danger)

        # ③ 탐지된 패턴
        st.markdown("### 🔎 탐지된 패턴")
        if patterns and patterns != "특이사항 없음":
            st.warning(patterns)
        else:
            st.success("특이사항이 없습니다.")

        # ④ 쉬운 설명
        st.markdown("### 💬 쉽게 말하면")
        st.info(easy if easy else result)

        # ⑤ 추천 행동
        if actions:
            st.markdown("### 💡 지금 당장 해야 할 행동")
            st.success(actions)

        # ⑥ 가족 알림
        if "필요" in notify:
            st.divider()
            st.markdown("### 👨‍👩‍👧 가족 보호 알림")
            st.error("🚨 위험 거래가 감지되었습니다. 보호자에게 알림을 전송하는 것을 권장합니다.")

            col1, col2 = st.columns(2)
            with col1:
                family_name  = st.text_input("보호자 이름", placeholder="홍길순")
            with col2:
                family_phone = st.text_input("보호자 연락처", placeholder="010-1234-5678")

            if st.button("📨 보호자 알림 전송 (시뮬레이션)"):
                st.success(f"📨 {family_name or '보호자'}님께 알림을 전송했습니다. (시뮬레이션)\n\n"
                           f"'[안심케어 AI] {name}고객님 계정에서 위험 거래가 감지되었습니다. 확인 부탁드립니다.'")