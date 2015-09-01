
#include <stdio.h>            //
#include <string.h>           //
#include <XBee.h>             // Xbee API Mode
#include <Wire.h>             // enable I2C communication channel
#include <SoftwareSerial.h>   //
#include <IRTemp.h>           //
#include <DHT.h>              //
#include <ENV_TMP.h>          //
#include <DFR_CO2.h>          //
#include <AtlasProbes.h>      //
#include <SHT1x.h>            //
#include <Adafruit_AM2315.h>  //
#include "DS1307.h"
#include "rgb_lcd.h"

//////////////////////////////////////////////////////////////////////

//XBee:
#define TX_DELAY 2000 //in miliseconds
#define TX_PACKET_BUFFER_SIZE 84

//Sensor modules:
#define SEN_IRT     0 // IR temperature / leaf temperature
#define SEN_TPS     0 // External temperature / soil temperature
#define SEN_TPA     0 // External temperature / ambient temperature
#define SEN_CO2     0 // CO2
#define SEN_CO2_MH  0 // C02
#define SEN_MOI     0 // Soil moisture
#define SEN_PH      0 // Ph - I2C (Red)
#define SEN_EC      0 // Electrical Conductivity - I2C (Green)
#define SEN_ORP     0 // Oxidation-Reduction Potential - I2C (Blue)
#define SEN_OD      0 // Dissolved Oxygen ( "DO" is a reserved word in c/c++ programing language) - I2C (Yellow)
#define SEN_RGB     1 // RGB Sensor
#define SEN_SHT10   1 // Soil Temperature and Humidity Sensor 
#define SEN_AM2315  1 // Air Humidity and Temp sensor - I2C
#define LCD_ON      1 // Monitor


//Pin assignment:
#define PIN_SEN_TPS_DAT    -1 // analog in
#define PIN_SEN_CO2_DAT    -1  // analog in
#define PIN_SEN_MOI_DAT    -1  // analog in
#define PIN_SEN_CO2_MH_DAT -1 // analog in

#define PIN_SEN_TPA_DAT   -1   // digital in
#define PIN_SEN_IRT_CLK   -1   // digital in
#define PIN_SEN_IRT_DAT   -1   // digital in
#define PIN_SEN_IRT_ACQ   -1   // digital out
#define PIN_SEN_CO2_SIG   -1   // digital in / not currently used

// For the RGB Sensor
#define PIN_SOFTWARE_SERIAL_TX  2  // digital in - serial port emulated - white
#define PIN_SOFTWARE_SERIAL_RX  3  // digital in - serial port emulated - yellow

// For the SHT10
#define PIN_SHT10_DATA  8 // data - white
#define PIN_SHT10_CLOCK 9 // clock - yellow

// Other variable
#define SOFTWARE_SERIAL_BUAD_RATE 38400 // Do no change this!!
#define setup_clock 0                   // Default to 0, the clock must be set only the first time our when the power supply is removed


//Fiware Entity:
#define DEVICE_TYPE "Zone"
#define DEVICE_ID "0013A20040AFC19B" // Zone1

//////////////////////////////////////////////////////////////////////

//SH + SL Address of receiving XBee (coordinator)
XBeeAddress64 coordinator = XBeeAddress64(0x00000000, 0x00000000);
ZBTxStatusResponse txStatus = ZBTxStatusResponse();
char buf[TX_PACKET_BUFFER_SIZE];
int statusLed = 13;
int errorLed = 13;
XBee xbee = XBee();

//Sensor data pointers
IRTemp* sen_irt_ptr;
ENV_TMP* sen_tps_ptr;
DHT* sen_tpa_ptr;
DFR_CO2* sen_co2_ptr;
AtlasProbes* sen_atlas_ptr;
Adafruit_AM2315* sen_am2315;
SHT1x* sen_sht10;
DS1307* clock;
SoftwareSerial *soft_serial;
rgb_lcd lcd;

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

void sendElementData()
{
  strcpy(buf, "{");
  strcat(buf, "\"element\":{");
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
  strcat(buf, "}");
  sendData(buf, strlen(buf));
}

//////////////////////////////////////////////////////////////////////

void sendAttributeData(char* a_name, char* a_type, char* a_value)
{
  strcpy(buf, "{");
  strcat(buf, "\"attribute\":{");
  strcat(buf, "\"name\":");
  strcat(buf, "\"");
  strcat(buf, a_name);
  strcat(buf, "\",");
  strcat(buf, "\"type\":");
  strcat(buf, "\"");
  strcat(buf, a_type);
  strcat(buf, "\",");
  strcat(buf, "\"value\":");
  strcat(buf, "\"");
  strcat(buf, a_value);
  strcat(buf, "\"}");
  strcat(buf, "}");
  sendData(buf, strlen(buf));
}

//////////////////////////////////////////////////////////////////////

void setup()
{
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);
  
  // For arduino leonardo
  //Serial1.begin(9600);          // enable serial port
  //xbee.setSerial(Serial1);      // xbee comunication to serial
  // for arduino uno
  Serial.begin(9600);          // enable serial port
  xbee.setSerial(Serial);      // xbee comunication to serial
  Wire.begin();                // enable I2C port
  
  // -----------------------------------
  
  clock = new DS1307();
  clock->begin();
  
  if(setup_clock){
    clock->fillByYMD(2015,8,11);//Jan 19,2013
    clock->fillByHMS(9,52,00);//15:28 30"
    clock->fillDayOfWeek(MON);//Saturday
    clock->setTime();//write time to the RTC chip
  }
  
  // -----------------------------------
  
  if(SEN_IRT)  
    sen_irt_ptr = new IRTemp(PIN_SEN_IRT_ACQ, PIN_SEN_IRT_CLK, PIN_SEN_IRT_DAT);
  
  if(SEN_TPS)
    sen_tps_ptr = new ENV_TMP(PIN_SEN_TPS_DAT);
    
  if(SEN_TPA)
    sen_tpa_ptr = new DHT(PIN_SEN_TPA_DAT, DHT22);
    
  if(SEN_CO2)
    sen_co2_ptr = new DFR_CO2(PIN_SEN_CO2_DAT, PIN_SEN_CO2_SIG);
           
  if(SEN_EC || SEN_ORP || SEN_OD || SEN_PH)
    sen_atlas_ptr = new AtlasProbes();
    
  if(SEN_RGB){
    soft_serial = new SoftwareSerial(PIN_SOFTWARE_SERIAL_RX, PIN_SOFTWARE_SERIAL_TX);
    soft_serial-> begin(SOFTWARE_SERIAL_BUAD_RATE);
    soft_serial-> print("E");    // command to stop continuous readings
    delay(25);                   // give some time to the arduino 
    soft_serial-> print("M3");   // select the reading mode, for more information please refer to the ENV-RGB documentation
    delay(25);                  // give some time to the arduino 
  }
  
  if (SEN_SHT10)
    sen_sht10 = new SHT1x(PIN_SHT10_DATA, PIN_SHT10_CLOCK);

  if (SEN_AM2315)
    sen_am2315 = new Adafruit_AM2315(); 

  if(LCD_ON){
    lcd.begin(16, 2);
    lcd.setCursor(0, 0);
    lcd.print("Fresh - Introsys");
    lcd.setCursor(0, 1);
    lcd.print("Sensor Node");
    delay(1000);
  }

  delay(1000);
}

//////////////////////////////////////////////////////////////////////

void loop()
{
  sendElementData();
  
  if(SEN_IRT)
  {
    float val_1 = sen_irt_ptr->getIRTemperature(CELSIUS);
    //float val_2 = sen_irt_ptr->getAmbientTemperature(CELSIUS);
    char s_val[32];
    floatToAscii(val_1, s_val);
    sendAttributeData("IRtemp", "Celsius", s_val);
    
    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Ifra Red: ");
      lcd.setCursor(0,1);
      lcd.print(s_val);
      lcd.print(" C");
      delay(100);
    }
        
  }
  
// -----------------------------------

  if(SEN_TPS)
  {

    
    float val = sen_tps_ptr->readTemperature();
    char s_val[32];
    floatToAscii(val, s_val);
    sendAttributeData("SoilTemp", "Celsius", s_val);
    
    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Soil Temp: ");
      lcd.setCursor(0,1);
      lcd.print(s_val);
      lcd.print(" C");
      delay(100);
    }
  }
 
// -----------------------------------

  if(SEN_TPA)
  {
        
    float val_1 = sen_tpa_ptr->readTemperature();
    float val_2 = sen_tpa_ptr->readHumidity();
    char s_val_1[32];
    char s_val_2[32];
    floatToAscii(val_1, s_val_1);
    floatToAscii(val_2, s_val_2);
    sendAttributeData("AirTemperature", "Celsius", s_val_1);
    sendAttributeData("AirHumidity", "Percent", s_val_2);

    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Air Temp: ");
      lcd.setCursor(0,1);
      lcd.print(s_val_1);
      lcd.print(" C");
      delay(100);      
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Air Humidity: ");
      lcd.setCursor(0,1);
      lcd.print(s_val_2);
      lcd.print(" %");
      delay(100);
    }
    
  }
  
// -----------------------------------
  
  if(SEN_CO2)
  {
    float val = sen_co2_ptr->readValue();
    int percent = sen_co2_ptr->getPercentage(val);
    char s_val[32];
    if(percent==-1)
      strcpy(s_val, "400"); //strcpy(s_co2, "<400");
    else
      floatToAscii(percent, s_val);
    sendAttributeData("CO2", "ppm", s_val);
    
    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      lcd.print("CO2: ");
      lcd.print(s_val);
      lcd.print(" ppm");
      delay(100);
    }
  
  }
  
// -----------------------------------
  
  if(SEN_CO2_MH)
  {
    // val belongs to the interval [0,4, 2.0] expressed in V
    int val = analogRead(PIN_SEN_CO2_MH_DAT);
    // using linear interpolation we obtain the value of the read in ppm in the interval [0, 2000] 
    float ppm = 2000*((val-400)/(2000-400));
    char s_val[32];
    floatToAscii(ppm, s_val);
    sendAttributeData("CO2", "PPM", s_val);
    
   // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      lcd.print("CO2: ");
      lcd.print(s_val);
      lcd.print(" ppm");
      delay(100);
    }
  }
  
  
// -----------------------------------

  if(SEN_MOI)
  {
    int val = analogRead(PIN_SEN_MOI_DAT);
    float percent = (1-(val/1024.))*100.;
    char s_val[32];
    floatToAscii(percent, s_val);
    sendAttributeData("Moisture", "Percent", s_val);
    
    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Moisture: ");
      lcd.setCursor(0,1);
      lcd.print(s_val);
      lcd.print(" %");
      delay(100);
    }
  
  }
  
// -----------------------------------

  if(SEN_PH)
  {
    int i;
    int code; 
    SensorValues data[_PH_N_FIELDS_VALUES];
    SensorValues *ptr_data = data;
       
    // this is self holding (the sleep time is 1400ms)
    code = sen_atlas_ptr->getFormatedReadings(PH, ptr_data); 
 
    if(code == 1 && ((int)ptr_data) != 0){
      for(i=0; i < _PH_N_FIELDS_VALUES; i++){
        sendAttributeData(ptr_data[i].s_name, ptr_data[i].s_unit, ptr_data[i].s_value);  
      }
    }
      
    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      char msg[30];
      sprintf(msg,"%s: %d %s", ptr_data[0].s_name, ptr_data[0].s_value, ptr_data[0].s_unit); 
      lcd.print(msg);
      delay(100);
    }

    delete ptr_data; 
  
  }
  
// -----------------------------------
  
  if(SEN_EC)
  {
    int i;
    int code; 
    SensorValues data[_EC_N_FIELDS_VALUES];
    SensorValues *ptr_data = data;
       
    // this is self holding (the sleep time is 1400ms)
    code = sen_atlas_ptr->getFormatedReadings(EC, ptr_data); 
 
    if(code == 1 && ((int)ptr_data) != 0){
      for(i=0; i < _EC_N_FIELDS_VALUES; i++){
        sendAttributeData(ptr_data[i].s_name, ptr_data[i].s_unit, ptr_data[i].s_value);  
      }
    }
      
    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      char msg[30];
      sprintf(msg,"%s: %d %s", ptr_data[0].s_name, ptr_data[0].s_value, ptr_data[0].s_unit); 
      lcd.print(msg);
      delay(100);
    }

    delete ptr_data;  
  
  }// SEN_EC
  
// -----------------------------------  
  
  if(SEN_ORP)
  {
    
    int i;
    int code; 
    SensorValues data[_ORP_N_FIELDS_VALUES];
    SensorValues *ptr_data = data;
       
    // this is self holding (the sleep time is 1400ms)
    code = sen_atlas_ptr->getFormatedReadings(ORP, ptr_data); 
 
    if(code == 1 && ((int)ptr_data) != 0){
      for(i=0; i < _ORP_N_FIELDS_VALUES; i++){
        sendAttributeData(ptr_data[i].s_name, ptr_data[i].s_unit, ptr_data[i].s_value);  
      }
    }
    
    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      char msg[30];
      sprintf(msg,"%s: %d %s", ptr_data[0].s_name, ptr_data[0].s_value, ptr_data[0].s_unit); 
      lcd.print(msg);
      delay(100);
    }

    delete ptr_data;  
    
  }
  
// -----------------------------------

  if(SEN_OD)
  {
    int i;
    int code; 
    SensorValues data[_OD_N_FIELDS_VALUES];
    SensorValues *ptr_data = data;
       
    // this is self holding (the sleep time is 1400ms)
    code = sen_atlas_ptr->getFormatedReadings(OD, ptr_data); 
 
    if(code == 1 && ((int)ptr_data) != 0){
      for(i=0; i < _OD_N_FIELDS_VALUES; i++){
        sendAttributeData(ptr_data[i].s_name, ptr_data[i].s_unit, ptr_data[i].s_value);  
      }
    }
    
    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      char msg[30];
      sprintf(msg,"%s: %d %s", ptr_data[0].s_name, ptr_data[0].s_value, ptr_data[0].s_unit); 
      lcd.print(msg);
      delay(100);
    }

    delete ptr_data;  
    
  }
  
// -----------------------------------
  
  if(SEN_RGB)
  {
    String td_value = "";
    int sensor_data[8] = {0,0,0,0,0,0,0,0}; // R, G, B, lxr, lxg, lxb, lxtoal, lxbeyond
    int sensor_data_index = 0;
    boolean sensor_stringcomplete = false;
   
    soft_serial->print("R");   
    
    while (soft_serial->available()) 
    {
      char inchar = (char)soft_serial->read();            
      if(inchar == ',')
      {
        sensor_data[sensor_data_index++] = td_value.toInt(); // values range from 0 to 255        
        td_value = "";       
      } 
      else if (inchar == '\r') 
      {
        sensor_data[sensor_data_index] = td_value.toInt(); // values range from 0 to 255
        td_value = "";
        sensor_stringcomplete = true;
        sensor_data_index = 0;
        
      }else{       
        td_value += inchar;      
      }
    } 
    
    
    if (sensor_stringcomplete)
    {
      String msg = ""; // this is just a workaround
      char r [3];
      itoa(sensor_data[0], r, 10);
      sendAttributeData("R", "color", r);
      msg.concat("R");
      msg.concat(r);
      char g [3];
      itoa(sensor_data[1], g, 10);        
      sendAttributeData("G", "color", g);
      msg.concat("|G");
      msg.concat(r);
      char b [3];
      itoa(sensor_data[2], b, 10);       
      sendAttributeData("B", "color", b);
      msg.concat("|B");
      msg.concat(r);
      char lxr [4];
      itoa(sensor_data[3], lxr, 10);        
      sendAttributeData("lxr", "color", lxr);
      char lxg [4];
      itoa(sensor_data[4], lxg, 10);        
      sendAttributeData("lxg", "color", lxg);
      char lxb [4];
      itoa(sensor_data[5], lxb, 10);        
      sendAttributeData("lxb", "color", lxb);
      char lxtotal [4];
      itoa(sensor_data[6], lxtotal, 10);        
      sendAttributeData("lxtotal", "color", lxtotal);
      char lxbeyond [4];
      itoa(sensor_data[7], lxbeyond, 10);        
      sendAttributeData("lxbeyond", "color", lxbeyond); 
    
      // -----------------------------------
      if(LCD_ON){
        char buf[30];
        lcd.clear();
        lcd.setCursor(0,0);
        char type_s[] = "RGB Sensor: ";
        lcd.print(type_s);
        lcd.setCursor(0,1);
        msg.toCharArray(buf,30);
        lcd.print(buf);
        delay(100);
      }      
    } 
  }
  
// -----------------------------------
  
  if (SEN_SHT10)
  {
  float temperature;
  char s_temperature[32];
  temperature = sen_sht10->readTemperatureC();
  floatToAscii(temperature, s_temperature);
  sendAttributeData("SoilTemperature", "Celsius", s_temperature); 
  
  float humidity;
  char s_humidity[32];
  humidity = sen_sht10->readHumidity();
  floatToAscii(humidity, s_humidity);
  sendAttributeData("SoilHumidity", "Percent", s_humidity);  
  

    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      char msg_1[30];
      char msg_2[30];
      
      lcd.setCursor(0,0);
      lcd.print("Soil temp: ");
      lcd.setCursor(0,1);
      lcd.print(s_temperature);
      delay(100);
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Soil Humidity: ");
      lcd.setCursor(0,1);
      lcd.print(s_humidity);
      lcd.print(" %");
      delay(100);
    }
  
  }
    
// -----------------------------------

  if (SEN_AM2315)
  {
    float temperature = sen_am2315->readTemperature();
    char s_temperature[32];
    floatToAscii(temperature, s_temperature);
    sendAttributeData("AirTemperature", "Celsius", s_temperature); 
    
    float humidity = sen_am2315->readHumidity();
    char s_humidity[32];
    floatToAscii(humidity, s_humidity);
    sendAttributeData("AirHumidity", "Percent", s_humidity); 

    // -----------------------------------
    if(LCD_ON){
      lcd.clear();
      char msg_1[30];
      char msg_2[30];
      lcd.setCursor(0,0);
      lcd.print("Air Temp: ");
      lcd.setCursor(0,1);
      lcd.print(s_temperature);
      delay(100);      
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Air Humidity: ");
      lcd.setCursor(0,1);
      lcd.print(s_humidity);
      lcd.print(" %");
      delay(100);
    }

  }
    
  clock->getTime();
  char time[20];
  sprintf(time, "%d-%d-%d %d:%d:%d",
    clock->year, 
    clock->month, 
    clock->dayOfMonth, 
    clock->hour, 
    clock->minute, 
    clock->second);
  sendAttributeData("RTCTIME","DD-MM-YY|hh-mm-ss",time); 
  
  delay(200);
  //delay(1000);
  
} // lopp()


//////////////////////////////////////////////////////////////////////
//EOF
