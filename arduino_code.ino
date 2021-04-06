#include <OneWire.h>
#include <DallasTemperature.h>

#define PH_PIN 1
#define ONE_WIRE 2
#define RELAY 3

OneWire oneWire(ONE_WIRE);
DallasTemperature temp_sensors(&oneWire);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(RELAY, OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("hello\n");
  temp_sensors.requestTemperatures();
  float temp = temp_sensors.getTempCByIndex(0);
  //digitalWrite(RELAY, HIGH);
  int relay_test = analogRead(2);
  if (temp < 36.5){
    digitalWrite(RELAY, HIGH);
  }
  else {
    if(temp > 37.0){
      digitalWrite(RELAY, LOW);
    }
  }
  
  Serial.print(temp);

  Serial.print(", ");
  int ph_reading = analogRead(PH_PIN); 
  //int ph_reading = 512;
  Serial.print(ph_reading);
  Serial.print(", ");
  Serial.print(relay_test);
  Serial.print(",\n");
  
  //Serial.println("Hello world again");
  delay(800);
}
