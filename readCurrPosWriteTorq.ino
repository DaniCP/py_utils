// inslude the SPI library:
#include <SPI.h>
/*lee por puerto serie un valor 0-255 y configura la salida del potenciometro
           _______
  5v/10V -|A     W|- arduA1
supply0V -|B   Vdd|- 5V/10V
ardu gnd -|Vss SDO|- none
ardu gnd -|GND SDI|- ardu pin11
    pin10-|~CS CLK|- ardu pin13
      |_______|

curr_out - ardu A4
encoder_out - ardu A5
*/

#define CURRENT_PIN A4
#define ENCODER_PIN A5
byte buff[4]; //[c_high,c_low,pos_high,pos_low]

const int slaveSelectPin = 10;
int PotWiperVoltage = 1;
int RawVoltage = 0;
float Voltage = 0;

void setup() {
  Serial.begin(9600);
  pinMode(CURRENT_PIN, INPUT);
  pinMode(ENCODER_PIN, INPUT);
  // set the slaveSelectPin as an output:
  pinMode(slaveSelectPin, OUTPUT);
  // initialize SPI:
  SPI.begin();
}

void loop() {
  if (Serial.available()){
    char in = Serial.read();
    digitalPotWrite(in);
    formar_trama(read_curr(), read_pos());
    Serial.write(buff,4);
  }
}

/*
**** FUNCIONES ****
*/
void formar_trama(int curr, int pos){
   //[0,1,2,3]
   //[c_high,c_low,pos_high,pos_low]
  buff[1]=curr & 255;
  buff[0]= (curr >> 8) & 255;
  buff[3]= pos & 255;
  buff[2]= (pos >> 8) & 255;
}
int read_curr(){
  return analogRead(CURRENT_PIN);
}
int read_pos(){
  return analogRead(ENCODER_PIN);
}
void digitalPotWrite(byte value) {
  // take the SS pin low to select the chip:
  digitalWrite(slaveSelectPin, LOW);
  //  send in the address and value via SPI:
  SPI.transfer(value);
  // take the SS pin high to de-select the chip:
  digitalWrite(slaveSelectPin, HIGH);
}
