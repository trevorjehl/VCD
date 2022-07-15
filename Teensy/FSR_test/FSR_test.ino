/* 
Trevor Jehl, CNMC 2022
FSR simple testing sketch */
 
int fsrPin = A4;     // the FSR and 10K pulldown are connected to a0
int fsrReading;     // the analog reading from the FSR resistor divider
 
void setup(void) {
  // We'll send debugging information via the Serial monitor
  Serial.begin(9600);   
}
 
void loop(void) {
  fsrReading = analogRead(fsrPin);  
 
  Serial.println(fsrReading);     // the raw analog reading
 
  delay(100);
} 
