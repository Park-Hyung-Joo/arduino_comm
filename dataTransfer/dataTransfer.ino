#include <SPI.h>
#define _MAXBYTES 127 // max length of bytesArray -> 최대 255까지 가능
//CLK : 13 DATA(MOSI): 11
const int EN = 10;
const int RST = 9;
byte bitStream[_MAXBYTES];
byte len;
byte isRight;
SPISettings set_obj(125000, MSBFIRST, SPI_MODE1); 
/*
125000: CLK freqency -> 125000, 250000, 500000, 1000000, 2000000, 4000000 가능 단 다른 핀의 펄스폭이 clk 주기 보다 넓을 수 있음( 3~7us )
MSBFIRST -> most significant bit first
LSBFIRST -> least significant bit first
SPI_MODE0: CLK idle = low, bit transfer = rising edge
SPI_MODE1: CLK idle = low, bit transfer = falling edge
SPI_MODE2: CLK idle = HIGH, bit transfer = falling edge
SPI_MODE3: CLK idle = HIGH, bit transfer = rising edge
*/
void setup() {
  // put your setup code here, to run once:
  pinMode(EN, OUTPUT);
  pinMode(RST, OUTPUT);
  digitalWrite(EN, LOW);
  digitalWrite(RST, LOW);
  Serial.begin(115200);
  SPI.begin();
  SPI.beginTransaction(set_obj);
 // pinMode(LED_BUILTIN, OUTPUT);
 // digitalWrite(LED_BUILTIN, 0);
  Serial.write(1);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(!Serial.available()) delay(1);
  len = Serial.read();
  Serial.readBytes(bitStream, len);
  Serial.write(bitStream, len);

  while(!Serial.available()) delay(1);
  isRight = Serial.read();
  if(isRight == 1){
    //칩과 통신 시작 전에 RST핀에서 펄스 출력
    digitalWrite(RST, HIGH);
    delayMicroseconds(6);
    digitalWrite(RST,LOW);
    //통신 시작
    digitalWrite(EN, HIGH);
    SPI.transfer(bitStream,len);
    // SPI.transfer(0b00100100);
    digitalWrite(EN, LOW);
    //칩과의 통신 끝
    //통신이 끝난것을 파이썬 프로그램에 알림
    Serial.write(1);
  }
  else{
    while(1);
    }
  delay(10);
}
