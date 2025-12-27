#include "FastLED.h"

#define WS2812_DIN_PIN 4
CRGB leds[1];

void setup() {
  FastLED.addLeds<WS2812B, WS2812_DIN_PIN, GRB>(leds, 1);
  FastLED.setBrightness(30);
  leds[0] = CRGB::Red;
  FastLED.show();
}

void loop() {
  leds[0] = CRGB::Red;
  FastLED.show();
  delay(500);

  leds[0] = CRGB::Green;
  FastLED.show();
  delay(500);

  leds[0] = CRGB::Blue;
  FastLED.show();
  delay(500);
}
