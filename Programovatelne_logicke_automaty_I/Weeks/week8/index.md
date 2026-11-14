---
title: HMI - Udalosti (Alarmy, Warnings, Log)
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 8
---

# HMI - Správa udalostí (Alarmy, Warnings, Logovanie)

Vizuálna reprezentácia stroja (čerpadlá svietiace na zeleno) je pre operátora dôležitá počas normálnej prevádzky. Keď sa však niečo pokazí, samotná grafika nestačí. Operátor musí vedieť **čo presne sa stalo, kedy sa to stalo a prečo sa stroj zastavil**. Na tento účel slúži v systéme WinCC (TIA Portal) komplexný systém správy alarmov (Alarms) a logovania (Data/Alarm Logging).

---

## 1. Architektúra Alarmov (HMI Alarms)

Alarmový systém v TIA Portal zhromažďuje chybové stavy a systémové hlásenia, zaraďuje ich do kategórií (Triedy alarmov) a zobrazuje ich v špeciálnom objekte nazývanom **Alarm View** priamo na obrazovke panela.

### Triedy alarmov (Alarm Classes)
Trieda určuje prioritu a správanie správy (napríklad, či vyžaduje potvrdenie operátorom a akou farbou sa zobrazí).
*   **Errors (Alarmy):** Kritické chyby stroja, ktoré spôsobujú jeho okamžité zastavenie (napr. *A001: Skrat na motore dopravníka*). Tieto správy blikajú načerveno a **vyžadujú od operátora potvrdenie (Acknowledge - ACK)**, že si chybu všimol, skôr než môže stroj znova spustiť.
*   **Warnings (Varovania):** Informujú o stave, ktorý ešte nie je kritický, ale čoskoro môže byť problémom (napr. *W001: Nízka hladina chladiacej kvapaliny*). Stroj zvyčajne nezastavia, svietia na žlto a často nevyžadujú potvrdenie.
*   **Diagnosis (Systémové hlásenia):** Správy od samotného PLC alebo HMI o stave hardvéru (napr. *Výpadok spojenia cez Profinet*).

### Typy alarmov podľa spôsobu vyvolania
*   **Discrete Alarms (Bitové alarmy):** Aktivujú sa zmenou logického stavu (Bit z 0 na 1). Toto je najbežnejší typ. V PLC si pripravíme slovo (Word) alebo pole bitov, ktoré obsahuje chyby, a ak v ňom "vyskočí" napr. druhý bit, HMI vygeneruje príslušný text.
*   **Analog Alarms (Analógové alarmy):** Sledujú hodnotu čísla (Int, Real). Alarm sa automaticky vygeneruje, ak premenná prekročí nami nastavenú medzu (Limit). *Napríklad: Ak premenná `HMI_Teplota` prekročí hodnotu 85.0, HMI samo vyhodí Warning "Zvýšená teplota".*
*   **Controller Alarms (Program-Alarm):** Pokročilá metóda podporovaná v S7-1500. Text alarmu sa nepíše v HMI projekte, ale definuje sa priamo v kóde PLC cez inštrukciu `Program_Alarm`. HMI si tento text "vytiahne" samo. Výhodou je, že pri zmene textu netreba prekladať a nahrávať nový softvér do HMI panelu.

---

## 2. Implementácia bitových (Discrete) alarmov

Toto je štandardný a najpoužívanejší postup konfigurácie alarmov medzi PLC a HMI.

1.  **Vytvorenie Wordu chýb (v PLC):** 
    Z hľadiska komunikácie nie je dobré posielať z PLC do HMI 50 samostatných boolovských tagov. Namiesto toho v PLC vytvoríme dátový typ `Word` (16 bitov) alebo pole Wordov, napr. `DB_Alarmy.Zariadenie_1`. Každý bit v tomto slove priradíme jednej chybe.
2.  **HMI Tags (Prepojenie):** 
    Tento Word natiahneme z PLC do zoznamu HMI Tags. Pre komunikáciu je nastavený režim *Acquisition mode: Cyclic in operation* (HMI sa pravidelne pýta PLC na zmenu).
3.  **HMI Alarms (Texty a bity):** 
    V strome projektu HMI otvoríme sekciu *HMI Alarms -> Discrete alarms*. Vytvoríme nový riadok.
    *   `Alarm text`: Tu napíšeme správu pre operátora (napr. *Otvorený ochranný kryt linky*).
    *   `Trigger Tag`: Priradíme náš Word (`DB_Alarmy.Zariadenie_1`).
    *   `Trigger Bit`: Uvedieme, na ktorý bit z tohto Wordu má tento konkrétny text reagovať (napr. bit číslo 4).
    *   `Alarm class`: Nastavíme, či ide o *Error* alebo *Warning*.

---

## 3. Zobrazenie na obrazovke: Alarm View a Alarm Window

Keď je databáza alarmov pripravená, musíme ju operátorovi vizualizovať. Na to slúžia dva podobné, no funkčne odlišné grafické prvky.

### Alarm View (Zobrazenie v objekte)
Toto je tabuľkový objekt, ktorý sa vkladá na klasickú obrazovku HMI (napríklad si vytvoríme samostatnú Screen s názvom "Aktuálne poruchy"). V jeho nastaveniach konfigurujeme, ktoré stĺpce operátor uvidí (Čas vzniku, Trieda, Text, Stav potvrdenia). 
Zobrazuje alarmy na základe vybraného filtra:
*   **Current alarm states:** Zobrazuje len chyby, ktoré práve teraz reálne na stroji pretrvávajú (aktívne a nepotvrdené).
*   **Alarm buffer:** Zobrazuje históriu. Vidno tam, kedy alarm prišiel (Come - C), kedy bol potvrdený (Acknowledge - A) a kedy chyba reálne zmizla (Go - G).

### Alarm Window (Pop-up okno)
Na rozdiel od Alarm View, *Alarm Window* nie je umiestnené na konkrétnej obrazovke, ale definuje sa v nastaveniach HMI ako vrchné (Top-most) plávajúce okno. 
Ak je zapnuté, akonáhle nastane kritický alarm typu *Error*, okno s chybou samo vyskočí (Pop-up) a prekryje aktuálnu obrazovku, aby si operátor okamžite všimol problém. Po potvrdení (ACK) a odstránení chyby sa okno zasa samo schová.

---

## 4. Logovanie a Archivácia dát (Data a Alarm Logging)

Stroje bežia 24/7 a inžinieri nie sú pri nich neustále. Ak operátor v noci zastaví stroj kvôli chybe, inžinier na druhý deň potrebuje zistiť, čo sa dialo a aký bol v danom čase odber prúdu motora. (Poznámka: Táto funkcia vyžaduje Comfort Panely alebo WinCC Advanced, Basic panely neumožňujú archiváciu na SD/USB, len obmedzený interný buffer).

### Alarm Logging (Logovanie chýb)
*   Umožňuje ukladanie histórie alarmov (kedy vznikli a kedy zanikli) do súboru (napr. CSV/TXT) na USB kľúč, SD kartu v paneli alebo na sieťový disk.
*   Zabraňuje strate dát po reštarte panela (pretože interný *Alarm buffer* v RAM pamäti sa po výpadku napájania vymaže).

### Data Logging (Trendovanie procesných hodnôt)
Používa sa na historické ukladanie analógových dát z PLC (teplota pece, rýchlosť stroja).
1.  **Vytvorenie Data Logu:** Zvolíš si formát (CSV), uložisko (SD karta v HMI) a kapacitu (napr. 10 000 záznamov). Ak sa kapacita naplní, panel staré dáta začne premazávať (Circular log).
2.  **Logging Tags:** Vyberieš HMI tag (napr. aktuálna teplota) a priradíš ho k Data logu. Zvolíš stratégiu zápisu:
    *   *Cyclic:* Ukladaj hodnotu každých 5 sekúnd.
    *   *On change:* Ulož hodnotu len vtedy, ak sa zmení o definovanú odchýlku.
3.  **Zobrazenie cez Trend View:** Zalogované dáta z CSV súboru dokáže WinCC priamo čítať a zobraziť operátorovi na obrazovke v podobe grafu s historickou osou času.

---

## 📝 Otázky na opakovanie

1. Aký je rozdiel v správaní stroja a operátora medzi triedou alarmu *Error* a *Warning*?
2. Prečo je z hľadiska záťaže komunikácie efektívnejšie spracovávať Discrete alarmy prenášaním Word/Int premenných z PLC namiesto desiatok samostatných boolovských (bitových) Tagov?
3. Zadefinuj situáciu (Comes / Goes / Acknowledges), pri ktorej alarm typu Error z pohľadu HMI systému úplne zmizne zo zoznamu *Current alarm states*. Čo všetko sa musí udiať?
4. Aký je rozdiel z pohľadu operátora medzi HMI objektmi *Alarm View* a *Alarm Window*?
5. Čo sa stane s uloženou históriou alarmov (*Alarm buffer*) v bežnom paneli (bez konfigurácie logovania na SD kartu), ak panel reštartujeme alebo stratí napájanie? 

---

## 📚 Užitočné zdroje

1. [Siemens TIA Portal Manual: Configuring alarms](https://docs.tia.siemens.cloud/r/simatic_wincc_unified_v18_manual_enus_20/hmi_configuring_alarms)
2. [Siemens Industry Online Support: How do you configure messages and alarms in WinCC (TIA Portal)?](https://support.industry.siemens.com/cs/document/62329998/how-do-you-configure-messages-and-alarms-in-wincc-(tia-portal)-?dti=0&lc=en-SK)
3. [Siemens Application Example: Long-term Data Archiving with WinCC / WinCC Runtime Professional](https://support.industry.siemens.com/cs/document/109477071/long-term-data-archiving-with-wincc-professional?dti=0&lc=en-SK)