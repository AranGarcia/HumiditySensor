 void setup() {
  Serial.begin(115200);
}

void loop() {
  int value = random(0, 1024);

  byte buff[10];
  int shift;
  for(int i = 0; i < 10; ++i){
    shift = 8 * i;
    buff[i] = (value >> shift) & 255;
  }
  
  
  int bytesSent = Serial.write(buff, sizeof(buff));
  delay(1000);
}
