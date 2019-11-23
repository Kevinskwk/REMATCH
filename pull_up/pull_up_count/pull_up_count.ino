#include <hcsr04.h>

#define NUM 2
#define MAX_DISTANCE 2000  //in mm
#define MIN_DISTANCE 20  //in mm
#define INTERVAL 30  //in millisecond
#define LIMIT 400 //in mm

int LED = 6;
bool cooldown = false; 
unsigned int distance[NUM];

HCSR04 sensor[NUM] = {
  HCSR04(3, 2, MIN_DISTANCE, MAX_DISTANCE),
  HCSR04(5, 4, MIN_DISTANCE, MAX_DISTANCE)
};

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  //update_distance();
  //Serial.println(distance[0]);
  //Serial.println(distance[1]);

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

void update_distance() {
  for (uint8_t i = 0; i < NUM; i++) {
    delay(INTERVAL);
    distance[i] = sensor[i].distanceInMillimeters();
  }
}

bool debounce(){
  update_distance();
  for (uint8_t i = 0; i < NUM; i++) {
    if (distance[i] > 500) return false;
  }
  delay(50);
  update_distance();
  for (uint8_t i = 0; i < NUM; i++) {
    if (distance[i] > 500) return false;
  }
  return true;
}


bool debounce_inverted(){
  update_distance();
  for (uint8_t i = 0; i < NUM; i++) {
    if (distance[i] <= 500) return false;
  }
  delay(50);
  update_distance();
  for (uint8_t i = 0; i < NUM; i++) {
    if (distance[i] <= 500) return false;
  }
  return true;
}
