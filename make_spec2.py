# -*- coding: utf-8 -*-
"""기능명세서 생성 (안정적 버전 - 3페이지 이내)"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# 여백
for sec in doc.sections:
    sec.top_margin    = Cm(1.5)
    sec.bottom_margin = Cm(1.5)
    sec.left_margin   = Cm(2.0)
    sec.right_margin  = Cm(2.0)

DARK  = (0x1E, 0x3A, 0x5F)
WHITE = (0xFF, 0xFF, 0xFF)
LIGHT = "DBEAFE"
HDR   = "1E3A5F"

# ── helpers ───────────────────────────────────────────────────────
def shd(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    e = OxmlElement('w:shd')
    e.set(qn('w:val'),   'clear')
    e.set(qn('w:color'), 'auto')
    e.set(qn('w:fill'),  hex_color)
    tcPr.append(e)

def cv(cell, text, bold=False, sz=9, align=WD_ALIGN_PARAGRAPH.LEFT, rgb=None, wrap=True):
    for p in cell.paragraphs:
        for r in p.runs:
            r.text = ''
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(sz)
    if rgb:
        run.font.color.rgb = RGBColor(*rgb)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def heading(text, sz=11, color=DARK):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(sz)
    r.font.color.rgb = RGBColor(*color)

def body(text, sz=9, indent=0, space_after=1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent   = Cm(indent)
    p.paragraph_format.space_before  = Pt(0)
    p.paragraph_format.space_after   = Pt(space_after)
    r = p.add_run(text)
    r.font.size = Pt(sz)

def set_col_widths(table, widths_cm):
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            cell.width = Cm(widths_cm[i])

# ══════════════════════════════════════════════════════════════════
# 제목
# ══════════════════════════════════════════════════════════════════
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(3)
tr = title_p.add_run("JB금융그룹 Fin:AI Challenge  기능 명세서")
tr.bold = True
tr.font.size = Pt(15)
tr.font.color.rgb = RGBColor(*DARK)

note_p = doc.add_paragraph()
note_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
note_p.paragraph_format.space_after = Pt(4)
nr = note_p.add_run(
    "본 문서는 예선 제출용 기능명세서입니다. 본선 진출 시 동일 문서를 기준으로 보완하며, "
    "기능 변경이 발생한 경우 '7. 기능 변경이력'에 반드시 기록합니다."
)
nr.font.size = Pt(8)
nr.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

# 기본 정보 테이블
info = doc.add_table(rows=2, cols=6)
info.style = 'Table Grid'
info_data = [
    [("팀명", True, HDR), ("유해린", False, LIGHT),
     ("주제 구분", True, HDR), ("지정주제 1", False, LIGHT),
     ("작성일", True, HDR), ("2026.06.07", False, LIGHT)],
    [("서비스명", True, HDR), ("Slowfit", False, LIGHT),
     ("팀원(역할)", True, HDR), ("유해린(기획/개발)", False, LIGHT),
     ("AI 모델", True, HDR), ("Gemini 2.5 Flash", False, LIGHT)],
]
for i, row_data in enumerate(info_data):
    row = info.rows[i]
    for j, (text, bold, bg) in enumerate(row_data):
        shd(row.cells[j], bg)
        rgb = WHITE if bold else None
        cv(row.cells[j], text, bold=bold, sz=9,
           align=WD_ALIGN_PARAGRAPH.CENTER, rgb=rgb)
set_col_widths(info, [2.5, 2.5, 2.5, 3.0, 2.5, 2.5])

# ══════════════════════════════════════════════════════════════════
# 1. 서비스 개요
# ══════════════════════════════════════════════════════════════════
heading("1. 서비스 개요 (Service)")
ov = doc.add_table(rows=4, cols=2)
ov.style = 'Table Grid'
ov_data = [
    ("서비스 한줄 소개",
     "고령 고객의 자산·연금·생활비·이상거래를 AI가 통합 분석하여 안전한 노후 생활을 지원하는 Multi-Agent AI 서비스"),
    ("개발 목표",
     "고령 고객의 금융사기 피해를 예방하고, 노후 자산·연금·생활비를 통합 관리하는 AI Agent 서비스 구현"),
    ("타겟 사용자",
     "핵심: 은퇴 이후 노후 자산관리가 필요한 고령 고객  /  확장: 은퇴 앞둔 50대, 고령 부모를 둔 보호자 가족"),
    ("기대 효과",
     "① 고령층 금융사기 피해 예방  ② 노후 자산·연금 통합 관리  ③ 복잡한 금융 정보 쉬운 설명  ④ 가족 기반 금융 안전망"),
]
for i, (lbl, val) in enumerate(ov_data):
    row = ov.rows[i]
    shd(row.cells[0], HDR)
    cv(row.cells[0], lbl, bold=True, sz=9, align=WD_ALIGN_PARAGRAPH.CENTER, rgb=WHITE)
    cv(row.cells[1], val, sz=9)
set_col_widths(ov, [3.0, 12.5])

# ══════════════════════════════════════════════════════════════════
# 2. 시스템 구성도
# ══════════════════════════════════════════════════════════════════
heading("2. 시스템 구성도 (Architecture)")
arch = doc.add_table(rows=1, cols=1)
arch.style = 'Table Grid'
shd(arch.rows[0].cells[0], "F8FAFC")
arch_cell = arch.rows[0].cells[0]
arch_cell.text = ''
p = arch_cell.paragraphs[0]
p.paragraph_format.space_before = Pt(3)
p.paragraph_format.space_after  = Pt(3)

arch_lines = [
    ("[사용자 (고령 고객 / 보호자)]", True),
    ("나이·자산·소득·지출 입력 / 거래내역·금융문서 업로드 / 버킷리스트·보이스피싱 텍스트 입력", False),
    ("↓  REST API  ↓", False),
    ("[프론트엔드]  React + TypeScript + Vite + Tailwind CSS", True),
    ("홈 / 케어에이전트 / 시뮬레이션 / 버킷리스트 / 보이스피싱 / 문서해석 / 상품추천  6개 SPA 페이지", False),
    ("사용자 유형별 적응형 UI (고령층: 대형 텍스트·버튼 / 금융초보자: 툴팁 설명)", False),
    ("↓  FastAPI (Python)  ↓", False),
    ("[AI Agent 처리 레이어]  Google Gemini 2.5 Flash", True),
    ("① 재무분석 Agent  →  ② 이상거래탐지 Agent  →  ③ 케어플랜 Agent  →  ④ 검증 Agent (자동 재생성)", False),
    ("+ 시뮬레이션 / 버킷리스트 / 보이스피싱 / 문서해석(멀티모달) / 상품추천 전용 Agent", False),
    ("↓", False),
    ("[출력]  위험도·안정도 결과 / 맞춤 케어플랜 / 30년 자산변화 / PDF 리포트 다운로드", True),
]

for i, (text, is_bold) in enumerate(arch_lines):
    if i == 0:
        r = arch_cell.paragraphs[0].add_run(text)
        r.bold = is_bold
        r.font.size = Pt(8.5)
    else:
        p2 = arch_cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after  = Pt(0)
        r2 = p2.add_run(text)
        r2.bold = is_bold
        r2.font.size = Pt(8.5)

# ══════════════════════════════════════════════════════════════════
# 3. 핵심 기능 명세
# ══════════════════════════════════════════════════════════════════
heading("3. 핵심 기능 명세 (Feature Specification)")
note2 = doc.add_paragraph()
note2.paragraph_format.space_after = Pt(2)
nr2 = note2.add_run("핵심 기능 위주로 간략히 작성하되, 예선 제출본을 기준으로 본선에서 동일 형식을 유지하여 보완합니다.")
nr2.font.size = Pt(8)
nr2.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

features = [
    ("AI 종합 케어\n에이전트\n(Multi-Agent)",
     "4단계 Multi-Agent 파이프라인으로 재무 상태와 거래 위험을 종합 분석하고 맞춤 케어 플랜을 생성.\n①재무분석→②이상거래탐지→③케어플랜→④검증+자동재생성",
     "입력: 나이·자산·소득·지출·거래내역(선택)\n출력: 재무위험도, 월현금흐름, 핵심위험요인, 자산유지기간, 거래위험도, 위험신호, 즉각조치, 단기/장기 케어플랜, 신뢰도, PDF리포트",
     "Gemini 2.5 Flash\nMulti-Agent 파이프라인\n자동 재생성 로직\nfpdf2 PDF 생성",
     "O"),
    ("미래 생활 안정\n시뮬레이션",
     "자산·연금·생활비·의료비 기반으로 노후 생활 안정성과 30년 자산 변화 추이를 분석",
     "입력: 나이·건강상태·금융자산·부동산·월소득·월생활비·의료비·부양가족·대출여부\n출력: 노후안정도, 월현금흐름, 5/10/10년+ 미래예측, 추천행동, 30년 자산변화 배열(차트)",
     "Gemini 2.5 Flash\n현금흐름·자산유지기간 사전계산\n30년 연도별 자산 시뮬레이션",
     "O"),
    ("노후 버킷리스트\n재무 계획",
     "이루고 싶은 꿈(버킷리스트)을 재무 정보와 연결하여 달성 가능성과 실천 계획을 분석",
     "입력: 나이·자산·소득·지출, 버킷리스트(항목명·예상비용·목표시기)\n출력: 꿈별 달성가능성(달성가능/노력필요/어려움), 우선순위, 실천계획, 응원메시지",
     "Gemini 2.5 Flash\n달성가능성 사전계산\n(자산+저축 vs 비용)",
     "O"),
    ("보이스피싱\n즉시 판단",
     "의심스러운 전화·문자 내용을 입력하면 7가지 사기 판단 기준으로 즉시 분석하여 위험도와 대응 방법을 제공",
     "입력: 의심 통화·문자 텍스트\n출력: 판정(사기/정상/주의), 위험도(높음/보통/낮음), 발견된 위험신호, 쉬운설명, 즉시 행동 지침",
     "Gemini 2.5 Flash\n7대 사기패턴 탐지 프롬프트\n(긴급성·사칭·이체유도 등)",
     "O"),
    ("문서 쉽게\n이해하기",
     "보험 약관·대출 계약서 등을 업로드하면 핵심 내용을 사용자 수준에 맞게 쉽게 요약",
     "입력: PDF·이미지 파일(멀티모달) 또는 텍스트, 문서유형, 사용자유형\n출력: 한줄요약, 쉬운설명, 핵심내용, 주의사항",
     "Gemini 2.5 Flash (멀티모달)\nbase64 파일 인코딩\n사용자 유형별 어조 최적화",
     "O"),
    ("맞춤 금융\n상품 추천",
     "나이·자산·투자성향·재무목표 기반으로 JB금융그룹 계열사(전북은행·광주은행·JB우리캐피탈·JB자산운용) 상품 우선 추천",
     "입력: 나이·소득·자산·월저축·재무목표·투자성향·연금/IRP·세금관심도·대출여부\n출력: 종합평가, 단기·장기·노후 추천상품, 절세방법, 우선순위 행동",
     "Gemini 2.5 Flash\nJB금융 계열사 상품 DB 내장\n목표·성향별 맞춤 프롬프트",
     "O"),
]

feat = doc.add_table(rows=1 + len(features), cols=5)
feat.style = 'Table Grid'
hdrs = ["기능명", "기능 설명", "입력/출력 데이터", "관련 기술", "구현\n여부"]
for j, h in enumerate(hdrs):
    shd(feat.rows[0].cells[j], HDR)
    cv(feat.rows[0].cells[j], h, bold=True, sz=8.5,
       align=WD_ALIGN_PARAGRAPH.CENTER, rgb=WHITE)

for i, (name, desc, io, tech, done) in enumerate(features):
    row = feat.rows[i + 1]
    shd(row.cells[0], "EFF6FF")
    cv(row.cells[0], name, bold=True, sz=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    cv(row.cells[1], desc, sz=8.5)
    cv(row.cells[2], io,   sz=8.5)
    cv(row.cells[3], tech, sz=8.5)
    cv(row.cells[4], done, bold=True, sz=9,
       align=WD_ALIGN_PARAGRAPH.CENTER, rgb=(0x05, 0x96, 0x69))

set_col_widths(feat, [2.3, 4.3, 4.7, 3.2, 1.0])

# ══════════════════════════════════════════════════════════════════
# 4. 주요 기능 흐름도
# ══════════════════════════════════════════════════════════════════
heading("4. 주요 기능 흐름도 (Flow)")

flow = doc.add_table(rows=1, cols=2)
flow.style = 'Table Grid'

# 왼쪽: 일반 흐름
shd(flow.rows[0].cells[0], "F8FAFC")
c0 = flow.rows[0].cells[0]
c0.text = ''
p0 = c0.paragraphs[0]
p0.paragraph_format.space_after = Pt(1)
r0 = p0.add_run("[공통 흐름]")
r0.bold = True; r0.font.size = Pt(8.5)
for step in [
    "① 서비스 접속 → 내 프로필 설정 (저장 시 전 페이지 자동 적용)",
    "② 원하는 기능 선택 (6가지 서비스 카드)",
    "③ 추가 정보 입력 또는 문서 업로드",
    "④ AI 분석 수행 (Gemini 2.5 Flash)",
    "⑤ 위험도·안정도·추천 결과 + 쉬운 설명 출력",
    "⑥ 후속 행동 안내 / PDF 리포트 다운로드",
]:
    sp = c0.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after  = Pt(0)
    sr = sp.add_run(step)
    sr.font.size = Pt(8.5)

# 오른쪽: Multi-Agent 상세 흐름
shd(flow.rows[0].cells[1], "F8FAFC")
c1 = flow.rows[0].cells[1]
c1.text = ''
p1 = c1.paragraphs[0]
p1.paragraph_format.space_after = Pt(1)
r1 = p1.add_run("[AI 종합 케어 에이전트 - Multi-Agent 상세 흐름]")
r1.bold = True; r1.font.size = Pt(8.5)
for step in [
    "① 재무분석 Agent: 위험도(안정/주의/위험)·월현금흐름·자산유지기간 산출",
    "② 이상거래탐지 Agent: 거래내역 입력 시 위험도·위험신호 탐지 (없으면 Skip)",
    "③ 케어플랜 Agent: ①②결과 종합 → 즉각조치·단기계획·장기전략 생성",
    "④ 검증 Agent: 일관성 검증 → '수정 필요' 판정 시 케어플랜 자동 재생성 (최대 1회)",
    "→ 최종 결과 반환 / PDF 종합 케어 리포트 다운로드",
]:
    sp = c1.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after  = Pt(0)
    sr = sp.add_run(step)
    sr.font.size = Pt(8.5)

set_col_widths(flow, [7.75, 7.75])

# ══════════════════════════════════════════════════════════════════
# 5. 향후 발전 방향
# ══════════════════════════════════════════════════════════════════
heading("5. 향후 발전 방향 (Future Work)")
future_table = doc.add_table(rows=1, cols=2)
future_table.style = 'Table Grid'
future_items_l = [
    "SMS API 연동을 통한 이상거래 감지 시 보호자 자동 알림 발송",
    "JB금융그룹 실제 금융 상품 데이터 연동으로 추천 고도화",
    "OCR 기능 추가로 사진 촬영 금융 문서 분석 가능하도록 확장",
    "고령층 전용 음성 인터페이스(TTS/STT) 추가",
]
future_items_r = [
    "Multi-Agent 구조 고도화: 이상거래·재무분석 Agent 실시간 연동",
    "실제 거래 API 연동을 통한 자동 거래내역 분석 구현",
    "개인정보 보호·환각(Hallucination) 최소화를 위한 검증 파이프라인 강화",
    "PoC → 파일럿 → 내부 적용 → 고객 서비스화 단계별 발전 경로 수립",
]
for cell, items in [(future_table.rows[0].cells[0], future_items_l),
                    (future_table.rows[0].cells[1], future_items_r)]:
    cell.text = ''
    for i, item in enumerate(items):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(1)
        r = p.add_run(f"· {item}")
        r.font.size = Pt(8.5)
set_col_widths(future_table, [7.75, 7.75])

# ══════════════════════════════════════════════════════════════════
# 6. 부록
# ══════════════════════════════════════════════════════════════════
heading("6. 부록 (Appendix)")
appendix = doc.add_table(rows=2, cols=4)
appendix.style = 'Table Grid'
app_data = [
    [("개발 언어", "Python 3.x / TypeScript"),
     ("백엔드", "FastAPI + uvicorn"),
     ("프론트엔드", "React 18 + Vite + Tailwind CSS"),
     ("AI 모델", "Google Gemini 2.5 Flash")],
    [("PDF 생성", "fpdf2"),
     ("파일 처리", "base64 (멀티모달 분석)"),
     ("환경변수", "python-dotenv"),
     ("배포 환경", "로컬 (API:8000 / FE:5173)")],
]
for i, row_data in enumerate(app_data):
    row = appendix.rows[i]
    for j, (lbl, val) in enumerate(row_data):
        shd(row.cells[j], HDR)
        # 라벨과 값을 한 셀에
        row.cells[j].text = ''
        p = row.cells[j].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after  = Pt(1)
        r_lbl = p.add_run(lbl + "\n")
        r_lbl.bold = True
        r_lbl.font.size = Pt(8)
        r_lbl.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)
        r_val = p.add_run(val)
        r_val.font.size = Pt(8.5)
        r_val.font.color.rgb = RGBColor(*WHITE)
        row.cells[j].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
set_col_widths(appendix, [3.875, 3.875, 3.875, 3.875])

# ══════════════════════════════════════════════════════════════════
# 7. 기능 변경이력
# ══════════════════════════════════════════════════════════════════
heading("7. 기능 변경이력 (Change Log)")
note3 = doc.add_paragraph()
note3.paragraph_format.space_after = Pt(2)
nr3 = note3.add_run(
    "본선 단계에서 기능 추가·수정·삭제가 발생한 경우 아래 항목을 기준으로 기록합니다. "
    "예선 제출 시에는 비워두거나 예정사항만 간단히 기재할 수 있습니다."
)
nr3.font.size = Pt(8)
nr3.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

change = doc.add_table(rows=4, cols=4)
change.style = 'Table Grid'
ch_hdrs = ["변경 일자", "변경 대상 기능", "변경 내용", "변경 사유"]
for j, h in enumerate(ch_hdrs):
    shd(change.rows[0].cells[j], HDR)
    cv(change.rows[0].cells[j], h, bold=True, sz=9,
       align=WD_ALIGN_PARAGRAPH.CENTER, rgb=WHITE)

changes = [
    ("2026.06.07", "전체 아키텍처",
     "Streamlit → FastAPI + React 전환",
     "프로덕션 수준 구조로 개선, 확장성 확보"),
    ("2026.06.07", "AI 종합 케어 에이전트",
     "4단계 Multi-Agent 파이프라인 신규 구현",
     "재무분석·거래탐지·케어플랜·검증 분리로 정확도 향상"),
    ("2026.06.07", "보이스피싱 판단, 노후 버킷리스트",
     "신규 기능 2개 추가",
     "고령층 금융사기 예방 및 꿈 실현 재무계획 기능 강화"),
]
for i, (date, target, content, reason) in enumerate(changes, 1):
    row = change.rows[i]
    for j, text in enumerate([date, target, content, reason]):
        cv(row.cells[j], text, sz=9,
           align=WD_ALIGN_PARAGRAPH.CENTER if j == 0 else WD_ALIGN_PARAGRAPH.LEFT)
set_col_widths(change, [2.0, 3.5, 5.0, 5.0])

# ── 저장 ──────────────────────────────────────────────────────────
out = r"C:\Users\yoohr\OneDrive\바탕 화면\데이콘\[데이콘] JB금융그룹 Fin AI Challenge 기능명세서_Slowfit.docx"
doc.save(out)
print("done")
