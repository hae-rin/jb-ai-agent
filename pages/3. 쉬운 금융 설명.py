import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="쉬운 금융 설명", page_icon="💬", layout="centered")

if "user_type" not in st.session_state:
    st.session_state.user_type = "고령층"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_type = st.selectbox("사용자 유형", ["고령층", "일반 사용자", "금융 초보자"], key="user_type")

if user_type == "고령층":
    st.markdown("""
    <style>
    .stApp, .stApp p, .stApp div, .stApp label, .stApp span { font-size: 20px !important; }
    .stButton > button { font-size: 22px !important; height: 60px !important; width: 100% !important; }
    .stTextInput input, .stTextArea textarea, .stNumberInput input { font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("💬 쉬운 금융 설명")
st.caption("어려운 금융 용어나 궁금한 점을 물어보시면 쉽게 설명해드립니다.")
st.divider()

# ──────────────────────────────────────────────
# 빠른 질문 버튼
# ──────────────────────────────────────────────
st.markdown("### 💡 자주 묻는 질문")

quick_questions = [
    "유동성 리스크가 뭐예요?",
    "ELS가 뭐예요?",
    "변동금리와 고정금리 차이가 뭐예요?",
    "보이스피싱을 당하면 어떻게 해야 하나요?",
    "적금이랑 예금이 어떻게 달라요?",
    "연금저축이 뭐예요?",
]

cols = st.columns(2)
for i, q in enumerate(quick_questions):
    if cols[i % 2].button(q, key=f"quick_{i}", use_container_width=True):
        st.session_state.chat_history.append({"role": "user", "content": q})
        st.rerun()

st.divider()

# ──────────────────────────────────────────────
# 대화 출력
# ──────────────────────────────────────────────
st.markdown("### 🗨️ 대화")

if not st.session_state.chat_history:
    st.info("💬 안녕하세요! 금융 관련 궁금한 점이 있으시면 편하게 물어보세요. 어려운 말 없이 쉽게 설명해드릴게요 😊")

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# ──────────────────────────────────────────────
# AI 응답 생성 (새 메시지가 있을 때)
# ──────────────────────────────────────────────
if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
    with st.spinner("쉽게 설명 중입니다..."):
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_history[:-1]
        ]
        last_question = st.session_state.chat_history[-1]["content"]

        system_context = f"""
당신은 고령 고객을 위한 친절한 금융 상담 AI입니다.
사용자 유형: {user_type}
- 고령층: 아주 쉬운 말, 짧은 문장, 비유 활용
- 일반 사용자: 핵심 위주 설명
- 금융 초보자: 금융 용어 쉽게 풀이

지침:
- 금융 전문 용어는 반드시 쉬운 말로 풀어서 설명하세요.
- 일상적인 비유를 활용해서 설명하세요. (예: 적금은 저금통 같은 거예요)
- 따뜻하고 친근한 말투를 사용하세요.
- 답변은 3~5문장으로 간결하게 작성하세요.
- 고객을 따님, 아드님 등 가족 호칭으로 절대 부르지 마세요. "고객님"으로만 호칭하세요.
- 마크다운(**볼드**, *이탤릭*) 절대 금지. 순수 텍스트.
"""
        # 대화 이력 포함해서 멀티턴으로 전송
        messages = []
        for m in st.session_state.chat_history[:-1][-10:]:  # 최근 10개만
            messages.append(f"{'사용자' if m['role'] == 'user' else 'AI'}: {m['content']}")

        full_prompt = system_context
        if messages:
            full_prompt += "\n\n이전 대화:\n" + "\n".join(messages)
        full_prompt += f"\n\n사용자 질문: {last_question}\n\nAI 답변:"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        reply = response.text.strip()

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

# ──────────────────────────────────────────────
# 입력창
# ──────────────────────────────────────────────
st.divider()
user_input = st.chat_input("궁금한 금융 용어나 질문을 입력하세요...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.rerun()

# 대화 초기화
if st.session_state.chat_history:
    if st.button("🗑️ 대화 초기화"):
        st.session_state.chat_history = []
        st.rerun()