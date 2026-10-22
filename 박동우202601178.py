import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import math

# 1. 앱 제목 설정
st.title("부산 지하철 역별 이용객 수 지도 분석")
st.write("CSV 파일을 업로드하면 부산 지하철 역별 이용객 수를 지도에 시각화해 줍니다.")

# 2. 파일 업로드 기능
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 업로드된 CSV 파일을 pandas로 읽기
    df = pd.read_csv(uploaded_file)

    # 3. 업로드된 데이터 표로 보여주기
    st.subheader("📊 업로드된 데이터 미리보기")
    st.dataframe(df)

    # 4. Folium 지도 생성 (부산 중심 좌표 기준)
    st.subheader("🗺️ 부산 지하철 이용객 수 지도")
    busan_map = folium.Map(location=[35.1796, 129.0756], zoom_start=11)

    # 5. 각 행(역)마다 CircleMarker를 지도에 표시하기
    for index, row in df.iterrows():
        name = row['역명']
        line = row['호선']
        lat = row['위도']
        lon = row['경도']
        passengers = row['이용객수']

        # 원의 면적이 이용객수에 비례하도록 반지름(radius)을 제곱근으로 계산
        # 숫자가 너무 크거나 작으면 보기가 불편하므로 적당히 크기를 조절(예: 0.15 곱하기)
        radius = math.sqrt(passengers) * 0.15

        # 마우스를 올리면 역명과 호선, 클릭하면 이용객 수가 나오도록 툴팁과 팝업 설정
        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color='blue',  # 테두리 색상
            fill=True,
            fill_color='skyblue',  # 내부 채우기 색상
            fill_opacity=0.6,  # 투명도
            tooltip=f"{line} {name}",  # 마우스를 올렸을 때 나오는 설명
            popup=f"{name}: 이용객수 {passengers:,}명"  # 클릭했을 때 나오는 팝업
        ).add_to(busan_map)

    # 6. Streamlit 화면에 folium 지도 출력하기
    st_folium(busan_map, width=700, height=500)

else:
    st.info("💡 분석을 시작하려면 CSV 파일을 먼저 업로드해주세요.")