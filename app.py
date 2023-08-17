from pyzbar.pyzbar import decode
import cv2
import numpy as np
import serial
import time

waiting = 10
max_motor_speed = 80
camera_num = 1

SERIAL_PORT = "COM11"  # 직접 설정해주어야 합니다. 예) 'COM11' (Windows) or '/dev/ttyUSB0' (Linux)
baud = 115200


def set_motor_speed(left_speed, right_speed):
    left_motor_speed = int(left_speed) - max_motor_speed
    right_motor_speed = int(right_speed) - max_motor_speed
    print(f"Left Speed: {left_motor_speed}, Right Speed: {right_motor_speed}")
    command = f"{right_motor_speed} {left_motor_speed}\n"
    ser.write(command.encode())
    time.sleep(0.1)


cap = cv2.VideoCapture(camera_num)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([40, 255, 255])

kp = 0.1
ki = 0.0
kd = 0.0
prev_error = 0
integral = 0

min_output = -50
max_output = 50
max_speed = 100

ser = serial.Serial(SERIAL_PORT, baudrate=baud, timeout=1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    decoded_objects = decode(frame)
    for obj in decoded_objects:
        if obj.type == 'QRCODE' and obj.data.decode('utf-8') == "STOP":
            print("QR Code detected: STOP")
            set_motor_speed(0, 0)
            time.sleep(waiting)

    moments = cv2.moments(yellow_mask)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        error = cx - frame.shape[1] / 2
        integral += error
        derivative = error - prev_error
        output = kp * error + ki * integral + kd * derivative
        output = max(min(output, max_output), min_output)

        left_speed = max_speed + output
        right_speed = max_speed - output
        set_motor_speed(left_speed, right_speed)

        prev_error = error

    cv2.imshow("Camera", cv2.bitwise_and(frame, frame, mask=yellow_mask))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

command = f"0 0\n"
ser.write(command.encode())
