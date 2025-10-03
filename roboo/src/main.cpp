#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

String incomingtext = "";

void setup() {
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  Serial.begin(9600);
  lcd.print("waiting...");
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(incomingtext);
      incomingtext = "";
    }
    else {
      incomingtext += c;
    }
  }
}