---
layout: subject
title: Wokwi Simulator
---
# 💡 Wokwi Simulator

Wokwi je online simulátor pre Arduino, ESP32, Raspberry Pi Pico a ďalšie mikrokontroléry.  
Umožňuje testovať kód a zapojenia **bez potreby fyzického hardvéru**.

---

## 🔗 Odkazy

- 🌐 [Spusti Wokwi Simulator](https://wokwi.com/)
- 📘 [Dokumentácia Wokwi](https://docs.wokwi.com/)
- 🧩 [Príklady projektov](https://wokwi.com/projects)

---

## 🧪 Ukážka použitia

1. Otvor stránku [wokwi.com](https://wokwi.com/).  
2. Klikni **New Project → Arduino Uno**.  
3. Do súboru `sketch.ino` vlož napríklad:
   ```cpp
   void setup() {
     pinMode(13, OUTPUT);
   }

   void loop() {
     digitalWrite(13, HIGH);
     delay(500);
     digitalWrite(13, LOW);
     delay(500);
   }
