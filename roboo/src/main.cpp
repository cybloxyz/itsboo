#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const char* lyrics[] = {
    "how can i",
    "move on?",
    "when",
    "i'm still",
    "in love <3",
    "with you!",
    "'cause if one day",
    "you wake up",
    "and find that you're",
    "missing me",
    "then your heart",
    "starts to wonder",
    "where on this earth",
    "i could be",
    "thinkin' maybe",
    "you'll come back",
    "here to the place",
    "that we'd meet",
    "and you'll see me",
    "waiting for you",
    "on the corner",
    "of the street",
    "so i'm not",
    "moving..",
    "i'm not moving"
};

const unsigned long durations[] = {
  1000,
  1000,
  1100,
  550,
  650,
  550,
  1500,
  520,
  800,
  1000,
  900,
  900,
  900,
  2000,
  800,
  1000,
  2000,
  1000,
  1200,
  1000,
  1000,
  1000,
  1000,
  1000,
  2500,
  5000
};

const int numLyrics - sizeof(lyrics) / sizeof(lyrics[0]);
int currentLine = 0;
unsigned long previousMillis = 0;

void setup() {
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("playing song...")
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
      for (size_t i = 0; i <= strlen(lyrics[currentLine]) - 16; i++) {
        lcd.setCursor(0, 0)
        lcd.print(string(lyrics[currentLine]).substring(i, i + 16));
        delay(300);
      }
    }

    currentLine++;
    if (currentLine >= numLyrics) currentLine = 0;
  }
}