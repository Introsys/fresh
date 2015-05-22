#include <XBee.h>

#include "DHT.h"
#include "ENV_TMP.h"

//////////////////////////////////////////////////////////////////////

#define TX_DELAY 2000 //in miliseconds
#define TX_PACKET_BUFFER_SIZE 84

#define SENSOR_TEMP_1_PIN 0 //AN0
#define SENSOR_TEMP_2_PIN 2 //DI2
#define SENSOR_TEMP_2_TYPE DHT22 //DHT 22 (AM2302)

#define DEVICE_TYPE "Zone"
#define DEVICE_ID "Zone1"

//////////////////////////////////////////////////////////////////////

//SH + SL Address of receiving XBee (coordinator)
XBeeAddress64 coordinator = XBeeAddress64(0x00000000, 0x00000000);
ZBTxStatusResponse txStatus = ZBTxStatusResponse();

ENV_TMP sensor_temp_1 = ENV_TMP(SENSOR_TEMP_1_PIN);
DHT sensor_temp_2 = DHT(SENSOR_TEMP_2_PIN, SENSOR_TEMP_2_TYPE);

XBee xbee = XBee();

//XBee leds
int statusLed = 13;
int errorLed = 13;

//Packet Payload Buffer
char buf[TX_PACKET_BUFFER_SIZE];

//////////////////////////////////////////////////////////////////////

void flashLed(int pin, int times, int wait)
{
  for (int i = 0; i < times; i++)
  {
    digitalWrite(pin, HIGH);
    delay(wait);
    digitalWrite(pin, LOW);

    if (i + 1 < times)
    {
      delay(wait);
    }
  }
}

//////////////////////////////////////////////////////////////////////

void floatToAscii(float f, char* ascii)
{
  int frac;
  //get three numbers to the right of the decimal point
  frac=(unsigned int)(f*1000)%1000;  

  itoa((int)f, ascii, 10);
  strcat(ascii,".");
  //put the frac after the decimal
  itoa(frac, &ascii[strlen(ascii)], 10);
}

//////////////////////////////////////////////////////////////////////

void sendData(char* data, uint8_t data_size)
{
  ZBTxRequest zbTx = ZBTxRequest(coordinator, (uint8_t*)data, data_size);
  xbee.send(zbTx);
  
  // flash TX indicator
  flashLed(statusLed, 1, 100);

  // after sending a tx request, we expect a status response
  // wait up to half second for the status response
  if (xbee.readPacket(500)) {
    // got a response!

    // should be a znet tx status            	
    if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
      xbee.getResponse().getZBTxStatusResponse(txStatus);

      // get the delivery status, the fifth byte
      if (txStatus.getDeliveryStatus() == SUCCESS) {
        // success.  time to celebrate
        flashLed(statusLed, 5, 50);
      } else {
        // the remote XBee did not receive our packet. is it powered on?
        flashLed(errorLed, 3, 500);
      }
    }
  } else if (xbee.getResponse().isError()) {
    //nss.print("Error reading packet.  Error code: ");  
    //nss.println(xbee.getResponse().getErrorCode());
  } else {
    // local XBee did not provide a timely TX Status Response -- should not happen
    flashLed(errorLed, 2, 50);
  }
  
  delay(TX_DELAY);
}

//////////////////////////////////////////////////////////////////////

void setup()
{
  // put your setup code here, to run once:
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);

  Serial.begin(9600);
  xbee.setSerial(Serial);
  
  delay(2000);
}

//////////////////////////////////////////////////////////////////////

void loop()
{
  //send contextElement data:
  strcpy(buf, "");
  strcat(buf, "element{");
  strcat(buf, "\"type\":");
  strcat(buf, "\"");
  strcat(buf, DEVICE_TYPE);
  strcat(buf, "\",");
  strcat(buf, "\"isPattern\":");
  strcat(buf, "\"");
  strcat(buf, "false");
  strcat(buf, "\",");
  strcat(buf, "\"id\":");
  strcat(buf, "\"");
  strcat(buf, DEVICE_ID);
  strcat(buf, "\"}");
  strcat(buf, "\n");
  sendData(buf, strlen(buf));
  
  float f_temp_1 = sensor_temp_1.readTemperature();
  char s_temp_1[32];
  floatToAscii(f_temp_1, s_temp_1);
  
  //send attribute data:
  strcpy(buf, "");
  strcat(buf, "attribute{");
  strcat(buf, "\"name\":");
  strcat(buf, "\"");
  strcat(buf, "temp_1");
  strcat(buf, "\",");
  strcat(buf, "\"type\":");
  strcat(buf, "\"");
  strcat(buf, "float");
  strcat(buf, "\",");
  strcat(buf, "\"value\":");
  strcat(buf, "\"");
  strcat(buf, s_temp_1);
  strcat(buf, "\"}");
  strcat(buf, "\n");
  sendData(buf, strlen(buf));
  
  float f_temp_2 = sensor_temp_2.readTemperature();
  char s_temp_2[32];
  floatToAscii(f_temp_2, s_temp_2);
  
  //send attribute data:
  strcpy(buf, "");
  strcat(buf, "attribute{");
  strcat(buf, "\"name\":");
  strcat(buf, "\"");
  strcat(buf, "temp_2");
  strcat(buf, "\",");
  strcat(buf, "\"type\":");
  strcat(buf, "\"");
  strcat(buf, "float");
  strcat(buf, "\",");
  strcat(buf, "\"value\":");
  strcat(buf, "\"");
  strcat(buf, s_temp_2);
  strcat(buf, "\"}");
  strcat(buf, "\n");
  sendData(buf, strlen(buf));
  
  float f_humi_2 = sensor_temp_2.readHumidity();
  char s_humi_2[32];
  floatToAscii(f_humi_2, s_temp_2);
  
  //send attribute data:
  strcpy(buf, "");
  strcat(buf, "attribute{");
  strcat(buf, "\"name\":");
  strcat(buf, "\"");
  strcat(buf, "humidity");
  strcat(buf, "\",");
  strcat(buf, "\"type\":");
  strcat(buf, "\"");
  strcat(buf, "float");
  strcat(buf, "\",");
  strcat(buf, "\"value\":");
  strcat(buf, "\"");
  strcat(buf, s_temp_2);
  strcat(buf, "\"}");
  strcat(buf, "\n");
  sendData(buf, strlen(buf));
}
