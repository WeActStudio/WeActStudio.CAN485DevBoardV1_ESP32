* [中文版本](./README_zh.md)
# WeActStudio.CAN485DevBoardV1_ESP32
![display](Images/1.png)

|Dir Name|Explain|
| :--:|:--:|
|Doc|DataSheet|
|Hardware|Hardware Development Kit|
|Examples|Examples|

## Attention
1. Pressing the GPIO0 key to power on will keep the device in Boot mode. It needs to be powered on again to run.
2. When burning the firmware, the TF card needs to be removed; otherwise, the burning process will fail.
3. Arduino Development Environment:
   - ESP32 board: `ESP32 Dev Module`

## Pinout
```
// TF Card
"CS": GPIO13,
"SCK": GPIO14,
"MOSI": GPIO15,
"MISO": GPIO2,

// RS485
"DE": GPIO17,
"RO": GPIO21,
"DI": GPIO22,

// CAN
"RX": GPIO26,
"TX": GPIO27,

// Input Voltage
"VIN": GPIO36,
int analogVolts = analogReadMilliVolts(36);
int vin_Volts = analogVolts * ( 51 + 510 + 51 ) / 51;

// WS2812
"LED": GPIO4,

// KEY
"KEY": GPIO0
```

```
/*---------------------------------------
- WeAct Studio Official Link
- taobao: weactstudio.taobao.com
- aliexpress: weactstudio.aliexpress.com
- github: github.com/WeActStudio
- gitee: gitee.com/WeAct-TC
- blog: www.weact-tc.cn
---------------------------------------*/
```
