from datetime import datetime
import json

import serial

ser = serial.Serial(
    port='/dev/cu.usbmodemFD141',  # 시리얼 포트
    baudrate=9600,
)

while True:

    try:
        if ser.readable():
            res = ser.readline()
            json_data = json.loads(res.decode()[:-1])
            json_data['time'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')  # 현재 시간 JSON에 추가
            print(json_data)

    except serial.serialutil.SerialException:
        print('아두이노가 연결되어 있지 않습니다.')
        break

    except KeyboardInterrupt:
        print('아두이노 시리얼 통신을 중단합니다.')
        break
