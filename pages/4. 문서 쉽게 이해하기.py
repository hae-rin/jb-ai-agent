import streamlit as st
from utils import apply_user_css
from google import genai
from dotenv import load_dotenv
import os
import re
import base64

load_dotenv()

@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

st.set_page_config(page_title="문서 쉽게 이해하기", page_icon="📄", layout="centered", initial_sidebar_state="collapsed")

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
  background:linear-gradient(135deg,#5B21B6 0%,#8B5CF6 100%);
  border-radius:16px;padding:24px 32px 20px;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans KR',sans-serif;">
  <div style="margin-bottom:14px;">
    <a href="/" style="color:rgba(255,255,255,0.75);text-decoration:none;font-size:13px;font-weight:500;">← 홈으로</a>
  </div>
  <div style="display:flex;align-items:center;gap:16px;">
    <div style="font-size:42px;line-height:1;">📄</div>
    <div>
      <div style="font-size:{'28px' if user_type == '고령층' else '22px'};font-weight:800;color:white;line-height:1.2;">문서 쉽게 이해하기</div>
      <div style="font-size:{'16px' if user_type == '고령층' else '13px'};color:rgba(255,255,255,0.82);margin-top:5px;line-height:1.6;">보험 약관, 대출 문서, 금융 안내문을 쉬운 말로 설명해드립니다.</div>
    </div>
  </div>
</div>
""")

# ──────────────────────────────────────────────
# 입력 방식 선택
# ──────────────────────────────────────────────
st.markdown("### 📥 문서 입력 방식")
input_method = st.radio(
    "입력 방식을 선택하세요",
    ["📁 파일 첨부 (PDF, JPG, PNG)", "✏️ 텍스트 직접 입력"],
    horizontal=True,
    label_visibility="collapsed"
)

doc_type = st.selectbox(
    "문서 유형",
    ["보험 약관", "대출 문서", "금융 안내문", "적금/예금 상품", "ELS/펀드 상품", "기타 금융 문서"]
)

uploaded_file = None
doc_text = ""

# ──────────────────────────────────────────────
# 파일 첨부
# ──────────────────────────────────────────────
if "📁 파일 첨부" in input_method:
    uploaded_file = st.file_uploader(
        "파일을 업로드하세요",
        type=["pdf", "jpg", "jpeg", "png"],
        help="PDF, JPG, PNG 파일을 지원합니다."
    )
    if uploaded_file:
        file_type = uploaded_file.type
        st.success(f"✅ 파일 업로드 완료: {uploaded_file.name} ({round(uploaded_file.size/1024, 1)} KB)")

        # 이미지면 미리보기
        if file_type in ["image/jpeg", "image/png"]:
            st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)

# ──────────────────────────────────────────────
# 텍스트 직접 입력
# ──────────────────────────────────────────────
else:
    examples = {
        "보험 약관": """제3조 (보험금의 지급)
보험자는 피보험자가 보험기간 중 급격하고도 우연한 외래의 사고로 인하여 신체에 상해를 입은 경우, 그 상해로 인하여 사망하거나 장해분류표에서 정한 각 장해지급률에 해당하는 장해상태가 되었을 때 보험수익자에게 약정한 보험금을 지급합니다. 단, 보험금 지급사유가 발생한 날로부터 3년 이내에 청구하지 않을 경우 소멸시효가 완성됩니다.""",
        "대출 안내문": """본 상품은 변동금리부 주택담보대출로, 금융채 6개월물 금리에 연동되어 6개월마다 대출금리가 변경됩니다. 중도상환 시 잔여 대출원금의 1.2%에 해당하는 중도상환수수료가 부과되며, 대출 실행일로부터 3년 경과 후에는 면제됩니다.""",
        "적금 상품 설명서": """본 상품은 월 납입식 정기적금으로 계약기간은 12개월, 24개월, 36개월 중 선택 가능합니다. 기본금리는 연 3.5%이며, 자동이체 납입 시 0.2%p, 당행 주거래 고객 우대금리 0.3%p가 적용됩니다. 만기 전 해지 시 중도해지이율이 적용되며, 이자소득세 15.4%가 원천징수됩니다.""",
        "ELS 상품 설명서": """본 ELS는 KOSPI200 지수를 기초자산으로 하며, 6개월마다 조기상환 기회가 부여됩니다. 최초 기준가격 대비 85% 이상 유지 시 연 6.5% 수익으로 조기상환되며, 만기(3년) 시 기준가격의 55% 이상이면 원금이 보장됩니다. 단, 기준가격이 55% 미만으로 하락한 경우 원금 손실이 발생할 수 있습니다.""",
    }

    cols = st.columns(2)
    for i, (label, content) in enumerate(examples.items()):
        if cols[i % 2].button(f"📋 {label}", key=f"ex_{i}", use_container_width=True):
            st.session_state.doc_example = content

    doc_text = st.text_area(
        "문서 내용을 붙여넣으세요",
        value=st.session_state.get("doc_example", ""),
        placeholder="분석할 금융 문서 내용을 여기에 붙여넣으세요.",
        height=200,
        label_visibility="collapsed"
    )

st.divider()

# ──────────────────────────────────────────────
# 분석 버튼
# ──────────────────────────────────────────────
if st.button("📖 AI 쉬운 설명 시작", type="primary"):
    has_file = uploaded_file is not None
    has_text = doc_text.strip() != ""

    if not has_file and not has_text:
        st.warning("파일을 업로드하거나 텍스트를 입력해주세요.")
    else:
        try:
            with st.spinner("AI가 문서를 분석 중입니다..."):

                system_prompt = f"""당신은 고령 고객을 위한 금융 문서 해설 AI입니다.
사용자 유형: {user_type}
- 고령층: 아주 쉬운 말, 짧은 문장, 일상 비유 활용
- 일반 사용자: 핵심 위주 설명
- 금융 초보자: 금융 용어 쉽게 풀이

문서 유형: {doc_type}

고객을 따님, 아드님 등 가족 호칭으로 절대 부르지 마세요. "고객님"으로만 호칭하세요.
마크다운(**볼드**, *이탤릭*) 절대 금지. 숫자 목록(1. 2. 3.)은 사용 가능. 순수 텍스트.

반드시 아래 형식으로만 답하세요.

한줄요약:
(문서 전체를 한 문장으로 요약)

쉬운설명:
(쉽게 말하면 형식으로. {user_type} 수준으로 3~5문장. 일상 비유 활용)

핵심내용:
(꼭 알아야 할 내용. 번호 목록 3~5가지)

주의사항:
(조심해야 할 내용. 없으면 "특별한 주의사항 없음". 번호 목록)"""

                # 파일 첨부 분석
                if has_file:
                    file_bytes = uploaded_file.read()
                    file_type  = uploaded_file.type
                    b64        = base64.standard_b64encode(file_bytes).decode("utf-8")

                    if file_type == "application/pdf":
                        contents = [
                            {"inline_data": {"mime_type": "application/pdf", "data": b64}},
                            system_prompt
                        ]
                    else:  # 이미지
                        contents = [
                            {"inline_data": {"mime_type": file_type, "data": b64}},
                            system_prompt
                        ]

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=contents
                    )

                # 텍스트 분석
                else:
                    prompt = system_prompt + f"\n\n분석할 문서:\n{doc_text}"
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

        summary = extract("한줄요약", result)
        easy    = extract("쉬운설명", result)
        key     = extract("핵심내용", result)
        caution = extract("주의사항", result)

        st.divider()

        # 한 줄 요약
        st.markdown("### 📌 한 줄 요약")
        st.info(summary if summary else result)

        # 쉬운 설명
        st.markdown("### 💬 쉽게 말하면")
        st.write(easy)

        # 핵심 내용
        if key:
            st.markdown("### 📋 꼭 알아야 할 내용")
            st.success(key)

        # 주의사항
        if caution and caution != "특별한 주의사항 없음":
            st.markdown("### ⚠️ 주의사항")
            st.warning(caution)