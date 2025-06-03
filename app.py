
import streamlit as st
import json
import random

# Load grammar list
with open("grammar_list.json", "r", encoding="utf-8") as f:
    grammar_data = json.load(f)

st.title("📘 문법 문제 자동 생성기")

# Step 1: 문법 선택
교재명 = st.selectbox("① 교재 선택", list(grammar_data.keys()))
대단원 = st.selectbox("② 대단원 선택", list(grammar_data[교재명].keys()))
중단원 = st.selectbox("③ 중단원 선택", list(grammar_data[교재명][대단원].keys()))
소단원 = st.selectbox("④ 소단원 선택", grammar_data[교재명][대단원][중단원])

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

# PDF 기능은 향후 추가 예정
