#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();

#ifndef STASSID
#define STASSID "xxxx"
#define STAPSK  "xxx"
#endif

unsigned int localPort = 5005;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,
char  ReplyBuffer[14];       // a string to send back

char x_val[11];
char y_val[11];
char z_val[11];

WiFiUDP Udp;
IPAddress ip(192, 168, 7, 54);

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", localPort);
  Udp.begin(localPort);

  Serial.println("Adafruit MMA8451 test!");
  

  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("MMA8451 found!");
  
  mma.setRange(MMA8451_RANGE_2_G);
  
  Serial.print("Range = "); Serial.print(2 << mma.getRange());  
  Serial.println("G");
}

void loop() {
  // put your main code here, to run repeatedly:

  mma.read();
  Serial.println(mma.x/4);
  sprintf(x_val, "%ld", mma.x/4);
  sprintf(y_val, "%ld", mma.y/4);
  sprintf(z_val, "%ld", mma.z/4);
  Serial.print("Sending packet to: ");
  Serial.println(ip);
  Udp.beginPacket(ip, localPort);
  Udp.write("{'x': ");
  Udp.write(x_val);
  Udp.write(", 'y': ");
  Udp.write(y_val);
  Udp.write(", 'z': ");
  Udp.write(z_val);
  Udp.write("}");
  Udp.endPacket();

  delay(1000);

}
