#ifndef ATLAS_PROBES_H
#define ATLAS_PROBES_H

#if ARDUINO >= 100
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

#include <Wire.h>  // enable I2C communication channel


/* AtlasProbes library

BSD license
Written by Introsys, SA
based on code examples from Atlas Scientific
*/

// This difine the number of parameters readed by each sensor (e.g. The EC sensor reads 4 diferent parameters)
#define _EC_N_FIELDS_VALUES  4
#define _ORP_N_FIELDS_VALUES 1
#define _PH_N_FIELDS_VALUES  1
#define _OD_N_FIELDS_VALUES  2

#define byte uint8_t

// each field has to be a unique number, should preferably given in sequence
typedef enum {
  EC  = 100,  // I2C ID number for EZO EC Circuit (default is 100)
  ORP = 101,  // I2C ID number for EZO ORP Circuit (default is 98)
  PH  = 102,  // I2C ID number for EZO PH Circuit (default is ??) TODO TBD
  OD  = 103   // I2C ID number for EZO DO Circuit (default is ??) TODO TBD
} SensorType;


typedef struct {
   char* s_name;
   char* s_unit;
   char* s_value;

} SensorValues; // holds the parameter name and value (e.g. name = 'salt', value = 100)

class AtlasProbes {

///////////////////////////////////////////////////////////////////////////////////////

private:

  char probe_data[48]; // the max value needed by the EC reading is 32 Bytes

  int sensor_type;
  int time;

  byte code;
  byte in_char;
  byte i;

  void parseECValues(SensorValues* data);
  void parseORPValues(SensorValues* data);
  void parsePHValues(SensorValues* data);
  void parseODValues(SensorValues* data);
  int  probeReading(int address);

///////////////////////////////////////////////////////////////////////////////////////

public:

  AtlasProbes();
  int getFormatedReadings(SensorType type, SensorValues *reading);
  int getRawProbeReading(SensorType type, char *data);
  int sendATCommand(char* command);

  inline void string_pars();

};


#endif
//EOF
