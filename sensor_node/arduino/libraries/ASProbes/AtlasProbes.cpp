#include "AtlasProbes.h"

/* AtlasProbes library

BSD license
Written by Introsys, SA
based on code examples from Atlas Scientific
*/


// TODO doc
AtlasProbes::AtlasProbes(){

  code=0;                     //used to hold the I2C response code.
  in_char=0;                  //used as a 1 byte buffer to store in bound bytes from the EC Circuit.
  i=0;                        //counter used for ec_data array.
  int time=1400;              //used to change the delay needed depending on the command sent to the EZO Class EC Circuit (default 1400ms)

}// AtlasProbes()

// ---------------------------------------------------------------------------------------------------

//
int AtlasProbes::probeReading(int address){

    int error;
    Wire.flush();                            // clear the communication channel.

    delay(250);
    memset(probe_data, 0, sizeof(probe_data));

    Wire.beginTransmission(address);         // call the circuit by its ID number.
    Wire.write('r');                         // send a READ ('r') command to the EC Circuit define above and returns a single reading
    error = Wire.endTransmission();          // end the I2C data transmission.

    delay(1000); 		             // give time to receive the response to the I2C query

    //Serial.print("\n\n\n");
    //Serial.print(error);
    //Serial.print("\n\n\n");

    if (error == 0){			     // verify that the device exists in the I2C channel
	// !! IMPORTANT !!
	delay(time);                         // wait the correct amount of time for the circuit to complete its instruction.
	Wire.requestFrom(address, 48, 1);    // call the circuit and request 20 bytes (this may be more then we need).
	code = Wire.read();                  // the first byte is the response code, we read this separately.
	while (Wire.available()) {           // are there bytes to receive.
	in_char = Wire.read();               // receive a byte.
	probe_data[i] = in_char;             // load this byte into our array.
	i += 1;                              // incur the counter for the array element.
	if (in_char == 0) {                  // if we see that we have been sent a null command.
	    i = 0;                           // reset the counter i to 0.
	    Wire.endTransmission();          // end the I2C data transmission.
	    break;                           // exit the while loop.
	}
	}

	// 1 means the command was successful
	// 2 means the command has failed
	// 254 means the command has not yet been finished calculating
	// 255 means there is no further data to send
    }else {
	code = 2;
    }
    return code;

}// getProbeReading

// ---------------------------------------------------------------------------------------------------

//
int AtlasProbes::getRawProbeReading(SensorType type, char *data){

    int code = probeReading(type);
    data = &probe_data[0]; // pointer to the data
    return code;

}//getRawProbeReading(int address, char *data){


// ---------------------------------------------------------------------------------------------------

int AtlasProbes::getFormatedReadings(SensorType type, SensorValues* reading){

    int code;
    switch(type){
    case EC:
        code = probeReading(EC);
        parseECValues(reading);
        return code;
    case ORP:
        code = probeReading(ORP);
        parseORPValues(reading);
        return code;
    case OD:
        code = probeReading(OD);
        parseODValues(reading);
        return code;
    case PH:
        code = probeReading(PH);
        parsePHValues(reading);
        return code;
    default:
        return 0;

    }
}// getFormatedReadings(SensorType type, SensorValues* reading)

// ---------------------------------------------------------------------------------------------------

int AtlasProbes::sendATCommand(char* command){

    // TODO send commands to the EZO Circuit board and return the operation result (Error - *ER<CR> or Success - *OK<CR>)

    /* Command List
     C
     CAL
     Factory
     I
     I2C
     K
     L
     Name
     O
     R
     Response
     Serial
     Sleep
     Status
     T
     */
    return true;
} // AtlasProbes::sendATCommand

// ---------------------------------------------------------------------------------------------------
// the functions that follow will break up the CSV strings into its individual parts.(e.g. EC|TDS|SAL|SG )
// this is done using the C command “strtok”.

void AtlasProbes::parseECValues(SensorValues* data){

   char *ec;
   char *tds;
   char *sal;
   char *sg;

   ec = strtok(probe_data, ",");     // let's pars the string at each comma.
   tds=strtok(NULL, ",");            // let's pars the string at each comma.
   sal=strtok(NULL, ",");            // let's pars the string at each comma.
   sg=strtok(NULL, ",");             // let's pars the string at each comma.

   data[0].s_name = "EC";            // We now print each value we parsed separately.
   data[0].s_unit = "EC Unit";
   data[0].s_value = ec;             // this is the EC value.

   data[1].s_name = "TDS";           // We now print each value we parsed separately.
   data[1].s_unit = "TDS Unit";
   data[1].s_value = tds;            // this is the TDS value.

   data[2].s_name = "SAL";           // We now print each value we parsed separately.
   data[2].s_unit = "SAL Unit";
   data[2].s_value = sal;            // this is the salinity value.

   data[3].s_name = "SG";            // We now print each value we parsed separately.
   data[3].s_unit = "SG Unit";
   data[3].s_value = sg;             // this is the specific gravity.

}// parseECValues(SensorValues* data)

// ---------------------------------------------------------------------------------------------------

void AtlasProbes::parseORPValues(SensorValues* data){
    data[0].s_name  = "ORP";
    data[0].s_unit = "";
    data[0].s_value = probe_data;
}// parseORPValues(SensorValues* data)

// ---------------------------------------------------------------------------------------------------

void AtlasProbes::parseODValues(SensorValues* data){

    char *od;
    char *sat;
    sat=strtok(probe_data, ",");           //let's pars the string at each comma
    od=strtok(NULL, ",");                  //let's pars the string at each comma

    data[0].s_name = "SAT";                // We now print each value we parsed separately.
    data[0].s_unit = "";
    data[0].s_value = sat;                 // this is the EC value.

    data[1].s_name = "OD";                 // We now print each value we parsed separately.
    data[1].s_unit = "";
    data[1].s_value = od;                  // this is the TDS value.

}// parseODValues(SensorValues* data)

// ---------------------------------------------------------------------------------------------------

void AtlasProbes::parsePHValues(SensorValues* data){

    data[0].s_name = "PH";
    data[0].s_unit = "";
    data[0].s_value = probe_data;

}// parsePHValues(SensorValues* data)

//EOF

