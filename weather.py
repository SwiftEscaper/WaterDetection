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
def find_STN(lat, lng, auth_key, request_time):  
    url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm5.php?tm2={request_time}&obs=TA&stn=0&disp=0&help=1&authKey={auth_key}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"요청 실패, 상태 코드: {response.status_code}")
        return None

    try:
        data_lines = parse_response(response.text)
        
        min_distance = float('inf')
        closest_station = None

        for line in data_lines:
            _, station_id, station_lat, station_lon, *_ = line.split()
            distance = euclideanDistance(lat, lng, station_lat, station_lon)
            
            if distance < min_distance:
                min_distance = distance
                closest_station = station_id
                
        return closest_station
        
    except Exception as e:
        print(f"텍스트 응답을 처리하는 중 오류 발생: {e}")
        return None
    

# 강수량 판단 함수
def judgment_rain(stn, auth_key, request_time):
    url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm={request_time}&stn={stn}&help=1&authKey={auth_key}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"요청 실패, 상태 코드: {response.status_code}")
        return None
    
    try:
        data_lines = parse_response(response.text)
        
        # 추출할 컬럼 목록
        #columns = ["TM", "STN", "RN", "RN_DAY", "RN_JUN"]
        columns = ["TM", "STN", "RN"]
        record = dict(zip(columns, data_lines[0].split()))
        return record['RN']
    
    except Exception as e:
        print(f"응답 처리 중 오류 발생: {e}")
        return None
        
        
if __name__ == '__main__':
    '''
    현재 90 ~ 296까지 운영 중
    유클리드 거리로 가장 가까운 지점 번호 가져옴 -> 고려 (만약에 범위가 크게 벗어나면)
    '''
    
    request_time = '202408200900'
    auth_key = '1rEfi1JvQG6xH4tSbwBu9Q'
    
    # 현재 위치 설정 (위도, 경도)
    latitude, longitude = 42.3167, 130.4
    
    closest_station = find_STN(latitude, longitude, auth_key, request_time)  # 102번 (37.9661, 124.6305)
    print("STN", closest_station)
    
    rain_data = judgment_rain(closest_station, auth_key, request_time)
    print(rain_data)