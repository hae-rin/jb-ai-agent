import streamlit as st
from utils import apply_user_css
from google import genai
from dotenv import load_dotenv
import os
import re
import plotly.graph_objects as go

load_dotenv()

@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

st.set_page_config(page_title="노후 버킷리스트", page_icon="🌟", layout="centered", initial_sidebar_state="collapsed")

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
  background:linear-gradient(135deg,#92400E 0%,#F59E0B 100%);
  border-radius:16px;padding:24px 32px 20px;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;">
  <div style="margin-bottom:14px;">
    <a href="/" style="color:rgba(255,255,255,0.75);text-decoration:none;font-size:13px;font-weight:500;">← 홈으로</a>
  </div>
  <div style="display:flex;align-items:center;gap:16px;">
    <div style="font-size:42px;line-height:1;">🌟</div>
    <div>
      <div style="font-size:{'28px' if user_type == '고령층' else '22px'};font-weight:800;color:white;line-height:1.2;">노후 버킷리스트</div>
      <div style="font-size:{'16px' if user_type == '고령층' else '13px'};color:rgba(255,255,255,0.82);margin-top:5px;line-height:1.6;">살면서 꼭 이루고 싶은 것들을 AI가 실현 가능한 재무 계획으로 만들어드립니다.</div>
    </div>
  </div>
</div>
""")

# ──────────────────────────────────────────────
# 재무 정보
# ──────────────────────────────────────────────
st.markdown("### 💰 내 재무 상황")

_age = st.session_state.get("profile_age", 70)
_income = st.session_state.get("profile_income", 80)
_asset = st.session_state.get("profile_asset", 20000)
_expense = st.session_state.get("profile_expense", 150)
st.info(f"📋 홈 프로필 적용 중 — {_age}세 | 월 소득 {_income}만원 | 금융 자산 {_asset:,}만원 | 월 생활비 {_expense}만원")

with st.expander("재무 정보 수정하기", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        age    = st.number_input("나이", min_value=1, max_value=100, key="profile_age")
        income = st.number_input("월 연금/소득 (만원)", min_value=0, step=5, key="profile_income")
    with col2:
        asset   = st.number_input("현재 금융 자산 (만원)", min_value=0, step=100, key="profile_asset")
        expense = st.number_input("월 생활비 (만원)", min_value=0, step=5, key="profile_expense")

monthly_savings = income - expense
if monthly_savings > 0:
    st.success(f"매달 약 {monthly_savings}만원을 저축할 수 있습니다.")
elif monthly_savings < 0:
    st.error(f"매달 약 {abs(monthly_savings)}만원이 부족합니다. 자산을 활용해야 합니다.")
else:
    st.info("수입과 지출이 딱 맞습니다.")

st.divider()

# ──────────────────────────────────────────────
# 버킷리스트 입력
# ──────────────────────────────────────────────
st.markdown("### 🌈 이루고 싶은 꿈 목록")
st.caption("최대 5가지까지 입력하실 수 있습니다. 꿈 내용과 예상 비용, 목표 시기를 입력해주세요.")

col1, col2 = st.columns(2)
with col1:
    if st.button("🌏 여행 중심 예시 불러오기"):
        st.session_state["b_name_0"] = "일본 교토 여행"
        st.session_state["b_cost_0"] = 300
        st.session_state["b_years_0"] = 1
        st.session_state["b_name_1"] = "유럽 여행"
        st.session_state["b_cost_1"] = 800
        st.session_state["b_years_1"] = 3
        st.session_state["b_name_2"] = "가족 여행"
        st.session_state["b_cost_2"] = 200
        st.session_state["b_years_2"] = 2
        st.session_state["b_name_3"] = ""
        st.session_state["b_cost_3"] = 0
        st.session_state["b_years_3"] = 1
        st.session_state["b_name_4"] = ""
        st.session_state["b_cost_4"] = 0
        st.session_state["b_years_4"] = 1
        st.rerun()
with col2:
    if st.button("👨‍👩‍👧 가족 중심 예시 불러오기"):
        st.session_state["b_name_0"] = "손주 대학 등록금 지원"
        st.session_state["b_cost_0"] = 1000
        st.session_state["b_years_0"] = 5
        st.session_state["b_name_1"] = "가족 여행"
        st.session_state["b_cost_1"] = 300
        st.session_state["b_years_1"] = 1
        st.session_state["b_name_2"] = "불우이웃 기부"
        st.session_state["b_cost_2"] = 100
        st.session_state["b_years_2"] = 1
        st.session_state["b_name_3"] = ""
        st.session_state["b_cost_3"] = 0
        st.session_state["b_years_3"] = 1
        st.session_state["b_name_4"] = ""
        st.session_state["b_cost_4"] = 0
        st.session_state["b_years_4"] = 1
        st.rerun()

for i in range(5):
    st.session_state.setdefault(f"b_name_{i}", "")
    st.session_state.setdefault(f"b_cost_{i}", 0)
    st.session_state.setdefault(f"b_years_{i}", 1)

st.markdown("---")
st.markdown("꿈 내용 | 예상 비용 (만원) | 목표 시기 (년 후)")

bucket_items = []
for i in range(5):
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        name = st.text_input(
            f"꿈 {i+1}",
            key=f"b_name_{i}",
            placeholder="예: 일본 여행",
            label_visibility="collapsed"
        )
    with col2:
        cost = st.number_input(
            "비용",
            min_value=0, step=10,
            key=f"b_cost_{i}",
            label_visibility="collapsed"
        )
    with col3:
        years = st.number_input(
            "시기",
            min_value=1, max_value=30,
            key=f"b_years_{i}",
            label_visibility="collapsed"
        )
    if name.strip():
        bucket_items.append({"name": name.strip(), "cost": cost, "years": years})

st.divider()

# ──────────────────────────────────────────────
# AI 분석
# ──────────────────────────────────────────────
if st.button("🌟 AI 재무 계획 만들기", type="primary"):
    if not bucket_items:
        st.warning("꿈을 하나 이상 입력해주세요.")
    else:
        with st.spinner("AI가 맞춤 재무 계획을 만들고 있습니다..."):
            items_text = "\n".join([
                f"{i+1}. {item['name']} — 예상 비용 {item['cost']}만원, 목표 시기 {item['years']}년 후"
                for i, item in enumerate(bucket_items)
            ])

            prompt = f"""
당신은 고령 고객의 꿈을 재무 계획으로 연결해주는 AI 노후 코치입니다.
사용자 유형: {user_type}
- 고령층: 아주 쉬운 말, 짧은 문장, 따뜻한 말투
- 일반 사용자: 핵심 위주 설명
- 금융 초보자: 금융 용어 쉽게 풀이

고객 정보:
- 나이: {age}세
- 현재 금융 자산: {asset}만원
- 월 소득/연금: {income}만원
- 월 생활비: {expense}만원
- 월 저축 가능: {monthly_savings}만원 ({"흑자" if monthly_savings >= 0 else "적자"})

버킷리스트:
{items_text}

각 꿈에 대해 현재 재무 상황을 바탕으로 실현 가능성을 분석하고 구체적인 재무 계획을 만들어주세요.

고객을 따님, 아드님 등 가족 호칭으로 절대 부르지 마세요. 반드시 "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

종합평가:
(현재 재무 상황과 꿈 실현 가능성 전반 평가. 2문장)

꿈분석:
(각 꿈별로 "꿈 이름: 달성 가능/노력 필요/어려움 — 이유 — 월 필요 저축액" 형식. 번호 목록)

우선순위:
(먼저 이루어야 할 꿈 순서와 이유. 번호 목록)

실천계획:
(지금 당장 시작할 수 있는 구체적 행동 3가지. 번호 목록)

응원메시지:
(고객님의 꿈을 응원하는 따뜻하고 짧은 메시지. 2문장)
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

        overall  = extract("종합평가", result)
        analysis = extract("꿈분석", result)
        priority = extract("우선순위", result)
        plan     = extract("실천계획", result)
        cheer    = extract("응원메시지", result)

        st.divider()

        # ① 종합 평가
        st.markdown("### 📊 종합 평가")
        st.info(overall)

        # ② 타임라인 차트
        st.markdown("### 📅 꿈 실현 타임라인")

        valid_items = [item for item in bucket_items if item["cost"] > 0]
        if valid_items:
            bar_x, bar_y, bar_colors, bar_texts = [], [], [], []

            for item in valid_items:
                months = item["years"] * 12
                monthly_needed = round(item["cost"] / months, 1) if months > 0 else item["cost"]
                total_available = asset + max(monthly_savings, 0) * months

                if total_available >= item["cost"]:
                    color = "#22C55E"
                    status = "달성 가능"
                elif total_available >= item["cost"] * 0.7:
                    color = "#F59E0B"
                    status = "노력 필요"
                else:
                    color = "#EF4444"
                    status = "어려움"

                bar_x.append(item["years"])
                bar_y.append(item["name"])
                bar_colors.append(color)
                bar_texts.append(f"{item['years']}년 후  |  {item['cost']}만원  |  {status}")

            fig = go.Figure(go.Bar(
                x=bar_x,
                y=bar_y,
                orientation="h",
                marker_color=bar_colors,
                text=bar_texts,
                textposition="outside",
            ))
            fig.update_layout(
                height=max(200, 90 * len(valid_items) + 80),
                margin=dict(t=20, b=20, l=20, r=220),
                xaxis_title="목표 시기 (년 후)",
                plot_bgcolor="white",
                xaxis=dict(gridcolor="#F1F5F9", dtick=1),
                yaxis=dict(gridcolor="#F1F5F9"),
            )
            st.plotly_chart(fig, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            col1.success("■ 달성 가능")
            col2.warning("■ 노력 필요")
            col3.error("■ 어려움")

        # ③ 꿈별 분석
        st.markdown("### 🔍 꿈별 상세 분석")
        st.write(analysis)

        # ④ 우선순위
        if priority:
            st.markdown("### 🥇 추천 순서")
            st.success(priority)

        # ⑤ 실천 계획
        if plan:
            st.markdown("### 💡 실천 계획")
            st.success(plan)

        # ⑥ 응원 메시지
        if cheer:
            st.markdown("### 💌 응원 메시지")
            st.info(cheer)
