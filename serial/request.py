"""
request.py
    1. 아두이노의 시리얼 출력을 JSON으로 변환(현재시간 데이터 추가)
    2. JSON 데이터를 http://127.0.0.1:8000/ URL에 post 메소드로 request
    3. request를 보낼 때 csrf_token 추가
"""
from datetime import datetime
import json

import serial
import requests

URL = 'http://127.0.0.1:8000/'
arduino_port = '/dev/cu.usbmodemFD141'

ser = serial.Serial(
    port=arduino_port,  # 시리얼 포트
    baudrate=9600,
)

print('아두이노와 통신 시작')
print(f'아두이노의 접속 포트는 {arduino_port} 입니다.\n')

while True:

    try:
        if ser.readable():
            res = ser.readline()
            json_data = json.loads(res.decode()[:-1])
            json_data['time'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            print(json_data)
            client = requests.session()

            client.get(URL)  # sets cookie

            if 'csrftoken' in client.cookies:
                csrf_token = client.cookies['csrftoken']
            else:
                csrf_token = client.cookies['csrf']

            sensor_data = dict(
                **json_data,
                csrfmiddlewaretoken=csrf_token
            )
            response = client.post(URL, data=sensor_data, headers=dict(Referer=URL))
            print(f'아두이노 데이터 {URL} 전송 완료\n')

    except serial.serialutil.SerialException:
        print('아두이노가 연결되어 있지 않습니다.')
        break

    except requests.exceptions.ConnectionError:
        print('인터넷 전송이 불가능합니다.')
        continue

    except KeyboardInterrupt:
        print('아두이노 시리얼 통신을 중단합니다.')
        break
