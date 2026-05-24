import streamlit as st

st.set_page_config(
    page_title="안심케어 AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ 안심케어 AI")
st.subheader("AI 노후 인생 코치")
st.markdown("은퇴 이후의 생활비, 현금흐름, 금융사기 위험을 AI가 쉽고 안전하게 관리해드립니다.")
st.markdown("미래 생활 안정 분석부터 이상거래 탐지, 가족 보호 알림까지 고령 고객님의 노후 생활을 안전하게 지켜드립니다.")

st.divider()

st.markdown("### 주요 서비스")

st.html("""
    <style>
        div[data-testid="stAlertContainer"] {
            min-height: 145px !important;
            max-height: 145px !important;
            display: flex !important;
            align-items: flex-start !important;
        }
    </style>
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📅 **미래 생활 안정 시뮬레이션**\n\n자산, 연금, 생활비를 기반으로 미래 생활 안정성과 노후 리스크를 분석합니다.")
    if st.button("생활 안정 분석 시작하기 →", key="btn_finance", use_container_width=True):
        st.switch_page("pages/1. 미래 생활 안정 시뮬레이션.py")

with col2:
    st.warning("👨‍👩‍👧 **가족 보호 알림**\n\n위험 상황 발생 시 보호자에게 알림을 전송합니다.")
    if st.button("가족 알림 보기 →", key="btn_family", use_container_width=True):
        st.switch_page("pages/2. 가족 보호 알림.py")

with col3:
    st.success("💬 **쉬운 금융 설명**\n\n어려운 금융 용어와 분석 결과를 쉬운 말로 설명해드립니다.")
    if st.button("쉬운 설명 보기 →", key="btn_explain", use_container_width=True):
        st.switch_page("pages/3. 쉬운 금융 설명.py")

col4, col5, col6 = st.columns(3)

with col4:
    st.error("🕵️ **이상거래 탐지**\n\n평소와 다른 위험 거래와 금융사기 패턴을 AI가 탐지합니다.")
    if st.button("거래 탐지 보기 →", key="btn_detect", use_container_width=True):
        st.switch_page("pages/4. 이상거래 탐지.py")

with col5:
    st.info("📄 **문서 쉽게 이해하기**\n\n복잡한 보험·대출 문서를 쉬운 말로 바꿔드립니다.")
    if st.button("문서 분석 보기 →", key="btn_doc", use_container_width=True):
        st.switch_page("pages/5. 문서 쉽게 이해하기.py")

with col6:
    st.success("💎 **맞춤 금융 상품 추천**\n\n나이, 자산, 목표에 따라 단기·장기·노후 맞춤 계좌와 투자 상품을 추천해드립니다.")
    if st.button("맞춤 상품 추천 →", key="btn_recommend", use_container_width=True):
        st.switch_page("pages/6. 맞춤 금융 상품 추천.py")

st.divider()
st.caption("천천히, 쉽게, 안전하게. AI가 여러분의 노후 금융 생활을 지켜드립니다. | JB금융그룹 Fin:AI Challenge")