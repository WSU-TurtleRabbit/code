const int outputPin = 8;
void pulsePin(int outputPin, int pulseTime);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
  pinMode(outputPin, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(5000);
  pulsePin(outputPin, 20000);
}

void pulsePin(int outputPin, int pulseTime){
  digitalWrite(outputPin, HIGH);
  delayMicroseconds(pulseTime);
  digitalWrite(outputPin,LOW);
}