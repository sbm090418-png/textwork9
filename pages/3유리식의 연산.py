import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit 앱 제목
st.title('유리함수 마스터')

# --- 설명 섹션 ---
st.header('유리함수 그래프 그리기 원리')
# ... (설명 콘텐츠)

# --- 문제 생성 및 풀이 섹션 ---
st.header('유리함수 그래프 문제 풀기')

# 예시로 계수 고정
a, b, c, d = 2, -1, 1, 3  # y = (2x - 1) / (x + 3)

# 문제 제시
st.subheader(f'문제: 다음 유리함수의 점근선, 정의역, 치역을 구하시오.')
st.latex(r'y = \frac{2x - 1}{x + 3}')

# 정답 계산
vertical_asymptote = -d/c  # x = -3
horizontal_asymptote = a/c  # y = 2
domain = f'x != {vertical_asymptote}'
range_val = f'y != {horizontal_asymptote}'

# 사용자 입력 위젯
st.subheader('당신의 풀이')
user_va = st.text_input('수직 점근선 (x=?)', key='va')
user_ha = st.text_input('수평 점근선 (y=?)', key='ha')

# 정답 확인 버튼
if st.button('정답 확인'):
    st.markdown('---')
    st.subheader('결과')
    
    # 점근선 확인 로직 (간단화)
    if user_va == f'x={vertical_asymptote}' and user_ha == f'y={horizontal_asymptote}':
        st.success('🎉 점근선 정답입니다! 🎉')
    else:
        st.error('😢 다시 확인해보세요.')
        st.info(f'정답 풀이: 수직 점근선 $x={vertical_asymptote}$, 수평 점근선 $y={horizontal_asymptote}$')

    # 그래프 그리기
    # ... (matplotlib/plotly 코드 삽입하여 그래프 및 점근선 표시)

# ---
