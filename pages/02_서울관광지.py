
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

places = [
    {"순위": 1, "관광지": "명동", "영문명": "Myeongdong", "위도": 37.5636, "경도": 126.9869, "설명": "쇼핑과 한국 길거리 음식으로 유명한 번화가"},
    {"순위": 2, "관광지": "N서울타워", "영문명": "N Seoul Tower", "위도": 37.5512, "경도": 126.9882, "설명": "서울의 아름다운 전경을 볼 수 있는 랜드마크"},
    {"순위": 3, "관광지": "코엑스", "영문명": "COEX", "위도": 37.5116, "경도": 127.0592, "설명": "쇼핑과 별마당도서관으로 유명한 복합문화공간"},
    {"순위": 4, "관광지": "강남역", "영문명": "Gangnam Station", "위도": 37.4979, "경도": 127.0276, "설명": "쇼핑과 음식점, 카페가 많은 서울의 번화가"},
    {"순위": 5, "관광지": "홍대 거리", "영문명": "Hongdae", "위도": 37.5563, "경도": 126.9236, "설명": "버스킹과 음악, 젊은 문화를 즐길 수 있는 거리"},
    {"순위": 6, "관광지": "경복궁", "영문명": "Gyeongbokgung Palace", "위도": 37.5796, "경도": 126.9770, "설명": "조선 왕조의 대표 궁궐"},
    {"순위": 7, "관광지": "성수동", "영문명": "Seongsu-dong", "위도": 37.5445, "경도": 127.0560, "설명": "개성 있는 카페와 팝업스토어가 많은 지역"},
    {"순위": 8, "관광지": "북촌한옥마을", "영문명": "Bukchon Hanok Village", "위도": 37.5826, "경도": 126.9830, "설명": "한국의 전통 한옥을 볼 수 있는 마을"},
    {"순위": 9, "관광지": "동대문디자인플라자", "영문명": "DDP", "위도": 37.5669, "경도": 127.0095, "설명": "독특한 건축물과 전시가 유명한 문화공간"},
    {"순위": 10, "관광지": "광장시장", "영문명": "Gwangjang Market", "위도": 37.5700, "경도": 126.9997, "설명": "다양한 한국 전통 음식과 먹거리가 있는 시장"}
]

df = pd.DataFrame(places)

st.title("🇰🇷 외국인이 좋아하는 서울 관광지 TOP 10")
st.write("서울의 인기 관광지를 지도에서 확인해 보세요!")

st.info("이 순위는 공식 통계 순위가 아닌 관광지 추천 목록입니다.")

st.subheader("🗺️ 서울 관광지 지도")

st.map(
    df,
    latitude="위도",
    longitude="경도",
    color="#FF5733",
    size=150,
    zoom=10
)

st.divider()

st.subheader("📍 관광지 상세 정보")

selected = st.selectbox(
    "관광지를 선택하세요!",
    df["관광지"].tolist()
)

place = df[df["관광지"] == selected].iloc[0]

st.markdown(f"### 🏆 {int(place['순위'])}위 {place['관광지']}")
st.write(f"영문명: {place['영문명']}")
st.write(place["설명"])

st.link_button(
    "📌 구글 지도에서 위치 확인",
    f"https://www.google.com/maps/search/?api=1&query={place['위도']},{place['경도']}"
)

st.divider()

st.subheader("🏅 서울 관광지 TOP 10")

st.dataframe(
    df[["순위", "관광지", "영문명", "설명"]],
    use_container_width=True,
    hide_index=True
)

st.success("서울 관광지 탐험을 시작해 보세요! 🌏")
