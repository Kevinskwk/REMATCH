#define outA 2
#define outB 3

int counter = 0;
int aState;
int aLastState;

void setup() {
  pinMode(outA,INPUT);
  pinMode(outB,INPUT);
  Serial.begin(9600);
  aLastState = digitalRead(outA);
}

void loop() {
  // put your main code here, to run repeatedly:
  aState = digitalRead(outA);
  if (aState != aLastState){ 
    if (digitalRead(outB) != aState) {
      counter ++;
      Serial.write(1);
    } else {
      counter --;
      Serial.write(2);
    }
    //Serial.print("Position: ");
    //Serial.println(counter);
  }
  aLastState = aState;
}
