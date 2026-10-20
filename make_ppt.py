from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
import os

BLUE_DARK  = RGBColor(0x1A, 0x3A, 0x6B)
BLUE_MID   = RGBColor(0x2E, 0x6D, 0xB8)
BLUE_LIGHT = RGBColor(0xD6, 0xE4, 0xF7)
ACCENT     = RGBColor(0xE8, 0x6A, 0x2C)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_BG    = RGBColor(0xF5, 0xF7, 0xFA)
GRAY_TEXT  = RGBColor(0x44, 0x44, 0x55)
GREEN      = RGBColor(0x1A, 0x7A, 0x4A)

IMG_DIR  = r"C:\_dev_slide\assets\images"
ANIM_DIR = r"C:\_dev_slide\assets\animations\mp4"

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_rect(slide, l, t, w, h, fill=None, line=None, line_w=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
        if line_w:
            shape.line.width = Pt(line_w)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, l, t, w, h,
             size=18, bold=False, color=None, align=PP_ALIGN.LEFT,
             wrap=True, italic=False):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.color.rgb = color if color else GRAY_TEXT
    return txb


def slide_header(slide, title):
    add_rect(slide, 0, 0, 13.33, 1.35, fill=BLUE_DARK)
    add_rect(slide, 0, 1.35, 13.33, 0.06, fill=ACCENT)
    add_rect(slide, 0, 1.41, 13.33, 6.09, fill=GRAY_BG)
    add_text(slide, title, 0.4, 0.25, 12.5, 0.9, size=28, bold=True, color=WHITE)


def slide_cover(prs):
    slide = prs.slides.add_slide(BLANK)
    add_rect(slide, 0, 0, 13.33, 7.5, fill=BLUE_DARK)
    add_rect(slide, 0, 0, 13.33, 0.08, fill=ACCENT)
    dec = slide.shapes.add_shape(9, Inches(9.5), Inches(-1.5), Inches(6), Inches(6))
    dec.fill.solid(); dec.fill.fore_color.rgb = RGBColor(0x25, 0x50, 0x90)
    dec.line.fill.background()
    add_text(slide, "확률과 통계", 1.0, 1.2, 9, 1.0, size=22, color=ACCENT)
    add_text(slide, "Ⅲ. 통계 — 확률분포", 1.0, 2.0, 10, 1.5, size=44, bold=True, color=WHITE)
    add_text(slide, "이산·연속 확률변수 / 기댓값과 표준편차", 1.0, 3.5, 9, 0.8, size=22, color=BLUE_LIGHT)
    add_rect(slide, 1.0, 4.6, 5.5, 0.06, fill=ACCENT)
    add_text(slide, "대학교 1학년  |  확률과 통계", 1.0, 4.8, 6, 0.5, size=16,
             color=RGBColor(0xAA, 0xBB, 0xDD))


def section_divider(prs, num, title, subtitle=""):
    slide = prs.slides.add_slide(BLANK)
    add_rect(slide, 0, 0, 13.33, 7.5, fill=BLUE_MID)
    add_rect(slide, 0, 0, 0.12, 7.5, fill=ACCENT)
    add_text(slide, f"SECTION  {num:02d}", 0.5, 2.2, 12, 0.7,
             size=16, color=RGBColor(0xCC, 0xDD, 0xFF))
    add_text(slide, title, 0.5, 2.9, 12, 1.2, size=40, bold=True, color=WHITE)
    if subtitle:
        add_text(slide, subtitle, 0.5, 4.1, 10, 0.8, size=20, color=BLUE_LIGHT, italic=True)


def content_slide(prs, title, bullets, note=""):
    slide = prs.slides.add_slide(BLANK)
    slide_header(slide, title)
    y = 1.7
    for item in bullets:
        if item.get("head"):
            add_rect(slide, 0.3, y - 0.05, 12.7, 0.55, fill=BLUE_LIGHT)
            add_text(slide, item["text"], 0.5, y, 12.2, 0.5, size=17, bold=True, color=BLUE_DARK)
            y += 0.6
        else:
            indent = 0.5 + item.get("level", 0) * 0.4
            dot_color = ACCENT if item.get("level", 0) == 0 else BLUE_MID
            add_rect(slide, indent - 0.25, y + 0.14, 0.12, 0.12, fill=dot_color)
            add_text(slide, item["text"], indent, y, 12.5 - indent, 0.45, size=16, color=GRAY_TEXT)
            y += 0.5
    if note:
        add_rect(slide, 0.3, 6.7, 12.7, 0.6, fill=RGBColor(0xFF, 0xF0, 0xE0))
        add_text(slide, f"📌  {note}", 0.5, 6.72, 12.3, 0.55, size=14,
                 color=RGBColor(0x99, 0x44, 0x00))


def analogy_slide(prs, title, img_filename, concept, analogy_title, points, note=""):
    """왼쪽 설명 + 오른쪽 비유 이미지"""
    slide = prs.slides.add_slide(BLANK)
    slide_header(slide, title)

    # 왼쪽 텍스트 영역
    y = 1.7
    add_rect(slide, 0.3, y - 0.1, 6.5, 0.55, fill=BLUE_LIGHT)
    add_text(slide, concept, 0.5, y, 6.2, 0.5, size=17, bold=True, color=BLUE_DARK)
    y += 0.65
    for pt in points:
        add_rect(slide, 0.5, y + 0.13, 0.12, 0.12, fill=ACCENT)
        add_text(slide, pt, 0.75, y, 5.8, 0.45, size=15, color=GRAY_TEXT)
        y += 0.52

    # 오른쪽 이미지 + 비유 제목
    img_path = os.path.join(IMG_DIR, img_filename)
    if os.path.exists(img_path):
        add_rect(slide, 7.1, 1.5, 5.9, 5.5, fill=WHITE, line=BLUE_MID, line_w=1)
        add_text(slide, f"비유:  {analogy_title}", 7.2, 1.55, 5.7, 0.5,
                 size=15, bold=True, color=BLUE_MID)
        try:
            slide.shapes.add_picture(img_path, Inches(7.3), Inches(2.15), Inches(5.5), Inches(4.5))
        except Exception:
            add_text(slide, f"[이미지: {img_filename}]", 7.3, 3.5, 5.5, 1.0,
                     size=14, color=GRAY_TEXT, align=PP_ALIGN.CENTER)
    else:
        add_rect(slide, 7.1, 1.5, 5.9, 5.5, fill=BLUE_LIGHT, line=BLUE_MID, line_w=1)
        add_text(slide, f"비유:  {analogy_title}", 7.2, 1.55, 5.7, 0.5,
                 size=15, bold=True, color=BLUE_DARK)
        add_text(slide, f"[{img_filename}]", 7.3, 3.5, 5.5, 1.0,
                 size=13, color=GRAY_TEXT, align=PP_ALIGN.CENTER)

    if note:
        add_rect(slide, 0.3, 6.7, 12.7, 0.6, fill=RGBColor(0xFF, 0xF0, 0xE0))
        add_text(slide, f"📌  {note}", 0.5, 6.72, 12.3, 0.55, size=14,
                 color=RGBColor(0x99, 0x44, 0x00))


def anim_slide(prs, title, mp4_filename, caption=""):
    """Manim 애니메이션 동영상 슬라이드"""
    slide = prs.slides.add_slide(BLANK)
    slide_header(slide, title)
    mp4_path = os.path.join(ANIM_DIR, mp4_filename)

    add_rect(slide, 1.0, 1.6, 11.33, 5.5, fill=RGBColor(0x11, 0x11, 0x22))
    if os.path.exists(mp4_path):
        try:
            slide.shapes.add_movie(
                mp4_path,
                Inches(1.0), Inches(1.6), Inches(11.33), Inches(5.1),
                mime_type="video/mp4"
            )
        except Exception:
            add_text(slide, f"[동영상: {mp4_filename}]", 1.0, 3.8, 11.33, 1.0,
                     size=16, color=WHITE, align=PP_ALIGN.CENTER)
    else:
        add_text(slide, f"[동영상: {mp4_filename}]", 1.0, 3.8, 11.33, 1.0,
                 size=16, color=WHITE, align=PP_ALIGN.CENTER)

    if caption:
        add_text(slide, caption, 1.0, 6.85, 11.33, 0.5, size=14,
                 color=GRAY_TEXT, align=PP_ALIGN.CENTER)


def two_col_slide(prs, title, left_title, left_items, right_title, right_items):
    slide = prs.slides.add_slide(BLANK)
    slide_header(slide, title)
    for side, x, col, items, st in [
        ("left",  0.3, BLUE_MID, left_items,  left_title),
        ("right", 6.9, GREEN,    right_items, right_title),
    ]:
        add_rect(slide, x, 1.6, 6.1, 5.7, fill=WHITE, line=col, line_w=1.2)
        add_rect(slide, x, 1.6, 6.1, 0.55, fill=col)
        add_text(slide, st, x + 0.15, 1.63, 5.8, 0.48, size=17, bold=True, color=WHITE)
        y = 2.3
        for item in items:
            add_rect(slide, x + 0.25, y + 0.13, 0.1, 0.1, fill=col)
            add_text(slide, item, x + 0.45, y, 5.5, 0.5, size=15, color=GRAY_TEXT)
            y += 0.52


def formula_slide(prs, title, formulas, desc=""):
    slide = prs.slides.add_slide(BLANK)
    slide_header(slide, title)
    y = 1.8
    for f in formulas:
        add_rect(slide, 1.0, y, 11.3, 0.95, fill=WHITE, line=BLUE_MID, line_w=1.0)
        add_text(slide, f["label"],   1.3, y + 0.05, 3.5, 0.45, size=15, bold=True, color=BLUE_DARK)
        add_text(slide, f["formula"], 5.0, y + 0.05, 7.0, 0.45, size=18, bold=True, color=ACCENT)
        y += 1.1
    if desc:
        add_rect(slide, 1.0, y + 0.1, 11.3, 0.9, fill=RGBColor(0xE8, 0xF4, 0xE8), line=GREEN, line_w=1)
        add_text(slide, desc, 1.2, y + 0.15, 11.0, 0.8, size=15, italic=True, color=GREEN)


def table_slide(prs, title, col_headers, rows, note=""):
    slide = prs.slides.add_slide(BLANK)
    slide_header(slide, title)
    n_cols = len(col_headers)
    col_w  = 10.5 / n_cols
    sx, y  = 1.4, 2.0
    for ci, h in enumerate(col_headers):
        add_rect(slide, sx + ci * col_w, y, col_w, 0.55, fill=BLUE_DARK, line=WHITE, line_w=0.5)
        add_text(slide, h, sx + ci * col_w + 0.05, y + 0.05, col_w - 0.1, 0.45,
                 size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    y += 0.55
    for ri, row in enumerate(rows):
        bg = WHITE if ri % 2 == 0 else BLUE_LIGHT
        for ci, cell in enumerate(row):
            add_rect(slide, sx + ci * col_w, y, col_w, 0.52, fill=bg,
                     line=RGBColor(0xCC, 0xDD, 0xEE), line_w=0.3)
            add_text(slide, str(cell), sx + ci * col_w + 0.05, y + 0.05,
                     col_w - 0.1, 0.42, size=14, color=GRAY_TEXT, align=PP_ALIGN.CENTER)
        y += 0.52
    if note:
        add_rect(slide, 0.3, 6.7, 12.7, 0.6, fill=RGBColor(0xFF, 0xF0, 0xE0))
        add_text(slide, note, 0.5, 6.72, 12.3, 0.55, size=14, color=RGBColor(0x99, 0x44, 0x00))


def summary_slide(prs):
    slide = prs.slides.add_slide(BLANK)
    add_rect(slide, 0, 0, 13.33, 7.5, fill=BLUE_DARK)
    add_rect(slide, 0, 0, 0.12, 7.5, fill=ACCENT)
    add_text(slide, "핵심 정리", 0.5, 0.5, 12, 0.9, size=36, bold=True, color=WHITE)
    add_rect(slide, 0.5, 1.45, 5.5, 0.05, fill=ACCENT)
    items = [
        ("01", "확률변수",       "각 근원사건에 실수를 대응시키는 함수"),
        ("02", "이산 확률변수",   "값이 셀 수 있음 → 확률질량함수(PMF)"),
        ("03", "연속 확률변수",   "실수 범위의 값 → 확률밀도함수(PDF), 넓이=확률"),
        ("04", "기댓값 E(X)",    "E(X) = Σ xᵢpᵢ  —  분포의 무게중심"),
        ("05", "분산 V(X)",      "V(X) = E(X²) − {E(X)}²"),
        ("06", "aX + b 변환",    "E(aX+b) = aE(X)+b,   V(aX+b) = a²V(X)"),
    ]
    y = 1.7
    for num, name, desc in items:
        add_rect(slide, 0.5, y, 1.0, 0.65, fill=ACCENT)
        add_text(slide, num, 0.5, y + 0.08, 1.0, 0.5, size=18, bold=True,
                 color=WHITE, align=PP_ALIGN.CENTER)
        add_rect(slide, 1.55, y, 11.4, 0.65, fill=RGBColor(0x23, 0x4E, 0x88))
        add_text(slide, name, 1.75, y + 0.08, 3.2, 0.5, size=16, bold=True, color=ACCENT)
        add_text(slide, desc, 5.1,  y + 0.10, 7.7, 0.5, size=15, color=BLUE_LIGHT)
        y += 0.75


# ── 슬라이드 구성 ───────────────────────────────────────────

slide_cover(prs)

# ─── SECTION 1: 확률변수 ───
section_divider(prs, 1, "확률변수와 확률분포",
                "Random Variable & Probability Distribution")

# 확률변수 개념 + 비유(자동판매기)
analogy_slide(prs, "확률변수란?",
    "analogy_01_rv.jpg",
    "확률변수 — 함수로 이해하기",
    "자동판매기 = 함수",
    [
        "시행의 각 결과 → 하나의 실수로 변환",
        "동전 2개 던지기 → X = 앞면 횟수 (0, 1, 2)",
        "기호: P(X = x)  →  X가 값 x를 취할 확률",
        "확률변수 ≠ 확률값,  확률변수는 '대응 규칙'",
    ],
    note="자동판매기처럼 '입력(근원사건) → 출력(실수)'하는 함수입니다"
)

two_col_slide(prs, "이산확률변수 vs 연속확률변수",
    "이산확률변수 (Discrete)",
    ["값이 유한개 또는 셀 수 있음",
     "각 값에 확률을 직접 대응",
     "확률질량함수(PMF) 사용",
     "예) 주사위 눈, 동전 앞면 횟수",
     "Σpᵢ = 1 항상 성립"],
    "연속확률변수 (Continuous)",
    ["값이 어떤 구간의 모든 실수",
     "특정 한 점의 확률 = 0",
     "확률밀도함수(PDF) 사용",
     "예) 키, 몸무게, 대기 시간",
     "구간의 넓이 = 확률"]
)

# 이항분포 비유 + 애니메이션
analogy_slide(prs, "이산확률변수 — 확률분포표",
    "analogy_05_binom.png",
    "이산확률변수의 확률분포",
    "동전 던지기 = 이산 시행",
    [
        "X가 취하는 각 값과 확률을 표로 정리",
        "모든 확률의 합 = 1  (p₁ + p₂ + ⋯ = 1)",
        "각 확률: 0 ≤ pᵢ ≤ 1",
        "동전 4개 → X ~ B(4, 0.5)",
    ],
    note="확률분포표의 합이 1인지 항상 먼저 확인!"
)
anim_slide(prs, "【애니메이션】 이산확률분포 — 막대그래프",
    "anim_01_pmf.mp4",
    "동전 4개를 던질 때 앞면 횟수의 확률분포  B(4, 0.5)")

table_slide(prs, "확률분포표 예시 — 동전 2개를 던질 때 앞면 횟수 X",
    ["X (앞면 횟수)", "P(X = x)", "계산 근거"],
    [
        ["0", "1/4",       "뒷뒷 → (T, T)"],
        ["1", "2/4 = 1/2", "앞뒷, 뒷앞 → (H,T), (T,H)"],
        ["2", "1/4",       "앞앞 → (H, H)"],
        ["합 계", "1",     "—"],
    ]
)

# ─── SECTION 2: 연속확률변수 ───
section_divider(prs, 2, "연속확률변수와 확률밀도함수",
                "Continuous Random Variable & PDF")

analogy_slide(prs, "연속확률변수 — 확률밀도함수",
    "analogy_04_cont.jpg",
    "연속확률변수의 확률밀도함수(PDF)",
    "빗물 측정 = 연속 확률",
    [
        "X의 값이 어떤 구간의 모든 실수",
        "넓이 = 확률  (P(a≤X≤b) = 곡선 아래 면적)",
        "성질 ①  f(x) ≥ 0",
        "성질 ②  전체 넓이 = 1",
        "P(X = c) = 0  (특정 점의 확률은 0)",
    ],
    note="강수량처럼 연속된 값 → 구간으로만 확률을 말할 수 있습니다"
)
anim_slide(prs, "【애니메이션】 확률밀도함수 — 넓이가 확률",
    "anim_02_pdf.mp4",
    "정규분포 곡선 아래 넓이 = 확률  (68% / 95% 규칙)")

# ─── SECTION 3: 기댓값과 분산 ───
section_divider(prs, 3, "기댓값, 분산, 표준편차",
                "Expected Value, Variance, Standard Deviation")

analogy_slide(prs, "기댓값 — 확률분포의 무게중심",
    "analogy_02_ev.png",
    "기댓값 E(X)",
    "시소 균형점 = 기댓값",
    [
        "E(X) = Σ xᵢ·pᵢ  (이산확률변수)",
        "무게중심: 분포가 균형을 이루는 지점",
        "주사위 1개  →  E(X) = 3.5",
        "기댓값은 실제로 나오는 값이 아닐 수 있음",
    ],
    note="시소의 균형점처럼 — 확률(무게)로 가중 평균한 값입니다"
)
anim_slide(prs, "【애니메이션】 기댓값 — 주사위 무게중심",
    "anim_03_ev.mp4",
    "주사위 X ~ Uniform(1,6),  E(X) = 3.5  (빨간 점선)")

formula_slide(prs, "이산확률변수의 기댓값·분산·표준편차", [
    {"label": "기댓값 (평균)  E(X)",
     "formula": "E(X) = Σ xᵢ · pᵢ"},
    {"label": "분산  V(X)",
     "formula": "V(X) = E(X²) − {E(X)}²"},
    {"label": "표준편차  σ(X)",
     "formula": "σ(X) = √V(X)"},
    {"label": "계산 편의 공식",
     "formula": "V(X) = E(X²) − {E(X)}²"},
],
desc="💡  실전 팁:  V(X) = E(X²) − {E(X)}² 공식이 계산이 빠릅니다!")

analogy_slide(prs, "분산 — 흩어진 정도",
    "analogy_03_var.jpg",
    "분산 V(X)와 표준편차 σ(X)",
    "과녁 정확도 = 분산",
    [
        "V(X) = E((X−μ)²)  : 평균에서 벗어난 정도",
        "분산이 작다 → 값이 평균 주위에 몰림 (정확)",
        "분산이 크다 → 값이 넓게 퍼짐 (부정확)",
        "σ(X) = √V(X)  (원래 단위로 되돌림)",
    ],
    note="과녁의 탄착군이 좁을수록 분산이 작습니다"
)

table_slide(prs, "기댓값·분산 계산 예제 — 배송 소요 일수 X",
    ["X (일)", "P(X)", "x·P(X)", "x²·P(X)"],
    [
        ["1", "0.1", "0.1", "0.1"],
        ["2", "0.2", "0.4", "0.8"],
        ["3", "0.4", "1.2", "3.6"],
        ["4", "0.2", "0.8", "3.2"],
        ["5", "0.1", "0.5", "2.5"],
        ["합 계", "1.0", "E(X) = 3.0", "E(X²) = 10.2"],
    ],
    note="V(X) = 10.2 − 3.0² = 1.2   /   σ(X) = √1.2 ≈ 1.095"
)

content_slide(prs, "확률변수의 선형변환  Y = aX + b", [
    {"text": "변환 규칙 (a, b는 상수)", "head": True},
    {"text": "E(aX + b) = a·E(X) + b", "level": 0},
    {"text": "V(aX + b) = a²·V(X)   ← b는 분산에 영향 없음!", "level": 0},
    {"text": "σ(aX + b) = |a|·σ(X)", "level": 0},
    {"text": "왜 b가 분산에 영향이 없을까?", "head": True},
    {"text": "분산은 '흩어진 정도' → 전체를 평행이동해도 흩어짐은 동일", "level": 0},
    {"text": "예시", "head": True},
    {"text": "E(X) = 3,  V(X) = 2 일 때  Y = 5X − 1 을 구하면?", "level": 0},
    {"text": "E(Y) = 5×3 − 1 = 14", "level": 1},
    {"text": "V(Y) = 5²×2 = 50", "level": 1},
    {"text": "σ(Y) = √50 = 5√2", "level": 1},
], note="a²이 붙는 이유: 분산은 '제곱 단위'이기 때문입니다.")

anim_slide(prs, "【애니메이션】 선형변환 — 분포가 이동·확장",
    "anim_04_transform.mp4",
    "Y = 2X+1  →  평균은 이동, 분산은 4배 확대")

summary_slide(prs)

path = r"C:\_dev_slide\slides\lecture_sample.pptx"
prs.save(path)
print(f"저장 완료: {path}  (슬라이드 수: {len(prs.slides)}장)")
