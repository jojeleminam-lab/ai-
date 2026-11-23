from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="Iris 데이터 시각화 대시보드", page_icon="🌸", layout="wide"
)


# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    # 현재 파일(pages/iris_dashboard.py)의 상위 폴더(루트)에 있는 Iris.csv 경로 지정
    current_dir = Path(__file__).resolve().parent
    csv_path = current_dir.parent / "Iris.csv"

    # 한글 인코딩(cp949 / utf-8) 자동 대응
    try:
        df = pd.read_csv(csv_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="utf-8")

    # 컬럼명 앞뒤 공백 제거 (예: '꽃받침 길이 ' -> '꽃받침 길이')
    df.columns = df.columns.str.strip()
    return df


df = load_data()

# 타이틀 및 설명
st.title("🌸 Iris(붓꽃) 품종별 데이터 분석 대시보드")
st.markdown(
    "사이드바에서 품종과 축을 선택해 **인터랙티브 그래프**를 탐색해보세요."
)

# --- 사이드바 필터 ---
st.sidebar.header("🔍 그래프 설정")

# 품종 필터링
species_list = df["품종"].unique().tolist()
selected_species = st.sidebar.multiselect(
    "표시할 품종 선택", options=species_list, default=species_list
)

# 수치형 컬럼 목록
numeric_cols = [col for col in df.columns if col != "품종"]

x_axis = st.sidebar.selectbox("X축 변수 선택", options=numeric_cols, index=2)
y_axis = st.sidebar.selectbox("Y축 변수 선택", options=numeric_cols, index=3)

# 필터링된 데이터프레임
filtered_df = df[df["품종"].isin(selected_species)]

if filtered_df.empty:
    st.warning("최소 한 개 이상의 품종을 선택해주세요.")
    st.stop()

# 상단 요약 지표 (KPI)
col1, col2, col3, col4 = st.columns(4)
col1.metric("선택된 데이터 수", f"{len(filtered_df)} 개")
col2.metric(f"평균 {x_axis}", f"{filtered_df[x_axis].mean():.2f} cm")
col3.metric(f"평균 {y_axis}", f"{filtered_df[y_axis].mean():.2f} cm")
col4.metric("선택된 품종 수", f"{len(selected_species)} 종")

st.divider()

# --- 메인 그래프 영역 (2단 구성) ---
left_col, right_col = st.columns(2)

with left_col:
    st.subheader(f"📊 {x_axis} vs {y_axis} 산점도")
    fig_scatter = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        color="품종",
        size="꽃잎길이",
        hover_data=numeric_cols,
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_scatter.update_layout(
        legend_title_text="품종", margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with right_col:
    st.subheader(f"📦 품종별 {y_axis} 분포 (Box & Strip)")
    fig_box = px.box(
        filtered_df,
        x="품종",
        y=y_axis,
        color="품종",
        points="all",  # 개별 데이터 포인트 함께 표시
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_box.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_box, use_container_width=True)

# --- 하단 3D 산점도 및 원본 데이터 ---
st.subheader("🧊 3D 다변량 분포 탐색")
fig_3d = px.scatter_3d(
    filtered_df,
    x="꽃받침 길이",
    y="꽃받침 너비",
    z="꽃잎길이",
    color="품종",
    size="꽃잎 너비",
    opacity=0.8,
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig_3d.update_layout(height=550, margin=dict(l=0, r=0, t=20, b=0))
st.plotly_chart(fig_3d, use_container_width=True)

with st.expander("📋 필터링된 원본 데이터 보기"):
    st.dataframe(filtered_df, use_container_width=True)
