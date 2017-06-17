#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
 
// Wifi
#define SSID            "frugmunster"
#define SSID_PASSWORD   "xxxx"

// Mqtt
#define MQTT_SERVER     "server_name"
#define MQTT_PORT       1883
#define MQTT_ID         "me"
#define MQTT_USER       "fstakem"
#define MQTT_PASSWORD   "password"
#define MQTT_TOPIC      "test_topic"

// Mqtt commands
#define CMD_TX_ON       ""
#define CMD_TX_OFF      ""

// State
#define STATE_TX_ON     0  
#define STATE_TX_OFF    1 

// Other
#define TEST_MSG        "fred"   


// Globals
PubSubClient client;
int state = STATE_TX_ON;
const byte ledPin = 0;
unsigned long time;
char message_buff[100];


void setup() {
  Serial.begin(9600);
  client = PubSubClient(MQTT_SERVER, MQTT_PORT, handle_msg);
}

void connect() {
    if(!client.connected()) {
      // clientID, username, MD5 encoded password
      client.connect(MQTT_ID, MQTT_USER, MQTT_PASSWORD);
      client.publish(MQTT_TOPIC, TEST_MSG);
      client.subscribe(MQTT_TOPIC);
    }
}

void handle_msg(char* topic, byte* payload, unsigned int length) {
    int i = 0;

    //Serial.println("Message arrived:  topic: " + String(topic));
    //Serial.println("Length: " + String(length,DEC));

    for(i=0; i<length; i++) {
        message_buff[i] = payload[i];
    }
    message_buff[i] = '\0';

    String msgString = String(message_buff);

    //Serial.println("Payload: " + msgString);
    
    if (msgString.equals(CMD_TX_OFF)) {
        state = STATE_TX_OFF;
    } else if (msgString.equals(CMD_TX_ON)) {
        state = STATE_TX_ON;
    }
}

void handle_state() {
    if (state == STATE_TX_ON) {
        if (millis() > (time + 5000)) {
            time = millis();
            String pubString = TEST_MSG;
            pubString.toCharArray(message_buff, pubString.length()+1);
            client.publish(MQTT_TOPIC, message_buff);
        }
    } else if (state == STATE_TX_OFF) {
        
    }
}

void loop() {
    connect();
    handle_state();
    client.loop();
}


