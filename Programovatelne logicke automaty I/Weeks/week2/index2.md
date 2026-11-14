---
title: Základné inštrukcie
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 2
---

# Základné inštrukcie v prostredí TIA Portal

Programovanie programovateľných logických automatov (PLC) radu SIMATIC S7-1200 a S7-1500 v prostredí TIA Portal stavia na medzinárodnej norme **IEC 61131-3**. Pre základné inštrukcie sa najčastejšie využívajú grafické jazyky **LAD (Ladder Logic - Kontaktné schémy)** a **FBD (Function Block Diagram - Funkčné bloky)**. Tieto jazyky umožňujú intuitívny prepis logických rovníc a elektrických schém do programu PLC.

Pred samotným použitím inštrukcií je nutné pochopiť princíp **cyklického spracovania programu**:
1. Operačný systém PLC načíta fyzické stavy vstupov a zapíše ich do Procesného obrazu vstupov (PII).
2. Vykoná sa užívateľský program (napr. OB1), ktorý číta dáta z PII a výsledky ukladá do Procesného obrazu výstupov (PIQ).
3. Po ukončení cyklu PLC prepíše dáta z PIQ na fyzické výstupy.

---

## 1. Bitové logické inštrukcie (Bit Logic Operations)

Bitové inštrukcie pracujú s najmenšou dátovou jednotkou – **Bool** (hodnoty TRUE/FALSE, resp. 1/0). Tieto inštrukcie tvoria základ každého logického riadenia (napr. zapínanie motorov, vyhodnocovanie snímačov).

### Základné kontakty a cievky
*   **NO kontakt (Normally Open):** `---| |---`
    *   Inštrukcia skopíruje stav priradenej premennej. Ak je premenná `TRUE` (logická 1), kontakt je zopnutý a prepúšťa signál (RLO - Result of Logic Operation je 1). Využíva sa na snímanie zapínacích tlačidiel.
*   **NC kontakt (Normally Closed):** `---| / |---`
    *   Inštrukcia invertuje stav priradenej premennej. Ak je premenná `FALSE` (logická 0), kontakt je zopnutý. Používa sa typicky pre bezpečnostné prvky a vypínacie tlačidlá (STOP).
*   **Assignment (Priradenie / Cievka):** `---( )---`
    *   Zapisuje aktuálny stav RLO do priradenej premennej. Ak pred cievkou existuje uzavretá cesta, premenná sa nastaví na 1. Ak sa cesta preruší, premenná okamžite padne na 0.

### Pamäťové inštrukcie (Set / Reset)
Pri riadení procesov často potrebujeme, aby výstup zostal zopnutý aj po uvoľnení tlačidla (napríklad štart motora bez samoprídrže v kóde).
*   **Set (Nastavenie):** `---( S )---`
    *   Ak do inštrukcie príde signál 1, priradená premenná sa nastaví na 1 a zostane tak aj po zániku vstupného signálu.
*   **Reset (Nulovanie):** `---( R )---`
    *   Ak do inštrukcie príde signál 1, priradená premenná sa nastaví na 0.
*   **SR a RS Klopné obvody (Flip-Flops):**
    *   Predstavujú pamäťové bloky, ktoré majú vstup pre Set aj Reset. Rozdiel spočíva v priorite.
    *   **SR (Set/Reset dominantný na Reset):** Ak sú súčasne aktívne vstupy S aj R, výstup bude 0 (bezpečnejšie pre vypínanie strojov).
    *   **RS (Reset/Set dominantný na Set):** Ak sú aktívne oba vstupy, výstup bude 1.

### Detekcia hrán (Edge Detection)
Mnohé procesy nevyžadujú trvalý signál, ale iba reakciu na zmenu stavu (napr. spočítanie výrobkov prechádzajúcich cez snímač).
*   **P-Trig (Positive Edge):** Reaguje iba v momente, keď signál prejde z 0 na 1 (nábežná hrana). Inštrukcia prepustí logickú 1 len na dĺžku jedného cyklu PLC (scan cycle).
*   **N-Trig (Negative Edge):** Reaguje na zmenu z 1 na 0 (dobehová hrana).

---

## 2. Časovače IEC (Timers)

V moderných systémoch S7-1200/1500 sa používajú výhradne **IEC časovače**. Sú to funkčné bloky (FB), ktoré na svoje fungovanie potrebujú vlastnú pamäť – tzv. **Instančný dátový blok (Instance DB)**, v ktorom si ukladajú aktuálny čas (ET - Elapsed Time) a stav. Časové parametre (PT - Preset Time) sa zadávajú v dátovom type `Time` (napr. `T#5s`, `T#200ms`).

*   **TP (Pulse - Impulz):**
    *   Po zachytení nábežnej hrany na vstupe IN sa výstup Q nastaví na 1 po dobu špecifikovanú v parametri PT. Ak vstup IN klesne na 0 skôr, ako uplynie čas, časovač aj tak dokončí svoj impulz.
*   **TON (Timer On-Delay - Oneskorené zapnutie):**
    *   Najpoužívanejší časovač. Výstup Q sa nastaví na 1 až vtedy, keď je vstup IN aktívny nepretržite po dobu zadanú v PT. Ak IN padne na 0 pred uplynutím času, časovač sa vynuluje. Slúži na filtrovanie zákmitov a radenie procesov.
*   **TOF (Timer Off-Delay - Oneskorené vypnutie):**
    *   Výstup Q sa zapne okamžite po aktivácii vstupu IN. Keď vstup IN padne z 1 na 0, začne sa odpočítavať čas. Výstup Q klesne na 0 až po uplynutí PT.
*   **TONR (Timer On-Delay Retentive):**
    *   Funguje ako TON, ale čas sa pri výpadku vstupu IN nenuluje – pozastaví sa. Na vynulovanie času sa musí použiť samostatný vstup R (Reset). Vhodné pre meranie motohodín.

---

## 3. Počítadlá IEC (Counters)

Rovnako ako IEC časovače, aj IEC počítadlá (Counters) si vyžadujú vlastný instančný dátový blok na ukladanie aktuálnej hodnoty (CV - Current Value).

*   **CTU (Count Up - Pripočítavanie):**
    *   Pri každej nábežnej hrane na vstupe CU sa hodnota CV zvýši o 1. Keď CV dosiahne hodnotu nastavenú v PV (Preset Value), výstup Q sa zopne. Vstup R nuluje hodnotu CV na nulu.
*   **CTD (Count Down - Odpočítavanie):**
    *   Načíta sa (LD) počiatočná hodnota (PV). Pri každej hrani na vstupe CD sa CV znižuje o 1. Výstup Q zopne, keď CV klesne na 0 alebo do záporných hodnôt.
*   **CTUD (Count Up/Down):**
    *   Kombinované počítadlo. Obsahuje vstupy CU (hore) aj CD (dole), ako aj vstupy pre nulovanie a načítanie počiatočnej hodnoty. Využíva sa napr. pri počítaní áut na parkovisku (závora dnu, závora von).

---

## 4. Komparačné a Matematické inštrukcie

Pri spracovaní snímačov analógových hodnôt (teplota, tlak, vzdialenosť) a počítadiel PLC pracuje s celými číslami (Integer) alebo desatinnými číslami (Real).

### Komparátory
Vyhodnocujú vzťah medzi dvoma premennými a vracajú hodnotu Bool. Je dôležité dbať na to, aby obe porovnávané hodnoty mali rovnaký dátový typ (napr. Int s Int, Real s Real).
*   **== (Equal), <> (Not Equal):** Rovnosť a nerovnosť.
*   **> (Greater), < (Less), >= (Greater or Equal), <= (Less or Equal):** Väčšie, menšie.
*   **IN_RANGE / OUT_OF_RANGE:** Skontroluje, či sa testovaná hodnota nachádza v definovanom intervale. Veľmi užitočné pri alarmoch (napr. ak je teplota v rozsahu 20°C až 25°C, výstup je TRUE).

### Matematické operácie
Tieto inštrukcie sa na rozdiel od komparátorov pripájajú kedykoľvek v rámci netu (Networku), ale vykonajú sa iba vtedy, ak je podmienka pred nimi splnená (EN = Enable).
*   Základné operácie: **ADD** (Sčítanie), **SUB** (Odčítanie), **MUL** (Násobenie), **DIV** (Delenie - pozor na delenie nulou!), **MOD** (Zvyšok po delení).
*   **Inštrukcia CALCULATE:** 
    *   Špecifická pre Siemens TIA Portal. Namiesto radenia viacerých matematických inštrukcií za sebou umožňuje napísať generickú rovnicu (napr. `(IN1 * IN2) / IN3 + IN4`) do jedného bloku. Zvyšuje prehľadnosť kódu, šetrí pamäť a skracuje cyklus PLC. Výsledok sa zapisuje do parametra OUT.

---

## 📝 Otázky na opakovanie

1. Aký je rozdiel medzi inštrukciou Cievka (Assignment) a inštrukciou Set pri výpadku prichádzajúceho signálu?
2. Prečo je z bezpečnostného hľadiska na vypnutie kritického stroja vhodnejší klopný obvod typu SR než RS?
3. Vysvetli význam instančného dátového bloku (Instance DB) pri IEC časovačoch. Čo by sa stalo, keby dva rovnaké časovače zdieľali jeden DB?
4. Ktorý časovač by si použil na ignorovanie krátkych zábleskov (falošných signálov) z optického snímača na páse?
5. Aká je hlavná výhoda použitia inštrukcie CALCULATE v porovnaní so separátnymi inštrukciami ADD, MUL a DIV?

---

## 📚 Užitočné zdroje

1. [Siemens Industry Online Support: SIMATIC S7-1200 / S7-1500