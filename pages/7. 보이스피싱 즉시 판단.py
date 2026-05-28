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

st.set_page_config(page_title="보이스피싱 즉시 판단", page_icon="🚨", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

user_type = st.session_state.get("user_type", "고령층")
apply_user_css(user_type)

st.html(f"""
<div style="width:100%;margin-bottom:20px;box-sizing:border-box;
  background:linear-gradient(135deg,#991B1B 0%,#EF4444 100%);
  border-radius:16px;padding:24px 32px 20px;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;">
  <div style="margin-bottom:14px;">
    <a href="/" style="color:rgba(255,255,255,0.75);text-decoration:none;font-size:13px;font-weight:500;">← 홈으로</a>
  </div>
  <div style="display:flex;align-items:center;gap:16px;">
    <div style="font-size:42px;line-height:1;">🚨</div>
    <div>
      <div style="font-size:{'28px' if user_type == '고령층' else '22px'};font-weight:800;color:white;line-height:1.2;">보이스피싱 즉시 판단</div>
      <div style="font-size:{'16px' if user_type == '고령층' else '13px'};color:rgba(255,255,255,0.82);margin-top:5px;line-height:1.6;">의심스러운 전화나 문자 내용을 붙여넣으면 AI가 바로 사기 여부를 판단해드립니다.</div>
    </div>
  </div>
</div>
""")

# ──────────────────────────────────────────────
# 예시 불러오기
# ──────────────────────────────────────────────
st.markdown("### 📋 예시 불러오기")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⚠️ 사기 문자 예시"):
        st.session_state["vp_input"] = """[국민은행] 고객님 계좌가 이상거래로 인해 일시정지 되었습니다.
본인확인을 위해 아래 링크를 클릭하여 주민등록번호와 카드번호를 입력해 주세요.
http://kb-safe-verify.xyz/confirm
미처리시 계좌가 영구 동결됩니다."""
        st.rerun()
with col2:
    if st.button("⚠️ 사기 전화 예시"):
        st.session_state["vp_input"] = """검찰청 수사관입니다. 고객님 명의로 대포통장이 개설되어 현재 수사 중에 있습니다.
지금 즉시 본인 계좌에 있는 돈을 안전계좌로 이체하지 않으면 전 재산이 동결됩니다.
빨리 가까운 ATM으로 가셔서 010-9999-0000 계좌로 이체해 주세요.
절대 가족에게 말하지 마세요."""
        st.rerun()
with col3:
    if st.button("✅ 정상 문자 예시"):
        st.session_state["vp_input"] = """[전북은행] 고객님의 정기예금 만기일이 7일 후(2025-02-01)입니다.
만기 후 처리방법 선택은 인터넷뱅킹 또는 가까운 영업점을 방문해 주시기 바랍니다.
문의: 1588-4477 (전북은행 고객센터)"""
        st.rerun()

st.divider()

# ──────────────────────────────────────────────
# 입력
# ──────────────────────────────────────────────
st.markdown("### 📝 의심스러운 내용 입력")
st.caption("전화 통화 내용이나 문자 메시지를 그대로 붙여넣으세요.")

content = st.text_area(
    "내용 입력",
    value=st.session_state.get("vp_input", ""),
    placeholder="예)\n[국민은행] 계좌가 정지되었습니다. 즉시 링크를 클릭하여 본인 확인을 해주세요.\nhttp://...",
    height=220,
    label_visibility="collapsed"
)

st.divider()

# ──────────────────────────────────────────────
# 분석
# ──────────────────────────────────────────────
if st.button("🔍 지금 바로 판단하기", type="primary"):
    if not content.strip():
        st.warning("판단할 내용을 입력해주세요.")
    else:
        with st.spinner("AI가 분석 중입니다..."):
            prompt = f"""
당신은 금융 보이스피싱·스미싱 전문 탐지 AI입니다.
사용자 유형: {user_type}
- 고령층: 아주 쉬운 말, 짧은 문장
- 일반 사용자: 핵심 위주 설명
- 금융 초보자: 금융 용어 쉽게 풀이

아래 내용이 보이스피싱·스미싱·금융사기인지 판단하세요.

내용:
{content}

판단 기준:
1. 긴급성·공포감 조성 (즉시, 동결, 수사, 체포, 미처리시 등)
2. 개인정보·금융정보 요구 (주민등록번호, 카드번호, 비밀번호 등)
3. 출처 불명 링크 포함 여부
4. 공공기관·금융기관 사칭 (검찰, 경찰, 금감원, 국민은행 등)
5. 계좌 이체·ATM 이용 유도
6. 가족에게 비밀로 하라는 요구
7. 실제 공식 기관이 절대 하지 않는 요청

고객을 따님, 아드님 등 가족 호칭으로 절대 부르지 마세요. 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

판정: [사기/정상/주의]

위험도: [높음/보통/낮음]

발견된위험신호:
(사기 징후. 없으면 "이상 없음". 번호 목록)

쉬운설명:
(고령층도 바로 이해할 수 있는 쉬운 설명. 2~3문장)

지금해야할행동:
(지금 당장 해야 할 행동. 번호 목록)
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

        verdict  = extract("판정", result)
        risk     = extract("위험도", result)
        signals  = extract("발견된위험신호", result)
        easy     = extract("쉬운설명", result)
        actions  = extract("지금해야할행동", result)

        st.divider()

        # ① 판정 배너
        if "사기" in verdict:
            st.error("🚨 판정: 사기 — 즉시 전화를 끊고 아무것도 하지 마세요!")
        elif "주의" in verdict:
            st.warning("⚠️ 판정: 주의 — 섣불리 행동하지 마세요. 가족이나 은행에 먼저 확인하세요.")
        else:
            st.success("✅ 판정: 정상으로 보입니다.")

        # ② 위험도
        if "높음" in risk:
            st.error(f"위험도: 높음")
        elif "보통" in risk:
            st.warning(f"위험도: 보통")
        else:
            st.success(f"위험도: 낮음")

        # ③ 발견된 위험 신호
        st.markdown("### 🔎 발견된 위험 신호")
        if signals and signals != "이상 없음":
            st.error(signals)
        else:
            st.success("특별한 위험 신호가 없습니다.")

        # ④ 쉬운 설명
        st.markdown("### 💬 쉽게 말하면")
        st.info(easy if easy else result)

        # ⑤ 지금 해야 할 행동
        if actions:
            st.markdown("### 💡 지금 해야 할 행동")
            if "사기" in verdict or "주의" in verdict:
                st.error(actions)
            else:
                st.success(actions)

        # ⑥ 긴급 연락처 (사기/주의 시)
        if "사기" in verdict or "주의" in verdict:
            st.divider()
            st.markdown("### 📞 긴급 신고 연락처")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.error("🚨 금융감독원\n☎ 1332")
            with col2:
                st.error("🚨 경찰청\n☎ 112")
            with col3:
                st.error("🚨 금융범죄신고\n☎ 182")
