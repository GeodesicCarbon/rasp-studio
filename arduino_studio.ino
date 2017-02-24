const int ledPin = 12;
const int led2Pin = 13;
void setup(){
  for (int i = 2; i < 14; i++) {
    digitalWrite(i, HIGH);
    pinMode(i, OUTPUT);
  }
Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0) {
    relaySwitch(Serial.read() - '0');
  }
}

void relaySwitch(int command) {
  /*String msg = String("message: "); // Debugging
  msg += command/2+1;
  msg += " ";
  msg += command%2;
  msg += "\n";
  Serial.print(msg);*/
  if (command < 1 || command >26) {
    return;
  }
  digitalWrite(command/2+1, command%2);
}
