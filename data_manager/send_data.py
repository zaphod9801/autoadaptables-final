import serial
import requests
import time
import datetime

ser = serial.Serial('/dev/ttyS0', 9600)  

url = 'https://isa.requestcatcher.com/post'

def get_time_of_day():
    response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC-5")
    data = response.json()
    current_time = datetime.datetime.fromisoformat(data['datetime'][:-1])
    hour = current_time.hour

    if 6 <= hour < 18:
        return "DAY"
    else:
        return "NIGHT"

while True:
    try:
        time_of_day = get_time_of_day()
        print("Time of day:", time_of_day)

        ser.write(f"CMD:{time_of_day}\n".encode('utf-8'))
        
        line = ser.readline().decode('utf-8').strip()
        print("Datos leídos del Arduino:", line)
        
        response = requests.post(url, data={'sensor_data': line})
        print("Respuesta del servidor:", response.status_code, response.text)
        
        time.sleep(60)
        
    except serial.SerialException as e:
        print("Error de conexión serial: ", e)
        break
    except requests.RequestException as e:
        print("Error al enviar datos: ", e)
        break
    except KeyboardInterrupt:
        print("Programa interrumpido manualmente.")
        break