#ifndef ENV_TMP_H
#define ENV_TMP_H
#if ARDUINO >= 100
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

/* ENV-TMP library 

BSD license
written by Introsys, SA
*/

class ENV_TMP {
 private:
  uint8_t _pin;

 public:
  ENV_TMP(uint8_t pin);
  float readTemperature(bool S=false);
  float convertCtoF(float);
  float convertFtoC(float);
};
#endif
