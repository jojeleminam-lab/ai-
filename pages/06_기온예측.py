import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path

st.set_page_config(
    page_title="월별 평균기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 평균기온 분석 및 예측")
st.write(
    "원하는 월과 예측 연도를 선택하면, temperature.csv의 데이터를 바탕으로 "
    "해당 월의 연도별 평균기온을 계산하고 선형회귀로 미래 기온을 예측합니다."
)

# -------------------------------------------------
# 1. 데이터 불러오기
# -------------------------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "temperature.csv"

    # CSV 인코딩 자동 대응
    encodings = ["utf-8", "utf-8-sig", "cp949", "latin1"]
    last_error = None

    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            break
        except UnicodeDecodeError as error:
            last_error = error
    else:
        raise last_error

    required_columns = ["month", "year", "AverageTemperatureFahr"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            "CSV에 필요한 열이 없습니다: " + ", ".join(missing)
            + "\n필요한 열: month, year, AverageTemperatureFahr"
        )

    for col in required_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=required_columns)
    df["month"] = df["month"].astype(int)
    df["year"] = df["year"].astype(int)

    # 화씨(°F)를 섭씨(°C)로 변환
    df["temperature_c"] = (df["AverageTemperatureFahr"] - 32) * 5 / 9

    return df

try:
    data = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 문제가 발생했습니다: {e}")
    st.stop()

# -------------------------------------------------
# 2. 사용자 입력
# -------------------------------------------------
st.subheader("🔎 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "분석할 월을 선택하세요",
        options=list(range(1, 13)),
        format_func=lambda x: f"{x}월",
        index=0
    )

# 선택한 월의 연도별 평균기온 계산
monthly_data = data[data["month"] == selected_month].copy()

yearly = (
    monthly_data.groupby("year")
    .agg(
        average_temperature=("temperature_c", "mean"),
        data_count=("temperature_c", "count")
    )
    .reset_index()
    .sort_values("year")
)

if len(yearly) < 2:
    st.error("선택한 월의 데이터가 2개 연도 미만이라 선형회귀를 학습할 수 없습니다.")
    st.stop()

last_year = int(yearly["year"].max())
first_year = int(yearly["year"].min())

with col2:
    prediction_year = st.number_input(
        "예측할 연도를 입력하세요",
        min_value=last_year + 1,
        max_value=2200,
        value=min(last_year + 10, 2200),
        step=1
    )

# -------------------------------------------------
# 3. 선형회귀 모델 학습 및 예측
# -------------------------------------------------
X = yearly[["year"]].values
y = yearly["average_temperature"].values

model = LinearRegression()
model.fit(X, y)

predicted_temperature = float(
    model.predict(np.array([[prediction_year]]))[0]
)

# 회귀선의 좌표
line_years = np.arange(first_year, int(prediction_year) + 1)
line_predictions = model.predict(line_years.reshape(-1, 1))

# 각 실제 관측값에서 회귀선까지의 잔차 표시
fitted_values = model.predict(X)

# -------------------------------------------------
# 4. 예측 결과
# -------------------------------------------------
st.subheader(f"📊 {selected_month}월 평균기온 분석 결과")

metric1, metric2, metric3 = st.columns(3)
metric1.metric("예측 연도", f"{prediction_year}년")
metric2.metric("예측 평균기온", f"{predicted_temperature:.2f} °C")
metric3.metric("학습 데이터 기간", f"{first_year}년 ~ {last_year}년")

st.caption(
    f"{selected_month}월에 해당하는 모든 지역의 관측값을 연도별로 평균 내어 분석했습니다. "
    f"총 {len(yearly):,}개 연도의 평균값으로 모델을 학습했습니다."
)

# -------------------------------------------------
# 5. 그래프: 실제값 + 회귀선 + 예측값 + 잔차
# -------------------------------------------------
fig = go.Figure()

# 실제 관측 평균기온
fig.add_trace(go.Scatter(
    x=yearly["year"],
    y=yearly["average_temperature"],
    mode="markers",
    name="실제 연도별 평균기온",
    marker=dict(size=7),
    hovertemplate="%{x}년 실제 평균: %{y:.2f} °C<extra></extra>"
))

# 회귀선
fig.add_trace(go.Scatter(
    x=line_years,
    y=line_predictions,
    mode="lines",
    name="선형회귀 예측선",
    line=dict(width=3, dash="dash"),
    hovertemplate="%{x}년 회귀선 값: %{y:.2f} °C<extra></extra>"
))

# 잔차(실제값과 회귀선이 얼마나 차이 나는지) 표시
for year, actual, fitted in zip(yearly["year"], y, fitted_values):
    fig.add_trace(go.Scatter(
        x=[year, year],
        y=[actual, fitted],
        mode="lines",
        line=dict(width=1, dash="dot", color="rgba(130,130,130,0.35)"),
        showlegend=False,
        hoverinfo="skip"
    ))

# 예측 연도 위치를 표시하는 세로선
fig.add_vline(
    x=int(prediction_year),
    line_width=2,
    line_dash="dot",
    annotation_text=f"{prediction_year}년 예측",
    annotation_position="top right"
)

# 미래 예측 지점
fig.add_trace(go.Scatter(
    x=[prediction_year],
    y=[predicted_temperature],
    mode="markers+text",
    name="선택 연도 예측값",
    marker=dict(size=15, symbol="star"),
    text=[f"{predicted_temperature:.2f} °C"],
    textposition="top center",
    hovertemplate="%{x}년 예측 평균: %{y:.2f} °C<extra></extra>"
))

fig.update_layout(
    title=f"{selected_month}월 연도별 평균기온과 선형회귀 예측",
    xaxis_title="연도",
    yaxis_title="평균기온 (°C)",
    hovermode="x unified",
    legend_title="그래프 범례",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 6. 선형회귀 알고리즘 설명
# -------------------------------------------------
st.subheader("🧠 선형회귀 알고리즘은 어떻게 작동할까?")

st.markdown(
    """
    **선형회귀(Linear Regression)**는 과거 데이터의 분포를 가장 잘 설명하는
    직선을 찾아, 그 직선을 바탕으로 새로운 값을 예측하는 알고리즘입니다.

    1. **데이터 수집:** 선택한 월의 모든 지역별 기온 데이터를 모읍니다.
    2. **연도별 평균 계산:** 같은 연도에 측정된 기온을 평균 내어 연도별 대표 기온을 만듭니다.
    3. **직선 찾기:** 연도를 x축, 평균기온을 y축으로 놓고 실제 점들과 직선 사이의
       세로 거리(오차)가 전반적으로 가장 작아지도록 직선을 계산합니다.
    4. **미래 예측:** 사용자가 입력한 연도를 직선에 대입해 예측 기온을 구합니다.

    그래프에서 **점은 실제 관측 평균**, **점선은 선형회귀가 찾은 직선**,
    **별표는 사용자가 선택한 연도의 예측값**입니다.
    회색 점선은 실제 관측값과 회귀선 사이의 차이(잔차)를 보여줍니다.
    """
)

st.latex(r"\hat{y} = b_0 + b_1x")

st.markdown(
    """
    - `x`: 연도
    - `ŷ`: 해당 연도의 예측 평균기온
    - `b₀`: 직선의 시작 위치를 결정하는 절편
    - `b₁`: 연도가 1년 증가할 때 기온이 얼마나 변하는지 나타내는 기울기

    **주의:** 이 모델은 과거의 장기적인 직선 추세가 미래에도 이어진다고 가정합니다.
    계절별 기온 변화, 온실가스, 지역별 기후 차이 등 모든 요인을 반영하지 않으므로
    실제 미래 기온과 다를 수 있습니다. 특히 학습 기간보다 아주 먼 미래의 예측은
    참고용으로 해석해야 합니다.
    """
)

st.divider()
st.caption(
    "데이터 출처: temperature.csv | 분석 단위: 선택한 월의 전체 지역 연도별 평균 | "
    "원본 화씨 데이터를 섭씨로 변환하여 표시"
)
