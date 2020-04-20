
#include <MsTimer2.h>

int led_pin = 13;
int unlock_pin = 5; // to RELAY_EN line on relay board 
int accept_pin = 4; // GPIO16 (physical pin number) from Raspberry Pi
int doorswitch_pin = 3; // DOORSW_EN on glue board JP3
int doorled_en_pin = 2; // DOORLED_EN pin on glue board JP3
// Arduino D0/RX goes to RFIDTX on glue board JP3
// Arduino D1/TX goes to TO_RPI_RXD on blue board JP3

// state of unlock output signal, logic is active high
boolean unlock_state = LOW;
// Set when unlock signal is activated, counts down and deactivates
// unlock signal when count reaches zero.
int unlock_countdown = 0;
// time for unlock signal to remain on once activated
int unlock_on_interval = 500;

// state of door LED, logic is active high
boolean doorled_state = LOW;
// Set when door LED is activated, counts down and LED is turned of at 0
int doorled_countdown = 0;
// time for door LED to remain on, in hundredths of a second
int doorled_on_interval = 500;

// last seen state of door switch, logic is active low
boolean last_doorswitch_state = HIGH;

// last seen state of Raspberry Pi GPIO 16, logic active high
// Raspberry Pi raises GPIO 16 to a high state when an entry code
// is accepted.
boolean last_accept_state = LOW;

// timer interrupt service routine to update system state
// 
void update_state() {
  boolean activate_unlock = LOW;

  // update door LED state
  digitalWrite(doorled_en_pin,doorled_state);
  if ( doorled_countdown > 0 ) {
    doorled_countdown = doorled_countdown - 1;
    if ( doorled_countdown == 0) {
      doorled_state = LOW;
    }
  }
  // update door switch state
  // If door switch is asserted and door LED is inactive, activate door LED.
  // Since logic is active low, one wants the last state to be high 
  // and the new state to be low.
  boolean new_doorswitch_state = digitalRead(doorswitch_pin);
  if ( last_doorswitch_state && ( ! new_doorswitch_state ) ) {
    if ( ! doorled_state ) {
      doorled_state = HIGH;
      doorled_countdown = doorled_on_interval;
      activate_unlock = HIGH;
    }
  }
  // update accept state
  boolean new_accept_state = digitalRead(accept_pin);
  if ( new_accept_state && ( ! last_accept_state ) ) {
    activate_unlock = HIGH;
  }
  //   
  // update unlock state 
  if ( unlock_countdown > 0 ) {
    unlock_countdown = unlock_countdown - 1;
    if ( unlock_countdown == 0 ) {
      unlock_state = LOW;
    }
  }
  if ( activate_unlock ) {
    unlock_state = HIGH;
    unlock_countdown = unlock_on_interval;
  }
  digitalWrite(unlock_pin, unlock_state);
}
// 
void setup() {
  // put your setup code here, to run once:
  pinMode(led_pin, OUTPUT);
  pinMode(doorswitch_pin, INPUT_PULLUP);
  pinMode(doorled_en_pin, OUTPUT);
  pinMode(unlock_pin, OUTPUT);
  pinMode(accept_pin, INPUT);
  MsTimer2::set(10, update_state);
  MsTimer2::start();
  Serial.begin(9600);
}

int read_byte = 0;
bool byte_waiting = false;

void loop() {
  int led_blink_phase = millis() % 1000;

  // do a LED blink just to let people know somebody's home
  if ( led_blink_phase < 100 ) {
    digitalWrite(led_pin, HIGH);
  } else {
    digitalWrite(led_pin, LOW);
  }
  // relay bytes incoming on RX to TX, for Raspberry Pi to read
  if ( Serial.available() > 0 ) {
    read_byte = Serial.read();
    byte_waiting = true;
  }
  if ( byte_waiting ) {
    if ( Serial.availableForWrite() > 0 ) {
      Serial.write(read_byte);
      byte_waiting = false;
    }
  }
}
