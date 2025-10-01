#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);


const char* lyrics[] = {
  "everyone wants",
  " him",
  "that was",
  " my crime",
  "the wrong place",
  "at the..",
  " right time",
  "and i..",
  " break down",
  "then he's",
  " pullin' me in",
  "in the world of boys",
  "  he's a",
  " gentleman <3"
};

// Array waktu tampil masing-masing lirik (ms)
const unsigned long durations[] = {
  2500, // everyone wants
  800, //him
  800, // that was 
  1000,//my crime
  1500, // the wrong place
  1000, // at the 
  600,//right time
  1000, // and i
  800, //break down
  500, // then he's 
  800,//pullin' me in
  600, // in the world of boys
  500,  // he's a 
  1000,//gentleman
};
const int numLyrics = sizeof(lyrics)/sizeof(lyrics[0]);

void setup() {
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  Serial.begin(9600);
  lcd.print("Waiting you...");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "move") {
      // jalankan lagu sekali
      for (int i = 0; i < numLyrics; i++) {
        lcd.clear();
        if (strlen(lyrics[i]) <= 16) {
          lcd.setCursor(0, 0);
          lcd.print(lyrics[i]);
          delay(durations[i]);
        } else {
          for (size_t j = 0; j <= strlen(lyrics[i])-16; j++) {
            lcd.setCursor(0,0);
            lcd.print(String(lyrics[i]).substring(j,j+16));
            delay(300);
          }
          delay(durations[i]);
        }
      }
      lcd.clear();
      lcd.print("Done");
    }
  }
}
