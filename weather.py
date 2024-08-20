import requests
import json
import math

def euclideanDistance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    return math.sqrt(dlat**2 + dlon**2)


# 텍스트 응답에서 필요한 데이터 추출 함수
def parse_response(response_text):
    data_lines = [line for line in response_text.splitlines() if not line.startswith('#') and line.strip()]
    return data_lines


# 위도, 경도 찾는 함수
def find_STN(lat, lng):  
    closest_station = 0
    
    # 요청 시간 변수로 변환 ====================================================================================================================== 수정 필요
    url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm5.php?tm2=202408200900&obs=TA&stn=0&disp=0&help=1&authKey=1rEfi1JvQG6xH4tSbwBu9Q'
    
    response = requests.get(url)

    # 응답이 제대로 오면
    if response.status_code == 200:
        try:
            # 응답을 텍스트로 받음
            response_text = response.text
            
            # 주석 부분(#)을 제외하고 데이터 부분만 추출
            data_lines = [line for line in response_text.splitlines() if not line.startswith('#') and line.strip()]
            
            # 각 데이터 라인을 딕셔너리로 변환하고 필요한 열만 추출
            lat_data, lng_data = 0, 0
            min_distance = float('inf')

            for line in data_lines:
                values = line.split()  # 공백으로 분리
                station_lat = float(values[2])   # 가져온 위도
                station_lon = float(values[3])   # 가져온 경도
                
                distance = euclideanDistance(lat, lng, station_lat, station_lon)
                if distance < min_distance:
                    min_distance = distance
                    closest_station = values[1]
            
        except Exception as e:
            print(f"텍스트 응답을 처리하는 중 오류 발생: {e}")
    else:
        print(f"요청이 실패, 상태 코드: {response.status_code}")
        print(response.text)

    return closest_station
    

def judgment_rain(stn):
    # 요청 시간 변수로 변환 ====================================================================================================================== 수정 필요
    url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm=202211300900&stn={stn}&help=1&authKey=1rEfi1JvQG6xH4tSbwBu9Q'

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
            #selected_columns = ["TM", "STN", "RN", "RN_DAY", "RN_JUN"]
            selected_columns = ["TM", "STN", "RN"]
            
            # 각 데이터 라인을 딕셔너리로 변환하고 필요한 열만 추출
            data = []
            for line in data_lines:
                values = line.split()  # 공백으로 분리
                record = dict(zip(columns, values))
                selected_record = {col: record[col] for col in selected_columns}  # 필요한 열만 추출
                data.append(selected_record)
            
            return data[0]['RN']
            
        except Exception as e:
            print(f"텍스트 응답을 처리하는 중 오류가 발생했습니다: {e}")
    else:
        print(f"요청이 실패했습니다. 상태 코드: {response.status_code}")
        print(response.text)
        
        
if __name__ == '__main__':
    '''
    현재 90 ~ 296까지 운영 중
    유클리드 거리로 가장 가까운 지점 번호 가져옴 -> 고려 (만약에 범위가 크게 벗어나면)
    '''
    closest_station = find_STN(42.3167, 130.4)  # 102번 (37.9661, 124.6305)
    print("STN", closest_station)
    
    print(judgment_rain(closest_station))