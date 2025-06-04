import streamlit as st
import json
from io import BytesIO
from xhtml2pdf import pisa

# PDF 생성 함수
def generate_pdf_stream(html: str) -> BytesIO:
    pdf_file = BytesIO()
    pisa.CreatePDF(html, dest=pdf_file)
    pdf_file.seek(0)
    return pdf_file

# 문제 항목 생성
def build_questions_html(questions, answers, translations, show_answer=False):
    q_html = ""
    for idx, (q, a, k) in enumerate(zip(questions, answers, translations), 1):
        answer_html = f"<div class='answer'>정답: {a}</div>" if show_answer else ""
        q_html += f"<div class='question'><div class='english'>{idx}. {q}</div><div class='korean'>({k})</div>{answer_html}</div>"
    return q_html

# 전체 HTML 템플릿
def make_html_template(meta, questions_html, show_answer=False):
    title = "Answer Sheet" if show_answer else "Quiz"
    return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        @font-face {{
            font-family: 'GmarketSans';
            src: url("file:///mnt/data/GmarketSansTTFMedium.ttf");
        }}
        body {{
            font-family: 'GmarketSans', sans-serif;
            margin: 1cm;
            border: 2px solid #333;
            padding: 1cm;
            font-size: 13pt;
        }}
        .header {{
            text-align: center;
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        .info-box {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 12pt;
        }}
        .quiz-meta {{
            border-top: 1px solid #999;
            padding-top: 10px;
            margin-top: 10px;
            font-size: 12pt;
        }}
        .question {{
            margin-top: 25px;
            page-break-inside: avoid;
        }}
        .english {{
            margin-bottom: 4px;
        }}
        .korean {{
            margin-left: 10px;
            color: #444;
        }}
        .answer {{
            margin-top: 5px;
            color: blue;
        }}
    </style>
</head>
<body>

<div class="header">SNT Grammar {title}</div>

<div class="info-box">
    <div>총 문제 수: {meta['count']}</div>
    <div>점수: (       / {meta['count']})</div>
    <div>확인: 학부모 서명</div>
</div>

<div class="quiz-meta">
    교재명: {meta['book']} &nbsp;&nbsp; 대단원: {meta['big']}<br>
    중단원: {meta['middle']} &nbsp;&nbsp; 유형: {meta['qtype']}
</div>

<div style="margin-top:10px;">* 다음 문장을 완성하세요.</div>

{questions_html}

</body>
</html>
"""

# Streamlit 앱 시작
st.title("📘 문법 문제 자동 생성기")

with open("grammar_list.json", "r", encoding="utf-8") as f:
    grammar_data = json.load(f)

book = st.selectbox("① 교재 선택", list(grammar_data.keys()))
big = st.selectbox("② 대단원 선택", list(grammar_data[book].keys()))
middle = st.selectbox("③ 중단원 선택", list(grammar_data[book][big].keys()))
small = st.selectbox("④ 소단원 선택", grammar_data[book][big][middle])
level = st.selectbox("⑤ 난이도 선택 (A~E)", ["A", "B", "C", "D", "E"])
qtype = st.radio("⑥ 문제 유형", ["객관식", "영어빈칸", "한글빈칸", "배열형 영작"])
use_hint = st.checkbox("⑦ 힌트 사용 여부")
count = st.number_input("⑧ 문제 수", min_value=1, max_value=20, value=5)

if st.button("문제 생성하기"):
    questions = ["My / name / is / John."] * count
    answers = ["My name is John."] * count
    translations = ["내 이름은 존이야."] * count

    st.subheader("📝 생성된 문제")
    for i in range(count):
        st.markdown(f"**{i+1}. {questions[i]}**")
        st.markdown(f"- 해석: {translations[i]}")
        if use_hint:
            st.markdown("- 힌트: M____")
        with st.expander("정답 보기"):
            st.markdown(f"`{answers[i]}`")

    meta = {
        "book": book,
        "big": big,
        "middle": middle,
        "small": small,
        "level": level,
        "qtype": qtype,
        "hint": use_hint,
        "count": count
    }

    q_html = build_questions_html(questions, answers, translations, False)
    a_html = build_questions_html(questions, answers, translations, True)

    full_q_html = make_html_template(meta, q_html, show_answer=False)
    full_a_html = make_html_template(meta, a_html, show_answer=True)

    st.subheader("📥 PDF 출력")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📘 문제지 PDF 다운로드", generate_pdf_stream(full_q_html), file_name="문제지.pdf", mime="application/pdf")
    with col2:
        st.download_button("📙 정답지 PDF 다운로드", generate_pdf_stream(full_a_html), file_name="정답지.pdf", mime="application/pdf")
