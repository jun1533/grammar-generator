
import streamlit as st
import json
import random

# Load grammar list
with open("grammar_list.json", "r", encoding="utf-8") as f:
    grammar_data = json.load(f)

st.title("📘 문법 문제 자동 생성기")

# Step 1: 문법 선택
book = st.selectbox("① 교재 선택", list(grammar_data.keys()))
big = st.selectbox("② 대단원 선택", list(grammar_data[book].keys()))
middle = st.selectbox("③ 중단원 선택", list(grammar_data[book][big].keys()))
small = st.selectbox("④ 소단원 선택", grammar_data[book][big][middle])

# Step 2: 난이도
level = st.selectbox("④ 난이도 선택 (A: 초5 ~ E: 고3)", ["A", "B", "C", "D", "E"])

# Step 3: 문제 유형
qtype = st.radio("⑤ 문제 유형", ["객관식", "영어빈칸", "한글빈칸", "배열형 영작"])

# Step 4: 힌트 여부
use_hint = st.checkbox("⑥ 힌트 사용 여부 (영어빈칸/영작에만 해당)")

# Step 5: 문제 수 입력
count = st.number_input("⑦ 문제 수", min_value=1, max_value=20, value=5)

# Generate dummy questions
if st.button("문제 생성하기"):
    st.subheader("📝 생성된 문제")
    for i in range(1, count + 1):
        st.markdown(f"**{i}. [{small}] ({level}) 유형: {qtype}**")
        if qtype == "배열형 영작":
            sentence = "My / name / is / John."
            answer = "My name is John."
            hint = "단어를 올바르게 배열하세요." + (" (힌트: M___)" if use_hint else "")
            st.markdown(f"- 배열: `{sentence}`")
            st.markdown(f"- {hint}")
            with st.expander("정답 보기"):
                st.markdown(f"`{answer}`")
        else:
            st.markdown("- 이 기능은 현재 영작 유형만 샘플로 제공됩니다.")

import streamlit as st
from weasyprint import HTML
from io import BytesIO

# PDF 생성 함수
def generate_pdf_stream(html_content: str) -> BytesIO:
    pdf_file = BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)
    return pdf_file

# 샘플 HTML 템플릿 (여기에 문제나 정답 내용을 동적으로 넣어도 됨)
def create_quiz_html(is_answer: bool = False) -> str:
    content = """
    <html>
    <body style='font-family: sans-serif; padding: 2rem;'>
        <h2>SNT Grammar {title}</h2>
        <ol>
            <li>He <u>_____</u> happy yesterday.</li>
            <li>They <u>_____</u> at the park.</li>
        </ol>
    """.replace("{title}", "Answer Sheet" if is_answer else "Quiz")

    if is_answer:
        content += """
        <hr>
        <h4>정답</h4>
        <ul>
            <li>was</li>
            <li>were</li>
        </ul>
        """

    content += "</body></html>"
    return content

# Streamlit UI
st.title("📄 문법 문제지 / 정답지 실시간 PDF 생성기")

option = st.radio("출력할 항목을 선택하세요:", ["문제지", "정답지"])

if st.button("📥 PDF 생성 및 다운로드"):
    html = create_quiz_html(is_answer=(option == "정답지"))
    pdf = generate_pdf_stream(html)
    st.download_button(
        label="PDF 다운로드",
        data=pdf,
        file_name="문제지.pdf" if option == "문제지" else "정답지.pdf",
        mime="application/pdf"
    )
