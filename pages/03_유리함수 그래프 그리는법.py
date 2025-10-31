import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# --- 1. 개념 설명 함수 ---
def show_theory():
    st.header('📚 유리함수 개념 학습')
    st.markdown("""
    **유리함수(Rational Function)**는 두 다항식의 비 $\frac{P(x)}{Q(x)}$ 형태로 나타낼 수 있는 함수입니다.
    가장 기본적인 형태는 다음과 같습니다 (단, $c \ne 0$):
    """)
    st.latex(r'y = f(x) = \frac{ax+b}{cx+d}')

    st.subheader('1. 점근선 (Asymptotes) 구하기')
    st.markdown("""
    **점근선**은 그래프가 한없이 가까워지지만 절대 만나지 않는 선을 말합니다.
    """)
    
    st.markdown('**1) 수직 점근선 ($x=p$)**')
    st.info("""
    분모를 **0**으로 만드는 $x$ 값입니다. 함수가 이 지점에서 정의되지 않기 때문에 발생합니다.
    $$cx+d = 0 \implies x = -\frac{d}{c}$$
    """)

    st.markdown('**2) 수평 점근선 ($y=q$)**')
    st.info("""
    $x$의 절댓값이 한없이 커질 때 (무한대로 갈 때) $y$ 값이 수렴하는 값입니다. 분자와 분모의 최고차항 **계수의 비**로 결정됩니다.
    $$y = \frac{a}{c}$$
    """)
    
    st.subheader('2. 정의역 (Domain)과 치역 (Range) 구하기')
    st.markdown("""
    점근선을 기준으로 함수가 정의되는 영역(정의역)과 함수 값이 존재하는 영역(치역)을 결정합니다.
    """)
    
    st.markdown('**1) 정의역 ($D$)**')
    st.info(r"""
    수직 점근선 $x=p$를 제외한 모든 실수입니다.
    $$D = \{x \mid x \ne p \text{인 실수}\}$$
    """)

    st.markdown('**2) 치역 ($R$)**')
    st.info(r"""
    수평 점근선 $y=q$를 제외한 모든 실수입니다.
    $$R = \{y \mid y \ne q \text{인 실수}\}$$
    """)
    
    st.markdown('**❗ 주의: 공역(Codomain)에 대하여**')
    st.warning("""
    **공역**은 함수에서 $y$ 값이 될 수 있는 모든 가능한 값의 집합으로, 보통 문제에서 별도로 주어지며, 치역을 포함하는 더 넓은 개념입니다.
    유리함수 문제에서는 보통 함수가 실제로 가질 수 있는 값의 집합인 **치역**을 구하는 것이 주 목표입니다.
    """)


# --- 2. 문제 생성 및 풀이 함수 ---
def generate_problem():
    # 계수 a, b, c, d를 -5부터 5 사이의 랜덤 정수로 생성
    # 단, c는 0이 아니어야 하고, (ax+b)는 (cx+d)의 배수가 아니어야 한다.
    while True:
        a, b, c, d = random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5)
        if c != 0 and (a * d - b * c) != 0: # 상수 k (비례 상수)가 0이 아닌 경우 (직선 형태 방지)
            break
            
    # 정답 계산
    p = -d / c  # 수직 점근선 x = p
    q = a / c   # 수평 점근선 y = q

    # 문제 함수 수식 문자열 생성
    # 분모가 1이면 cx+d 대신 x+d로 표시
    denominator_str = f'{c}x + {d}' if c != 1 else f'x + {d}'
    if d < 0: denominator_str = denominator_str.replace('+ -', '- ')
    if c < 0 and c != -1: denominator_str = denominator_str.replace('-1x', '-x')
    
    # 분자 문자열 정리
    numerator_str = f'{a}x + {b}'
    if b < 0: numerator_str = numerator_str.replace('+ -', ' - ')
    if a == 1: numerator_str = numerator_str.replace('1x', 'x')
    if a == -1: numerator_str = numerator_str.replace('-1x', '-x')

    problem_func = f'y = \\frac{{{numerator_str}}}{{{denominator_str}}}'
    
    return problem_func, p, q, a, b, c, d

def show_problem_section():
    st.header('📝 문제 풀이 및 그래프 그리기')
    
    if 'problem' not in st.session_state:
        st.session_state.problem_data = generate_problem()
        st.session_state.problem, st.session_state.p, st.session_state.q, st.session_state.a, st.session_state.b, st.session_state.c, st.session_state.d = st.session_state.problem_data
        st.session_state.show_answer = False

    # 새로운 문제 생성 버튼
    if st.button('다른 문제 생성'):
        st.session_state.problem_data = generate_problem()
        st.session_state.problem, st.session_state.p, st.session_state.q, st.session_state.a, st.session_state.b, st.session_state.c, st.session_state.d = st.session_state.problem_data
        st.session_state.show_answer = False
        st.experimental_rerun()
        
    st.subheader(f'문제: 다음 유리함수의 점근선, 정의역, 치역을 구하고 그래프를 그리시오.')
    st.latex(st.session_state.problem)
    
    # 사용자 입력
    with st.form(key='user_answer_form'):
        st.markdown('---')
        st.subheader('당신의 풀이 입력')
        user_va = st.text_input(f'1. 수직 점근선 (형태: x=숫자) 예: x=-3', key='va_input')
        user_ha = st.text_input(f'2. 수평 점근선 (형태: y=숫자) 예: y=2', key='ha_input')
        
        st.markdown('3. 정의역과 치역은 점근선을 기준으로 설명해 보세요.')
        
        submit_button = st.form_submit_button('정답 및 풀이 확인')

    if submit_button:
        st.session_state.show_answer = True
        st.experimental_rerun()
    
    # 정답 및 풀이 영역
    if st.session_state.show_answer:
        st.markdown('---')
        st.subheader('🔑 정답 및 풀이')
        p, q, a, b, c, d = st.session_state.p, st.session_state.q, st.session_state.a, st.session_state.b, st.session_state.c, st.session_state.d

        st.markdown(f'**[계산 과정]**')
        st.markdown(f'유리함수 $y = \\frac{{{a}x + {b}}}{{{c}x + {d}}}$ 에 대하여')
        
        # 1. 수직 점근선
        st.markdown(r'**1) 수직 점근선**')
        st.latex(f'{c}x + {d} = 0 \implies x = \\frac{{-{d}}}{{{c}}} = {p}')
        st.success(f'**정답**: 수직 점근선은 $x = {p}$ 입니다.')

        # 2. 수평 점근선
        st.markdown(r'**2) 수평 점근선**')
        st.latex(f'y = \\frac{{\\text{{분자 최고차항 계수}}}}{{\\text{{분모 최고차항 계수}}}} = \\frac{{{a}}}{{{c}}} = {q}')
        st.success(f'**정답**: 수평 점근선은 $y = {q}$ 입니다.')
        
        # 3. 정의역/치역
        st.markdown(r'**3) 정의역 및 치역**')
        st.info(f'**정의역 (Domain)**: $x \\ne {p}$ 인 모든 실수')
        st.info(f'**치역 (Range)**: $y \\ne {q}$ 인 모든 실수')

        # 4. 그래프 그리기
        plot_rational_function(a, b, c, d, p, q)


# --- 3. 그래프 그리기 함수 (Matplotlib) ---
def plot_rational_function(a, b, c, d, p, q):
    st.subheader('📈 그래프 시각화')

    fig, ax = plt.subplots(figsize=(8, 8))
    
    # x, y 범위 설정
    xlim = 10
    x = np.linspace(-xlim, xlim, 500)
    
    # 함수 정의
    def f(x_val):
        return (a * x_val + b) / (c * x_val + d)

    # 수직 점근선 주변을 피해서 데이터를 두 부분으로 나눔
    x_part1 = x[x < p]
    x_part2 = x[x > p]

    y_part1 = f(x_part1)
    y_part2 = f(x_part2)
    
    # 유리함수 그래프
    ax.plot(x_part1, y_part1, color='blue', label='Rational Function')
    ax.plot(x_part2, y_part2, color='blue')

    # 점근선 표시
    ax.axvline(x=p, color='red', linestyle='--', label=f'Vertical Asymptote $x={p}$')
    ax.axhline(y=q, color='red', linestyle='--', label=f'Horizontal Asymptote $y={q}$')

    # 축 설정
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'$y = \\frac{{{a}x + {b}}}{{{c}x + {d}}}$ Graph')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right')
    
    # y축 범위 자동 조절 (점근선 근처 값 제외)
    y_min = min(np.min(y_part1[~np.isinf(y_part1)]), np.min(y_part2[~np.isinf(y_part2)]))
    y_max = max(np.max(y_part1[~np.isinf(y_part1)]), np.max(y_part2[~np.isinf(y_part2)]))
    
    # 적절한 여백 추가
    y_range = max(abs(y_max - q), abs(q - y_min)) * 1.5
    ax.set_ylim(q - y_range, q + y_range)
    ax.set_xlim(-xlim, xlim)
    
    # Streamlit에 그래프 표시
    st.pyplot(fig)


# --- 4. Streamlit 메인 함수 ---
def main():
    st.set_page_config(layout="wide")
    st.sidebar.title('유리함수 학습 도구')
    
    # 사이드바 메뉴
    menu = st.sidebar.radio('메뉴 선택', ['📚 개념 및 원리', '📝 문제 풀이 및 연습'])
    
    if menu == '📚 개념 및 원리':
        show_theory()
    elif menu == '📝 문제 풀이 및 연습':
        show_problem_section()

if __name__ == '__main__':
    main()
