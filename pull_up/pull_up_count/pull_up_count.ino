int echoPin = 10;
int trigPin = 7;
int LED = 8;
bool cooldown = false;
long duration;
float distance;

void setup() {
  // put your setup code here, to run once:
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  distance = ultrasonic_distance();
  if (debounce() && !cooldown) {
    Serial.println("ONE");
    cooldown = true;
    digitalWrite(LED, HIGH);
  }
  if (debounce_inverted()){
    cooldown = false;
    digitalWrite(LED, LOW);
  }
}

float ultrasonic_distance(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  return (duration*0.017);
}

bool debounce(){
  distance = ultrasonic_distance();
  if (distance <= 40) {
    delay(100);
    if (distance <=40) {
      return true;
    }
  }
  return false;
}

bool debounce_inverted() {
  distance = ultrasonic_distance();
  if (distance > 40 && distance <= 200) {
    delay(100);
    if (distance >40 && distance <= 200) {
      return true;
    }
  }
  return false;
}
