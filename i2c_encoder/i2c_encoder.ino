#include <Wire.h>
#define SLAVE_ADDRESS 0x05 //flash another Arduino with 0x04

byte encoderPin1 = 2;
byte encoderPin2 = 3;

volatile byte lastEncoded = 0;
volatile long encoderValue = 0;

long lastencoderValue = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(sendData);

  pinMode(encoderPin1, INPUT_PULLUP); 
  pinMode(encoderPin2, INPUT_PULLUP);

  digitalWrite(encoderPin1, HIGH);
  digitalWrite(encoderPin2, HIGH);

  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3) 
  attachInterrupt(0, updateEncoder, CHANGE); 
  attachInterrupt(1, updateEncoder, CHANGE);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1);
}

// callback for sending data
void sendData(){
  Wire.write(encoderValue-lastencoderValue);
  lastencoderValue = encoderValue;
} 

void updateEncoder(){
  byte MSB = digitalRead(encoderPin1); //MSB = most significant bit
  byte LSB = digitalRead(encoderPin2); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncoded << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
    encoderValue ++;
  }
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) {
    encoderValue --;
  }
  
  lastEncoded = encoded; //store this value for next time
  delay(1);
}
