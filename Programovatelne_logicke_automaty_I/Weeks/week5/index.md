---
title: Simulátor PLC (PLCSIM Basic a Advanced)
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 5
---

# Simulátor PLC (PLCSIM Basic a Advanced)

V modernom priemyselnom inžinierstve sa väčšina kódu napíše a odladí skôr, než vôbec dorazí fyzický hardvér na stavbu. Virtuálne oživovanie (Virtual Commissioning) šetrí čas, minimalizuje riziká poškodenia drahých komponentov a pre študentov poskytuje ideálne, bezpečné prostredie na testovanie programov. Siemens TIA Portal ponúka na tento účel dva nástroje: **S7-PLCSIM** (Basic) a **S7-PLCSIM Advanced**.

---

## 1. S7-PLCSIM (Basic Simulator)

Štandardný PLCSIM je integrovaný priamo v inštalácii prostredia TIA Portal (vyžaduje len dodatočné doinštalovanie vlastného balíka). Simuluje vnútorný chod PLC (S7-1200 a S7-1500), čím programátorovi umožňuje spúšťať kód takmer identicky, ako keby mal na stole reálny hardvér.

**Kľúčové vlastnosti a možnosti PLCSIM:**
*   **Virtuálna I/O zbernica:** Simulátor dokáže oživiť program aj bez pripojených fyzických senzorov a akčných členov.
*   **Spustenie (Simulation Start):** Prechod do simulačného režimu sa aktivuje v TIA Portal cez ikonu "Start Simulation" (ikonka počítača s modrou šípkou). Po potvrdení sa odpojí akékoľvek online spojenie s reálnym PLC a aktivuje sa virtuálna sieť.
*   **Sledovanie premenných (Watch Table):** Programátor môže vytvárať Watch Table, v ktorých vidí reálny (simulovaný) stav premenných (True/False, Integer, Real) a môže ich ručne prepisovať – takzvane *forsovať* vstupy.
*   **Zachytenie chýb:** Rovnako ako reálne PLC, aj PLCSIM sa prepne do režimu STOP, ak v programe vznikne kritická systémová chyba (napr. volanie neexistujúceho bloku bez ošetrenia chýb cez OB82). V diagnostickom bufferi sa dá dohľadať príčina rovnako ako v praxi.
*   **Krokovanie časovačov:** S7-PLCSIM nepracuje vždy v absolútne reálnom čase (Real-Time). Rýchlosť cyklu závisí od výkonu PC. Umožňuje však testovanie IEC časovačov a počítadiel.

**Obmedzenia štandardného PLCSIM:**
*   Dokáže simulovať len chod interného programu. **Nepodporuje otvorenú TCP/IP komunikáciu so svetom**. 
*   To znamená, že PLCSIM nemôže plnohodnotne komunikovať s programami tretích strán (napr. Python skript na tvojom PC, Unity 3D engine, alebo OPC UA klient). Výnimkou je len spojenie s TIA Portal simuláciou HMI panelu na tom istom stroji.

---

## 2. S7-PLCSIM Advanced

Pre potreby rozsiahlych inžinierskych projektov a tvorby tzv. **Digitálnych dvojčiat (Digital Twins)** Siemens vyvinul PLCSIM Advanced. Tento softvér funguje nezávisle na rozhraní TIA Portal a funguje ako samostatná virtuálna sieťová služba v rámci operačného systému Windows.

**Kľúčové vlastnosti a pridaná hodnota PLCSIM Advanced:**
*   **Virtuálna sieťovka (PLCSIM Virtual Eth. Adapter):** Advanced verzia vytvorí v PC virtuálny sieťový adaptér s vlastnou IP adresou. Z pohľadu celej siete (alebo tvojho lokálneho počítača) sa tento virtuálny adaptér tvári ako 100% hardvérové PLC.
*   **Komunikácia navonok:** Umožňuje prepojenie s OPC UA klientmi, MQTT brokermi (Node-RED), simulátormi fyziky (SIMIT, NX MCD, Unity, Unreal Engine) a databázami.
*   **Viacnásobné inštancie:** Zatiaľ čo štandardný PLCSIM spustí jedno PLC, PLCSIM Advanced umožňuje spustiť paralelne hneď niekoľko virtuálnych PLC súčasne. Tieto virtuálne automaty môžu medzi sebou následne komunikovať cez T-Send/T-Receive alebo PUT/GET presne tak, ako v ostrej prevádzke.
*   **API (Application Programming Interface):** Poskytuje API rozhranie pre C++ alebo C#. To umožňuje programátorom napísať vlastný kód na riadenie simulátora (napr. skript, ktorý nasimuluje hardvérovú chybu modulu v 43. sekunde chodu stroja).

**Ako s ním pracovať v TIA Portal?**
Aby bolo možné nahrať kód z TIA Portal do PLCSIM Advanced, je nutné v TIA Portal zvoliť v projektových nastaveniach možnosť: *Support simulation during block compilation* (Podpora simulácie). Potom už iba v okne pre stiahnutie vyberieme "Virtual Ethernet Adapter" namiesto bežnej sieťovej karty.

---

## 3. Simulácia projektov pomocou Sim Table

Často sa stáva, že proces vyžaduje rýchlu sekvenciu preklápania vstupov (napríklad simuláciu rýchleho snímača, kde trvá len 2 sekundy). Rýchle klikanie a prepisovanie vo Watch table je tu nedostatočné. 
PLCSIM preto poskytuje nástroj **SIM Table (Sequence table)**.

*   V tomto rozhraní si môžeš nahrať zoznam premenných (napr. senzor A, senzor B, tlačidlo Štart).
*   Môžeš nastaviť ich prepínanie v určitom čase (tzv. sekvencie). Napríklad: V čase 0.0 s zapni *Štart*, v čase 1.5 s nasimuluj zapnutie *Senzora A*, v čase 3.0 s vypni *Senzor A*.
*   Spustením sekvencie PLCSIM prehrá túto logiku bez toho, aby si musel zasahovať. Toto je základný spôsob, ako sa učia testovať automatizované stroje bez použitia rozsiahlych externých 3D simulátorov.

---

## 4. Spolupráca simulátora PLC s virtuálnym HMI

Významnou výhodou prostredia TIA Portal je jednotná databáza pre PLC aj HMI (vizualizačné panely).
Pre otestovanie celého stroja:
1.  Najskôr preložíš a stiahneš program do spusteného S7-PLCSIM.
2.  Následne označíš v strome projektu (Project tree) svoj HMI panel a rovnako na ňom stlačíš "Start Simulation".
3.  Vytvorí sa ti okno (Simulátor WinCC), ktoré predstavuje obrazovku panela.
4.  Tieto dva simulátory (PLC a HMI) sa automaticky prepoja. Ak klikneš na virtuálne tlačidlo na simulovanom displeji, v simulovanom PLC sa zopne príslušný bit a proces reaguje rovnako ako vo fyzickom svete.

---

## 📝 Otázky na opakovanie

1. Aký je hlavný rozdiel medzi štandardným S7-PLCSIM a PLCSIM Advanced z pohľadu sieťovej komunikácie?
2. Ktorý simulátor by si využil, ak by si chcel naprogramovať komunikáciu medzi PLC Siemens a simulačnou hrou vytvorenou v engine Unity (Digital Twin)?
3. Akú funkciu spĺňa nástroj *SIM Table (Sequence table)* v základnom PLCSIM? Prečo nestačí používať klasickú *Watch table* z prostredia TIA Portal?
4. Čo sa musí zaškrtnúť v nastaveniach vlastností projektu v TIA Portal, aby bolo možné kód vôbec nahrať do simulátora PLCSIM Advanced?
5. Vysvetli, prečo je výhodné oživovať HMI panel (WinCC simuláciu) súčasne so S7-PLCSIM v jednom systéme ešte pred nákupom reálneho panela.

---

## 📚 Užitočné zdroje

1. [Siemens Industry Online Support: S7-PLCSIM Advanced - Overview](https://support.industry.siemens.com/cs/document/109739153/simatic-s7-1500-s7-plcsim-advanced-overview?dti=0&lc=en-SK)
2. [TIA Portal SIMATIC S7-PLCSIM V18 Manual](https://support.industry.siemens.com/cs/document/109815049/simatic-s7-1500-s7-plcsim-v18?dti=0&lc=en-SK)
3. [Virtual Commissioning (Digital Twin) - Ako prepájať PLCSIM s externými modelmi](https://new.siemens.com/global/en/products/automation/industry-software/virtual-commissioning.html)