#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>


// Wifi
const char* SSID                    = "frugmunster";
const char* SSID_PASSWORD           = "xxx";

// Mqtt general
const char* MQTT_SERVER             = "hassbian.local";
const int MQTT_PORT                 = 1883;
const char* MQTT_ID                 = "fstakem98765";
const char* MQTT_USER               = "fstakem";
const char* MQTT_PASSWORD           = "password";

// Mqtt topics
const String MQTT_NODE_NAME         = "wemos_node/1";
const int NUM_OF_SENSORS            = 5;
const int mqtt_max_conn_attempts    = 3;

String get_data_topics[NUM_OF_SENSORS];
String get_tx_topics[NUM_OF_SENSORS];
String set_tx_topics[NUM_OF_SENSORS];
String set_tx_rate_ms_topic         = MQTT_NODE_NAME + "/tx_rate";
boolean sensor_tx_state[NUM_OF_SENSORS];

// Loop
unsigned long last_loop_time        = 0;
int loop_time_ms                    = 5000;

// Board variables
const byte ledPin                   = 0;

// Buffers
char tx_buff[100];
char rx_buff[100];
char topic_buff[200];


// Globals
WiFiClient wifi_client;
PubSubClient client(wifi_client);


void handle_msg(char* topic, byte* payload, unsigned int length);

void create_topics() {
    int i = 0;
    for(i = 0; i < NUM_OF_SENSORS; i++) {
        get_data_topics[i]  = MQTT_NODE_NAME + "/sensor/" + String(i) + "/get/data";
        get_tx_topics[i]    = MQTT_NODE_NAME + "/sensor/" + String(i) + "/get/tx";
        set_tx_topics[i]    = MQTT_NODE_NAME + "/sensor/" + String(i) + "/set/tx";
        set_tx_topics[i]    = MQTT_NODE_NAME + "/sensor/" + String(i) + "/set/tx";
        sensor_tx_state[i]  = false;
    }

    sensor_tx_state[0] = true;
}

void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(SSID);

    WiFi.begin(SSID, SSID_PASSWORD);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void mqtt_connect() {
    int mqtt_conn_attempts = 0;

    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        mqtt_conn_attempts += 1;
        
        if (client.connect(MQTT_ID, MQTT_USER, MQTT_PASSWORD)) {
            Serial.println("connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }

        if(mqtt_conn_attempts >= mqtt_max_conn_attempts) {
            break;
        }
    }
}

void mqtt_subscribe() {
    set_tx_rate_ms_topic.toCharArray(topic_buff, set_tx_rate_ms_topic.length()+1);
    client.subscribe(topic_buff);
    int i;

    for(i = 0; i < NUM_OF_SENSORS; i++) {
        set_tx_topics[i].toCharArray(topic_buff, set_tx_topics[i].length()+1);
        client.subscribe(topic_buff);
    }
}

void handle_msg(char* topic, byte* payload, unsigned int length) {
    int i = 0;

    for(i = 0; i < length; i++) {
        rx_buff[i] = payload[i];
    }
    rx_buff[i] = '\0';

    String topic_str = String(topic);
    String msg_str = String(rx_buff);

    Serial.println("Message arrived:  topic: " + topic_str);
    Serial.println("Length: " + String(length, DEC));
    Serial.println("Payload: " + msg_str);

    if (topic_str.equals(set_tx_rate_ms_topic)) {
        handle_set_tx_rate_ms(msg_str);
    }

    for(i = 0; i < NUM_OF_SENSORS; i++) {
        if (topic_str.equals(set_tx_topics[i])) {
            handle_set_tx_topics(i, msg_str);
        }
    }
}

void handle_set_tx_rate_ms(String msg) {
    int tx_rate = msg.toInt();

    if (tx_rate >= 100 && tx_rate < 60000) {
        loop_time_ms = tx_rate;
        Serial.println("Changed transmission rate to: " + msg);
    } else {
        Serial.println("Error: Incorrect transmission rate :: " + msg);
        Serial.println("Transmission rate must be between 100 and 60000 ms");
    }
}

void handle_set_tx_topics(int sensor_id, String msg) {
    if (msg.equals("on")) {
        sensor_tx_state[sensor_id] = true;
        Serial.println("Changing state to transmitting");
    } else if (msg.equals("off")) {
        sensor_tx_state[sensor_id] = false;
        Serial.println("Changing state to not transmitting");
    } else {
        Serial.println("Error: Unknown state :: " + msg);
    }
}

void handle_state() {
    int i = 0;

    if (millis() > (loop_time_ms + last_loop_time)) {
        last_loop_time = millis();

        for(i = 0; i < NUM_OF_SENSORS; i++) {
            if (sensor_tx_state[i]) {
                transmit_sensor_data(i);
            }
        }
    }
}

void transmit_sensor_data(int sensor_id) {
    get_sensor_data(sensor_id);
    String data_topic = get_data_topics[sensor_id];
    data_topic.toCharArray(topic_buff, data_topic.length()+1);
    client.publish(topic_buff, tx_buff);
}

void get_sensor_data(int sensor_id) {
    long rand_number = random(1, 100);
    String data = MQTT_NODE_NAME + "/sensor/" + String(sensor_id) + "/" + String(rand_number);
    data.toCharArray(tx_buff, data.length()+1);
}

void setup() {
    pinMode(BUILTIN_LED, OUTPUT);
    digitalWrite(BUILTIN_LED, LOW);
    Serial.begin(9600);
    setup_wifi();
    Serial.println("Setting mqtt server: " + String(MQTT_SERVER));
    Serial.println("Setting mqtt port: " + String(MQTT_PORT));
    delay(10000);

    IPAddress server(192,168,2,207);
    client.setServer(server, MQTT_PORT);
    client.setCallback(handle_msg);
    create_topics();
}

void loop() {
    if (!client.connected()) {
        mqtt_connect();
        mqtt_subscribe();
    }

    handle_state();
    client.loop();
}


