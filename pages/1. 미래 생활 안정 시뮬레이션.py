import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import re
import plotly.graph_objects as go

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="미래 생활 안정 시뮬레이션", page_icon="📅", layout="centered")

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

st.title("📅 미래 생활 안정 시뮬레이션")
st.caption("자산·연금·생활비·의료비를 바탕으로 노후 생활 안정성을 예측합니다.")
st.divider()

st.markdown("### 📋 정보 입력")

with st.expander("👤 기본 정보", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("나이", min_value=1, max_value=100, value=70)
    with col2:
        health_status = st.selectbox("건강 상태", ["양호", "보통", "주의 필요"])

with st.expander("💰 자산 정보 (필수)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        asset_financial = st.number_input("금융 자산 (만원)", min_value=0, value=20000, step=100,
                                          help="예금, 적금, 주식 등 현금화 가능한 자산")
        income = st.number_input("월 연금 / 월소득 (만원)", min_value=0, value=80, step=5)
    with col2:
        asset_real = st.text_input("부동산 자산", placeholder="예: 아파트 3억원 (자가)")
        monthly_expense = st.number_input("월 생활비 (만원)", min_value=0, value=150, step=5)
    medical = st.number_input("월 의료비 / 보험료 (만원)", min_value=0, value=30, step=5)
with st.expander("➕ 추가 정보 (선택)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        has_family     = st.selectbox("부양 가족 여부", ["없음", "배우자", "자녀", "배우자+자녀"])
        has_loan       = st.selectbox("대출 여부", ["없음", "있음 (소액)", "있음 (고액)"])
    with col2:
        family_contact = st.selectbox("보호자 연락 여부", ["연락 가능", "연락 어려움"])

st.divider()

if st.button("🔮 AI 시뮬레이션 시작", type="primary"):
    if income == 0 and asset_financial == 0:
        st.warning("금융 자산 또는 월소득을 입력해주세요.")
    else:
        # ── 사전 계산
        monthly_total_expense = monthly_expense + medical
        monthly_shortage = round(monthly_total_expense - income, 1)  # 양수 = 적자, 음수 = 흑자

        if monthly_shortage > 0:
            asset_sustain_months = int(asset_financial / monthly_shortage)
            asset_sustain_years  = asset_sustain_months // 12
            asset_sustain_remain = asset_sustain_months % 12
        else:
            asset_sustain_months = 9999
            asset_sustain_years  = 99
            asset_sustain_remain = 0

        if monthly_shortage <= 0:
            pre_risk = "안정"
        elif asset_sustain_years >= 10:
            pre_risk = "주의"
        else:
            pre_risk = "위험"

        # ── LLM 분석
        with st.spinner("AI가 미래를 분석 중입니다..."):
            prompt = f"""
당신은 고령 고객 전문 노후 재무 설계 AI입니다.
사용자 유형: {user_type}
- 고령층: 아주 쉬운 말, 짧은 문장
- 일반 사용자: 핵심 위주 설명
- 금융 초보자: 금융 용어 쉽게 풀이

고객 정보:
- 나이: {age}세 / 건강 상태: {health_status}
- 금융 자산: {asset_financial}만원
- 부동산 자산: {asset_real}
- 월 연금/소득: {income}만원
- 월 생활비: {monthly_expense}만원
- 월 의료비/보험료: {medical}만원
- 부양 가족: {has_family} / 대출: {has_loan} / 보호자 연락: {family_contact}
사전 계산 결과:
- 월 현금흐름: {"적자 " + str(monthly_shortage) + "만원" if monthly_shortage > 0 else "흑자 " + str(abs(monthly_shortage)) + "만원"}
- 자산 유지 가능 기간: {"약 " + str(asset_sustain_years) + "년 " + str(asset_sustain_remain) + "개월" if monthly_shortage > 0 else "안정적 (소득이 지출보다 많음)"}
- 사전 위험도: {pre_risk}

마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.
고객을 따님, 아드님 등 가족 호칭으로 절대 부르지 마세요. 반드시 "고객님"으로만 호칭하세요.

반드시 아래 형식으로만 답하세요.

노후안정도: [안정/주의/위험]

월현금흐름:
(월 수입·지출 현황과 부족/잉여액을 쉽게 설명. 2문장)

미래예측_현재~5년:
(현재부터 5년간 생활 전망. 2문장)

미래예측_5년~10년:
(5년~10년 사이 예상 변화. 2문장)

미래예측_10년이후:
(10년 이후 장기 리스크. 2문장)

추천행동:
(실천 가능한 행동 3가지. 번호 목록)

쉬운설명:
(쉽게 말하면 형식으로 3~4문장. 어르신도 바로 이해할 수 있게)

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

        risk       = extract("노후안정도", result)
        cashflow   = extract("월현금흐름", result)
        pred_5     = extract("미래예측_현재~5년", result)
        pred_10    = extract("미래예측_5년~10년", result)
        pred_after = extract("미래예측_10년이후", result)
        actions    = extract("추천행동", result)
        easy       = extract("쉬운설명", result)

        st.divider()

        # ① 노후 안정도
        if "위험" in risk:
            st.error("🔴 노후 생활 안정도: 위험")
        elif "주의" in risk:
            st.warning("🟡 노후 생활 안정도: 주의")
        else:
            st.success("🟢 노후 생활 안정도: 안정")

        # ② 월 현금흐름
        st.markdown("### 💰 월 현금흐름")
        if monthly_shortage > 0:
            st.error(f"매달 약 {monthly_shortage}만원이 부족합니다.")
        else:
            st.success(f"매달 약 {abs(monthly_shortage)}만원이 남습니다.")
        st.write(cashflow)

        # ── 그래프 1: 월 수입 vs 지출 막대 차트
        st.markdown("### 📊 월 수입 vs 지출 비교")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="월 수입",
            x=["월 수입"],
            y=[income],
            marker_color="#3B82F6",
            text=[f"{income}만원"],
            textposition="outside"
        ))
        fig_bar.add_trace(go.Bar(
            name="월 지출",
            x=["월 지출"],
            y=[monthly_total_expense],
            marker_color="#EF4444" if monthly_shortage > 0 else "#22C55E",
            text=[f"{monthly_total_expense}만원"],
            textposition="outside"
        ))
        fig_bar.update_layout(
            barmode="group",
            height=320,
            margin=dict(t=30, b=20),
            yaxis_title="금액 (만원)",
            legend=dict(orientation="h", y=1.1),
            plot_bgcolor="white",
            yaxis=dict(gridcolor="#F1F5F9")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # ── 그래프 2: 자산 변화 예측 라인 차트
        st.markdown("### 📉 자산 변화 예측 (30년)")

        year_points = list(range(0, 31))
        assets = []
        remaining = float(asset_financial)

        for y in year_points:
            assets.append(round(max(remaining, 0), 1))
            # 월 흑자/적자 반영 + 의료비 매년 3% 증가
            annual_net = (income - monthly_expense - medical * (1.03 ** y)) * 12
            remaining += annual_net

        max_asset = max(assets) if max(assets) > 0 else asset_financial
        safe_threshold    = max_asset * 0.6
        caution_threshold = max_asset * 0.3

        fig_line = go.Figure()

        # 배경 구간
        fig_line.add_hrect(y0=safe_threshold, y1=max_asset * 1.15,
                           fillcolor="#DCFCE7", opacity=0.25, line_width=0,
                           annotation_text="안정 구간", annotation_position="top left")
        fig_line.add_hrect(y0=caution_threshold, y1=safe_threshold,
                           fillcolor="#FEF3C7", opacity=0.25, line_width=0,
                           annotation_text="주의 구간", annotation_position="top left")
        fig_line.add_hrect(y0=0, y1=caution_threshold,
                           fillcolor="#FEE2E2", opacity=0.25, line_width=0,
                           annotation_text="위험 구간", annotation_position="top left")

        # 자산 변화 라인
        fig_line.add_trace(go.Scatter(
            x=year_points,
            y=assets,
            mode="lines",
            name="예상 금융 자산",
            line=dict(color="#3B82F6", width=3),
            hovertemplate="%{x}년 후: %{y:,.0f}만원<extra></extra>"
        ))

        # 5년 단위 마커 + 금액 표시
        marker_x = [0, 5, 10, 15, 20, 25, 30]
        marker_y = [assets[y] for y in marker_x]
        fig_line.add_trace(go.Scatter(
            x=marker_x,
            y=marker_y,
            mode="markers+text",
            name="5년 단위",
            marker=dict(size=10, color="#1D4ED8", symbol="circle"),
            text=[f"{v/10000:.1f}억원" if v >= 10000 else f"{int(v):,}만원" for v in marker_y],
            textposition="top center",
            showlegend=False,
            hovertemplate="%{x}년 후: %{y:,.0f}만원<extra></extra>"
        ))

        # 자산 소진 시점 (적자인 경우만)
        if monthly_shortage > 0 and asset_sustain_years <= 30:
            fig_line.add_vline(
                x=asset_sustain_years,
                line_dash="dash",
                line_color="#DC2626",
                annotation_text=f"⚠ {asset_sustain_years}년 후 소진",
                annotation_position="top right"
            )

        fig_line.update_layout(
            height=400,
            margin=dict(t=40, b=20, l=20, r=20),
            xaxis_title="현재로부터 (년)",
            yaxis_title="금융 자산 (만원)",
            plot_bgcolor="white",
            yaxis=dict(gridcolor="#F1F5F9", range=[0, max_asset * 1.2]),
            xaxis=dict(gridcolor="#F1F5F9", tickvals=marker_x),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # ③ 미래 예측 카드
        st.markdown("### 📅 미래 예측")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**현재 ~ 5년**")
            st.info(pred_5)
        with col2:
            st.markdown("**5년 ~ 10년**")
            st.warning(pred_10)
        with col3:
            st.markdown("**10년 이후**")
            st.error(pred_after)

        # ⑤ AI 추천 행동
        if actions:
            st.markdown("### 💡 AI 추천 행동")
            st.success(actions)

        # ⑥ 쉬운 말 설명
        st.markdown("### 💬 쉽게 말하면")
        st.info(easy if easy else result)