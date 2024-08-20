...
# TM     : 관측시각 (KST)
# STN    : 국내 지점번호
# RN     : 강수량 (mm) : 여름철에는 1시간강수량, 겨울철에는 3시간강수량
# RN_DAY : 일강수량 (mm) : 해당시간까지 관측된 양(통계표)
# RN_JUN : 일강수량 (mm) : 해당시간까지 관측된 양을 전문으로 입력한 값(전문)
...

import requests
import json
import math
import pandas as pd
import csv

##################################################################################################################
## 지점번호로 하나 가져와서
## 강수량만 return
##################################################################################################################


# 위도 경도 입력 받음
# 파일에서 읽어와서 가장 가까운 국내 지점번호 return
# 처음 한 번에만 실행

def haversine(lat1, lon1, lat2, lon2):
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # 유클리드 거리 계산
    distance = math.sqrt(dlat**2 + dlon**2)
    
    return distance

# 위도, 경도 찾는 함수
def find_STN(lat, lng):
    
    with open('META.csv', 'r', encoding='cp949') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            print
            
            
            
            
            
    #url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm5.php?tm=0&obs=TA&stn=0&disp=0&help=1&authKey=oEg3RFYKR-SIN0RWCtfkfA'
    #url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm5.php?tm2=201504060900&obs=TA&stn=0&disp=0&help=1&authKey=1rEfi1JvQG6xH4tSbwBu9Q'

    closest_station = 0
    
    response = requests.get(url)

    # 응답이 제대로 오면
    if response.status_code == 200:
        try:
            # 응답을 텍스트로 받음
            response_text = response.text
            
            # 주석 부분(#)을 제외하고 데이터 부분만 추출
            data_lines = [line for line in response_text.splitlines() if not line.startswith('#') and line.strip()]
            
            # 데이터 열의 이름들
            columns = [
                "TM", "STN", "LON", "LAT", "HT", "VAL"]
            
            # 추출할 컬럼 목록 (위도 / 경도)
            selected_columns = ["STN", "LAT", "LON"]
            
            # 각 데이터 라인을 딕셔너리로 변환하고 필요한 열만 추출
            lat_data, lng_data = 0, 0
            min_distance = float('inf')
            
            print(len(data_lines))
            for line in data_lines:
                values = line.split()  # 공백으로 분리
                lat_data = float(values[2])   # 가져온 위도
                lng_data = float(values[3])   # 가져온 경도
                
                distance = haversine(lat, lng, lat_data, lng_data)
                if distance < min_distance:
                    min_distance = distance
                    closest_station = values[1]
            
        except Exception as e:
            print(f"텍스트 응답을 처리하는 중 오류 발생: {e}")
    else:
        print(f"요청이 실패, 상태 코드: {response.status_code}")
        print(response.text)

    return closest_station
    

def rain():
    # URL 문자열
    url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?stn=0&help=1&authKey=oEg3RFYKR-SIN0RWCtfkfA'

    # GET 요청
    response = requests.get(url)

    # 응답 상태 코드 확인
    if response.status_code == 200:
        try:
            # 응답을 텍스트로 받음
            response_text = response.text
            
            # 주석 부분(#)을 제외하고 데이터 부분만 추출
            data_lines = [line for line in response_text.splitlines() if not line.startswith('#') and line.strip()]
            
            # 데이터 열의 이름들
            columns = [
                "TM", "STN", "WD", "WS", "GST_WD", "GST_WS", "GST_TM", "PA", "PS", "PT", "PR", "TA", "TD", "HM", "PV",
                "RN", "RN_DAY", "RN_INT", "SD_HR3", "SD_DAY", "SD_TOT", "WC", "WP", "WW", "CA_TOT", "CA_MID", "CH_MIN",
                "CT", "CT_TOP", "CT_MID", "CT_LOW", "VS", "SS", "SI", "ST_GD", "TS", "TE_005", "TE_01", "TE_02", "TE_03",
                "ST_SEA", "WH", "BF", "IR", "IX", "RN_JUN"
            ]
            
            # 추출할 컬럼 목록
            selected_columns = ["TM", "STN", "RN", "RN_DAY", "RN_JUN"]
            
            # 각 데이터 라인을 딕셔너리로 변환하고 필요한 열만 추출
            data = []
            for line in data_lines:
                values = line.split()  # 공백으로 분리
                record = dict(zip(columns, values))
                selected_record = {col: record[col] for col in selected_columns}  # 필요한 열만 추출
                data.append(selected_record)
            
            # JSON 형식으로 변환하여 파일로 저장
            with open('weather_data.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
            
            print("JSON 데이터가 'weather_data.json' 파일에 저장되었습니다.")
            
        except Exception as e:
            print(f"텍스트 응답을 처리하는 중 오류가 발생했습니다: {e}")
    else:
        print(f"요청이 실패했습니다. 상태 코드: {response.status_code}")
        print(response.text)
        
        
if __name__ == '__main__':
    closest_station = find_STN(42.3167, 130.4)
    print(closest_station)