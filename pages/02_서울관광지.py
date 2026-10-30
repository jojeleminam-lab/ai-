
import streamlit as st
import folium
import pandas as pd
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from urllib.parse import quote

# ----------------------------------
# 1. 페이지 설정
# ----------------------------------

st.set_page_config(
    page_title="Seoul 2 Days Travel Guide",
    page_icon="🇰🇷",
    layout="wide"
)

st.title("🇰🇷 SEOUL TRAVEL GUIDE")
st.subheader("서울 주요 관광지 TOP 10 | 1박 2일 여행 코스")
st.write(
    "Discover Seoul in 2 Days! "
    "서울의 대표 관광지와 맛집을 한눈에 확인하세요."
)

st.info(
    "여행 시간: 매일 오전 9시 ~ 오후 7시 | "
    "숙박: 서울 중심부 1박"
)

# ----------------------------------
# 2. 링크 생성 함수
# ----------------------------------

def google_map(name):
    return (
        "https://www.google.com/maps/search/?api=1&query="
        + quote(name + ", Seoul, South Korea")
    )

def booking_link(name):
    return (
        "https://www.booking.com/searchresults.html?ss="
        + quote(name + ", Seoul, South Korea")
    )

# ----------------------------------
# 3. 관광지 데이터
# ----------------------------------

places = [
    {
        "rank": 1,
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "day": 1,
        "description": "조선 왕조의 대표 궁궐로 한국의 전통 건축을 감상할 수 있습니다."
    },
    {
        "rank": 2,
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "day": 1,
        "description": "한국 전통 한옥과 아름다운 골목길을 체험할 수 있습니다."
    },
    {
        "rank": 3,
        "name": "광장시장",
        "english": "Gwangjang Market",
        "lat": 37.5700,
        "lon": 126.9997,
        "day": 1,
        "description": "빈대떡과 마약김밥 등 한국의 전통 먹거리가 유명합니다."
    },
    {
        "rank": 4,
        "name": "동대문디자인플라자",
        "english": "Dongdaemun Design Plaza",
        "lat": 37.5669,
        "lon": 127.0095,
        "day": 1,
        "description": "독특한 건축 디자인과 다양한 전시를 즐길 수 있습니다."
    },
    {
        "rank": 5,
        "name": "명동",
        "english": "Myeongdong",
        "lat": 37.5636,
        "lon": 126.9869,
        "day": 1,
        "description": "한국 화장품, 패션, 쇼핑과 길거리 음식의 중심지입니다."
    },
    {
        "rank": 6,
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "day": 1,
        "description": "남산에서 서울의 멋진 야경과 전경을 감상할 수 있습니다."
    },
    {
        "rank": 7,
        "name": "성수동",
        "english": "Seongsu-dong",
        "lat": 37.5445,
        "lon": 127.0560,
        "day": 2,
        "description": "트렌디한 카페, 편집숍과 팝업스토어가 유명합니다."
    },
    {
        "rank": 8,
        "name": "코엑스",
        "english": "COEX",
        "lat": 37.5116,
        "lon": 127.0592,
        "day": 2,
        "description": "별마당도서관과 쇼핑몰, 전시시설을 즐길 수 있습니다."
    },
    {
        "rank": 9,
        "name": "강남역",
        "english": "Gangnam Station",
        "lat": 37.4979,
        "lon": 127.0276,
        "day": 2,
        "description": "서울의 현대적인 도시문화와 쇼핑을 경험할 수 있습니다."
    },
    {
        "rank": 10,
        "name": "홍대 거리",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "day": 2,
        "description": "버스킹, 음악, 패션과 젊은 문화를 즐길 수 있습니다."
    }
]

# ----------------------------------
# 4. 여행 일정 데이터
# ----------------------------------

day1 = [
    ["09:00-09:40", "아침 식사", "이삭토스트 경복궁역점", "관광 전 아침 식사"],
    ["09:40-11:10", "경복궁", "궁궐 관람 및 전통문화 체험", "도보"],
    ["11:10-12:00", "북촌한옥마을", "한옥 골목과 전통 건축 감상", "도보 및 이동"],
    ["12:00-13:00", "점심 식사", "토속촌 삼계탕", "경복궁 인근 식사"],
    ["13:00-13:40", "광장시장", "전통시장과 한국 길거리 음식 구경", "대중교통"],
    ["13:40-14:40", "동대문디자인플라자", "건축물과 디자인 전시 관람", "대중교통"],
    ["14:40-15:50", "명동", "쇼핑 및 한국 화장품 체험", "대중교통"],
    ["15:50-17:30", "N서울타워", "남산 전망대 및 서울 전경 감상", "케이블카 또는 버스"],
    ["17:30-19:00", "저녁 식사", "명동교자", "칼국수와 만두 식사"]
]

day2 = [
    ["09:00-10:00", "아침 식사", "오트 성수", "브런치와 커피"],
    ["10:00-11:00", "성수동", "카페 거리 및 팝업스토어 구경", "도보"],
    ["11:00-11:45", "이동", "성수동 → 코엑스", "대중교통"],
    ["11:45-12:45", "코엑스", "별마당도서관과 쇼핑몰 관람", "도보"],
    ["12:45-13:45", "점심 식사", "무탄 코엑스", "트러플 스테이크 짜장면 등"],
    ["13:45-14:45", "강남역", "강남 거리 및 쇼핑", "대중교통"],
    ["14:45-16:00", "이동", "강남역 → 홍대", "지하철"],
    ["16:00-17:50", "홍대 거리", "버스킹과 거리문화 체험", "도보"],
    ["17:50-19:00", "저녁 식사", "육지 홍대", "숯불 돼지고기 구이"]
]

# ----------------------------------
# 5. 지도 생성
# ----------------------------------

st.divider()
st.header("🗺️ 서울 관광지 TOP 10 지도")
st.write("지도에서 숫자가 표시된 마커를 클릭해 관광지 정보를 확인하세요.")

seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="OpenStreetMap",
    control_scale=True
)

day1_group = folium.FeatureGroup(
    name="DAY 1 관광지",
    show=True
)

day2_group = folium.FeatureGroup(
    name="DAY 2 관광지",
    show=True
)

cluster1 = MarkerCluster().add_to(day1_group)
cluster2 = MarkerCluster().add_to(day2_group)

for place in places:

    popup_html = f"""
    <div style="width:220px">
        <h3>{place['rank']}위. {place['name']}</h3>
        <b>{place['english']}</b>
        <hr>
        <p>{place['description']}</p>
        <b>DAY {place['day']}</b>
    </div>
    """

    marker = folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{place['rank']}위 | {place['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=300
        ),
        icon=folium.Icon(
            color="red" if place["day"] == 1 else "blue",
            icon="info-sign"
        )
    )

    if place["day"] == 1:
        marker.add_to(cluster1)
    else:
        marker.add_to(cluster2)

seoul_map.add_child(day1_group)
seoul_map.add_child(day2_group)

folium.LayerControl(
    collapsed=False
).add_to(seoul_map)

st_folium(
    seoul_map,
    height=600,
    use_container_width=True
)

st.caption(
    "🔴 DAY 1 | 🔵 DAY 2 | 마커를 클릭하면 관광지 상세 정보를 확인할 수 있습니다."
)

# ----------------------------------
# 6. 관광지 일정표
# ----------------------------------

st.divider()
st.header("📅 1박 2일 상세 여행 일정")

st.write(
    "관광지와 식당을 이동 동선에 맞게 배치했습니다. "
    "시간은 추천 일정이며 교통 및 대기 상황에 따라 달라질 수 있습니다."
)

st.subheader("🌅 DAY 1 - 전통과 서울의 야경")

df1 = pd.DataFrame(
    day1,
    columns=["시간", "일정", "장소 및 활동", "이동 및 내용"]
)

st.dataframe(
    df1,
    use_container_width=True,
    hide_index=True
)

st.success(
    "DAY 1 완료! 경복궁부터 남산까지 서울의 전통과 야경을 즐기는 코스입니다."
)

st.divider()

st.subheader("🌆 DAY 2 - 트렌디한 현대 서울")

df2 = pd.DataFrame(
    day2,
    columns=["시간", "일정", "장소 및 활동", "이동 및 내용"]
)

st.dataframe(
    df2,
    use_container_width=True,
    hide_index=True
)

st.success(
    "DAY 2 완료! 성수동, 강남, 홍대에서 서울의 현대적인 문화를 즐겨보세요."
)

# ----------------------------------
# 7. 식당 추천 및 링크
# ----------------------------------

st.divider()
st.header("🍽️ 여행 동선별 추천 맛집")

restaurants = [
    {
        "day": "DAY 1 아침",
        "name": "이삭토스트 경복궁역점",
        "menu": "한국식 토스트와 커피",
        "reason": "경복궁 관광 전 간단하고 빠르게 아침을 해결하기 좋습니다."
    },
    {
        "day": "DAY 1 점심",
        "name": "토속촌 삼계탕",
        "menu": "전통 삼계탕",
        "reason": "경복궁 인근에서 한국의 대표 보양식을 경험할 수 있습니다."
    },
    {
        "day": "DAY 1 저녁",
        "name": "명동교자",
        "menu": "칼국수와 만두",
        "reason": "남산 관광 후 명동으로 돌아와 식사하기 좋습니다."
    },
    {
        "day": "DAY 2 아침",
        "name": "오트 성수",
        "menu": "브런치와 커피",
        "reason": "성수동 관광을 시작하기 좋은 브런치 식당입니다."
    },
    {
        "day": "DAY 2 점심",
        "name": "무탄 코엑스",
        "menu": "트러플 스테이크 짜장면 등",
        "reason": "코엑스 쇼핑과 관광 후 바로 식사하기 좋습니다."
    },
    {
        "day": "DAY 2 저녁",
        "name": "육지 홍대",
        "menu": "숯불 돼지고기 구이",
        "reason": "홍대 관광을 마무리하며 한국식 고기구이를 즐기기 좋습니다."
    }
]

for restaurant in restaurants:

    with st.expander(
        f"🍴 {restaurant['day']} | {restaurant['name']}"
    ):
        st.write(f"**추천 메뉴:** {restaurant['menu']}")
        st.write(restaurant["reason"])

        st.link_button(
            "📍 Google 지도에서 식당 위치 확인",
            google_map(restaurant["name"])
        )

# ----------------------------------
# 8. 호텔 추천
# ----------------------------------

st.divider()
st.header("🏨 서울 숙박 호텔 추천")

st.write(
    "1박 2일 여행의 이동 편의성을 고려해 "
    "명동과 종로 등 서울 중심부의 호텔을 추천합니다."
)

hotels = [
    {
        "name": "나인트리 바이 파르나스 서울 명동 2",
        "english": "Nine Tree by Parnas Seoul Myeongdong II",
        "reason": "명동과 을지로 사이에 위치해 관광과 대중교통 이용에 편리한 호텔입니다.",
        "type": "도심 관광 및 쇼핑"
    },
    {
        "name": "오라카이 인사동 스위츠",
        "english": "Orakai Insadong Suites",
        "reason": "인사동과 종로 중심부에 위치하며 넓은 객실과 주방 시설을 갖춘 숙박시설입니다.",
        "type": "전통문화 관광 및 가족 여행"
    },
    {
        "name": "호텔 PJ 명동",
        "english": "Hotel PJ Myeongdong",
        "reason": "명동과 동대문 사이에 있어 이동 동선을 잡기 좋은 호텔입니다.",
        "type": "관광 및 실용적인 숙박"
    }
]

for hotel in hotels:

    with st.container(border=True):

        st.subheader(f"🏨 {hotel['name']}")
        st.caption(hotel["english"])

        st.write(f"**추천 대상:** {hotel['type']}")
        st.write(hotel["reason"])

        col1, col2 = st.columns(2)

        with col1:
            st.link_button(
                "📍 호텔 위치 확인",
                google_map(hotel["name"]),
                use_container_width=True
            )

        with col2:
            st.link_button(
                "🔎 숙박 예약 검색",
                booking_link(hotel["name"]),
                use_container_width=True
            )

# ----------------------------------
# 9. 관광지 전체 목록
# ----------------------------------

st.divider()
st.header("🏆 서울 관광지 TOP 10")

for place in places:

    with st.expander(
        f"{place['rank']}위 | {place['name']} ({place['english']})"
    ):

        st.write(place["description"])
        st.write(f"방문 예정: DAY {place['day']}")

        st.link_button(
            "Google 지도에서 관광지 확인",
            google_map(place["name"])
        )

# ----------------------------------
# 10. 마무리
# ----------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center">
        <h2>🇰🇷 Enjoy Your Trip to Seoul!</h2>
        <p>서울에서 특별한 1박 2일을 보내세요.</p>
        <p>Seoul Travel Guide | Made with Streamlit & Folium</p>
    </div>
    """,
    unsafe_allow_html=True
)
