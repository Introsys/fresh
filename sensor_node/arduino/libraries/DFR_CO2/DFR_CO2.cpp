/* DFR-CO2 library 

BSD license
written by Introsys, SA
*/

#include "DFR_CO2.h"

DFR_CO2::DFR_CO2(uint8_t analog_pin, uint8_t bool_pin)
{
  _analog_pin = analog_pin;
  _bool_pin = bool_pin;
}

float DFR_CO2::readValue()
{
  int i;
  float v=0;

  for (i=0;i<READ_SAMPLE_TIMES;i++)
  {
    v += analogRead(_analog_pin);
    delay(READ_SAMPLE_INTERVAL);
  }
  v = (v/READ_SAMPLE_TIMES)*5/1024 ;

  return v;  
}

int DFR_CO2::getPercentage(float volts)
{
  if ((volts/DC_GAIN )>=ZERO_POINT_VOLTAGE)
  {
    return -1;
  }
  else
  {
    return pow(10, ((volts/DC_GAIN)-CO2Curve[1])/CO2Curve[2]+CO2Curve[0]);
  }
}

