import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import re
from datetime import datetime

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="가족 보호 알림", page_icon="👨‍👩‍👧", layout="centered")

if "user_type" not in st.session_state:
    st.session_state.user_type = "고령층"
if "alert_log" not in st.session_state:
    st.session_state.alert_log = []

user_type = st.selectbox("사용자 유형", ["고령층", "일반 사용자", "금융 초보자"], key="user_type")

if user_type == "고령층":
    st.markdown("""
    <style>
    .stApp, .stApp p, .stApp div, .stApp label, .stApp span { font-size: 20px !important; }
    .stButton > button { font-size: 22px !important; height: 60px !important; width: 100% !important; }
    .stTextInput input, .stTextArea textarea, .stNumberInput input { font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍👩‍👧 가족 보호 알림")
st.caption("위험 상황 발생 시 보호자에게 알림을 전송하고 가족이 함께 관리합니다.")
st.divider()

# ──────────────────────────────────────────────
# 고객 & 보호자 정보
# ──────────────────────────────────────────────
st.markdown("### 📋 기본 정보")

with st.expander("👤 고객 정보", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("고객 이름", placeholder="홍길동")
    with col2:
        age  = st.number_input("나이", min_value=1, max_value=100, value=70)

with st.expander("👨‍👩‍👧 보호자 정보", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        family_name     = st.text_input("보호자 이름", placeholder="홍길순")
        family_relation = st.selectbox("관계", ["자녀", "배우자", "형제/자매", "기타"])
    with col2:
        family_phone    = st.text_input("보호자 연락처", placeholder="010-1234-5678")
        family_name2    = st.text_input("보호자 이름 2 (선택)", placeholder="홍길남")
        family_phone2   = st.text_input("보호자 연락처 2 (선택)", placeholder="010-5678-1234")

st.divider()

# ──────────────────────────────────────────────
# 위험 상황 입력
# ──────────────────────────────────────────────
st.markdown("### ⚠️ 위험 상황 입력")

with st.expander("🚨 상황 설명", expanded=True):
    situation_type = st.selectbox(
        "상황 유형",
        ["이상거래 감지", "보이스피싱 의심", "고액 송금 시도", "해외 송금 감지", "직접 입력"]
    )

    if situation_type == "직접 입력":
        situation = st.text_area("상황 설명", placeholder="위험 상황을 직접 입력하세요.", height=100)
    else:
        situation_map = {
            "이상거래 감지": "평소와 다른 이상한 거래가 감지되었습니다. 고액 출금 및 모르는 계좌로 송금이 있었습니다.",
            "보이스피싱 의심": "보이스피싱으로 의심되는 전화를 받고 돈을 보내려 하고 있습니다.",
            "고액 송금 시도": "평소 소득 대비 매우 큰 금액의 송금을 시도하고 있습니다.",
            "해외 송금 감지": "해외 계좌로 큰 금액의 송금이 감지되었습니다."
        }
        situation = situation_map[situation_type]
        st.info(f"💬 {situation}")

    amount = st.text_input("관련 금액 (선택)", placeholder="예: 500만원")

st.divider()

# ──────────────────────────────────────────────
# AI 알림 메시지 생성 + 전송
# ──────────────────────────────────────────────
if st.button("📨 AI 알림 메시지 생성 및 전송", type="primary"):
    if not name or not family_name or not family_phone:
        st.warning("고객 이름, 보호자 이름, 보호자 연락처는 필수입니다.")
    elif not situation.strip():
        st.warning("위험 상황을 입력해주세요.")
    else:
        with st.spinner("AI가 알림 메시지를 생성 중입니다..."):
            prompt = f"""
당신은 고령 고객 보호 금융 AI입니다.
아래 상황을 바탕으로 보호자에게 전송할 알림 메시지를 작성하세요.

고객 정보:
- 이름: {name} / 나이: {age}세

보호자 정보:
- 이름: {family_name} / 관계: {family_relation}

위험 상황:
- 유형: {situation_type}
- 내용: {situation}
- 관련 금액: {amount if amount else "미입력"}

아래 3가지를 작성하세요.
마크다운 절대 금지. 순수 텍스트.

긴급알림메시지:
(SMS 형식. 2~3문장. 간결하고 명확하게. 보호자가 바로 이해할 수 있게)

상세설명:
(상황을 좀 더 자세히 설명. 3~4문장. 보호자가 취해야 할 행동 포함)

권고행동:
(보호자가 지금 당장 해야 할 행동. 번호 목록 2~3가지)
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

        sms     = extract("긴급알림메시지", result)
        detail  = extract("상세설명", result)
        actions = extract("권고행동", result)

        st.divider()
        st.markdown("### 📨 생성된 알림 메시지")

        # SMS 미리보기
        st.markdown("**📱 SMS 알림 (시뮬레이션)**")
        st.error(f"[안심케어 AI 긴급알림]\n\n{sms}")

        # 전송 대상
        targets = f"{family_name}님 ({family_phone})"
        if family_name2 and family_phone2:
            targets += f", {family_name2}님 ({family_phone2})"
        st.success(f"✅ 알림 전송 완료 → {targets} (시뮬레이션)")

        # 전송 시각 기록
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.alert_log.append({
            "시각": now,
            "고객": name,
            "상황": situation_type,
            "금액": amount or "-",
            "수신": targets
        })

        # 상세 설명
        st.markdown("### 📋 상세 상황 설명")
        st.warning(detail if detail else result)

        # 권고 행동
        if actions:
            st.markdown("### 💡 보호자 권고 행동")
            st.info(actions)

        # 추가 안내
        st.markdown("### 📞 긴급 연락처")
        col1, col2 = st.columns(2)
        with col1:
            st.error("🚨 금융감독원\n☎ 1332")
        with col2:
            st.error("🚨 경찰청 사이버수사대\n☎ 182")

st.divider()

# ──────────────────────────────────────────────
# 알림 발송 이력
# ──────────────────────────────────────────────
st.markdown("### 📋 알림 발송 이력")

if st.session_state.alert_log:
    for log in reversed(st.session_state.alert_log):
        st.markdown(f"""
> 🕐 **{log['시각']}** | 고객: {log['고객']} | 상황: {log['상황']} | 금액: {log['금액']}
> 수신: {log['수신']}
""")
    if st.button("🗑️ 이력 초기화"):
        st.session_state.alert_log = []
        st.rerun()
else:
    st.caption("아직 발송된 알림이 없습니다.")