/*
  This Sketch demonstrates how to use the Hardware Serial peripheral to communicate over an RS485 bus.

  Data received on the primary serial port is relayed to the bus acting as an RS485 interface and vice versa.

  UART to RS485 translation hardware (e.g., MAX485, MAX33046E, ADM483) is assumed to be configured in half-duplex
  mode with collision detection as described in
  https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/uart.html#circuit-a-collision-detection-circuit

  To use the script open the Arduino serial monitor (or alternative serial monitor on the Arduino port). Then,
  using an RS485 tranciver, connect another serial monitor to the RS485 port. Entering data on one terminal
  should be displayed on the other terminal.
*/
#include "hal/uart_types.h"
#include "FastLED.h"

#define WS2812_DIN_PIN 4
CRGB leds[1];

#define RS485_RX_PIN  21
#define RS485_TX_PIN  22
#define RS485_RTS_PIN 17

#define RS485 Serial1

void setup() {
  FastLED.addLeds<WS2812B, WS2812_DIN_PIN, GRB>(leds, 1);
  FastLED.setBrightness(30);
  leds[0] = CRGB::Red;
  FastLED.show();

  Serial.begin(115200);

  RS485.begin(9600, SERIAL_8N1, RS485_RX_PIN, RS485_TX_PIN);
  while (!RS485) {
    delay(10);
  }
  if (!RS485.setPins(-1, -1, -1, RS485_RTS_PIN)) {
    Serial.print("Failed to set RS485 pins");
  }

  // Certain versions of Arduino core don't define MODE_RS485_HALF_DUPLEX and so fail to compile.
  // By using UART_MODE_RS485_HALF_DUPLEX defined in hal/uart_types.h we work around this problem.
  // If using a newer IDF and Arduino core you can omit including hal/uart_types.h and use MODE_RS485_HALF_DUPLEX
  // defined in esp32-hal-uart.h (included during other build steps) instead.
  if (!RS485.setMode(UART_MODE_RS485_HALF_DUPLEX)) {
    Serial.print("Failed to set RS485 mode");
  }

  RS485.write("Hello World!!", 13);
  RS485.write("Hello WeAct Studio!!", 20);
}

bool is_rx = false;
bool is_tx = false;
unsigned long currentMillis = 0; 
unsigned long txMillis = 0; 
unsigned long rxMillis = 0; 
void loop() {

  if (RS485.available()) {
    is_rx = true;
    Serial.write(RS485.read());
  }
  if (Serial.available()) {
    is_tx = true;
    RS485.write(Serial.read());
  }

  currentMillis = millis(); 

  if(is_rx && rxMillis == 0)
  {
    leds[0] = CRGB::Green;
    FastLED.show();
    rxMillis = currentMillis;
    is_rx = false;
  }
  else
  {
    if(rxMillis && (currentMillis - rxMillis > 100))
    {
      rxMillis = 0;
      leds[0] = CRGB::Red;
      FastLED.show();
    }
  }

  if(is_tx && txMillis == 0)
  {
    leds[0] = CRGB::Blue;
    FastLED.show();
    txMillis = currentMillis;
    is_tx = false;
  }
  else
  {
    if(txMillis && (currentMillis - txMillis > 100))
    {
      txMillis = 0;
      leds[0] = CRGB::Red;
      FastLED.show();
    }
  }
}
