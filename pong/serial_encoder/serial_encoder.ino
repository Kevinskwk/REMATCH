byte encoderPin11 = 2;
byte encoderPin12 = 3;

byte encoderPin21 = 20;
byte encoderPin22 = 21;

volatile byte lastEncoded1 = 0;
volatile byte lastEncoded2 = 0;
//volatile long encoderValue = 0;

//long lastencoderValue = 0;

//int lastMSB1 = 0;
//int lastLSB1 = 0;
//int lastMSB2 = 0;
//int lastLSB2 = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(encoderPin11, INPUT_PULLUP); 
  pinMode(encoderPin12, INPUT_PULLUP);
  pinMode(encoderPin21, INPUT_PULLUP); 
  pinMode(encoderPin22, INPUT_PULLUP);

  digitalWrite(encoderPin11, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin12, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin21, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin22, HIGH); //turn pullup resistor on


  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3) 
  attachInterrupt(0, updateEncoder1, CHANGE); 
  attachInterrupt(1, updateEncoder1, CHANGE);
  attachInterrupt(2, updateEncoder2, CHANGE); 
  attachInterrupt(3, updateEncoder2, CHANGE);

}

void loop() {
  // put your main code here, to run repeatedly:
  // Serial.println(encoderValue);
}

void updateEncoder1(){
  byte MSB = digitalRead(encoderPin11); //MSB = most significant bit
  byte LSB = digitalRead(encoderPin12); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncoded1 << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
    //encoderValue ++;
    Serial.write(1);
  }
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) {
    //encoderValue --;
    Serial.write(2);
  }
  
  lastEncoded1 = encoded; //store this value for next time
  delay(1);
}

void updateEncoder2(){
  byte MSB = digitalRead(encoderPin21); //MSB = most significant bit
  byte LSB = digitalRead(encoderPin22); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncoded2 << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
    //encoderValue ++;
    Serial.write(3);
  }
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) {
    //encoderValue --;
    Serial.write(4);
  }
  
  lastEncoded2 = encoded; //store this value for next time
  delay(1);
}
