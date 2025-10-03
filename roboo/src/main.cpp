#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

String incomingtext = "";
const int buttonPin = 2;

// Tambahkan variabel untuk toggle button
int buttonState;        // Kondisi tombol saat ini
int lastButtonState = HIGH; // Kondisi tombol sebelumnya (HIGH karena INPUT_PULLUP)
bool toggleState = false; // Kondisi toggle: false = OFF, true = ON
unsigned long lastDebounceTime = 0; // Waktu terakhir perubahan tombol
unsigned long debounceDelay = 50;   // Waktu tunda debouncing (50ms)

void setup() {
  // Gunakan INPUT_PULLUP agar tombol terhubung ke GND
  // Kondisi default-nya adalah HIGH, saat ditekan menjadi LOW
  pinMode(buttonPin, INPUT_PULLUP);
  
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  Serial.begin(9600);
  lcd.print("waiting...");
}

void loop() {
  
  // *** Bagian Penanganan Input Serial ***
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

  // *** Bagian Toggle Button (Deteksi Perubahan Kondisi dengan Debouncing) ***
  
  // Baca kondisi tombol saat ini
  int reading = digitalRead(buttonPin);

  // Jika kondisi tombol berubah, reset timer debouncing
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  // Setelah waktu tunda debounce, periksa apakah kondisi tombol stabil
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // Jika kondisi tombol stabil berbeda dari buttonState yang tercatat
    if (reading != buttonState) {
      buttonState = reading;

      // Cek apakah tombol baru saja DITEKAN (berubah dari HIGH ke LOW)
      if (buttonState == LOW) { // Karena menggunakan INPUT_PULLUP
        
        // Lakukan toggle pada kondisi
        toggleState = !toggleState;

        // Kirim kondisi toggle ke Serial Monitor
        if (toggleState) {
          Serial.println("Toggle ON");
        } else {
          Serial.println("Toggle OFF");
        }

        // Anda bisa tambahkan aksi LCD di sini, misalnya:
        // lcd.setCursor(0, 1);
        // lcd.print(toggleState ? "ON " : "OFF");
      }
    }
  }

  // Simpan kondisi pembacaan saat ini sebagai kondisi terakhir untuk iterasi berikutnya
  lastButtonState = reading;
}