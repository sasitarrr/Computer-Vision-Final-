#include <Servo.h>
Servo myservo;

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);

#include <cvzone.h>
SerialData serialData(1, 1);
int valsRec[1];

void setup() {
  myservo.attach(3);
  
  Wire.begin();
  Serial.begin(9600);
  lcd.init();

  serialData.begin(); 
}

void loop(){
  serialData.Get(valsRec);
  
    if(valsRec[0]==1){
      lcd.cursor();
      delay(100);
      lcd.setCursor(0,0);
      lcd.backlight();
      lcd.print("Welcome !!!!!");
      
      lcd.setCursor(2,1);
      lcd.backlight();
      lcd.print("Mark attendance.");
      delay(100);
      
      for(int i = 0; i <=180; i+=5)
      {
        myservo.write(i);
        delay(20);
      }
      for(int i=180; i>=0; i-=5)
      { 
        myservo.write(i);
        delay(20);
      }      
    }
    else if(valsRec[0]==0){
      lcd.cursor();
      delay(100);
      lcd.setCursor(0,0);
      lcd.print("ACCESS DENIED");
      
      lcd.setCursor(2,1);
      lcd.print("Contact admin.");
      delay(100);     
    }   
}
