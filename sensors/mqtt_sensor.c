#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>


// Wifi
const char* ssid                = "frugmunster";
const char* ssid_password       = "";

// Mqtt
const char* mqtt_server         = "hassbian.local";
const int mqtt_port             = 1883;
const char* mqtt_id             = "fstakem98765";
const char* mqtt_user           = "fstakem";
const char* mqtt_password       = "password";
const char* mqtt_topic          = "/dev/test";

// Mqtt commands
const char* cmd_tx_on           = "";
const char* cmd_tx_off          = "";

// State
const int state_tx_on           = 0;
const int state_tx_off          = 1;

// Other
const char* test_msg            = "fred";  
const int mqttMaxConnAttempts   = 3;


// Globals
WiFiClient wifiClient;
PubSubClient client(wifiClient);
int state = state_tx_on;


const byte ledPin = 0;
unsigned long last_msg_time;
char message_buff[100];

void handle_msg(char* topic, byte* payload, unsigned int length);


void setup_wifi() {

    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, ssid_password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.println(WiFi.ping(mqtt_server));
}

void mqtt_connect() {
    int mqttConnAttempts = 0;

    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        mqttConnAttempts += 1;
        
        if (client.connect(mqtt_id)) {
            Serial.println("connected");
            client.publish(mqtt_topic, test_msg);
            client.subscribe(mqtt_topic);
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }

        if(mqttConnAttempts >= mqttMaxConnAttempts) {
            break;
        }
    }
}

void handle_msg(char* topic, byte* payload, unsigned int length) {
    int i = 0;

    Serial.println("Message arrived:  topic: " + String(topic));
    Serial.println("Length: " + String(length,DEC));

    for(i=0; i<length; i++) {
        message_buff[i] = payload[i];
    }
    message_buff[i] = '\0';

    String msgString = String(message_buff);

    Serial.println("Payload: " + msgString);
    
    /*
    if (msgString.equals(CMD_TX_OFF)) {
        state = STATE_TX_OFF;
    } else if (msgString.equals(CMD_TX_ON)) {
        state = STATE_TX_ON;
    }
    */
}

void handle_state() {
    if (state == state_tx_on) {
        if (millis() > (last_msg_time + 5000)) {
            digitalWrite(BUILTIN_LED, LOW);
            last_msg_time = millis();
            String pubString = test_msg;
            pubString.toCharArray(message_buff, pubString.length()+1);
            client.publish(mqtt_topic, message_buff);
            digitalWrite(BUILTIN_LED, HIGH);
        }
    } else if (state == state_tx_off) {
        
    }
}

void setup() {
    pinMode(BUILTIN_LED, OUTPUT);
    Serial.begin(9600);
    setup_wifi();
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(handle_msg);
}

void loop() {
    if (!client.connected()) {
        mqtt_connect();
    }
    handle_state();
    client.loop();
}


