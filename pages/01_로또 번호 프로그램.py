import streamlit as st
import random

st.set_page_config(page_title="로또 번호 생성기", page_icon="🎰", layout="centered")

st.title("🎰 대한민국 로또 번호 생성기")
st.markdown("1부터 45 사이의 숫자 중 **6개를 무작위로 추천**합니다!")

# 🎯 게임 수 입력 — 슬라이더 대신 직접 숫자 입력 (1~10)
game_count = st.number_input(
    "몇 게임을 생성하시겠습니까?", 
    min_value=1, 
    max_value=10, 
    value=1, 
    step=1
)

# 버튼 클릭 시 번호 생성
if st.button("번호 생성 🎲"):
    st.subheader(f"🎯 {game_count}게임 추천 결과")

    for i in range(game_count):
        numbers = random.sample(range(1, 46), 6)
        numbers.sort()
        st.write(f"**게임 {i+1}:** ", " ".join([f"{n:02d}" for n in numbers]))
else:
    st.info("👆 위에서 게임 수를 입력하고 '번호 생성 🎲' 버튼을 눌러주세요.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
