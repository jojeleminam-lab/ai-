
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# 페이지 설정
st.set_page_config(page_title="Iris 품종 예측 앱", page_icon="🌸", layout="centered")

st.title("🌸 붓꽃(Iris) 품종 예측 서비스")
st.write("꽃잎의 길이와 너비를 입력하면, **랜덤 포레스트(Random Forest)** 알고리즘을 통해 붓꽃의 품종을 예측하고 시각화해 줍니다.")

# 데이터 불러오기 및 모델 학습 함수
@st.cache_data
def load_data_and_model():
    # 한글 인코딩(cp949)을 고려하여 데이터 읽기
    df = pd.read_csv('Iris.csv', encoding='cp949')
    
    # 특성(X)과 타겟(y) 설정 (꽃잎 길이, 꽃잎 너비 사용)
    X = df[['꽃잎 길이', '꽃잎 너비']]
    y = df['품종']
    
    # 가장 많이 사용되는 분류 알고리즘 중 하나인 RandomForest 적용
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    
    return df, model

# 데이터 및 모델 로드
try:
    df, model = load_data_and_model()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 2. 입력 범위 안내
st.subheader("📊 입력 범위 안내")
min_len, max_len = float(df['꽃잎 길이'].min()), float(df['꽃잎 길이'].max())
min_wid, max_wid = float(df['꽃잎 너비'].min()), float(df['꽃잎 너비'].max())

st.markdown(f"""
* **꽃잎 길이 (Petal Length):** 최소 `{min_len}` ~ 최대 `{max_len}`
* **꽃잎 너비 (Petal Width):** 최소 `{min_wid}` ~ 최대 `{max_wid}`
""")

# 사용자 입력 받기 (슬라이더 활용)
st.subheader("🔍 붓꽃 정보 입력")
petal_length = st.slider("꽃잎 길이를 선택하세요", min_value=min_len, max_value=max_len, value=float(df['꽃잎 길이'].mean()), step=0.1)
petal_width = st.slider("꽃잎 너비를 선택하세요", min_value=min_wid, max_value=max_wid, value=float(df['꽃잎 너비'].mean()), step=0.1)

# 3. 사용자 입력값 기반 품종 예측
input_data = pd.DataFrame([[petal_length, petal_width]], columns=['꽃잎 길이', '꽃잎 너비'])
prediction = model.predict(input_data)[0]

# 결과 출력
st.subheader("🎯 예측 결과")
st.success(f"입력하신 붓꽃의 예측 품종은 **[{prediction}]** 입니다!")

# 4. 시각화 (가로축: 꽃잎 길이, 세로축: 꽃잎 너비)
st.subheader("📈 분류 결과 시각화")
st.write("기존 붓꽃 데이터의 분포와 사용자가 입력한 값(`초록색 별`)의 위치를 비교하여 왜 해당 품종으로 분류되었는지 확인할 수 있습니다.")

fig, ax = plt.subplots(figsize=(8, 6))

# 품종별 색상 지정
colors = {'Iris-setosa': '#ff9999', 'Iris-versicolor': '#66b3ff', 'Iris-virginica': '#99ff99'}

# 데이터셋의 품종별 산점도 플롯
for species in df['품종'].unique():
    subset = df[df['품종'] == species]
    ax.scatter(subset['꽃잎 길이'], subset['꽃잎 너비'], label=species, alpha=0.7, edgecolors='k', s=50)

# 5. 사용자가 입력한 값을 초록색 별로 표시
ax.scatter([petal_length], [petal_width], color='green', marker='*', s=350, edgecolor='black', label='사용자 입력값', zorder=5)

ax.set_xlabel('Petal Length (꽃잎 길이)', fontsize=12)
ax.set_ylabel('Petal Width (꽃잎 너비)', fontsize=12)
ax.set_title('Iris Petal Feature Distribution & User Input', fontsize=14)
ax.legend(loc='upper left')
ax.grid(True, linestyle='--', alpha=0.5)

# 스트림릿에 그래프 출력
st.pyplot(fig)
