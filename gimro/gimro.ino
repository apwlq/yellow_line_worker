const int motorDirectionPins[3] = {0, 8, 10};  // Index 0은 사용하지 않음
const int motorSpeedPins[3] = {0, 9, 11};

void setup() {
  Serial.begin(115200);
  for (int i = 1; i <= 2; i++) {
    pinMode(motorDirectionPins[i], OUTPUT);
    pinMode(motorSpeedPins[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int spaceIndex = input.indexOf(' ');
    if (spaceIndex != -1) {
      int number1 = input.substring(0, spaceIndex).toInt();
      int number2 = input.substring(spaceIndex + 1).toInt();

      controlMotor(number1, 1);
      controlMotor(number2, 2);
    }
  }
}

void controlMotor(int speed, int motorNumber) {
  if (speed > 0) {
    setMotorDirectionAndSpeed(motorNumber, LOW, speed);
  } else {
    setMotorDirectionAndSpeed(motorNumber, HIGH, abs(speed));
  }
}

void setMotorDirectionAndSpeed(int motorNumber, int direction, int speed) {
  if (speed < 0 || speed > 255) {
    Serial.println("에러: 속도는 0과 255 사이여야 합니다");
    return;
  }

  digitalWrite(motorDirectionPins[motorNumber], direction);
  analogWrite(motorSpeedPins[motorNumber], speed);

  Serial.print("모터 ");
  Serial.print(motorNumber);
  Serial.print(direction == LOW ? ": 전진 중, 속도: " : ": 후진 중, 속도: ");
  Serial.println(speed);
}
