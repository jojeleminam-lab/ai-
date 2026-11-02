import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="세계 MBTI 분석기",
    page_icon="🌍",
    layout="wide"
)

# CSV 데이터 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# MBTI 유형 추출
mbti_types = df.columns[1:].tolist()

st.title("🌍 세계 MBTI 분석기")

st.write("158개 국가의 MBTI 분포를 분석해 보세요!")

# 국가 선택
country = st.selectbox(
    "국가를 선택하세요.",
    df["Country"].tolist()
)

# 선택한 국가 데이터
selected = df[df["Country"] == country].iloc[0]

# MBTI 분포
result = pd.DataFrame({
    "MBTI": mbti_types,
    "비율(%)": [selected[t] * 100 for t in mbti_types]
})

result = result.sort_values(
    "비율(%)",
    ascending=False
)

st.subheader(f"📊 {country}의 MBTI 분포")

st.bar_chart(
    result.set_index("MBTI")
)

st.dataframe(
    result,
    use_container_width=True,
    hide_index=True
)

# 가장 높은 MBTI
st.success(
    f"가장 높은 유형은 {result.iloc[0]['MBTI']}입니다!"
)
