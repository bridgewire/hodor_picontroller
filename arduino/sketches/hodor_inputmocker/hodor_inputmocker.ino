void setup() {
  //Initialize serial and wait for port to open:
  pinMode(LED_BUILTIN,OUTPUT);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

// Emulate RFID reader output:
// (STX)
void write_sample(int d) {
  int k;

  Serial.write(2); // STX (ASCII decimal 02)
  // print twelve hex digits based on 'd'
  for ( k = 0; k < 12; k++ ) {
    int digit;

    digit = d % 15; // take last four bits of input
    if ( d < 10 ) {
      Serial.write(48+digit);
    } else {
      Serial.write(55+digit);
    }
  }
  Serial.write(3);   // ETX (ASCII decimal 03)
  Serial.write(13);  // CR
  Serial.write(10);  // LF
}

void loop() {
  // put your main code here, to run repeatedly:
  int d;

  for ( d = 0; d < 16; d++ ) {
    digitalWrite(LED_BUILTIN,HIGH);
    write_sample(d);
    delay(500);
    digitalWrite(LED_BUILTIN,LOW);
    delay(9500);    
  }
}
