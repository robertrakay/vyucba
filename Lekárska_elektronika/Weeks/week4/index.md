---
title: Arduino UNO R4 WiFi a IoT
layout: custom_default
has_children: true
nav_order: 4
show_sidebar: true
---

# Arduino UNO R4 WiFi: Nová generácia a IoT

Vitajte vo vyššej lige! Doteraz sme pracovali s klasickými 8-bitovými mikrokontrolérmi. Zatiaľ čo klasické Arduino UNO R3 je výborné na pochopenie základov elektroniky, moderný svet vyžaduje konektivitu. V tejto téme prejdeme na **Arduino UNO R4 WiFi**. Zistíme, čo všetko táto malá doska dokáže, ako reaguje na ľudský dotyk a ako ju prepojiť s vaším smartfónom cez webový prehliadač.

---

## 1. Teória: Čo je nové v UNO R4 WiFi? (Rozdiely oproti R3)

Na prvý pohľad vyzerá UNO R4 takmer rovnako ako jeho predchodca – má rovnaké rozloženie pinov, takže do neho pasujú staré súčiastky a "shieldy" (nadstavby). Vo vnútri je to však úplne iný stroj.

| Vlastnosť | Klasické Arduino UNO R3 | Arduino UNO R4 WiFi | Čo to znamená v praxi? |
| :--- | :--- | :--- | :--- |
| **Procesor (Mozog)** | 8-bit (ATmega328P) | **32-bit** (Renesas RA4M1) | Zvládne oveľa zložitejšiu matematiku a výpočty. |
| **Pracovná frekvencia** | 16 MHz | **48 MHz** | Kód beží 3-krát rýchlejšie. |
| **Pamäť (SRAM / Flash)**| 2 kB / 32 kB | **32 kB / 256 kB** | Zmestia sa vám tam obrovské programy a knižnice (ako napr. WiFi). |
| **Konektivita** | Žiadna | **Wi-Fi a Bluetooth** | Doska má vlastný ESP32-S3 čip na bezdrôtovú komunikáciu. |
| **Analógový výstup** | Iba PWM (Pulzujúci) | **Skutočný DAC (12-bit)** | Dokáže generovať čisté analógové napätie (napr. pre zvuk). |
| **USB Konektor** | Veľké USB-B (tlačiareň)| **Moderné USB-C** | Univerzálnejšie a robustnejšie pripojenie. |

*Poznámka:* Aj napriek brutálnemu nárastu výkonu doska **stále operuje na 5V logike**, takže vám nezničí staré senzory, ktoré boli na 5V zvyknuté!

---

## 2. Zoznámte sa s novými "hračkami"

Naša doska R4 WiFi má v sebe zabudované veci, kvôli ktorým ste si predtým museli kupovať externé moduly. Pridáme k tomu zopár klasických súčiastok a vytvoríme komplexný systém.

*   🔴 **LED Matrix (Zabudovaný):** Priamo na doske je matica 96 červených LED diód (rozloženie 12x8). Výborná vec na zobrazovanie ikoniek, smajlíkov, textu alebo chybových hlásení bez nutnosti pripájať externý displej.
*   👆 **Kapacitný vstup (Capacitive Touch):** Doska dokáže zmerať jemnú zmenu elektrickej kapacity. Stačí pripojiť holý drôt (alebo kúsok alobalu) na konkrétny pin. Keď sa k drôtu priblíži ľudský prst (ktorý má vlastnú kapacitu), Arduino to zaznamená ako dotyk bez toho, aby ste stlačili mechanické tlačidlo.
*   🔊 **Buzzer (Piezo menič):** Malá súčiastka, ktorá píska. Keď do nej pošleme PWM signál určitej frekvencie, začne vibrovať a vydávať tón.
*   🎛️ **Potenciometer:** Toto už poznáme z minula. Otočný rezistor pripojený na analógový pin (A0). Slúži na plynulé nastavenie hodnôt.
*   🌐 **Webserver (IoT - Internet of Things):** Vaše Arduino bude fungovať ako malá webová stránka. Pripojíme ho na WiFi, získame IP adresu a keď túto adresu napíšete do mobilu, otvorí sa vám ovládací panel.

---

## 3. Syntax a Knižnice (Čo musíme dopísať do kódu)

Aby sme nemuseli programovať komunikáciu na úrovni núl a jednotiek, využijeme hotové knižnice (Libraries). Tieto príkazy dávame úplne na začiatok kódu:

*   `#include "WiFiS3.h"` – Knižnica pre ovládanie WiFi čipu na doske R4.
*   `#include "Arduino_LED_Matrix.h"` – Knižnica na ovládanie svietiacej matice.
*   `#include "Arduino_CapacitiveTouch.h"` – Knižnica na čítanie dotyku.

Na generovanie tónov z Buzzera knižnicu nepotrebujeme, použijeme štandardný príkaz:
`tone(pin, frekvencia_v_Hz, trvanie_v_ms);` (Napríklad `tone(8, 1000, 200);` pískne tónom 1kHz na 200 milisekúnd).

---

## 4. Praktické úlohy: Od dotyku až po Internet

### 💖 Obvod 1: Kapacitný dotyk a Srdiečko na Matrixe
Začneme niečím efektným, čo sa dá spraviť s minimom súčiastok priamo na kontaktnom poli[cite: 3].
*   **Zapojenie:** Zapichnite jeden obyčajný drôtik (jumper káblik) do pinu **D0**. Na jeho druhom konci môže byť kúsok alobalu, alebo sa ho jednoducho budete dotýkať prstom.
*   **Úloha:** Pomocou knižnice pre kapacitný dotyk (`Arduino_CapacitiveTouch`) budeme sledovať pin D0[cite: 3]. Ak Arduino zaznamená dotyk, priamo na zabudovanom LED Matrixe sa zobrazí ikonka srdiečka[cite: 3].

```cpp
#include "Arduino_LED_Matrix.h"
#include "Arduino_CapacitiveTouch.h" // Knižnica pre dotykový senzor

ArduinoLEDMatrix matrix;
CapacitiveTouch touchSensor(D0);     // Nastavenie pinu D0 ako dotykový senzor

// Hexadecimálny kód pre nakreslenie srdiečka na matici 12x8
const uint32_t heart[] = {
  0x3184a444,
  0x42081100,
  0xa0040000
};

void setup() {
  Serial.begin(9600);
  matrix.begin(); // Spustenie matice
}

void loop() {
  // Prečítame stav dotykového senzora
  bool jeDotyk = touchSensor.read();

  if (jeDotyk) {
    matrix.loadFrame(heart); // Zasvieti srdiečko
    Serial.println("Dotyk zaznamenaný!");
  } else {
    matrix.clear();          // Zhasne maticu
  }
  delay(50);
}
🎛️ Obvod 2: Príprava hardvéru (Analóg a Zvuk)
Predtým, než pôjdeme na internet, rozšírime náš obvod na kontaktnom poli.

Potenciometer: Krajné nožičky na 5V a GND. Strednú (bežec) na analógový pin A0.

Buzzer (Piezo): Dlhšia nožička (alebo káblik označený +) pôjde na digitálny pin D8. Kratšia na GND. (Poznámka: Ak máte aktívny buzzer, píska sám, akonáhle dostane 5V. Ak máte pasívny buzzer, musíme použiť príkaz tone()).

🏆 Finálna Výzva: Všetko v jednom Webserveri! (IoT Dashboard)
Teraz spojíme všetko, čo sme sa naučili, do jedného masívneho projektu. Z Arduina urobíme malý webový server.

Ako to bude fungovať:

Arduino sa pripojí na vašu domácu/školskú WiFi sieť.

Vypíše vám na Serial Monitor svoju IP adresu (napr. 192.168.1.50).

Keď túto adresu otvoríte v prehliadači (na mobile alebo PC), Arduino vám odošle HTML kód webovej stránky.

Na webe uvidíte: Hodnotu z potenciometra a informáciu, či sa niekto dotýka pinu D0.

Z webu môžete: Stlačiť tlačidlo "Zahraj Tón", ktoré rozozvučí Buzzer na stole, a tlačidlo "Srdiečko", ktoré prepne LED Matrix!

Kód je dlhší, ale logicky rozdelený. Dôkladne si preštudujte komentáre.

C++
#include "WiFiS3.h"
#include "Arduino_LED_Matrix.h"
#include "Arduino_CapacitiveTouch.h"

// --- NASTAVENIE SIETE (Tu doplňte údaje svojej siete!) ---
char ssid[] = "TVOJA_WIFI_SIET"; 
char pass[] = "TVOJE_HESLO";     

WiFiServer server(80); // Webový server beží na štandardnom porte 80
ArduinoLEDMatrix matrix;
CapacitiveTouch touchSensor(D0);

// --- PINY ---
const int potPin = A0;
const int buzzerPin = 8;

// Grafiky pre matrix
const uint32_t heart[] = { 0x3184a444, 0x42081100, 0xa0040000 };
const uint32_t clear_frame[] = { 0, 0, 0 };

void setup() {
  Serial.begin(9600);
  matrix.begin();
  pinMode(buzzerPin, OUTPUT);

  // Pripojenie na WiFi
  Serial.print("Pripájam sa na WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nPripojené!");
  Serial.print("Zadaj túto IP adresu do prehliadača: ");
  Serial.println(WiFi.localIP());

  server.begin(); // Spustenie servera
}

void loop() {
  // Čakáme, či sa nejaký prehliadač nepripojí na Arduino
  WiFiClient client = server.available(); 

  if (client) {
    String currentLine = ""; // Bude uchovávať prichádzajúci HTTP príkaz z webu

    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        
        if (c == '\n') { // Koniec požiadavky od klienta
          if (currentLine.length() == 0) { // Ak je riadok prázdny, nasleduje naša odpoveď
            
            // 1. Získame aktuálne dáta zo senzorov
            int potValue = analogRead(potPin);
            bool isTouched = touchSensor.read();
            String touchStatus = isTouched ? "ÁNO (Dotyk)" : "NIE";

            // 2. Pošleme hlavičku HTML (aby prehliadač vedel, že mu posielame web)
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println(); // Prázdny riadok oddeluje hlavičku od obsahu

            // 3. Pošleme samotný dizajn a obsah stránky (HTML kód)
            client.print("<html><head>");
            client.print("<meta charset='UTF-8'>");
            // Automatický refresh stránky každé 2 sekundy (aby sme videli zmeny hodnôt)
            client.print("<meta http-equiv='refresh' content='2; URL=/' />");
            client.print("<style>body{font-family: Arial; text-align: center; margin-top: 50px;} ");
            client.print("a.button{background-color: #4CAF50; color: white; padding: 15px 20px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block;}</style>");
            client.print("</head><body>");
            
            client.print("<h1>🎛️ Arduino UNO R4 Ovládací Panel</h1>");
            
            // Výpis zo senzorov
            client.print("<h2>Analóg (Potenciometer): <b>" + String(potValue) + "</b></h2>");
            client.print("<h2>Kapacitný dotyk (D0): <b>" + touchStatus + "</b></h2>");
            
            client.print("<hr>");
            
            // Odkazy fungujúce ako tlačidlá pre Arduino
            client.print("<h3>Ovládanie z webu:</h3>");
            client.print("<a class='button' href=\"/beep\">🔊 Písknuť Buzzer</a>");
            client.print("<a class='button' href=\"/heart\">💖 Ukáž Srdce</a>");
            client.print("<a class='button' style='background-color:#f44336;' href=\"/clear\">⬛ Zhasni Matrix</a>");

            client.print("</body></html>");
            client.println();
            break; // Odpoveď odoslaná, ukončíme čítanie
            
          } else { 
            currentLine = ""; 
          }
        } else if (c != '\r') {  
          currentLine += c; // Postupne ukladáme riadok 
        }

        // --- VYHODNOTENIE POVELOV Z WEBU ---
        // Ak sa v adrese prehliadača (v HTTP požiadavke) objaví príkaz...
        if (currentLine.endsWith("GET /beep")) {
          tone(buzzerPin, 1000, 300); // Zahraj 1kHz tón na 300 ms
        }
        if (currentLine.endsWith("GET /heart")) {
          matrix.loadFrame(heart); // Rozsvieť srdce
        }
        if (currentLine.endsWith("GET /clear")) {
          matrix.clear(); // Zhasni matrix
        }
      }
    }
    // Zatvoríme pripojenie a čakáme na ďalší klik
    client.stop();
  }
}
💡 Na zamyslenie pre študentov:
Všimnite si v HTML kóde riadok s <meta http-equiv='refresh'...>. Táto značka núti prehliadač obnoviť stránku každé 2 sekundy, vďaka čomu sa vám automaticky aktualizuje hodnota z potenciometra a dotyku bez toho, aby ste museli stláčať "F5". Moderné profesionálne weby to riešia cez technológie ako AJAX alebo WebSockets, ale pre základné IoT riešenia je toto najjednoduchší a najrýchlejší postup!
---