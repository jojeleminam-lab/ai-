
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# 페이지 설정
st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 제목
st.title("🇰🇷 외국인이 좋아하는 서울 관광지 TOP 10")
st.write("서울의 인기 관광지를 인터랙티브 지도로 만나보세요!")
st.caption("Top 10 Seoul Tourist Attractions for International Visitors")

st.info("아래 순위는 공식 통계 순위가 아닌 대표 관광지 추천 목록입니다.")

# 관광지 데이터
places = [
    {
        "rank": 1,
        "name": "명동",
        "english": "Myeongdong",
        "lat": 37.5636,
        "lon": 126.9869,
        "category": "쇼핑",
        "description": "화장품 쇼핑과 한국 길거리 음식으로 유명한 번화가입니다."
    },
    {
        "rank": 2,
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "category": "랜드마크",
        "description": "남산에서 서울의 아름다운 전경을 감상할 수 있습니다."
    },
    {
        "rank": 3,
        "name": "코엑스",
        "english": "COEX",
        "lat": 37.5116,
        "lon": 127.0592,
        "category": "쇼핑·문화",
        "description": "별마당도서관과 쇼핑 공간으로 유명합니다."
    },
    {
        "rank": 4,
        "name": "강남역",
        "english": "Gangnam Station",
        "lat": 37.4979,
        "lon": 127.0276,
        "category": "도심·쇼핑",
        "description": "다양한 음식점과 카페, 쇼핑 매장이 모여 있습니다."
    },
    {
        "rank": 5,
        "name": "홍대 거리",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "category": "문화·공연",
        "description": "버스킹과 음악, 개성 있는 카페를 즐길 수 있습니다."
    },
    {
        "rank": 6,
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "category": "역사·문화",
        "description": "조선 왕조의 대표 궁궐로 한국의 전통문화를 체험할 수 있습니다."
    },
    {
        "rank": 7,
        "name": "성수동",
        "english": "Seongsu-dong",
        "lat": 37.5445,
        "lon": 127.0560,
        "category": "카페·패션",
        "description": "트렌디한 카페와 팝업스토어가 많은 지역입니다."
    },
    {
        "rank": 8,
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "category": "전통문화",
        "description": "한국 전통 한옥과 아름다운 골목길을 볼 수 있습니다."
    },
    {
        "rank": 9,
        "name": "동대문디자인플라자",
        "english": "Dongdaemun Design Plaza",
        "lat": 37.5669,
        "lon": 127.0095,
        "category": "건축·전시",
        "description": "독특한 건축물과 다양한 전시가 열리는 문화공간입니다."
    },
    {
        "rank": 10,
        "name": "광장시장",
        "english": "Gwangjang Market",
        "lat": 37.5700,
        "lon": 126.9997,
        "category": "전통시장·음식",
        "description": "빈대떡과 김밥 등 다양한 한국 음식을 즐길 수 있습니다."
    }
]

# 사이드바
st.sidebar.title("🌏 Seoul Travel")
st.sidebar.write("서울 관광지 TOP 10")

selected_category = st.sidebar.selectbox(
    "관광지 종류 선택",
    ["전체", "쇼핑", "문화", "음식", "랜드마크", "전통문화"]
)

# 카테고리 필터
def category_match(place, category):
    if category == "전체":
        return True
    if category == "쇼핑":
        return "쇼핑" in place["category"]
    if category == "문화":
        return "문화" in place["category"] or "공연" in place["category"] or "전시" in place["category"]
    if category == "음식":
        return "음식" in place["category"]
    if category == "랜드마크":
        return "랜드마크" in place["category"]
    if category == "전통문화":
        return "전통" in place["category"] or "역사" in place["category"]
    return True

filtered_places = [
    p for p in places
    if category_match(p, selected_category)
]

# 관광지 개수
col1, col2, col3 = st.columns(3)

col1.metric("전체 관광지", "10곳")
col2.metric("현재 표시 관광지", f"{len(filtered_places)}곳")
col3.metric("관광 도시", "SEOUL")

st.divider()

# Folium 지도 생성
st.subheader("🗺️ 서울 관광지 인터랙티브 지도")

seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

# 마커 클러스터
marker_cluster = MarkerCluster().add_to(seoul_map)

for place in filtered_places:

    popup_html = f"""
    <div style="width:220px">
        <h3>{place['rank']}위. {place['name']}</h3>
        <b>{place['english']}</b>
        <hr>
        <p>{place['description']}</p>
        <p>종류: {place['category']}</p>
    </div>
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{place['rank']}위 · {place['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=300
        ),
        icon=folium.Icon(
            color="red",
            icon="info-sign"
        )
    ).add_to(marker_cluster)

# 지도 출력
map_data = st_folium(
    seoul_map,
    width=None,
    height=600,
    returned_objects=["last_object_clicked"]
)

st.caption("📍 지도 마커를 클릭하면 관광지의 상세 정보를 확인할 수 있습니다.")

st.divider()

# 관광지 상세 정보
st.subheader("🔎 관광지 상세 정보")

selected_place = st.selectbox(
    "관광지를 선택하세요",
    [p["name"] for p in places]
)

place = next(
    p for p in places
    if p["name"] == selected_place
)

st.markdown(f"### 🏆 {place['rank']}위 · {place['name']}")

detail1, detail2 = st.columns(2)

with detail1:
    st.write(f"**영문명:** {place['english']}")
    st.write(f"**분류:** {place['category']}")
    st.write(f"**설명:** {place['description']}")

with detail2:
    st.write("**위치 정보**")
    st.write(f"위도: {place['lat']}")
    st.write(f"경도: {place['lon']}")

google_url = (
    f"https://www.google.com/maps/search/?api=1"
    f"&query={place['lat']},{place['lon']}"
)

st.link_button(
    "📍 Google 지도에서 위치 확인",
    google_url
)

st.divider()

# TOP 10 목록
st.subheader("🏅 서울 관광지 TOP 10")

for p in places:
    with st.expander(f"{p['rank']}위 · {p['name']} ({p['english']})"):
        st.write(p["description"])
        st.write(f"분류: {p['category']}")
        st.write(f"위치: {p['lat']}, {p['lon']}")

st.divider()

st.success("서울 관광지 탐험을 즐겨보세요! ✈️")

st.caption(
    "Seoul Tourist Guide | Made with Streamlit & Folium"
)
