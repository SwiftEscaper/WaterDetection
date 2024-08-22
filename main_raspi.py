import schedule
import requests
import time

import RainInfo
import WaterSensor

RAIN_AUTH_KEY = '1rEfi1JvQG6xH4tSbwBu9Q'

LATITUDE = 37.517423
LONGITUDE = 127.17903

request_time = RainInfo.get_hour_timestamp()
STN = RainInfo.find_STN(LATITUDE, LONGITUDE, RAIN_AUTH_KEY, request_time)   

def check_rainfall():
    request_time = RainInfo.get_hour_timestamp()
    rainfall = RainInfo.judgment_rain(STN, RAIN_AUTH_KEY, request_time)
    
    # 폭우가 예상이 되면
    if rainfall >= 25:
        consecutive_zeros = 0  # 0일 경우 track
        
        while True:
            # 센서 값을 측정하고
            value = WaterSensor.waterSensor()
        
            # 센서에 물이 닿을 경우
            if value == 1:
                flag = True
                
                data = {"event_type": 3}
                
                # 서버로 전송
                response = requests.post("http://10.246.246.93:10000/water", json=data)
                print(f"Response: {response}")
                
            elif value == 0:
                conseccutive_zeros += 1
                
            if consecutive_zeros >= (30 * 60 / 5):  # 30분 동안 센서에 물이 안 닿은 경우 while문 탈출
                print("No water detected for 30 minutes. Exiting loop.")
                break
            
            # sleep(5초)
            time.sleep(5)


def main():
    # hours
    schedule.every(5).seconds.do(RainInfo.check_rainfall)  # 테스트로 5초마다 실행


if __name__ == "__main__":
    main()