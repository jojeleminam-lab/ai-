
import streamlit as st

# ==========================================
# 🧭 MBTI 진로 탐색소
# 외부 라이브러리 추가 설치 없이 사용
# ==========================================

st.set_page_config(
    page_title="MBTI 진로 탐색소",
    page_icon="🧭",
    layout="centered"
)

CAREERS = {
    "ISTJ": [
        {
            "name": "회계사",
            "major": "회계학과, 경영학과, 세무학과",
            "personality": "꼼꼼하고 책임감이 강하며 숫자와 자료를 정확하게 다루는 사람",
            "salary": "약 4,000만~8,000만 원 이상",
            "description": "기업의 재무 상태를 확인하고 회계 및 세무 업무를 전문적으로 수행해요.",
            "skills": "회계 지식, 분석력, 정확성",
            "emoji": "📊"
        },
        {
            "name": "공무원",
            "major": "행정학과, 법학과, 정치외교학과 등",
            "personality": "성실하고 규칙을 잘 지키며 꾸준하게 목표를 이루는 사람",
            "salary": "직급·수당 등에 따라 차이",
            "description": "행정 업무를 처리하고 국민에게 필요한 공공 서비스를 제공해요.",
            "skills": "문서 작성, 의사소통, 책임감",
            "emoji": "🏛️"
        }
    ],
    "ISFJ": [
        {
            "name": "간호사",
            "major": "간호학과",
            "personality": "세심하고 배려심이 있으며 긴급한 상황에서도 침착하려는 사람",
            "salary": "약 3,000만~5,500만 원",
            "description": "환자의 건강 상태를 살피고 치료와 회복을 도와요.",
            "skills": "관찰력, 의사소통, 전문 지식",
            "emoji": "🩺"
        },
        {
            "name": "초등교사",
            "major": "교육대학교 초등교육과",
            "personality": "인내심이 있고 다른 사람을 돕는 것을 좋아하는 사람",
            "salary": "호봉·수당 등에 따라 차이",
            "description": "초등학생에게 다양한 과목을 가르치고 성장을 지원해요.",
            "skills": "설명 능력, 공감, 지도력",
            "emoji": "🍎"
        }
    ],
    "INFJ": [
        {
            "name": "심리상담사",
            "major": "심리학과, 상담학과, 상담심리학과",
            "personality": "다른 사람의 감정을 이해하고 고민을 진지하게 들어주는 사람",
            "salary": "약 2,800만~4,500만 원",
            "description": "사람들이 자신의 감정과 문제를 이해하고 해결하도록 도와요.",
            "skills": "경청, 공감, 상담 전문성",
            "emoji": "💬"
        },
        {
            "name": "작가",
            "major": "문예창작학과, 국어국문학과, 미디어 관련 학과",
            "personality": "상상력이 풍부하고 생각을 글로 표현하는 것을 좋아하는 사람",
            "salary": "수입 편차가 매우 큼",
            "description": "소설, 시나리오, 에세이 등 다양한 글을 창작해요.",
            "skills": "글쓰기, 관찰력, 창의성",
            "emoji": "✍️"
        }
    ],
    "INTJ": [
        {
            "name": "소프트웨어 개발자",
            "major": "컴퓨터공학과, 소프트웨어학과, 정보보호학과",
            "personality": "논리적이고 분석적이며 복잡한 문제를 해결하는 것을 좋아하는 사람",
            "salary": "약 3,500만~7,000만 원",
            "description": "프로그램과 서비스를 설계하고 코드를 작성해 문제를 해결해요.",
            "skills": "프로그래밍, 논리력, 문제 해결",
            "emoji": "💻"
        },
        {
            "name": "전략 기획자",
            "major": "경영학과, 경제학과, 산업공학과",
            "personality": "장기적인 계획을 세우고 여러 가능성을 분석하는 사람",
            "salary": "약 3,500만~6,500만 원",
            "description": "기업의 목표를 분석하고 성장 전략과 실행 계획을 세워요.",
            "skills": "분석력, 기획력, 의사결정",
            "emoji": "♟️"
        }
    ],
    "ISTP": [
        {
            "name": "기계 엔지니어",
            "major": "기계공학과, 자동차공학과, 로봇공학과",
            "personality": "직접 작동 원리를 알아보고 실용적으로 문제를 해결하는 사람",
            "salary": "약 3,500만~6,000만 원",
            "description": "기계와 장비를 설계하고 성능을 개선해요.",
            "skills": "공학 지식, 분석력, 실습 능력",
            "emoji": "⚙️"
        },
        {
            "name": "응급구조사",
            "major": "응급구조학과",
            "personality": "위기 상황에서 침착하게 판단하고 빠르게 행동하는 사람",
            "salary": "약 2,800만~4,500만 원",
            "description": "응급환자에게 필요한 응급처치와 이송 업무를 수행해요.",
            "skills": "응급처치, 체력, 상황 판단",
            "emoji": "🚑"
        }
    ],
    "ISFP": [
        {
            "name": "사진작가",
            "major": "사진학과, 영상학과, 미디어학과",
            "personality": "감각이 섬세하고 순간의 분위기와 아름다움을 잘 발견하는 사람",
            "salary": "수입 편차가 매우 큼",
            "description": "인물, 음식, 풍경 등을 사진으로 표현해요.",
            "skills": "구도, 조명, 편집, 창의성",
            "emoji": "📸"
        },
        {
            "name": "제품 디자이너",
            "major": "산업디자인학과, 제품디자인학과",
            "personality": "미적 감각과 창의성이 있고 사용자 입장에서 생각하는 사람",
            "salary": "약 3,000만~5,500만 원",
            "description": "제품의 형태와 기능을 설계해 더 편리한 사용 경험을 만들어요.",
            "skills": "디자인 도구, 스케치, 사용자 이해",
            "emoji": "🎨"
        }
    ],
    "INFP": [
        {
            "name": "작가",
            "major": "문예창작학과, 국어국문학과",
            "personality": "상상력이 풍부하고 자신만의 관점과 이야기를 표현하는 사람",
            "salary": "수입 편차가 매우 큼",
            "description": "독창적인 이야기를 글로 만들어 독자와 소통해요.",
            "skills": "글쓰기, 표현력, 꾸준함",
            "emoji": "📚"
        },
        {
            "name": "상담 전문가",
            "major": "상담심리학과, 심리학과, 상담학과",
            "personality": "공감 능력이 좋고 타인의 이야기를 편견 없이 들으려는 사람",
            "salary": "약 2,800만~4,500만 원",
            "description": "개인의 고민과 어려움을 이해하고 해결 과정을 지원해요.",
            "skills": "경청, 공감, 상담 지식",
            "emoji": "🌱"
        }
    ],
    "INTP": [
        {
            "name": "연구원",
            "major": "관심 분야의 자연과학·공학·사회과학 관련 학과",
            "personality": "호기심이 많고 원리를 깊게 파고들며 근거를 중시하는 사람",
            "salary": "약 3,500만~6,500만 원",
            "description": "실험과 분석을 통해 새로운 지식과 기술을 연구해요.",
            "skills": "분석력, 탐구심, 연구 방법",
            "emoji": "🔬"
        },
        {
            "name": "데이터 분석가",
            "major": "통계학과, 데이터사이언스학과, 산업공학과",
            "personality": "자료를 비교하고 패턴을 찾는 것을 즐기는 사람",
            "salary": "약 3,500만~6,500만 원",
            "description": "데이터를 분석해 기업과 조직의 의사결정을 도와요.",
            "skills": "통계, 데이터 분석, 논리력",
            "emoji": "📈"
        }
    ],
    "ESTP": [
        {
            "name": "영업 전문가",
            "major": "경영학과, 마케팅학과, 유통학과",
            "personality": "적극적이고 순발력이 있으며 사람들과 소통하는 것을 좋아하는 사람",
            "salary": "약 3,000만~6,000만 원 이상",
            "description": "고객의 필요를 파악하고 제품이나 서비스를 소개해요.",
            "skills": "협상, 소통, 고객 이해",
            "emoji": "🤝"
        },
        {
            "name": "스포츠 지도자",
            "major": "체육학과, 스포츠과학과, 스포츠지도학과",
            "personality": "활동적이고 도전을 즐기며 다른 사람을 이끄는 사람",
            "salary": "약 2,800만~4,500만 원",
            "description": "운동 기술을 지도하고 훈련과 체력 향상을 도와요.",
            "skills": "운동 지식, 지도력, 의사소통",
            "emoji": "🏅"
        }
    ],
    "ESFP": [
        {
            "name": "이벤트 기획자",
            "major": "광고홍보학과, 문화콘텐츠학과, 이벤트 관련 학과",
            "personality": "사교적이고 에너지가 넘치며 즐거운 경험을 만드는 것을 좋아하는 사람",
            "salary": "약 3,000만~5,000만 원",
            "description": "축제와 행사 등을 기획하고 현장을 운영해요.",
            "skills": "소통, 일정 관리, 창의성",
            "emoji": "🎉"
        },
        {
            "name": "배우",
            "major": "연극영화과, 연기예술학과",
            "personality": "표현력이 좋고 다양한 감정과 인물을 탐구하는 사람",
            "salary": "수입 편차가 매우 큼",
            "description": "무대나 영상 작품에서 인물을 연기해 이야기를 전달해요.",
            "skills": "연기, 표현력, 협업",
            "emoji": "🎭"
        }
    ],
    "ENFP": [
        {
            "name": "광고 기획자",
            "major": "광고홍보학과, 경영학과, 미디어학과",
            "personality": "아이디어가 풍부하고 새로운 방식으로 사람들의 관심을 끄는 사람",
            "salary": "약 3,200만~5,500만 원",
            "description": "제품과 브랜드를 알릴 창의적인 광고 전략을 만들어요.",
            "skills": "기획력, 글쓰기, 소통",
            "emoji": "💡"
        },
        {
            "name": "콘텐츠 제작자",
            "major": "미디어학과, 영상학과, 콘텐츠 관련 학과",
            "personality": "호기심이 많고 새로운 주제를 영상이나 글로 표현하는 사람",
            "salary": "수입 편차가 매우 큼",
            "description": "영상과 게시물 등 디지털 콘텐츠를 기획하고 제작해요.",
            "skills": "편집, 기획, 스토리텔링",
            "emoji": "🎬"
        }
    ],
    "ENTP": [
        {
            "name": "창업가",
            "major": "경영학과, 경제학과, 창업 관련 학과 등",
            "personality": "새로운 아이디어를 즐기고 도전과 문제 해결을 좋아하는 사람",
            "salary": "사업 성과에 따라 큰 차이가 있음",
            "description": "아이디어를 사업으로 발전시키고 조직과 서비스를 운영해요.",
            "skills": "기획, 실행력, 시장 분석",
            "emoji": "🚀"
        },
        {
            "name": "마케팅 전략가",
            "major": "경영학과, 광고홍보학과, 마케팅학과",
            "personality": "다양한 관점에서 생각하고 사람들의 반응을 분석하는 사람",
            "salary": "약 3,200만~6,000만 원",
            "description": "시장과 소비자를 분석해 제품을 알리는 전략을 세워요.",
            "skills": "분석력, 창의성, 소통",
            "emoji": "📣"
        }
    ],
    "ESTJ": [
        {
            "name": "프로젝트 관리자",
            "major": "산업공학과, 경영학과, 프로젝트 관련 전공",
            "personality": "계획적이고 책임감이 강하며 목표 달성을 위해 팀을 이끄는 사람",
            "salary": "약 4,000만~7,000만 원",
            "description": "일정과 예산, 인력을 관리해 프로젝트가 목표대로 진행되도록 해요.",
            "skills": "조직력, 일정 관리, 소통",
            "emoji": "📋"
        },
        {
            "name": "경영 관리자",
            "major": "경영학과, 경제학과, 산업공학과",
            "personality": "체계적으로 일하고 결정을 내리며 결과를 확인하는 사람",
            "salary": "직급과 기업 규모에 따라 차이",
            "description": "조직의 목표와 업무, 인력을 관리하고 운영을 개선해요.",
            "skills": "리더십, 의사결정, 관리 능력",
            "emoji": "🏢"
        }
    ],
    "ESFJ": [
        {
            "name": "호텔 서비스 매니저",
            "major": "호텔경영학과, 관광학과, 호텔외식경영학과",
            "personality": "친절하고 협력적이며 고객의 만족을 중요하게 생각하는 사람",
            "salary": "약 3,000만~5,000만 원",
            "description": "호텔 서비스 품질과 고객 응대, 현장 운영을 관리해요.",
            "skills": "서비스 정신, 소통, 문제 해결",
            "emoji": "🏨"
        },
        {
            "name": "인사 담당자",
            "major": "경영학과, 심리학과, 행정학과",
            "personality": "사람들과 잘 소통하고 협력과 조직 분위기를 중요하게 생각하는 사람",
            "salary": "약 3,200만~5,500만 원",
            "description": "채용과 교육, 인사 제도 운영을 통해 조직을 지원해요.",
            "skills": "소통, 문서 작성, 공정성",
            "emoji": "🧑‍🤝‍🧑"
        }
    ],
    "ENFJ": [
        {
            "name": "교사",
            "major": "교육학과, 사범대학 관련 학과 등",
            "personality": "다른 사람을 격려하고 지식과 경험을 나누는 것을 좋아하는 사람",
            "salary": "학교 종류·호봉·수당 등에 따라 차이",
            "description": "학생에게 지식을 가르치고 성장과 학습을 지원해요.",
            "skills": "설명 능력, 공감, 지도력",
            "emoji": "📖"
        },
        {
            "name": "인재 개발 전문가",
            "major": "교육학과, 경영학과, 심리학과",
            "personality": "사람의 강점을 발견하고 성장할 수 있도록 돕는 사람",
            "salary": "약 3,500만~6,000만 원",
            "description": "직원 교육과 역량 개발 프로그램을 기획하고 운영해요.",
            "skills": "교육 기획, 소통, 리더십",
            "emoji": "🌟"
        }
    ],
    "ENTJ": [
        {
            "name": "기업 경영자",
            "major": "경영학과, 경제학과, 산업공학과 등",
            "personality": "목표 지향적이고 결단력이 있으며 큰 그림을 보는 사람",
            "salary": "기업 규모와 성과에 따라 큰 차이가 있음",
            "description": "기업의 목표를 정하고 조직과 자원을 활용해 성과를 만들어요.",
            "skills": "리더십, 전략 수립, 의사결정",
            "emoji": "👑"
        },
        {
            "name": "경영 컨설턴트",
            "major": "경영학과, 경제학과, 산업공학과",
            "personality": "분석적이고 도전적이며 복잡한 문제를 해결하는 것을 즐기는 사람",
            "salary": "약 4,000만~8,000만 원 이상",
            "description": "기업의 문제를 분석하고 경영 성과를 높일 방법을 제안해요.",
            "skills": "분석력, 발표력, 문제 해결",
            "emoji": "📌"
        }
    ]
}

# ==========================================
# 화면 디자인
# ==========================================

st.markdown(
    """
    <div style="text-align:center; padding:10px 0 20px 0;">
        <div style="font-size:55px;">🧭</div>
        <h1>MBTI 진로 탐색소</h1>
        <p style="font-size:18px;">
            내 성향을 알아보고 미래의 직업을 탐험해 보자! 🚀
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "✨ MBTI는 진로를 정해 주는 정답지가 아니야! "
    "나의 흥미와 능력도 함께 생각하면서 참고해 보자."
)

mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

selected_mbti = st.selectbox(
    "🎯 나의 MBTI 유형을 선택해 줘!",
    mbti_types,
    help="검사 결과를 참고하거나 가장 가깝다고 느끼는 유형을 선택해 봐."
)

if st.button("🔍 나에게 맞는 진로 찾아보기", use_container_width=True):
    st.session_state["show_results"] = True
    st.session_state["selected_mbti"] = selected_mbti

if st.session_state.get("show_results", False):
    result_mbti = st.session_state.get(
        "selected_mbti", selected_mbti
    )

    st.markdown("---")
    st.header(f"🌈 {result_mbti} 추천 진로 TOP 2")
    st.write("두 직업을 살펴보고 어떤 분야가 더 끌리는지 생각해 봐!")

    for index, career in enumerate(CAREERS[result_mbti], start=1):
        with st.container(border=True):
            st.subheader(
                f"{career['emoji']} 추천 {index}. {career['name']}"
            )
            st.write(career["description"])

            st.markdown("🎓 **관련 학과**")
            st.write(career["major"])

            st.markdown("💡 **어울리는 성격과 특징**")
            st.write(career["personality"])

            st.markdown("🛠️ **중요한 역량**")
            st.write(career["skills"])

            st.markdown("💰 **참고 연봉**")
            st.write(career["salary"])

            st.caption(
                "연봉은 진로 탐색용 대략적인 안내이며 "
                "공식 직업별 평균 통계가 아닙니다. "
                "실제 보수는 경력, 기업 규모, 지역, 고용 형태 등에 따라 달라져요."
            )

    st.success(
        "🎉 진로 탐색 완료! 마음에 드는 직업의 관련 학과와 "
        "실제 하는 일을 더 찾아보면 좋아."
    )

    st.markdown("### 🔎 더 자세히 알아보기")
    st.markdown(
        "- [워크피디아 임금직업포털](https://www.wagework.go.kr/)"
    )
    st.markdown(
        "- [커리어넷 진로정보](https://www.career.go.kr/)"
    )

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:gray;">
        🌱 진로에는 정답이 없어! 다양한 경험을 통해 나만의 길을 찾아가자.
    </div>
    """,
    unsafe_allow_html=True
)
