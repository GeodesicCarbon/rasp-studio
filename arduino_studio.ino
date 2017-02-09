[sourcecode language="cpp"]
/*  Arduino side of relay system, listens to USB for serial
*   data (char \n char) and sets the pin as per instruction
*/
void setup() {
  Serial.begin(9600);
  for (int i = 2; i <9; i++) {
    digitalWrite(i, HIGH);
    pinMode(i, OUTPUT);
  }

  void loop() {
    if (Serial.available()){
      Serial.println(setPin(Serial.read()-'0', Serial.read()-'0'));
    }
  }

  int setPin(int pin, int status) { //Toggles status of a pin 2-8
    if (pin < 2 || pin > 8) {
      return -1;
    }
    if (status == 0) {
      digitalWrite(pin, HIGH);
      return 0;
    } else if (status == 1) {
      digitalWrite(pin, LOW)
      return 1;
    } else {
      return -1;
    }
  }
}
[/sourcecode]
