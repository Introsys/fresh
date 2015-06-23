/* DFR-ITM library 

BSD license
written by Introsys, SA
*/

#include "DFR_ITM.h"

DFR_ITM::DFR_ITM(uint8_t data_pin, uint8_t clock_pin)
{
  _data_pin = data_pin;
  _clock_pin = clock_pin;

  memset(_data_buf,0,sizeof(_data_buf));
}

float DFR_ITM::readValue()
{
  int i,j,PinState,tempData;
  int *p;

  for(i=0;i<5;i++)
  {
    for(j=0;j<8;j++)
    {
      do
      {
        PinState = digitalRead(_clock_pin);
      }
      while(PinState);
      delayMicroseconds(100);
      PinState = digitalRead(_data_pin);
      if(1 == PinState) 
         tempData = (tempData<<1 & 0xfe)+1;
      else
         tempData = (tempData<<1 & 0xfe);
      do
      {
        PinState = digitalRead(_clock_pin);
      }
      while(PinState != 1);
    }
    *p++ = tempData;
  }

  tempData = _data_buf[1]*256 + _data_buf[2];
  float realTemp = (float)tempData/16-273.15;

  return realTemp; //in celcius
}

