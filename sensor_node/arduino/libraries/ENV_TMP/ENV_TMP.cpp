/* ENV-TMP library 

BSD license
written by Introsys, SA
*/

#include "ENV_TMP.h"

ENV_TMP::ENV_TMP(uint8_t pin)
{

  _pin = pin;
  digitalWrite(_pin, LOW);

}

//boolean S == Scale.  True == Farenheit; False == Celcius
float ENV_TMP::readTemperature(bool S)
{
  float f;
  f = analogRead(_pin); 
  f *= .0048;		     // we are using .0048 because this device is running at 5 volts
  f *= 1000.0;		     //convert volts to millivolts
  f = 0.0512 * f - 20.5128;  //the equation from millivolts to temperature in Celcius

  if(S)
    f = convertCtoF(f);

  return f;
}

float ENV_TMP::convertCtoF(float c) {
	return c * 9 / 5 + 32;
}

float ENV_TMP::convertFtoC(float f) {
  return (f - 32) * 5 / 9; 
}

