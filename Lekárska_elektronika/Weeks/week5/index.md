---
title: Snímače, systém Grove a EKG
layout: custom_default
has_children: true
nav_order: 5
show_sidebar: true
---

# Snímače, systém Grove a bioelektronika (EKG)

Doteraz sme zapájali obvody ručne na kontaktnom poli (breadboarde). Hoci je to skvelé na pochopenie prúdu a odporu, pri veľkých projektoch sa z toho rýchlo stane "vrabčie hniezdo" desiatok káblov. Ak jeden káblik povolí, strávite hodinu hľadaním chyby. Pri zložitejších senzoroch preto prechádzame na modulárny systém, ktorý nám umožní sústrediť sa na to podstatné – na samotné dáta a programovanie.

---

## 1. Grove Shield a princíp spájania (Plug-and-Play)

**Grove** je stavebnicový systém od spoločnosti Seeed Studio. Základom je **Grove Base Shield**, čo je rozširujúca doska, ktorú jednoducho "nacvaknete" priamo na piny vášho Arduina UNO R4.

### Ako to funguje?
Zabudnite na spájkovanie a zložité počítanie odporov pre každý senzor. Systém Grove využíva **štandardizované 4-pinové konektory**. Konektor má drážku, takže sa **nedá zapojiť naopak** (ochrana proti prepólovaniu a odpáleniu súčiastok).

Farby káblov v Grove systéme majú vždy rovnaký význam:
*   ⬛ **Čierna (Pin 4):** GND (Zem)
*   🟥 **Červená (Pin 3):** VCC (Napájanie - 5V)
*   ⬜ **Biela (Pin 2):** Sekundárny signál / Vstup / Výstup
*   🟨 **Žltá (Pin 1):** Primárny signál / Vstup / Výstup

### Typy Grove portov na Shielde
Shield rozdeľuje piny Arduina do štyroch hlavných "zón":
1.  **D (Digitálne porty):** Pre tlačidlá, LED, relé (napr. D2, D3...).
2.  **A (Analógové porty):** Pre potenciometre a senzory, ktoré vracajú spojité hodnoty.
3.  **I2C (Inter-Integrated Circuit):** Zbernica pre zložité "inteligentné" senzory (displeje, gyroskopy). Sem sa nezapájajú priame napätia, ale prebieha tu dátová komunikácia (žltý kábel = SCL hodiny, biely = SDA dáta).
4.  **UART:** Sériová komunikácia pre Bluetooth alebo GPS moduly.

*(⚠️ **Dôležité upozornenie pre UNO R4:** Na Grove Shielde sa nachádza malý prepínač napätia (3.3V / 5V). Keďže Arduino UNO R4 operuje s 5V logikou, uistite sa, že je prepínač v polohe **5V**!)*

---

## 2. Senzor DHT (Teplota a Vlhkosť)

Jedným z najčastejšie používaných modulov je **DHT11** alebo **DHT22**. V jedinom plastovom puzdre sa nachádza kapacitný snímač vlhkosti a termistor na meranie teploty. 

Senzor si dáta sám spracuje a Arduinu pošle digitálny "balíček" núl a jednotiek. Prečo je to dôležité? Pretože digitálny signál nie je náchylný na rušenie dlhým káblom.

*   **Kam ho zapojiť:** Do akéhokoľvek Digitálneho portu na Shielde (napr. **D2**).
*   **V kóde:** Na dešifrovanie tohto balíčka potrebujeme stiahnuť knižnicu `DHT.h`. Následne nám stačí zavolať príkazy `dht.readTemperature()` a `dht.readHumidity()`.

---

## 3. Akcelerometer a Gyroskop (IMU senzor)

Predstavte si, že chcete s Arduinom postaviť balancujúceho robota, alebo zistiť, či sa predmet prevrátil. Potrebujete senzor **IMU (Inertial Measurement Unit)**. Najznámejší modul je Grove 6-Axis Accelerometer (obsahuje čip MPU6050 alebo podobný).

*   **Akcelerometer:** Meria zrýchlenie v 3 osiach (X, Y, Z). Dôležité: Keď senzor len tak leží na stole, os Z ukazuje hodnotu $1g$ (pôsobí na ňu zemská gravitácia). Vďaka tomu Arduino vie, kde je "dole".
*   **Gyroskop:** Meria uhlovú rýchlosť – teda ako rýchlo a ktorým smerom sa senzor otáča (rotuje okolo osí).
*   **Kam ho zapojiť:** Tento senzor komunikuje posielaním desiatok rôznych hodnôt tisíckrát za sekundu. Zapája sa **výlučne do portu I2C**.

---

## 4. Displej Modul (OLED / LCD)

Už vás nebaví pozerať sa na výpisy v Serial Monitore na PC? Pripojíme si displej! V systéme Grove sa často používa malý **OLED displej** alebo klasický **LCD (16x2 znakov)**.

*   Rovnako ako gyroskop, aj displej sa zapája do **I2C portu**.
*   **Magická výhoda I2C:** Možno sa pýtate – *„Čo ak chcem gyroskop aj displej, ale I2C porty mám vedľa seba len dva?“* 
Žiadny problém! Zbernica I2C funguje ako poštár. Každý senzor má z výroby napálenú svoju unikátnu "adresu" (napr. displej má adresu `0x3C` a gyroskop `0x68`). Vy môžete cez "rozdvojky" (Grove I2C Hub) zapojiť na tie isté 4 káble hoci aj 10 rôznych I2C senzorov naraz a Arduino si s každým pokecá bez toho, aby sa hádali!

---

## 5. EKG Senzor s Arduinom (Úvod do bioelektroniky)

Toto je oblasť, kde sa spája informatika, elektrotechnika a ľudské telo. **EKG (Elektrokardiograf)** zaznamenáva elektrickú aktivitu srdca.

**Ako to funguje?**
Srdce je v podstate svalové čerpadlo ovládané elektrickými impulzmi (vznikajú v tzv. SA uzle). Keď sa tieto mikro-impulzy šíria telom, dajú sa zmerať na koži. Zvyčajne ide o napätia v rádoch milivoltov (mV), navyše silne zarušené pohybom svalov a sieťovým brumom z okolitých káblov 230V.

Grove EKG senzor (obsahujúci špeciálny zosilňovač, napr. AD8232) funguje takto:
1. Prijme slabý signál z nálepiek (elektród) na vašom tele.
2. Zosilní ho, odfiltruje šum.
3. Pošle ho do Arduina ako kolísajúce napätie od 0V do 5V.

**Výhoda Arduino UNO R4 WiFi pre EKG:**
Klasické Arduino R3 malo na meranie 10-bitový analógový prevodník (rozlišovalo 1024 úrovní napätia). **Nové UNO R4 má 14-bitový ADC!** Dokáže rozoznať až 16 384 úrovní. Vaša EKG krivka (slávny komplex P-Q-R-S-T) vďaka tomu bude oveľa hladšia, presnejšia a ostrejšia.

*   **Kam ho zapojiť:** Keďže ide o plynule sa meniacu krivku, senzor sa zapája do **Analógového portu (napr. A0)**.
*   **Pripojenie na telo:** Senzor má 3 elektródy. Pravá ruka (RA), Ľavá ruka (LA) a Pravá noha (RL), ktorá slúži ako referenčná zem na odrušenie. *(Upozornenie: Toto je laboratórny experimentálny modul, neslúži na medicínsku diagnostiku!)*

### Ukážka: Vykreslenie EKG na Serial Plotter

V Arduino IDE nemusíte programovať zložitú grafiku, aby ste videli úder svojho srdca. Prostredie obsahuje nástroj **Serial Plotter** (Nástroje -> Sériový ploter). Ak Arduino posiela iba holé čísla, Plotter ich automaticky nakreslí do bežiaceho grafu.

```cpp
// EKG Senzor zapojený v Grove porte A0
const int ekgPin = A0;

void setup() {
  // Inicializujeme sériovú linku veľmi vysokou rýchlosťou,
  // aby sme stihli posielať dáta dostatočne rýchlo pre plynulý graf
  Serial.begin(115200); 

  // Pre Arduino UNO R4 prepneme ADC na vyššie rozlíšenie (12 bitov = 0 až 4095)
  // (štandard je 10 bitov, ale R4 vie viac!)
  analogReadResolution(12);
}

void loop() {
  // Prečítame aktuálnu hodnotu elektrickej aktivity srdca
  int ekgHodnota = analogRead(ekgPin);

  // Pošleme ju priamo do počítača.
  // Dôležité: Použijeme iba println s jedným číslom, aby mu Serial Plotter porozumel.
  Serial.println(ekgHodnota);

  // Krátke oneskorenie - EKG obvykle potrebuje vzorkovanie okolo 100-200 krát za sekundu
  delay(10); 
}
Po nahratí tohto kódu a pripojení elektród stačí otvoriť Serial Plotter v hornom menu Arduino IDE. Ak budete sedieť ticho a nebudete hýbať svalmi rúk, na obrazovke uvidíte skutočné údery vlastného srdca!
---
