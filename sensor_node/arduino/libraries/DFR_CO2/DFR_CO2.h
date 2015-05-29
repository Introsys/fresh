#ifndef DFR_CO2_H
#define DFR_CO2_H
#if ARDUINO >= 100
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

/* DFR-CO2 library 

BSD license
written by Introsys, SA
based on code from http://www.dfrobot.com/wiki/index.php/CO2_Sensor_SKU:SEN0159
*/

#define DC_GAIN (8.5)
#define READ_SAMPLE_INTERVAL (50) //define how many samples you are going to take in normal operation
#define READ_SAMPLE_TIMES (5) //define the time interval(in milisecond) between each samples in normal operation
#define ZERO_POINT_VOLTAGE (0.324) //define the output of the sensor in volts when the concentration of CO2 is 400PPM
#define REACTION_VOLTAGE (0.020) //define the voltage drop of the sensor when move the sensor from air into 1000ppm CO2

class DFR_CO2 {
 private:
  uint8_t _analog_pin;
  uint8_t _bool_pin;

  float CO2Curve[3] = {2.602,ZERO_POINT_VOLTAGE,(REACTION_VOLTAGE/(2.602-3))};
                                                     //two points are taken from the curve. 
                                                     //with these two points, a line is formed which is
                                                     //"approximately equivalent" to the original curve.
                                                     //data format:{ x, y, slope}; point1: (lg400, 0.324), point2: (lg4000, 0.280) 
                                                     //slope = ( reaction voltage ) / (log400 –log1000) 


 public:
  DFR_CO2(uint8_t analog_pin, uint8_t bool_pin);
  float readValue();
  int getPercentage(float volts);
};
#endif
