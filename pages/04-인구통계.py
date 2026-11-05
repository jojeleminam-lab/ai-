
import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# -----------------------------------
# 1. 기본 페이지 설정
# -----------------------------------

st.set_page_config(
    page_title="남양주시 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

PINK = "#FF1493"

AGE_GROUPS = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]


# -----------------------------------
# 2. CSV 파일 경로 설정
# -----------------------------------

# 현재 파일은 pages 폴더 안에 있으므로
# parent.parent를 사용하면 프로젝트 상위 폴더로 이동합니다.

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "population.csv"


# -----------------------------------
# 3. 한글 인코딩 자동 처리
# -----------------------------------

def read_csv_safely(source):

    encodings = [
        "cp949",
        "euc-kr",
        "utf-8-sig",
        "utf-8"
    ]

    last_error = None

    for encoding in encodings:

        try:
            if hasattr(source, "seek"):
                source.seek(0)

            return pd.read_csv(
                source,
                encoding=encoding,
                thousands=","
            )

        except UnicodeDecodeError as error:
            last_error = error

    raise last_error


# -----------------------------------
# 4. 데이터 불러오기
# -----------------------------------

@st.cache_data
def load_data(file_path, file_mtime):

    return read_csv_safely(file_path)


st.title("📊 남양주시 연령별 인구 분석")
st.caption("행정구역, 성별, 연도에 따른 연령별 인구 데이터를 확인할 수 있습니다.")

if not CSV_PATH.exists():

    st.error(
        "population.csv 파일을 찾을 수 없습니다.\n\n"
        "CSV 파일이 파이썬 파일의 상위 폴더에 있는지 확인해주세요."
    )

    uploaded_file = st.file_uploader(
        "CSV 파일을 직접 업로드할 수도 있습니다.",
        type=["csv"]
    )

    if uploaded_file is None:
        st.stop()

    try:
        df = read_csv_safely(uploaded_file)

    except Exception as error:
        st.error(f"CSV 파일을 읽을 수 없습니다: {error}")
        st.stop()

else:

    try:
        df = load_data(
            str(CSV_PATH),
            CSV_PATH.stat().st_mtime
        )

    except Exception as error:
        st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {error}")
        st.stop()


# -----------------------------------
# 5. 데이터 확인 및 정리
# -----------------------------------

if "행정구역" not in df.columns:
    st.error("'행정구역' 열을 찾을 수 없습니다. CSV 파일을 확인해주세요.")
    st.stop()


# 행정구역 뒤에 붙은 행정구역 코드 제거
def clean_region(value):

    value = str(value).strip()

    value = re.sub(
        r"\s*\(\d+\)\s*$",
        "",
        value
    )

    return value


df["행정구역_표시"] = df["행정구역"].apply(clean_region)


# 연도 자동 추출
years = sorted(
    {
        int(match.group(1))
        for column in df.columns
        if (match := re.search(r"(\d{4})년_", str(column)))
    }
)

if not years:
    st.error("CSV 파일에서 연도 데이터를 찾을 수 없습니다.")
    st.stop()


# -----------------------------------
# 6. 선택 메뉴
# -----------------------------------

st.subheader("🔎 분석 조건 선택")

col1, col2, col3 = st.columns(3)

with col1:

    districts = df["행정구역_표시"].tolist()

    selected_district = st.selectbox(
        "🏙️ 행정구역 선택",
        districts
    )

with col2:

    selected_gender = st.selectbox(
        "👥 성별 선택",
        ["전체", "남성", "여성"]
    )

with col3:

    selected_year = st.selectbox(
        "📅 연도 선택",
        years,
        index=len(years) - 1,
        format_func=lambda year: f"{year}년"
    )


# -----------------------------------
# 7. 성별에 따른 열 이름 설정
# -----------------------------------

gender_prefix = {
    "전체": "거주자",
    "남성": "남_거주자",
    "여성": "여_거주자"
}

prefix = gender_prefix[selected_gender]


# -----------------------------------
# 8. 연령대별 데이터 추출
# -----------------------------------

selected_row = df[
    df["행정구역_표시"] == selected_district
]

if selected_row.empty:
    st.error("선택한 행정구역의 데이터를 찾을 수 없습니다.")
    st.stop()

selected_row = selected_row.iloc[0]

population_data = []

for age in AGE_GROUPS:

    column_name = f"{selected_year}년_{prefix}_{age}"

    if column_name not in df.columns:

        st.error(
            f"CSV에서 다음 열을 찾을 수 없습니다: {column_name}"
        )

        st.stop()

    value = pd.to_numeric(
        selected_row[column_name],
        errors="coerce"
    )

    population_data.append(
        0 if pd.isna(value) else int(value)
    )


chart_df = pd.DataFrame({
    "연령대": AGE_GROUPS,
    "인구수": population_data
})


# -----------------------------------
# 9. 주요 통계
# -----------------------------------

total_population = chart_df["인구수"].sum()

max_age = chart_df.loc[
    chart_df["인구수"].idxmax(),
    "연령대"
]

max_population = chart_df["인구수"].max()

st.divider()

st.subheader("📌 주요 인구 통계")

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "총 연령별 인구",
    f"{total_population:,}명"
)

metric2.metric(
    "인구가 가장 많은 연령대",
    max_age
)

metric3.metric(
    "해당 연령대 인구",
    f"{max_population:,}명"
)


# -----------------------------------
# 10. 그래프 생성
# -----------------------------------

st.divider()

st.subheader("📈 연령대별 인구 그래프")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_df["연령대"],
        y=chart_df["인구수"],

        mode="lines+markers",

        name="인구수",

        line=dict(
            color=PINK,
            width=4
        ),

        marker=dict(
            color=PINK,
            size=9
        ),

        hovertemplate=
        "%{x}<br>인구수: %{y:,.0f}명<extra></extra>"
    )
)


# -----------------------------------
# 11. 그래프 디자인
# -----------------------------------

# Y축 눈금 간격 100,000명
max_value = int(chart_df["인구수"].max())

y_max = max(
    100000,
    ((max_value // 100000) + 1) * 100000
)

fig.update_layout(

    title=dict(
        text=f"{selected_district} {selected_year}년 {selected_gender} 연령별 인구",
        x=0.5,
        xanchor="center"
    ),

    xaxis=dict(

        title="연령대",

        type="category",

        categoryorder="array",

        categoryarray=AGE_GROUPS,

        showgrid=True,

        gridcolor="#F3DCE8",

        tickangle=0
    ),

    yaxis=dict(

        title="인구수 (명)",

        showgrid=True,

        gridcolor="#E5E5E5",

        dtick=100000,

        tick0=0,

        tickformat=",

        range=[0, y_max]
    ),

    plot_bgcolor="white",

    paper_bgcolor="white",

    font=dict(
        family="Noto Sans KR, Malgun Gothic, AppleGothic, sans-serif",
        size=13
    ),

    hovermode="x unified",

    height=550,

    margin=dict(
        l=40,
        r=30,
        t=80,
        b=50
    ),

    showlegend=False
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------------
# 12. 데이터 표 출력
# -----------------------------------

st.divider()

st.subheader("📋 연령대별 인구 데이터")

display_df = chart_df.copy()

display_df["인구수"] = display_df["인구수"].map(
    lambda value: f"{value:,}명"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------------
# 13. 데이터 안내
# -----------------------------------

st.divider()

st.caption(
    f"📍 행정구역: {selected_district} | "
    f"성별: {selected_gender} | "
    f"연도: {selected_year}년"
)

st.caption(
    "※ 원본 CSV 데이터를 바탕으로 연령대별 인구를 시각화한 자료입니다."
)
