import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="주사위 굴리기 앱", layout="wide")

st.title("주사위 굴리기 🎲")
st.markdown("간단한 주사위를 굴려서 결과와 분포, 히스토리를 확인해보세요.")

# --- 사이드바: 설정
with st.sidebar:
    st.header("설정")
    num_dice = st.number_input("굴릴 주사위 개수", min_value=1, max_value=10, value=1, step=1)
    sides = st.selectbox("주사위 면수", options=[4,6,8,10,12,20], index=1)
    keep_history = st.checkbox("히스토리 저장", value=True)
    st.write("---")
    st.markdown("앱 버전: 1.0  \n사용법: 주사위 개수와 면수를 선택 후 '굴리기'를 눌러 결과를 확인하세요.")


# 초기화: 세션 상태에 히스토리 저장
if "dice_history" not in st.session_state:
    st.session_state.dice_history = []  # 각 항목은 dict: {ts, n, sides, results}


def roll_dice(n: int, sides: int):
    """n개의 주사위를 굴려 결과 리스트 반환"""
    return [random.randint(1, sides) for _ in range(n)]


col1, col2 = st.columns([2, 1])

with col1:
    if st.button("굴리기 🎲"):
        results = roll_dice(num_dice, sides)
        total = sum(results)
        avg = total / len(results)
        ts = datetime.now().isoformat(sep=' ', timespec='seconds')

        # 저장 (선택 시)
        entry = {"timestamp": ts, "num_dice": num_dice, "sides": sides, "results": results, "total": total, "avg": avg}
        if keep_history:
            st.session_state.dice_history.insert(0, entry)  # 최신순

        # 결과 출력
        st.subheader("이번 굴림 결과")
        st.write(f"시간: {ts}")
        st.write(f"개별 결과: {results}")
        st.metric("합계", total)
        st.write(f"평균: {avg:.2f}")

        # 분포(간단한 막대)
        counts = pd.Series(results).value_counts().sort_index()
        df_counts = counts.rename_axis('value').reset_index(name='count')
        st.bar_chart(df_counts.set_index('value'))

with col2:
    st.subheader("빠른 정보")
    st.write(f"주사위: {num_dice}개 × {sides}면")
    st.write("히스토리 저장:" , "예" if keep_history else "아니오")
    if st.button("히스토리 비우기"):
        st.session_state.dice_history = []
        st.success("히스토리가 비워졌습니다.")


st.markdown("---")

# 히스토리 표시 및 다운로드
st.subheader("굴림 히스토리")
if len(st.session_state.dice_history) == 0:
    st.info("아직 저장된 굴림이 없습니다. '히스토리 저장'을 체크한 상태에서 굴려보세요.")
else:
    # 화면에 표로 보여주기
    hist_df = pd.DataFrame([
        {"timestamp": e["timestamp"], "num_dice": e["num_dice"], "sides": e["sides"], "results": str(e["results"]), "total": e["total"], "avg": e["avg"]}
        for e in st.session_state.dice_history
    ])
    st.dataframe(hist_df, use_container_width=True)

    # 다운로드 (CSV)
    csv = hist_df.to_csv(index=False).encode('utf-8')
    st.download_button("히스토리 다운로드 (CSV)", data=csv, file_name="dice_history.csv", mime="text/csv")


# 각주
st.markdown("---")
st.markdown("### 각주")
st.markdown("""
[A] 주사위 굴림은 `random.randint(1, sides)`를 사용합니다.  
[B] 히스토리는 세션 상태(`st.session_state.dice_history`)에 저장되며, 브라우저 세션이 끝나면 사라집니다.  
[C] 더 고급 기능(시뮬레이션 반복, 통계 테스트 등)이 필요하면 알려주세요.
""")

