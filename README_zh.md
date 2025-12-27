* [English version](./README.md)
# WeActStudio.CAN485DevBoardV1_ESP32
![display](Images/1.png)

|目录名称|内容|
| :--:|:--:|
|Doc| 数据手册|
|Hardware| 硬件开发资料|
|Examples|示例|

## 注意事项
1. 按住GPIO0键上电，会一直处于Boot模式，需要重新上电才能运行。
2. 固件烧录时需要弹出TF卡，否则会导致烧录失败。
3. Arduino开发环境：
   - ESP32开发板：`ESP32 Dev Module`

## 管脚说明
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