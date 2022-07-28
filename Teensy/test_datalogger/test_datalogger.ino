/*
  FSR Datalogger

  The circuit:
  FSR voltage dividor w/ potentiometer.

  Created 26 Jul 2022
  by Trevor Jehl
*/

#include <SD.h>
#include <SPI.h>
#include <TimeLib.h>

const int chipSelect = BUILTIN_SDCARD;

void initializeCard() {
  Serial.print("Initializing SD card...");
  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    while (1) {
      // No SD card, so don't do anything more - stay stuck here
    }
  }

  // Delete the old datalog.
  while (!SD.remove("datalog.txt")) {
    Serial.println("Failed to delete file.");
    delay(100);
  }

  Serial.println("Card initialized.");
}

void setup() {
  //UNCOMMENT THESE TWO LINES FOR TEENSY AUDIO BOARD:
  SPI.setMOSI(7);  // Audio shield has MOSI on pin 7
  SPI.setSCK(14);  // Audio shield has SCK on pin 14

  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect.
  }
  // Initialize SD card.
  initializeCard();
}


String readFSR() {
  // read three sensors and append to the string:
  int FSRPin = A3;
  int sensor = analogRead(FSRPin);
  
  // Return the string of the sensor reading for
  // datalog writing convenience
  return String(sensor);
}


void writeDataSD(String dataString) {
  // open the file
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    Serial.println(dataString);
  }
  else {
    // if the file isn't open, pop up an error:
    Serial.println("Error opening datalog.txt");
  }
  
}


void loop() {
  //  Serial.println(hour());
  // make a string for assembling the data to log:
  String dataString = "";
  // Add 'millis;' to the start of the datafile, 
  // useful for determining sample rate
  dataString += String(millis());
  dataString += String("; ");
  
  // Read the value of the FSR, add it to data to be logged
  String FSR_Reading = readFSR();
  dataString += String(FSR_Reading);

  // Write dataString to a new line in txt file
  writeDataSD(dataString);
  delay(20); // run at a reasonable not-too-fast speed
}