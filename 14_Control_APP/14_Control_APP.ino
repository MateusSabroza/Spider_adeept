/**********************************************************************
  Product     : Adeept Hexpod for Arduino
  Base        : WIFI_control (V5.0 official library)
  Modified    : 2026/05/31 — WiFi Sabroza2, porta 4000, comandos app
**********************************************************************/
#include "hexpod.h"
#include <Adafruit_NeoPixel.h>

#define LED_COUNT 6
extern Adafruit_NeoPixel strip;

String comdata = "";
int judge = 0;
// 0=parado, 1=frente, 2=trás, 3=direita, 4=esquerda, 5=equilíbrio, 8=desvio
int ws2812Mode = -1;
int ledR = 0, ledG = 0, ledB = 0;

QUANRUPED q;

void ESP8266_Setup() {
  Serial.begin(115200);
  Serial.println("AT+CWMODE=3\r\n");
  delay(3000);
  Serial.println("AT+CWJAP=\"Sabroza2\",\"1113152331A\"\r\n");
  delay(5000);
  Serial.println("AT+CWSAP=\"Adeept_ADA033\",\"12345678\",8,2\r\n");
  delay(1000);
  Serial.println("AT+RST\r\n");
  delay(5000);
  Serial.println("AT+CIPMUX=1\r\n");
  delay(1000);
  Serial.println("AT+CIPSERVER=1,4000\r\n");
  delay(1000);
  Serial.println("AT+CIPSTO=7000\r\n");
  delay(1000);
}

void setup() {
  strip.begin();
  strip.setBrightness(50);
  q.servo_attach();
  ESP8266_Setup();
  q.self_balanced_setup();
  // verde = pronto
  for (int i = 0; i < LED_COUNT; i++) strip.setPixelColor(i, strip.Color(0, 200, 0));
  strip.show();
}

void loop() {
  while (Serial.available() > 0) {
    comdata += char(Serial.read());
    delay(1);
  }
  if (comdata.length() > 0) {
    parse_command();
    comdata = "";
  }

  switch (judge) {
    case 1: q.moveforward();  break;
    case 2: q.movebackward(); break;
    case 3: q.turnright();    break;
    case 4: q.turnleft();     break;
    case 5: q.steaty();       break;
    case 8: q.advoid();       break;
  }

  led_update();
}

void led_update() {
  static unsigned long prev = 0;
  static int brightness = 0, fade = 10;
  static int hue = 0;
  static int pos = 0, dir = 1;
  static int state = 0;
  unsigned long now = millis();

  switch (ws2812Mode) {
    case 0: // breath
      if (now - prev >= 100) { prev = now;
        brightness += fade;
        if (brightness <= 0 || brightness >= 255) fade = -fade;
        for (int i = 0; i < LED_COUNT; i++)
          strip.setPixelColor(i, strip.Color(map(brightness,0,255,0,ledR), map(brightness,0,255,0,ledG), map(brightness,0,255,0,ledB)));
        strip.show();
      } break;
    case 1: // rainbow
      if (now - prev >= 100) { prev = now;
        for (int i = 0; i < LED_COUNT; i++) {
          int h = (hue + i * 32) % 256;
          h = 255 - h;
          uint32_t c = h < 85  ? strip.Color(255-h*3,0,h*3) :
                       h < 170 ? strip.Color(0,(h-85)*3,255-(h-85)*3) :
                                  strip.Color((h-170)*3,255-(h-170)*3,0);
          strip.setPixelColor(i, c);
        }
        strip.show(); hue = (hue+1)%256;
      } break;
    case 2: // flowing
      if (now - prev >= 300) { prev = now;
        strip.clear();
        strip.setPixelColor(pos, strip.Color(ledR,ledG,ledB));
        int p1=pos-dir, p2=pos-2*dir;
        if (p1>=0 && p1<LED_COUNT) strip.setPixelColor(p1, strip.Color(ledR/3,ledG/3,ledB/3));
        if (p2>=0 && p2<LED_COUNT) strip.setPixelColor(p2, strip.Color(ledR/6,ledG/6,ledB/6));
        strip.show();
        pos += dir;
        if (pos<=0 || pos>=LED_COUNT-1) dir=-dir;
      } break;
    case 3: // police
      if (now - prev >= 300) { prev = now;
        state = (state+1)%4; strip.clear();
        for (int i = 0; i < LED_COUNT; i++)
          if (state==0 || (state==1 && i%2==1) || (state==3 && i%2==0))
            strip.setPixelColor(i, strip.Color(ledR,ledG,ledB));
        strip.show();
      } break;
  }
}

void parse_command() {
  // Parar (verificar antes dos comandos de movimento)
  if (comdata.indexOf("DTS") >= 0 ||
      comdata.indexOf("forwardStop") >= 0 ||
      comdata.indexOf("backwardStop") >= 0 ||
      comdata.indexOf("leftStop") >= 0 ||
      comdata.indexOf("rightStop") >= 0 ||
      comdata.indexOf("automaticOff") >= 0 ||
      comdata.indexOf("keepDistanceOff") >= 0 ||
      comdata.indexOf("steadyOff") >= 0) {
    judge = 0;
    q.servo_init();
    q.strip_begin(0, 200, 0);
  }
  // Modos especiais (verificar antes dos movimentos simples)
  else if (comdata.indexOf("automatic") >= 0)  { judge = 8; }
  else if (comdata.indexOf("keepDistance") >= 0) { judge = 8; }  // usa desvio como proxy
  else if (comdata.indexOf("steady") >= 0)     { judge = 5; }
  // Movimento
  else if (comdata.indexOf("forward") >= 0)    { judge = 1; }
  else if (comdata.indexOf("backward") >= 0)   { judge = 2; }
  else if (comdata.indexOf("lookright") >= 0 || comdata.indexOf("right") >= 0) { judge = 3; }
  else if (comdata.indexOf("lookleft") >= 0  || comdata.indexOf("left") >= 0)  { judge = 4; }
  // LEDs
  else if (comdata.indexOf("lightMode") >= 0) {
    int a = comdata.indexOf("["), b = comdata.indexOf("]");
    if (a >= 0 && b > a) {
      String rgb = comdata.substring(a+1, b);
      int c1 = rgb.indexOf(","), c2 = rgb.indexOf(",", c1+1);
      ledR = rgb.substring(0, c1).toInt();
      ledG = rgb.substring(c1+1, c2).toInt();
      ledB = rgb.substring(c2+1).toInt();
    }
    if      (comdata.indexOf("breath")   >= 0) ws2812Mode = 0;
    else if (comdata.indexOf("rainbow")  >= 0) ws2812Mode = 1;
    else if (comdata.indexOf("flowing")  >= 0) ws2812Mode = 2;
    else if (comdata.indexOf("police")   >= 0) ws2812Mode = 3;
  }
}
