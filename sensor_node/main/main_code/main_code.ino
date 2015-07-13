#include <IRTemp.h>
#include <DHT.h>
#include <ENV_TMP.h>
#include <DFR_CO2.h>
#include <AtlasProbes.h> 
#include <XBee.h>       // xbee API Mode

#include <Wire.h>  // enable I2C communication channel



//////////////////////////////////////////////////////////////////////

//XBee:
#define TX_DELAY 2000 //in miliseconds
#define TX_PACKET_BUFFER_SIZE 84

//Sensor modules:
#define SEN_IRT     0 // IR temperature / leaf temperature
#define SEN_TPS     0 // External temperature / soil temperature
#define SEN_TPA     0 // External temperature / ambient temperature
#define SEN_CO2     0 // CO2
#define SEN_CO2_MH  1 // CO2 MH
#define SEN_MOI     0 // Soil moisture
#define SEN_PH      0 // Ph 
#define SEN_EC      0 // Electrical Conductivity
#define SEN_ORP     0 // Oxidation-Reduction Potential 
#define SEN_OD      0 // Dissolved Oxygen ( "DO" is a reserved word in c/c++ programing language)

//Pin assignment:
#define PIN_SEN_TPS_DAT    2 // analog in
#define PIN_SEN_CO2_DAT    3 // analog in
#define PIN_SEN_MOI_DAT    1 // analog in
#define PIN_SEN_CO2_MH_DAT 0 // analog in

#define PIN_SEN_TPA_DAT   2   // digital in
#define PIN_SEN_IRT_CLK   6   // digital in
#define PIN_SEN_IRT_DAT   7   // digital in
#define PIN_SEN_IRT_ACQ   8   // digital out
#define PIN_SEN_CO2_SIG   -1  // digital in / not currently used

//Fiware Entity:
#define DEVICE_TYPE "Zone"
#define DEVICE_ID "ZoneX"

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
  
  Serial.begin(9600);          // enable serial port
  xbee.setSerial(Serial);      // xbee comunication to serial
  Wire.begin();                // enable I2C port
  
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
  
  
  delay(2000);
}

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
  }
  
// -----------------------------------

  if(SEN_TPS)
  {
    float val = sen_tps_ptr->readTemperature();
    char s_val[32];
    floatToAscii(val, s_val);
    sendAttributeData("SoilTemp", "Celsius", s_val);
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
    sendAttributeData("AmbientTemp", "Celsius", s_val_1);
    sendAttributeData("Humidity", "Percent", s_val_2);
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
  }
  
// -----------------------------------

  if(SEN_MOI)
  {
    int val = analogRead(PIN_SEN_MOI_DAT);
    float percent = (1-(val/1024.))*100.;
    char s_val[32];
    floatToAscii(percent, s_val);
    sendAttributeData("Moisture", "Percent", s_val);
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
    
  delete ptr_data;
    
  }
  delay(200);
  //delay(1000);
}



