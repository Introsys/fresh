#ifndef DFR_ITM_H
#define DFR_ITM_H
#if ARDUINO >= 100
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

/* DFR-ITM library 

BSD license
written by Introsys, SA
based on code from http://www.dfrobot.com/wiki/index.php?title=Infrared_thermometer_%28SKU:SEN0093%29
*/

class DFR_ITM {

 private:

  uint8_t _clock_pin; //digital in
  uint8_t _data_pin;  //digital in

  int _data_buf[5];

 public:

  DFR_ITM(){};
  DFR_ITM(uint8_t data_pin, uint8_t clock_pin);
  float readValue();

};
#endif
