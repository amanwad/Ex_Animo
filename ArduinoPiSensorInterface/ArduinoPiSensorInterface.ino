String buff;
#include <SparkFunMLX90614.h>

IRTherm thermObj;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  thermObj.begin();
  thermObj.setUnit(TEMP_F);
  while(!Serial);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.write("Hello");

  while(!(Serial.available()>0));
  buff =  Serial.readStringUntil('\n');
  float thermsum = 0;
  if(thermObj.read()) {
    for(int i = 0; i < 20; i++) {
      thermsum+=thermObj.object();
      delay(20);
    }
    thermsum/=20;
  }
  String mess = String(thermsum, 2)+"\n";
  Serial.print(mess);
//  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(1000);                       // wait for a second
//  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
//  delay(1000);
//  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(1000);                       // wait for a second
//  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
//  delay(1000);
  
  //Serial.write("Hello\n");
}
