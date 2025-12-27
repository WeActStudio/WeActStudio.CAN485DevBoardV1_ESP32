void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(115200);

  //set the resolution to 12 bits (0-4095)
  analogReadResolution(12);
}

void loop() {
  // read the analog / millivolts value for pin 36:
  int analogValue = analogRead(36);
  int analogVolts = analogReadMilliVolts(36);
  int vin_Volts = analogVolts * ( 51 + 510 + 51 ) / 51;

  // print out the values you read:
  Serial.printf("ADC analog value = %d\n", analogValue);
  Serial.printf("ADC millivolts value = %d\n", analogVolts);
  Serial.printf("VIN millivolts value = %d\n", vin_Volts); 

  delay(100);  // delay in between reads for clear read from serial
}
