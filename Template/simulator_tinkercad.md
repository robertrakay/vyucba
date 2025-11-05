
---

## 🧰 2️⃣ `Simulator/Tinkercad.md`

```yaml
---
layout: subject
title: Tinkercad Circuits
---
# ⚙️ Tinkercad Circuits

Tinkercad je bezplatný online nástroj od Autodesku, ktorý umožňuje **navrhovať a simulovať elektronické obvody a Arduino projekty**.

---

## 🔗 Odkazy

- 🌐 [Otvoriť Tinkercad Circuits](https://www.tinkercad.com/circuits)
- 📘 [Tinkercad Tutoriály](https://learn.tinkercad.com/)
- 🎥 [YouTube návody](https://www.youtube.com/results?search_query=tinkercad+arduino+tutorial)

---

## 🧩 Postup

1. Prihlás sa na [tinkercad.com](https://www.tinkercad.com/).
2. V menu klikni na **Circuits → Create new Circuit**.
3. Vyber **Arduino Uno**, pridaj LED a rezistor.
4. Pripoj komponenty podľa schémy a klikni **Start Simulation**.

---

### 💡 Príklad kódu

```cpp
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
