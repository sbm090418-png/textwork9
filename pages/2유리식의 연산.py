Python
import streamlit as st
from sympy import symbols, parse_expr, together, simplify, denom, Poly, solve

# --- 설정 및 변수 정의 ---
# 'x'를 SymPy의 기호 변수로 정의
x = symbols('x')

# --- Streamlit UI 구성 ---
st.set_page_config(layout="wide", page_title="유리식 연산 특징 학습 앱")
st.title("유리식 연산 특징 학습 앱 💡")
st.subheader("SymPy를 활용한 유리식(분수식) 계산기")

st.markdown("""
이 앱은 두 개의 유리식을 입력받아 연산을 수행하고, 
유리식 연산의 **핵심 특징 (통분, 약분, 제약 조건)**을 학습할 수 있도록 돕습니다.
""")

# --- 입력 섹션 ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 첫 번째 유리식 $A$")
    eq1_str = st.text_input("분수식 $A$를 입력하세요 (예: 1/(x-1))", "1/(x-1)")

with col2:
    st.markdown("#### 두 번째 유리식 $B$")
    eq2_str = st.text_input("분수식 $B$를 입력하세요 (예: 1/(x+1))", "1/(x+1)")

operation = st.selectbox(
    "수행할 연산을 선택하세요.",
    ('덧셈 (+)', '뺄셈 (-)', '곱셈 (×)', '나눗셈 (÷)')
)

st.markdown("---")

# --- 연산 및 학습 로직 ---
if st.button('연산 실행 및 특징 학습'):
    try:
        # 1. 수식 파싱: 입력 문자열을 SymPy 수식 객체로 변환
        A = parse_expr(eq1_str, evaluate=False, local_dict={'x': x})
        B = parse_expr(eq2_str, evaluate=False, local_dict={'x': x})

        st.subheader(f"입력된 식: $A = {st.latex(A)}$ 및 $B = {st.latex(B)}$")

        # 2. 연산 수행 및 결과 처리
        if operation == '덧셈 (+)':
            expr = A + B
            result = together(expr)  # together는 통분을 수행
        elif operation == '뺄셈 (-)':
            expr = A - B
            result = together(expr)
        elif operation == '곱셈 (×)':
            expr = A * B
            result = simplify(expr)
        elif operation == '나눗셈 (÷)':
            expr = A / B
            result = simplify(expr)
            
        st.markdown("---")
        st.header(f"결과: $A$ {operation.split(' ')[0]} $B$")
        st.subheader("최종 결과 (간소화):")
        st.latex(f'{result}')
        
        st.markdown("---")
        
        # 3. 유리식 연산 특징 학습 내용
        st.header("✨ 연산별 학습 특징 분석")
        
        # 3-1. 덧셈/뺄셈의 특징: 통분
        if operation in ('덧셈 (+)', '뺄셈 (-)'):
            st.markdown("#### 특징 1: 덧셈과 뺄셈의 핵심은 **통분**")
            st.write(
                f"덧셈/뺄셈을 수행하려면 분모를 **최소공배수로 통분**해야 합니다. "
                f"통분 전의 식: $A {operation.split(' ')[0]} B = {st.latex(expr)}$"
            )
            
        # 3-2. 곱셈/나눗셈의 특징: 약분
        elif operation in ('곱셈 (×)', '나눗셈 (÷)'):
            st.markdown("#### 특징 1: 곱셈과 나눗셈의 핵심은 **약분**")
            
            if operation == '나눗셈 (÷)' and B != 0:
                st.write(
                    "나눗셈은 역수를 취한 후 곱셈으로 바꾸어 연산합니다. $A \div B = A \times \\frac{1}{B}$."
                    "이후 **인수분해**하여 공통 인수를 제거하는 **약분** 과정을 통해 간소화합니다."
                )
            else: # 곱셈
                st.write(
                    "곱셈은 분자끼리, 분모끼리 곱한 후, **인수분해**하여 공통 인수를 제거하는 **약분** 과정을 통해 간소화합니다."
                )
        
        # 3-3. 공통 특징: 제약 조건 (분모가 0이 되는 값)
        st.markdown("#### 특징 2: 유리식의 **정의되지 않는 값 (제약 조건)**")
        
        # 분모 추출 및 0이 되는 지점 찾기
        den_A = Poly(denom(A), x)
        den_B = Poly(denom(B), x)
        
        zeros_A = solve(den_A, x)
        zeros_B = solve(den_B, x)
        
        # 나눗셈($A \div B$)은 나누는 식 B의 분모와 분자 모두 0이 되면 안 됩니다.
        if operation == '나눗셈 (÷)':
            num_B = Poly(B.as_numer_denom()[0], x)
            zeros_B_num = solve(num_B, x)
            all_zeros = set(zeros_A) | set(zeros_B) | set(zeros_B_num)
        else:
            all_zeros = set(zeros_A) | set(zeros_B) 
        
        # 최종 결과의 분모가 0이 되는 지점도 포함
        den_result = Poly(denom(result), x)
        all_zeros = all_zeros | set(solve(den_result, x))

        
        st.error(
            f"유리식은 **분모가 0이 되는 값**에서는 정의되지 않습니다. "
            f"따라서 $x$는 $\\text{{ {', '.join(map(str, sorted(all_zeros)))}}}$ 일 때 정의되지 않습니다."
        )
        if not all_zeros:
             st.success("해당 범위 내에서 분모를 0으로 만드는 실수 $x$ 값은 없습니다.")


    except Exception as e:
        st.error(f"수식 파싱 또는 연산 오류가 발생했습니다. 입력을 다시 확인해주세요: {e}")
