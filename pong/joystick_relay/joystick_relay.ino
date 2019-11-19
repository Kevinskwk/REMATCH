int joyX = A0;
int outUp = 10;
int outDown = 11;
int xValue;

void setup() {
  Serial.begin(9600);
  pinMode(outUp, OUTPUT);
  pinMode(outDown, OUTPUT);
}
 
void loop() {
  // put your main code here, to run repeatedly:
  xValue = analogRead(joyX);
 
  //print the values with to plot or view
  if (xValue >510){
    analogWrite(outUp, 255);
    digitalWrite(outDown, 0);
  }
  else if (xValue < 490){
    analogWrite(outDown, 255);
    analogWrite(outUp, 0);
  }
  else {
    analogWrite(outUp, 0);
    analogWrite(outDown, 0);
  }
}
