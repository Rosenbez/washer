/*
 *  This sketch sends accelerometer data over UDP to a server.
 *
 */
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();

// WiFi network name and password:
const char * networkName = "xxx";
const char * networkPswd = "xxx";

//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * udpAddress = "192.168.1.187";
const int udpPort = 5005;

//Are we currently connected?
boolean connected = false;
float voltage;
//The udp library class
WiFiUDP udp;

char x_val[11];
char y_val[11];
char z_val[11];
char batt[15];

void setup(){
  // Initilize hardware serial:
  Serial.begin(115200);
  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("MMA8451 found!");
  //Connect to the WiFi network
  connectToWiFi(networkName, networkPswd);
}

void loop(){
  //only send data when connected
  if(connected){
    //Send a packet
    Serial.print("reading sensor");
    mma.read();
    sprintf(x_val, "%f", mma.x_g);
    sprintf(y_val, "%f", mma.y_g);
    sprintf(z_val, "%f", mma.z_g);
    Serial.printf("  x: %s, y: %s, z: %s", x_val, y_val, z_val);
    Serial.println();
    
    voltage = analogRead(A13)*2*(3.3/4096);
    Serial.printf("Bat voltage: %f", voltage);
    sprintf(batt, "%f", voltage);
    Serial.println();
    
    udp.beginPacket(udpAddress,udpPort);
    Serial.print("sending udp packet");
    Serial.println();
    char databuff[90];
    sprintf(
      databuff, 
      "{'x': %s, 'y': %s, 'z': %s, 'batt': %s}",
      x_val, y_val, z_val, batt
    );
    write_buff(databuff, udp);
    udp.endPacket(); 
  }
  //Wait for 1 second
  delay(1000);
}

void write_buff(char* buff, WiFiUDP& udp) {
   
   for (int i = 0; buff[i] != 0; i++) {
     udp.write((uint8_t)buff[i]);
   }
}

void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  
  //Initiate connection
  WiFi.begin(ssid, pwd);

  Serial.println("Waiting for WIFI connection...");
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case SYSTEM_EVENT_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
          udp.begin(WiFi.localIP(),udpPort);
          connected = true;
          break;
      case SYSTEM_EVENT_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;
          break;
      default: break;
    }
}
