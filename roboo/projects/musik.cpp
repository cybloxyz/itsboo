#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Array lirik
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

const int numLyrics = sizeof(lyrics) / sizeof(lyrics[0]);
int currentLine = 0;
unsigned long previousMillis = 0;

void setup() {
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Playing song...");
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= durations[currentLine]) {
    previousMillis = currentMillis;
    lcd.clear();
    
    if (strlen(lyrics[currentLine]) <= 16) {
      lcd.setCursor(0, 0);
      lcd.print(lyrics[currentLine]);
    } else {
      // Scroll teks panjang
      for (size_t i = 0; i <= strlen(lyrics[currentLine]) - 16; i++) {
        lcd.setCursor(0, 0);
        lcd.print(String(lyrics[currentLine]).substring(i, i + 16));
        delay(300); // scroll speed
      }
    }

    currentLine++;
    if (currentLine >= numLyrics) currentLine = 0;
  }
}
