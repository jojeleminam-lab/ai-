from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="인천광역시 폐기물 재활용률 현황",
    page_icon="♻️",
    layout="wide",
)

st.title("♻️ 인천광역시 군·구별 폐기물 발생 및 재활용 현황 (2023)")
st.markdown(
    "인천광역시 10개 군·구의 폐기물 유형별 발생량, 재활용량 및 재활용률을 비교할 수 있는 대시보드입니다."
)


# 2. 데이터 로드 (pages 폴더의 상위 폴더에서 CSV 탐색)
@st.cache_data
def load_data():
    # 현재 파일(pages/xxx.py)의 부모(pages)의 부모(루트 폴더) 경로 계산
    root_dir = Path(__file__).resolve().parent.parent
    file_path = root_dir / "인천광역시_폐기물 재활용률_20231231.csv"

    # 공공데이터 인코딩(cp949 또는 utf-8) 자동 대응
    for enc in ["cp949", "utf-8", "euc-kr"]:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            break
        except UnicodeDecodeError:
            continue

    # 컬럼 공백 제거 및 재활용률(%) 계산 컬럼 추가
    df.columns = df.columns.str.strip()

    categories = {
        "생활계": ("생활계 폐기물 발생량(톤_년)", "생활계 폐기물 재활용량(톤_년)"),
        "사업장 배출시설계": (
            "사업장 배출시설계 폐기물 발생량(톤_년)",
            "사업장 배출시설계 폐기물_재활용(톤_년)",
        ),
        "건설": ("건설 폐기물 발생량(톤_년)", "건설 폐기물 재활용(톤_년)"),
        "지정": ("지정 폐기물 발생량(톤_년)", "지정 폐기물 재활용(톤_년)"),
    }

    # 총합 계산
    gen_cols = [v[0] for v in categories.values()]
    rec_cols = [v[1] for v in categories.values()]

    df["총 발생량(톤_년)"] = df[gen_cols].sum(axis=1)
    df["총 재활용량(톤_년)"] = df[rec_cols].sum(axis=1)
    df["전체 재활용률(%)"] = (df["총 재활용량(톤_년)"] / df["총 발생량(톤_년)"] * 100).round(2)

    # 유형별 재활용률(%) 계산
    for name, (gen_col, rec_col) in categories.items():
        df[f"{name} 재활용률(%)"] = (df[rec_col] / df[gen_col] * 100).round(2)

    return df, categories


try:
    df, categories = load_data()
except FileNotFoundError:
    st.error("상위 폴더에서 '인천광역시_폐기물 재활용률_20231231.csv' 파일을 찾을 수 없습니다.")
    st.stop()

# 3. 사이드바 필터
st.sidebar.header("🔍 조회 옵션")
selected_regions = st.sidebar.multiselect(
    "군·구 선택",
    options=df["군구별"].tolist(),
    default=df["군구별"].tolist(),
)

waste_type = st.sidebar.selectbox(
    "폐기물 유형 선택",
    options=["전체 합계"] + list(categories.keys()),
)

filtered_df = df[df["군구별"].isin(selected_regions)].copy()

if filtered_df.empty:
    st.warning("최소 1개 이상의 군·구를 선택해 주세요.")
    st.stop()

# 4. 상단 핵심 요약 지표 (KPI)
total_gen = filtered_df["총 발생량(톤_년)"].sum()
total_rec = filtered_df["총 재활용량(톤_년)"].sum()
avg_rate = (total_rec / total_gen * 100) if total_gen > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("선택 지역 총 발생량", f"{total_gen:,.1f} 톤/년")
col2.metric("선택 지역 총 재활용량", f"{total_rec:,.1f} 톤/년")
col3.metric("평균 재활용률", f"{avg_rate:.2f} %")

st.divider()

# 5. 인터랙티브 Plotly 시각화
tab1, tab2, tab3 = st.tabs(["📊 발생량 vs 재활용량", "📈 유형별 재활용률 비교", "📋 원본 및 요약 데이터"])

with tab1:
    st.subheader(f"군·구별 {waste_type} 발생량 및 재활용량 비교")

    if waste_type == "전체 합계":
        gen_col, rec_col = "총 발생량(톤_년)", "총 재활용량(톤_년)"
    else:
        gen_col, rec_col = categories[waste_type]

    plot_df = filtered_df.sort_values(by=gen_col, ascending=False)

    fig1 = go.Figure()
    fig1.add_trace(
        go.Bar(
            x=plot_df["군구별"],
            y=plot_df[gen_col],
            name="발생량 (톤/년)",
            marker_color="#636EFA",
            hovertemplate="<b>%{x}</b><br>발생량: %{y:,.1f} 톤<extra></extra>",
        )
    )
    fig1.add_trace(
        go.Bar(
            x=plot_df["군구별"],
            y=plot_df[rec_col],
            name="재활용량 (톤/년)",
            marker_color="#00CC96",
            hovertemplate="<b>%{x}</b><br>재활용량: %{y:,.1f} 톤<extra></extra>",
        )
    )

    fig1.update_layout(
        barmode="group",
        xaxis_title="군·구",
        yaxis_title="물량 (톤/년)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        template="plotly_white",
        height=480,
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("폐기물 유형별 재활용률(%) 비교")

    rate_cols = [f"{name} 재활용률(%)" for name in categories.keys()]
    melted_df = filtered_df.melt(
        id_vars=["군구별"],
        value_vars=rate_cols,
        var_name="폐기물 유형",
        value_name="재활용률(%)",
    )
    melted_df["폐기물 유형"] = melted_df["폐기물 유형"].str.replace(" 재활용률(%)", "", regex=False)

    fig2 = px.bar(
        melted_df,
        x="군구별",
        y="재활용률(%)",
        color="폐기물 유형",
        barmode="group",
        text_auto=".1f",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig2.update_traces(textposition="outside", hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:.2f}%<extra></extra>")
    fig2.update_layout(
        yaxis=dict(range=[0, 115], title="재활용률 (%)"),
        xaxis_title="군·구",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        height=500,
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("군·구별 상세 데이터 및 계산된 재활용률")
    st.dataframe(
        filtered_df.style.format(
            {col: "{:,.1f}" for col in filtered_df.select_dtypes(include="float").columns}
        ),
        use_container_width=True,
    )

