#include <Arduino.h>
#include <WiFi.h>
#include "html.h"

class motor 
{
private:
  int speed;
  int in1;
  int in2;
  int pmw_pin;

public:
  motor(int In1, int In2, int Pmw);
  void set_speed(int speed);

  void forward(int speed);
  void forward();

  void back(int speed);
  void back();

  void stop();
  ~motor();
};

motor::motor(int In1, int In2, int Pmw)
{
  in1 = In1;
  in2 = In2;
  pmw_pin = Pmw;
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(pmw_pin, OUTPUT);
}

void motor::forward(int Speed)
{
  if ((Speed < 0) or (Speed > 255))
    Speed = 250;

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(pmw_pin, Speed);
  speed = Speed;
}

void motor::forward()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(pmw_pin, speed);
}

void motor::back(int Speed)
{
  if ((Speed < 0) or (Speed > 255))
    Speed = 250;

  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(pmw_pin, speed);
  speed = Speed;
}

void motor::back()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(pmw_pin, speed);
}

void motor::set_speed(int Speed)
{
  if ((Speed < 0) or (Speed > 255))
    Speed = 250;
  speed = Speed;
  analogWrite(pmw_pin, speed);
}

void motor::stop()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, HIGH);
  analogWrite(pmw_pin, 128);
}

motor::~motor()
{
}

motor small(GPIO_NUM_14, GPIO_NUM_27, GPIO_NUM_12);
motor big(GPIO_NUM_26, GPIO_NUM_25, GPIO_NUM_33);

// вводим имя и пароль точки доступа
const char *ssid = "magick";
const char *password = "isintheair";
uint8_t a = 0;

int ledBrightness = 0; // Initial LED brightness

WiFiServer server(80); // Create a server on port 80

void setup()
{
  delay(500);
  Serial.begin(115200);

  small.set_speed(254);
  big.set_speed(240);

  // Connect to Wi-Fi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println(HTML_CONTENT);

  server.begin();
}

void loop()
{
  WiFiClient client = server.available(); // Check if a client has connected
  // client.setTimeout(2);

  if (client)
  {
    Serial.println("New client");
    String currentLine = ""; // Make a String to hold incoming data from the client

    while (client.connected())
    { // Loop while the client is connected
      if (client.available())
      {                         // If there's bytes to read from the client,
        char c = client.read(); // read a byte
        Serial.write(c);        // Print it out to the serial monitor

        if (c == '\n')
        { // If the byte is a newline character
          // Check if the client's request is to turn the LED on
          if (currentLine.startsWith("GET /forward"))
          {
            big.set_speed(254);
            small.set_speed(240);

            big.forward();
            delay(20);
            small.forward();
          }
          // Check if the client's request is to turn the LED off
          else if (currentLine.startsWith("GET /backward"))
          {
            big.set_speed(254);
            small.set_speed(240);

            small.back();
            delay(20);
            big.back();
          }
          else if (currentLine.startsWith("GET /stop"))
          {
            big.stop();
            small.stop();
          }
          else if (currentLine.startsWith("GET /left"))
          {
            big.set_speed(255);
            small.set_speed(255);

            big.forward();
            small.back();

            delay(50);
            big.set_speed(180);
            small.set_speed(140);
          }
          else if (currentLine.startsWith("GET /right"))
          {
            big.set_speed(255);
            small.set_speed(255);

            big.back();
            small.forward();

            delay(100);
            big.set_speed(180);
            small.set_speed(140);
          }
          // Check if the client's request is to set LED brightness
          else if (currentLine.startsWith("GET /brightness1"))
          {
            int brightnessValue = currentLine.substring(currentLine.indexOf('=') + 1).toInt();
            small.set_speed(brightnessValue);
          }
          else if (currentLine.startsWith("GET /brightness2"))
          {
            int brightnessValue = currentLine.substring(currentLine.indexOf('=') + 1).toInt();
            big.set_speed(brightnessValue);
          }
          // Clear the currentLine variable
          currentLine = "";
        }
        else if (c != '\r')
        {                   // If the byte is not a carriage return character
          currentLine += c; // Add it to the currentLine
        }

        // Check if the client has sent an empty line
        if (currentLine.length() == 0)
        {
          // Send a standard HTTP response header
          client.println(HTML_CONTENT);
          break;
        }
      }
    }

    // Close the connection
    client.stop();
    Serial.println("Client disconnected");
  }

  if (a == 120)
    Serial.println("Blink:D");
  a++;

}