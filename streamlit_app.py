import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="도형탐험대", layout="wide")

st.title("도형탐험대 �")
st.markdown("사용자가 도형을 선택하고 크기를 조절해 넓이와 둘레를 확인하고, matplotlib으로 시각화해봅니다.")

shape = st.selectbox("도형 선택", ["삼각형", "사각형", "원"]) 

col1, col2 = st.columns([2, 1])

area = None
perimeter = None

if shape == "삼각형":
    st.subheader("삼각형 설정")
    a = st.slider("변 a (BC)", min_value=0.5, max_value=20.0, value=3.0, step=0.1)
    b = st.slider("변 b (CA)", min_value=0.5, max_value=20.0, value=4.0, step=0.1)
    c = st.slider("변 c (AB)", min_value=0.5, max_value=20.0, value=5.0, step=0.1)

    # 유효성 검사: 삼각형 부등식
    valid = (a + b > c) and (b + c > a) and (c + a > b)
    if not valid:
        st.warning("선택한 길이로는 삼각형을 만들 수 없습니다. 세 값을 조정하세요.")
    else:
        s = 0.5 * (a + b + c)
        area = math.sqrt(max(0.0, s * (s - a) * (s - b) * (s - c)))
        perimeter = a + b + c

        # 좌표 계산: A=(0,0), B=(c,0), C=(x,y)
        c_len = c
        x = (b * b + c_len * c_len - a * a) / (2 * c_len)
        y_sq = max(0.0, b * b - x * x)
        y = math.sqrt(y_sq)
        pts = np.array([[0.0, 0.0], [c_len, 0.0], [x, y], [0.0, 0.0]])

        fig, ax = plt.subplots(figsize=(5,5))
        ax.plot(pts[:,0], pts[:,1], '-o')
        ax.set_aspect('equal', 'box')
        pad = max(a,b,c) * 0.2
        xmin, xmax = pts[:,0].min() - pad, pts[:,0].max() + pad
        ymin, ymax = pts[:,1].min() - pad, pts[:,1].max() + pad
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_title(f"삼각형: a={a:.2f}, b={b:.2f}, c={c:.2f}")
        st.pyplot(fig)

elif shape == "사각형":
    st.subheader("사각형 설정")
    w = st.slider("가로 (width)", min_value=0.5, max_value=30.0, value=6.0, step=0.1)
    h = st.slider("세로 (height)", min_value=0.5, max_value=30.0, value=4.0, step=0.1)

    area = w * h
    perimeter = 2 * (w + h)

    # 사각형 좌표 (원점 중심 정렬)
    pts = np.array([[0,0],[w,0],[w,h],[0,h],[0,0]])
    fig, ax = plt.subplots(figsize=(5,5))
    ax.plot(pts[:,0], pts[:,1], '-o')
    ax.set_aspect('equal', 'box')
    pad = max(w,h) * 0.2
    ax.set_xlim(-pad, w + pad)
    ax.set_ylim(-pad, h + pad)
    ax.set_title(f"사각형: width={w:.2f}, height={h:.2f}")
    st.pyplot(fig)

else:  # 원
    st.subheader("원 설정")
    r = st.slider("반지름 (radius)", min_value=0.1, max_value=15.0, value=3.0, step=0.1)
    area = math.pi * r * r
    perimeter = 2 * math.pi * r

    fig, ax = plt.subplots(figsize=(5,5))
    circle = plt.Circle((0,0), r, fill=False, linewidth=2)
    ax.add_patch(circle)
    ax.set_aspect('equal', 'box')
    pad = r * 0.3
    ax.set_xlim(-r - pad, r + pad)
    ax.set_ylim(-r - pad, r + pad)
    ax.set_title(f"원: radius={r:.2f}")
    st.pyplot(fig)

# 우측에 결과 출력
with col2:
    st.subheader("계산 결과")
    if area is None or perimeter is None:
        st.write("유효하지 않은 도형입니다.")
    else:
        st.metric("넓이 (area)", f"{area:.3f}")
        st.metric("둘레 (perimeter)", f"{perimeter:.3f}")
        # 간단한 요약
        st.markdown(f"**요약**: 넓이 = {area:.3f}, 둘레 = {perimeter:.3f}")

st.markdown("---")
st.markdown("도움: 삼각형의 경우 슬라이더로 변 길이를 조정해 삼각형 부등식이 성립하는지 확인하세요.")

