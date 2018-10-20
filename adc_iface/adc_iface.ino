 void setup() {
  Serial.begin(115200);
}

void loop() {

  byte buff[10];
  int shift;
  int value;

  for(int i = 0; i < 100; ++i){
    value = i;
    
    for(int j = 0; j < 10; ++j){
      shift = 8 * j;
      buff[j] = (value >> shift) & 255;
    }

    Serial.write(buff, sizeof(buff));
    delay(8);
  }

  for(int i = 100; i > 0; --i){
    value = i;
    
    for(int j = 0; j < 10; ++j){
      shift = 8 * j;
      buff[j] = (value >> shift) & 255;
    }

    Serial.write(buff, sizeof(buff));
    delay(8);
  }
}
