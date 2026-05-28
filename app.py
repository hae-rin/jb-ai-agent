import json
from pathlib import Path

import streamlit as st
from utils import apply_user_css

_PROFILE_FILE = Path("profile.json")

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
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] { padding: 0 !important; }

/* 클리핑 방지 */
[data-testid="stHorizontalBlock"],
[data-testid="stColumn"],
[data-testid="stVerticalBlock"] {
    overflow: visible !important;
}

/* 서비스 카드 */
.jb-card {
    position: relative;
    border: 1.5px solid #E5E7EB;
    border-radius: 18px;
    background: white;
    padding: 28px 20px 20px;
    text-align: center;
    transform: translateY(0);
    transition: box-shadow 0.25s ease, transform 0.22s ease, border-color 0.22s ease;
    will-change: transform;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', sans-serif;
    margin-bottom: 6px;
}
.jb-card:hover {
    box-shadow: 0 14px 38px rgba(37,99,235,0.15);
    transform: translateY(-8px);
    border-color: #93C5FD;
}
.jb-card:active {
    transform: translateY(-2px) scale(0.97);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
/* 버튼 hover 시 카드 애니메이션 */
[data-testid="stColumn"] [data-testid="stVerticalBlock"]:has(button:hover) .jb-card {
    box-shadow: 0 14px 38px rgba(37,99,235,0.15) !important;
    transform: translateY(-8px) !important;
    border-color: #93C5FD !important;
}
[data-testid="stColumn"] [data-testid="stVerticalBlock"]:has(button:active) .jb-card {
    transform: translateY(-2px) scale(0.97) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
}

</style>
""", unsafe_allow_html=True)


# ── 프로필 초기 로드 (세션당 1회) ─────────────────────────
if not st.session_state.get("_profile_loaded"):
    saved = {}
    if _PROFILE_FILE.exists():
        try:
            saved = json.loads(_PROFILE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    st.session_state.setdefault("profile_age",    saved.get("age",       70))
    st.session_state.setdefault("profile_income",  saved.get("income",    80))
    st.session_state.setdefault("profile_asset",   saved.get("asset",  20000))
    st.session_state.setdefault("profile_expense", saved.get("expense",  150))
    st.session_state.setdefault("user_type",       saved.get("user_type", "고령층"))
    st.session_state["_profile_loaded"] = True

user_type = st.session_state.get("user_type", "고령층")
apply_user_css(user_type)

# ── 히어로 배너 ──────────────────────────────────────────
st.html("""
<div style="
  width:100%; margin:0; padding:0; box-sizing:border-box;
  background:linear-gradient(135deg,#EEF4FF 0%,#DBEAFE 60%,#EFF6FF 100%);
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;
">
  <div style="max-width:1500px;margin:0 auto;padding:52px 60px 48px;display:flex;align-items:center;gap:36px;">
    <div style="flex:1.4;min-width:260px;">
      <div style="font-size:46px;font-weight:900;color:#1E3A5F;line-height:1.2;margin-bottom:14px;">
        AI가 지켜드리는<br><span style="color:#2563EB;">안심 금융 생활</span>
      </div>
      <div style="font-size:15px;color:#4B5563;line-height:1.85;margin-bottom:22px;">
        생활비, 연금, 현금흐름부터 금융사기 위험까지<br>
        AI가 분석하고 가족에게 알림을 전해드립니다.
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:30px;">
        <span style="display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.88);border-radius:20px;padding:7px 15px;font-size:13px;color:#374151;font-weight:500;">⏱ AI 맞춤 분석</span>
        <span style="display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.88);border-radius:20px;padding:7px 15px;font-size:13px;color:#374151;font-weight:500;">🛡 실시간 위험 감지</span>
        <span style="display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.88);border-radius:20px;padding:7px 15px;font-size:13px;color:#374151;font-weight:500;">📊 노후 생활 분석</span>
      </div>
    </div>
  </div>
</div>
""")


# ── 프로필 ────────────────────────────────────────────────
with st.expander("👤 내 프로필 설정 (전 페이지에서 자동 적용)", expanded=False):
    st.selectbox("사용자 유형", ["고령층", "일반 사용자", "금융 초보자"], key="user_type")
    p1, p2 = st.columns(2)
    with p1:
        st.number_input("나이", min_value=1, max_value=100, key="profile_age")
        st.number_input("월 소득/연금 (만원)", min_value=0, step=5, key="profile_income")
    with p2:
        st.number_input("금융 자산 (만원)", min_value=0, step=100, key="profile_asset")
        st.number_input("월 생활비 (만원)", min_value=0, step=5, key="profile_expense")

    st.caption("💾 저장하면 앱을 껐다 켜도 설정이 유지됩니다.")
    if st.button("💾 프로필 저장", type="primary"):
        data = {
            "age":       st.session_state["profile_age"],
            "income":    st.session_state["profile_income"],
            "asset":     st.session_state["profile_asset"],
            "expense":   st.session_state["profile_expense"],
            "user_type": st.session_state["user_type"],
        }
        _PROFILE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        st.success("저장되었습니다!")

# ── 섹션 타이틀 ───────────────────────────────────────────
st.html("""
<div style="text-align:center;margin:44px 0 20px;font-size:20px;font-weight:700;color:#1F2937;
            font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;">
  <span style="color:#D1D5DB;">── </span>주요 서비스<span style="color:#D1D5DB;"> ──</span>
</div>
""")

# ── 서비스 카드 ─────────────────────────────────────────────
_cards = [
    ("🤖", "AI 종합 케어 에이전트",    "재무 상태, 거래 위험, 맞춤 케어 플랜까지 AI가 단계별로 분석해드립니다.",    "#2563EB", "#EFF6FF", "pages/0. AI 종합 케어 에이전트.py",     "에이전트 시작하기 →"),
    ("📊", "미래 생활 안정 시뮬레이션", "자산, 연금, 월 생활비를 기반으로 노후 생활 안정성을 분석합니다.",          "#0891B2", "#ECFEFF", "pages/1. 미래 생활 안정 시뮬레이션.py", "생활 안정 분석 시작하기 →"),
    ("🌟", "노후 버킷리스트",           "꼭 이루고 싶은 꿈을 AI가 실현 가능한 재무 계획으로 만들어드립니다.",        "#D97706", "#FFFBEB", "pages/6. 노후 버킷리스트.py",          "버킷리스트 시작하기 →"),
    ("🚨", "보이스피싱 즉시 판단",      "의심스러운 전화나 문자를 붙여넣으면 AI가 바로 사기 여부를 판단해드립니다.", "#DC2626", "#FFF1F2", "pages/7. 보이스피싱 즉시 판단.py",     "지금 바로 판단하기 →"),
    ("📄", "문서 쉽게 이해하기",        "복잡한 보험·대출 문서를 쉬운 말로 핵심만 요약해드립니다.",                  "#7C3AED", "#F5F3FF", "pages/4. 문서 쉽게 이해하기.py",       "문서 분석 보기 →"),
    ("💎", "맞춤 금융 상품 추천",       "나이, 자산, 목표에 따라 단기·장기·노후 맞춤 상품을 추천해드립니다.",        "#059669", "#ECFDF5", "pages/5. 맞춤 금융 상품 추천.py",      "맞춤 상품 추천 →"),
]

for row_start in range(0, 6, 3):
    cols = st.columns(3, gap="medium")
    for i, (col, (icon, title, desc, color, bg, page, cta)) in enumerate(
        zip(cols, _cards[row_start:row_start + 3])
    ):
        with col:
            st.markdown(f"""
<div class="jb-card">
  <div style="width:68px;height:68px;border-radius:50%;background:{bg};
    display:inline-flex;align-items:center;justify-content:center;
    font-size:32px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,0.07);">{icon}</div>
  <div style="font-size:16px;font-weight:700;color:{color};margin-bottom:8px;line-height:1.4;">{title}</div>
  <div style="font-size:13.5px;color:#6B7280;line-height:1.75;margin-bottom:4px;">{desc}</div>
</div>
""", unsafe_allow_html=True)
            if st.button(cta, key=f"nav_{row_start+i}", use_container_width=True):
                st.switch_page(page)

# ── 특별한 이유 + 푸터 ────────────────────────────────────
st.html("""
<div style="margin:52px 0 0;padding:0 32px 48px;
            font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;">
  <div style="font-size:18px;font-weight:700;color:#1F2937;margin-bottom:14px;">안심케어 AI가 특별한 이유</div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">
    <div style="background:#F9FAFB;border-radius:14px;padding:20px 18px;display:flex;gap:14px;align-items:flex-start;">
      <div style="width:44px;height:44px;border-radius:50%;background:#EFF6FF;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:22px;">🛡️</div>
      <div><div style="font-size:14px;font-weight:700;color:#1F2937;margin-bottom:4px;">금융 사기 예방</div><div style="font-size:12px;color:#6B7280;line-height:1.6;">AI가 위험 패턴을 분석하여 금융 사기를 예방합니다.</div></div>
    </div>
    <div style="background:#F9FAFB;border-radius:14px;padding:20px 18px;display:flex;gap:14px;align-items:flex-start;">
      <div style="width:44px;height:44px;border-radius:50%;background:#F5F3FF;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:22px;">🔒</div>
      <div><div style="font-size:14px;font-weight:700;color:#1F2937;margin-bottom:4px;">개인정보 보호</div><div style="font-size:12px;color:#6B7280;line-height:1.6;">강력한 보안으로 고객님의 정보를 안전하게 보호합니다.</div></div>
    </div>
    <div style="background:#F9FAFB;border-radius:14px;padding:20px 18px;display:flex;gap:14px;align-items:flex-start;">
      <div style="width:44px;height:44px;border-radius:50%;background:#EFF6FF;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:22px;">💙</div>
      <div><div style="font-size:14px;font-weight:700;color:#1F2937;margin-bottom:4px;">가족과 함께 안심</div><div style="font-size:12px;color:#6B7280;line-height:1.6;">가족 보호자와 연결되어 더 든든하게 지켜드립니다.</div></div>
    </div>
    <div style="background:#F9FAFB;border-radius:14px;padding:20px 18px;display:flex;gap:14px;align-items:flex-start;">
      <div style="width:44px;height:44px;border-radius:50%;background:#ECFDF5;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:22px;">✨</div>
      <div><div style="font-size:14px;font-weight:700;color:#1F2937;margin-bottom:4px;">24시간 AI 케어</div><div style="font-size:12px;color:#6B7280;line-height:1.6;">언제 어디서나 AI가 든든한 금융 동반자가 됩니다.</div></div>
    </div>
  </div>
  <div style="text-align:center;margin-top:48px;padding-top:28px;border-top:1px solid #E5E7EB;font-size:13px;color:#9CA3AF;">
    🛡️ &nbsp;© 2024 안심케어 AI. All rights reserved. &nbsp;|&nbsp; JB금융그룹 Fin:AI Challenge
  </div>
</div>
""")
