
import streamlit as st
import json
from io import BytesIO
from xhtml2pdf import pisa

# 📌 PDF 생성 함수 (xhtml2pdf 버전)
def generate_pdf_stream(html: str) -> BytesIO:
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_file)
    pdf_file.seek(0)
    return pdf_file

# 📌 HTML 생성 함수
def make_html(questions: list, answers: list, meta: dict, show_answer=False) -> str:
    rows = ""
    for idx, (q, a) in enumerate(zip(questions, answers), 1):
        rows += f"""
        <div style='margin-top: 24px; page-break-inside: avoid;'>
            <b>{idx}. {q}</b><br>
            <span style='color: gray;'>Hint: {"(힌트: M___)" if meta["hint"] else "없음"}</span><br>
            {'<span style="color: blue;">정답: ' + a + '</span>' if show_answer else ''}
        </div>
        """
    return f"""
    <html>
    <body style='font-family: sans-serif; padding: 40px;'>
        <h2>SNT Grammar {'Answer Sheet' if show_answer else 'Quiz'}</h2>
        <p>📘 교재: {meta['book']} / {meta['big']} / {meta['middle']} / {meta['small']}<br>
        🧠 난이도: {meta['level']} / ✏️ 유형: {meta['qtype']}</p>
        {rows}
    </body>
    </html>
    """

# 📘 Streamlit 앱 본문
st.title("📘 문법 문제 자동 생성기")

# Load grammar list
with open("grammar_list.json", "r", encoding="utf-8") as f:
    grammar_data = json.load(f)

# Step 1~5: 조건 선택
book = st.selectbox("① 교재 선택", list(grammar_data.keys()))
big = st.selectbox("② 대단원 선택", list(grammar_data[book].keys()))
middle = st.selectbox("③ 중단원 선택", list(grammar_data[book][big].keys()))
small = st.selectbox("④ 소단원 선택", grammar_data[book][big][middle])
level = st.selectbox("⑤ 난이도 선택 (A: 초5 ~ E: 고3)", ["A", "B", "C", "D", "E"])
qtype = st.radio("⑥ 문제 유형", ["객관식", "영어빈칸", "한글빈칸", "배열형 영작"])
use_hint = st.checkbox("⑦ 힌트 사용 여부 (영어빈칸/영작에만 해당)")
count = st.number_input("⑧ 문제 수", min_value=1, max_value=20, value=5)

# 문제 생성
if st.button("문제 생성하기"):
    st.subheader("📝 생성된 문제")

    question_list = []
    answer_list = []

    for i in range(count):
        q = "My / name / is / John."
        a = "My name is John."
        question_list.append(q)
        answer_list.append(a)

        st.markdown(f"**{i+1}. [{small}] ({level}) 유형: {qtype}**")
        st.markdown(f"- 배열: `{q}`")
        st.markdown(f"- 힌트: {'(힌트: M___)' if use_hint else '없음'}")
        with st.expander("정답 보기"):
            st.markdown(f"`{a}`")

    # 메타 정보 구성
    meta = {
        "book": book,
        "big": big,
        "middle": middle,
        "small": small,
        "level": level,
        "qtype": qtype,
        "hint": use_hint,
    }

    # HTML & PDF 생성
    quiz_html = make_html(question_list, answer_list, meta, show_answer=False)
    answer_html = make_html(question_list, answer_list, meta, show_answer=True)

    st.markdown("---")
    st.subheader("📥 PDF 출력")

    col1, col2 = st.columns(2)
    with col1:
        quiz_pdf = generate_pdf_stream(quiz_html)
        st.download_button("📘 문제지 PDF 다운로드", data=quiz_pdf, file_name="문제지.pdf", mime="application/pdf")
    with col2:
        answer_pdf = generate_pdf_stream(answer_html)
        st.download_button("📙 정답지 PDF 다운로드", data=answer_pdf, file_name="정답지.pdf", mime="application/pdf")
