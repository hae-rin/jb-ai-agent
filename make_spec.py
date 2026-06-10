"""기능명세서 docx 생성 스크립트"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── 여백 설정 ──────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)

# ── 유틸 ──────────────────────────────────────────────────────────
def add_heading(doc, text, level=1, size=15, bold=True, color=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    return p

def add_body(doc, text, size=10.5, indent=0):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    run = p.add_run(text)
    run.font.size = Pt(size)
    return p

def add_bullet(doc, text, size=10.5, indent=0.5):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(indent)
    run = p.add_run(text)
    run.font.size = Pt(size)
    return p

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def cell_text(cell, text, bold=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT, color=None):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)

# ══════════════════════════════════════════════════════════════════
# 제목
# ══════════════════════════════════════════════════════════════════
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("JB금융그룹 Fin:AI Challenge 기능 명세서")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x5F)
doc.add_paragraph()

# ── 안내 ──────────────────────────────────────────────────────────
note = doc.add_paragraph()
nr = note.add_run(
    "본 문서는 JB금융그룹 Fin:AI Challenge 예선 제출용 기능명세서입니다. "
    "본선 진출 시에는 동일 문서를 기준으로 보완하며, 기능 추가·수정·삭제가 발생한 경우 "
    "'7. 기능 변경이력'에 변경 내역을 기록하여 함께 제출합니다."
)
nr.font.size = Pt(9.5)
nr.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

# ── 기본 정보 테이블 ──────────────────────────────────────────────
doc.add_paragraph()
info_table = doc.add_table(rows=3, cols=4)
info_table.style = 'Table Grid'
HEADER_BG = "1E3A5F"
CELL_BG   = "EFF6FF"

info_rows = [
    [("팀명", True, HEADER_BG), ("유해린", False, CELL_BG),
     ("주제 구분", True, HEADER_BG), ("지정주제 1", False, CELL_BG)],
    [("팀원 정보(역할)", True, HEADER_BG), ("유해린 (기획, 개발)", False, CELL_BG),
     ("작성일", True, HEADER_BG), ("2026.06.07", False, CELL_BG)],
    [("서비스명", True, HEADER_BG), ("Slowfit", False, CELL_BG),
     ("기술 스택", True, HEADER_BG), ("FastAPI · React · Gemini 2.5 Flash", False, CELL_BG)],
]
for i, row_data in enumerate(info_rows):
    row = info_table.rows[i]
    for j, (text, is_header, bg) in enumerate(row_data):
        cell = row.cells[j]
        set_cell_bg(cell, bg)
        color = (0xFF, 0xFF, 0xFF) if is_header else (0x0F, 0x17, 0x2A)
        cell_text(cell, text, bold=is_header, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color=color)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

# ══════════════════════════════════════════════════════════════════
# 1. 서비스 개요
# ══════════════════════════════════════════════════════════════════
doc.add_paragraph()
add_heading(doc, "1. 서비스 개요 (Service)", size=13, color=(0x1E, 0x3A, 0x5F))

overview = doc.add_table(rows=5, cols=2)
overview.style = 'Table Grid'
labels = ["서비스명", "서비스 한줄 소개", "개발 목표", "타겟 사용자", "기대 효과"]
values = [
    "Slowfit (삶처럼, 금융도 천천히)",
    "고령 고객의 자산·연금·생활비·이상거래를 AI가 통합 분석하여 안전한 노후 생활을 지원하는 AI Agent 서비스",
    "고령 고객의 금융사기 피해를 예방하고, 노후 자산·연금·생활비를 통합 관리할 수 있는 Multi-Agent AI 서비스를 개발한다.",
    "핵심 타겟: 은퇴 이후 노후 자산관리가 필요한 고령 고객\n확장 타겟: 은퇴를 앞둔 50대, 고령 부모를 둔 보호자 가족",
    "· 고령층의 금융사기 피해 예방 및 금융 안전성 향상\n· 노후 자산·연금·생활비 통합 관리를 통한 안정적 노후 생활 지원\n· 복잡한 금융 문서·정보를 쉬운 말로 제공하여 금융 이해도 향상\n· 사용자 유형별(고령층·금융초보자·일반 사용자) 적응형 UI/UX 제공",
]
for i, (lbl, val) in enumerate(zip(labels, values)):
    row = overview.rows[i]
    set_cell_bg(row.cells[0], HEADER_BG)
    cell_text(row.cells[0], lbl, bold=True, size=10,
              align=WD_ALIGN_PARAGRAPH.CENTER, color=(0xFF, 0xFF, 0xFF))
    row.cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    row.cells[1].text = ''
    p = row.cells[1].paragraphs[0]
    r2 = p.add_run(val)
    r2.font.size = Pt(10)

# ══════════════════════════════════════════════════════════════════
# 2. 시스템 구성도
# ══════════════════════════════════════════════════════════════════
doc.add_paragraph()
add_heading(doc, "2. 시스템 구성도 (Architecture)", size=13, color=(0x1E, 0x3A, 0x5F))

arch_lines = [
    ("사용자 (고령 고객 / 보호자 가족)", True),
    ("  · 나이, 자산, 연금, 생활비, 의료비 입력", False),
    ("  · 거래 내역 텍스트 입력", False),
    ("  · 금융 문서 업로드 (PDF / 이미지)", False),
    ("  · 버킷리스트 항목 및 보이스피싱 의심 내용 입력", False),
    ("", False),
    ("▼", False),
    ("", False),
    ("프론트엔드 (React + TypeScript + Vite + Tailwind CSS)", True),
    ("  · 6개 페이지 SPA: 홈 / 케어 에이전트 / 시뮬레이션 / 버킷리스트 / 보이스피싱 / 문서해석 / 상품추천", False),
    ("  · 사용자 유형별 적응형 UI (고령층 대형 텍스트, 금융초보자 툴팁)", False),
    ("  · 로컬 프로필 저장 및 자동 적용", False),
    ("", False),
    ("▼  REST API (FastAPI)", False),
    ("", False),
    ("AI Agent 처리 레이어 (Google Gemini 2.5 Flash)", True),
    ("  ① 재무 분석 Agent     — 위험도·현금흐름·자산유지 기간 산출", False),
    ("  ② 이상거래 탐지 Agent — 거래 패턴 기반 위험 신호 탐지", False),
    ("  ③ 케어 플랜 Agent     — 즉각조치·단기계획·장기전략 생성", False),
    ("  ④ 검증 Agent         — 일관성 검증 및 오류 시 자동 재생성", False),
    ("  + 시뮬레이션 / 버킷리스트 / 보이스피싱 / 문서해석 / 상품추천 전용 Agent", False),
    ("", False),
    ("▼", False),
    ("", False),
    ("출력", True),
    ("  · 노후 안정도 분석 / 30년 자산 변화 그래프", False),
    ("  · 이상거래 위험도 / 위험 신호 목록", False),
    ("  · 맞춤 케어 플랜 / 버킷리스트 달성 가능성 분석", False),
    ("  · 보이스피싱 판정 결과 / 즉시 행동 안내", False),
    ("  · 금융 문서 핵심 요약 / JB금융 상품 추천", False),
    ("  · PDF 종합 케어 리포트 다운로드", False),
]
for text, is_bold in arch_lines:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    r3 = p.add_run(text)
    r3.font.size = Pt(10)
    r3.bold = is_bold
    p.paragraph_format.space_after = Pt(0)

# ══════════════════════════════════════════════════════════════════
# 3. 핵심 기능 명세
# ══════════════════════════════════════════════════════════════════
doc.add_paragraph()
add_heading(doc, "3. 핵심 기능 명세 (Feature Specification)", size=13, color=(0x1E, 0x3A, 0x5F))

note2 = doc.add_paragraph()
nr2 = note2.add_run("핵심 기능 위주로 간략히 작성하되, 예선 제출본을 기준으로 본선에서 동일 형식을 유지하여 보완합니다.")
nr2.font.size = Pt(9.5)
nr2.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

features = [
    {
        "name": "AI 종합 케어 에이전트\n(Multi-Agent)",
        "desc": "4단계 Multi-Agent 파이프라인으로 고령 고객의 재무 상태와 거래 위험을 종합 분석하고 맞춤 케어 플랜을 생성한다.\n①재무분석→②이상거래탐지→③케어플랜→④검증+재생성",
        "io": "입력: 나이, 금융자산, 월소득/연금, 월지출, 거래내역(선택)\n출력: 재무위험도(안정/주의/위험), 월현금흐름, 핵심위험요인, 자산유지예상, 거래위험도, 위험신호, 즉각조치, 단기계획, 장기전략, 검증 신뢰도, PDF 리포트",
        "tech": "Google Gemini 2.5 Flash\nMulti-Agent 파이프라인 (4-step)\n자동 재생성 로직 (검증 실패 시)\nfpdf2 (PDF 생성)",
        "done": "O",
    },
    {
        "name": "미래 생활 안정\n시뮬레이션",
        "desc": "자산, 연금, 생활비, 의료비를 기반으로 노후 생활 안정성과 30년 자산 변화 추이를 분석한다.",
        "io": "입력: 나이, 건강상태, 금융자산, 부동산, 월소득, 월생활비, 의료비, 부양가족, 대출여부\n출력: 노후안정도(안정/주의/위험), 월현금흐름, 5년·10년·10년이후 미래예측, 추천행동, 핵심인사이트, 30년 자산변화 배열(차트용)",
        "tech": "Google Gemini 2.5 Flash\n현금흐름·자산유지기간 사전 계산\n30년 연도별 자산 시뮬레이션",
        "done": "O",
    },
    {
        "name": "노후 버킷리스트\n재무 계획",
        "desc": "고객이 이루고 싶은 꿈(버킷리스트)을 입력하면 재무 정보를 바탕으로 달성 가능성과 실천 계획을 분석한다.",
        "io": "입력: 나이, 금융자산, 월소득, 월지출, 버킷리스트(항목명·예상비용·목표시기)\n출력: 종합평가, 꿈별 달성가능성(달성가능/노력필요/어려움), 우선순위, 실천계획, 응원메시지",
        "tech": "Google Gemini 2.5 Flash\n달성 가능성 사전 계산 (자산+저축 vs 비용)\n동적 항목 추가/삭제 UI",
        "done": "O",
    },
    {
        "name": "보이스피싱\n즉시 판단",
        "desc": "의심스러운 전화·문자 내용을 붙여넣으면 AI가 7가지 사기 판단 기준으로 즉시 분석한다.",
        "io": "입력: 의심 통화·문자 텍스트\n출력: 판정(사기/정상/주의), 위험도(높음/보통/낮음), 발견된 위험신호, 쉬운설명, 즉시 행동 지침",
        "tech": "Google Gemini 2.5 Flash\n룰 기반 7대 사기 패턴 탐지 프롬프트\n(긴급성·개인정보요구·링크·사칭·이체유도 등)",
        "done": "O",
    },
    {
        "name": "문서 쉽게\n이해하기",
        "desc": "보험 약관, 대출 계약서, 금융 상품 설명서 등을 업로드하거나 텍스트를 입력하면 핵심 내용을 쉽게 요약한다.",
        "io": "입력: PDF·이미지 파일(멀티모달) 또는 텍스트, 문서 유형, 사용자 유형\n출력: 한줄요약, 쉬운설명, 핵심내용, 주의사항",
        "tech": "Google Gemini 2.5 Flash (멀티모달)\nbase64 파일 인코딩 처리\n사용자 유형별 어조 최적화",
        "done": "O",
    },
    {
        "name": "맞춤 금융\n상품 추천",
        "desc": "나이, 자산, 투자 성향, 재무 목표를 기반으로 JB금융그룹 계열사(전북은행·광주은행·JB우리캐피탈·JB자산운용) 상품을 우선 추천한다.",
        "io": "입력: 나이, 월소득, 자산, 월저축가능액, 재무목표, 투자성향, 연금/IRP여부, 세금관심도, 대출여부\n출력: 종합평가, 단기·장기·노후 추천 상품, 절세 방법, 쉬운설명, 우선순위 행동",
        "tech": "Google Gemini 2.5 Flash\nJB금융 계열사 상품 DB 내장\n목표·성향별 맞춤 추천 프롬프트",
        "done": "O",
    },
    {
        "name": "사용자 프로필\n관리",
        "desc": "나이·자산·소득·지출·사용자 유형을 저장하여 모든 서비스 페이지에 자동 적용한다.",
        "io": "입력: 나이, 금융자산, 월소득, 월지출, 사용자 유형(고령층/일반/금융초보자)\n출력: profile.json 저장, 전 페이지 프로필 자동 주입",
        "tech": "FastAPI REST API\nReact Context API (전역 상태)\nlocalStorage 연동",
        "done": "O",
    },
]

feat_table = doc.add_table(rows=1 + len(features), cols=5)
feat_table.style = 'Table Grid'
headers = ["기능명", "기능 설명", "입력/출력 데이터", "관련 기술 및 알고리즘", "구현\n여부"]
header_row = feat_table.rows[0]
for j, h in enumerate(headers):
    set_cell_bg(header_row.cells[j], HEADER_BG)
    cell_text(header_row.cells[j], h, bold=True, size=9.5,
              align=WD_ALIGN_PARAGRAPH.CENTER, color=(0xFF, 0xFF, 0xFF))
    header_row.cells[j].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

for i, f in enumerate(features):
    row = feat_table.rows[i + 1]
    set_cell_bg(row.cells[0], CELL_BG)
    cell_text(row.cells[0], f["name"], bold=True, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    row.cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for j, key in enumerate(["desc", "io", "tech", "done"]):
        row.cells[j+1].text = ''
        p = row.cells[j+1].paragraphs[0]
        if key == "done":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r4 = p.add_run(f[key])
        r4.font.size = Pt(9.5)
        if key == "done":
            r4.bold = True
            r4.font.color.rgb = RGBColor(0x05, 0x96, 0x69)
        row.cells[j+1].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

# ══════════════════════════════════════════════════════════════════
# 4. 주요 기능 흐름도
# ══════════════════════════════════════════════════════════════════
doc.add_paragraph()
add_heading(doc, "4. 주요 기능 흐름도 (Flow)", size=13, color=(0x1E, 0x3A, 0x5F))

flows = [
    ("일반 흐름 (공통)", [
        "서비스 접속 (Slowfit 홈 화면)",
        "내 프로필 설정 → 나이·자산·소득·지출·사용자유형 입력 후 저장",
        "원하는 기능 선택 (6가지 서비스 카드)",
        "추가 정보 입력 또는 문서 업로드",
        "AI 분석 수행 (Gemini 2.5 Flash)",
        "결과 화면 출력 (위험도·안정도·추천 결과·쉬운설명)",
        "후속 행동 안내 / PDF 리포트 다운로드",
    ]),
    ("AI 종합 케어 에이전트 상세 흐름 (Multi-Agent)", [
        "①재무 분석 Agent: 위험도(안정/주의/위험), 월현금흐름, 핵심위험요인, 자산유지기간 산출",
        "②이상거래 탐지 Agent: 거래내역 입력 시 위험도·위험신호 탐지 (입력 없으면 '분석 없음')",
        "③케어 플랜 Agent: ①②결과를 종합하여 즉각조치·단기계획·장기전략 생성",
        "④검증 Agent: 일관성 검증 → '수정 필요' 판정 시 케어 플랜 자동 재생성 (최대 1회)",
        "최종 결과 반환 / PDF 리포트 다운로드 가능",
    ]),
]
for title, steps in flows:
    p = doc.add_paragraph()
    r5 = p.add_run(f"[{title}]")
    r5.bold = True
    r5.font.size = Pt(10.5)
    for i, step in enumerate(steps, 1):
        bp = doc.add_paragraph()
        bp.paragraph_format.left_indent = Cm(0.5)
        bp.paragraph_format.space_after = Pt(1)
        br = bp.add_run(f"{i}. {step}")
        br.font.size = Pt(10)
    doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════
# 5. 향후 발전 방향
# ══════════════════════════════════════════════════════════════════
add_heading(doc, "5. 향후 발전 방향 (Future Work)", size=13, color=(0x1E, 0x3A, 0x5F))
future_items = [
    "실제 SMS API 연동을 통한 보호자 알림 자동 발송 구현 (이상거래 감지 시)",
    "JB금융그룹 실제 금융 상품 데이터 연동을 통한 맞춤 추천 고도화",
    "OCR 기능 추가로 사진 촬영한 금융 문서도 분석 가능하도록 확장",
    "멀티 Agent 구조 고도화: 이상거래 탐지 Agent + 재무 분석 Agent 실시간 연동",
    "고령층 전용 음성 인터페이스(TTS/STT) 추가",
    "가입 시 보호자 알림 사전 동의 수집 → 이상거래 감지 시 고객 개입 없이 자동 발송 구조 발전",
    "실제 거래 API 연동으로 자동 거래내역 분석 기능 구현",
]
for item in future_items:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.space_after = Pt(1)
    r6 = p.add_run(f"· {item}")
    r6.font.size = Pt(10)

# ══════════════════════════════════════════════════════════════════
# 6. 부록
# ══════════════════════════════════════════════════════════════════
doc.add_paragraph()
add_heading(doc, "6. 부록 (Appendix)", size=13, color=(0x1E, 0x3A, 0x5F))

appendix_table = doc.add_table(rows=8, cols=2)
appendix_table.style = 'Table Grid'
appendix_items = [
    ("개발 언어", "Python 3.x, TypeScript"),
    ("백엔드 프레임워크", "FastAPI (uvicorn)"),
    ("프론트엔드 프레임워크", "React 18 + Vite + Tailwind CSS"),
    ("AI 모델", "Google Gemini 2.5 Flash (google-genai 라이브러리)"),
    ("PDF 생성", "fpdf2"),
    ("파일 처리", "base64 인코딩 (PDF·이미지 멀티모달 분석)"),
    ("환경변수 관리", "python-dotenv (.env 파일)"),
    ("배포 환경", "로컬 개발 (FastAPI 포트 8000 + Vite 포트 5173)"),
]
for i, (label, value) in enumerate(appendix_items):
    row = appendix_table.rows[i]
    set_cell_bg(row.cells[0], HEADER_BG)
    cell_text(row.cells[0], label, bold=True, size=10,
              align=WD_ALIGN_PARAGRAPH.CENTER, color=(0xFF, 0xFF, 0xFF))
    row.cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    row.cells[1].text = ''
    p = row.cells[1].paragraphs[0]
    r7 = p.add_run(value)
    r7.font.size = Pt(10)

# ══════════════════════════════════════════════════════════════════
# 7. 기능 변경이력
# ══════════════════════════════════════════════════════════════════
doc.add_paragraph()
add_heading(doc, "7. 기능 변경이력 (Change Log)", size=13, color=(0x1E, 0x3A, 0x5F))

note3 = doc.add_paragraph()
nr3 = note3.add_run(
    "본선 단계에서 기능 추가·수정·삭제가 발생한 경우 아래 항목을 기준으로 기록합니다. "
    "예선 제출 시에는 비워두거나 예정사항만 간단히 기재할 수 있습니다."
)
nr3.font.size = Pt(9.5)
nr3.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

change_table = doc.add_table(rows=4, cols=4)
change_table.style = 'Table Grid'
change_headers = ["변경 일자", "변경 대상 기능", "변경 내용", "변경 사유"]
for j, h in enumerate(change_headers):
    set_cell_bg(change_table.rows[0].cells[j], HEADER_BG)
    cell_text(change_table.rows[0].cells[j], h, bold=True, size=10,
              align=WD_ALIGN_PARAGRAPH.CENTER, color=(0xFF, 0xFF, 0xFF))

changes = [
    ("2026.06.07", "전체 아키텍처", "Streamlit → FastAPI + React 전환", "프로덕션 수준 구조로 개선, 확장성 확보"),
    ("2026.06.07", "AI 종합 케어 에이전트", "4단계 Multi-Agent 파이프라인 신규 구현", "재무분석·거래탐지·케어플랜·검증 Agent 분리로 정확도 향상"),
    ("2026.06.07", "보이스피싱 즉시 판단, 노후 버킷리스트", "신규 기능 추가", "고령층 금융사기 예방 및 꿈 실현 재무계획 기능 강화"),
]
for i, (date, target, content, reason) in enumerate(changes, 1):
    row = change_table.rows[i]
    for j, text in enumerate([date, target, content, reason]):
        row.cells[j].text = ''
        p = row.cells[j].paragraphs[0]
        r8 = p.add_run(text)
        r8.font.size = Pt(10)

# ── 저장 ──────────────────────────────────────────────────────────
out_path = r"C:\Users\yoohr\OneDrive\바탕 화면\데이콘\[데이콘] JB금융그룹 Fin AI Challenge 기능명세서_Slowfit.docx"
doc.save(out_path)
print(f"저장 완료: {out_path}")
