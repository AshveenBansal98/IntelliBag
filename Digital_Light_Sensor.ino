#include <Wire.h>
#include <Digital_Light_TSL2561.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(12,13);

/* As these are pins these need to be int */
const int reed = 31; //pin of reed switch
const int fsrPin = 12;  // pin of force sensitive resistor
const int led = 51; // pin of LED
const int buzz = 6; //pin of buzzer
const int minLight = 30; //minimum light sensor value to view contents of bag clearly
const int minWeight = 5; //minimum value fsr gives when a person is wearing the bag
const int buzzer_rfid = 32; //for receiving signal from pi to raise buzzer
const int rfid_sch = 43; //for giving singal to pi to do a schedule check
void setup()
{
  Wire.begin();
  Serial.begin(9600);
  mySerial.begin(9600); 
  TSL2561.init();
  pinMode(led, OUTPUT);
  pinMode(reed, INPUT);
  pinMode(buzz, OUTPUT);
  pinMode(buzzer_rfid, INPUT);
  pinMode(rfid_sch, OUTPUT);
}

void loop()
{
    unsigned int light = TSL2561.readVisibleLux();
    unsigned int weight = analogRead(fsrPin);
    uint8_t zip = digitalRead(reed); //zip = 1 means zip is closed, 0 means open
    uint8_t buzzer = digitalRead(buzzer_rfid);
	
    if (mySerial.available()>0){ //take commands from bluetooth
      char bt_value = mySerial.read();
      if(bt_value == '1'){ // 1 means schedule check
         digitalWrite(rfid_sch, HIGH);
         delay(2000);
         digitalWrite(rfid_sch, LOW);
      }
      else if(bt_value == '2'){ // 2 means raise the buzzer
        buzzer = 1;
      }
    }
      
    Serial.println(weight);
    if(light <= minLight && zip == 0){ //if light is not sufficient enough and zip is opened then on the led
      digitalWrite(led, HIGH);
    }
    else{
      digitalWrite(led, LOW);
    }
  
    if((weight > minWeight && zip == 0) || buzzer == 1){ //person is wearing the bag and someone opens the zip
      digitalWrite(buzz, HIGH);
    }
    else{
        digitalWrite(buzz, LOW);
    }
  
    delay(1000);
}