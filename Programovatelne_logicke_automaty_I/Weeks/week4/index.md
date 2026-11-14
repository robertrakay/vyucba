---
title: Architektúra blokov (OB, FC, FB)
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 4
---

# Architektúra programových blokov (OB, FC, FB)

Kvalitný PLC program v systémoch Siemens sa nikdy nepíše ako dlhý "špagetový" kód v jednom bloku. Namiesto toho sa využíva **štruktúrované programovanie**. Program sa rozdeľuje na menšie, logické a znovu použiteľné časti (bloky), ktoré plnia špecifické funkcie. Hlavnou úlohou programátora je rozhodnúť, kedy použije Organizačný blok (OB), kedy Funkciu (FC) a kedy Funkčný blok (FB).

---

## 1. Organizačné bloky (OB - Organization Blocks)

Organizačné bloky predstavujú **rozhranie medzi operačným systémom PLC a užívateľským programom**. Nedajú sa volať z iných blokov v programe; sú spúšťané výhradne samotným PLC na základe špecifických udalostí (času, chýb alebo hardvérových prerušení).

### OB1: Main (Program Cycle)
*   Toto je **hlavný riadiaci cyklus**. Operačný systém ho volá neustále dokola v nekonečnej slučke (tzv. scan cycle).
*   Ak napíšeš všetok kód priamo do OB1, program síce bude fungovať, ale bude absolútne neprehľadný.
*   **Best Practice:** OB1 by mal slúžiť iba ako akýsi "manažér" alebo "rozcestník". Nemala by v ňom byť priama logika na spínanie výstupov, malo by v ňom prebiehať len volanie (Call) ďalších blokov (FC a FB) v logickom poradí.

### Špeciálne organizačné bloky (Interrupts)
Slúžia na riešenie situácií, ktoré neznesú odklad, alebo na vykonávanie logiky, ktorá si vyžaduje absolútne presné časovanie. Ak nastane podmienka pre ich spustenie, PLC **preruší** vykonávanie bežného cyklu (OB1), vykoná kód v špeciálnom OB a potom sa vráti presne tam, kde v OB1 prestalo.

*   **OB100 (Startup):** Vykoná sa presne jedenkrát pri prechode PLC zo stavu STOP do stavu RUN. Používa sa na inicializáciu premenných, kalibráciu snímačov alebo nastavenie štartovacích parametrov, ktoré je potrebné vykonať pred spustením hlavného cyklu.
*   **OB30 - OB38 (Cyclic Interrupt):** Spúšťa sa v presne definovanom časovom intervale (napr. presne každých 100 ms). Zatiaľ čo cyklus OB1 kolíše podľa toho, ako dlho trvá spracovanie kódu (napr. raz 2 ms, inokedy 15 ms), Cyclic Interrupt je absolútne presný. Využíva sa na výpočty derivácií a integrálov, zber štatistických dát a predovšetkým na volanie blokov pre PID regulátory.
*   **OB40 (Hardware Interrupt):** Spustí sa v okamihu, keď fyzický vstup na karte PLC zaregistruje zmenu (nábežnú alebo dobehovú hranu). Je nezávislý od času cyklu OB1. Využíva sa na kritické snímače, kde reakčný čas hrá dôležitú rolu (zachytenie rýchlo letiaceho výrobku).
*   **OB82 (Diagnostic Error Interrupt):** Spustí sa, ak niektorý z hardvérových modulov (napr. I/O karta, pripojený frekvenčný menič) nahlási chybu (napr. skrat na snímači, strata komunikácie). Zabraňuje tomu, aby PLC automaticky spadlo do stavu STOP (ak OB82 chýba, závažná chyba často vedie k zastaveniu chodu celého PLC).

---

## 2. Funkcie (FC - Functions)

Funkcie (FC) sú bloky kódu, ktoré obsahujú užívateľský program, ale **nemajú vlastnú vnútornú pamäť**. 
Keď funkcia skončí svoje vykonávanie, všetky dočasné premenné (TEMP), ktoré vo vnútri použila, sa zmažú a pre ďalší cyklus nie sú k dispozícii. 

**Vlastnosti a rozhranie (Interface):**
Rozhranie FC definuje piny, cez ktoré blok komunikuje s okolím:
*   `Input`: Vstupné parametre (len na čítanie).
*   `Output`: Výstupné parametre (na zápis výsledku).
*   `InOut`: Parametre, ktoré funkcia prečíta, modifikuje a zapíše späť.
*   `Temp`: Dočasné premenné, platné len v čase vykonávania FC. Neudržujú stav.
*   `Return`: Matematický alebo logický výsledok (Návratová hodnota funkcie, podobne ako v C/C++).

**Kedy použiť FC?**
FC sa využívajú na matematické prepočty, formátovanie dát, alebo logické operácie, kde výsledok závisí *výlučne od aktuálneho stavu vstupov*.
*   *Príklad:* Prepočet analógového signálu (0-27648) na reálnu teplotu (0.0 °C - 100.0 °C). Ak na vstup FC privedieš rovnaké číslo, na výstupe vždy dostaneš ten istý výsledok. Funkcia si nepotrebuje pamätať včerajšiu teplotu.

---

## 3. Funkčné bloky (FB - Function Blocks)

Funkčné bloky (FB) predstavujú "vyššiu ligu" a sú základom objektovo orientovaného riadenia. Na rozdiel od FC, **FB majú vlastnú vnútornú pamäť**. 
Táto pamäť je fyzicky uložená v priradenom **Instančnom dátovom bloku (Instance DB)**, ktorý sa vytvorí zakaždým, keď blok FB zavoláš v kóde.

**Vlastnosti a rozhranie (Interface):**
Rozhranie FB má oproti FC navyše kľúčovú sekciu:
*   `Static`: Premenné v tejto sekcii sú statické (trvalé). Ich stav sa ukladá do Instance DB a prežije koniec cyklu PLC. FB si vďaka nim pamätá, čo sa dialo v predchádzajúcich cykloch.

**Kedy použiť FB a prístup s viacnásobnými inštanciami (Multi-instance)?**
FB sa používajú vtedy, ak logika musí ovládať priebeh procesu v čase – teda potrebuje časovače, počítadlá, hrany signálov alebo si musí pamätať svoj vlastný stav (State Machine).

*   *Príklad:* Máme linku s 3 rovnakými dopravníkmi. Naprogramujeme jeden univerzálny FB pre dopravník (ktorý obsahuje jeho zapínanie, chybové stavy a oneskorenia zastavenia).
*   V OB1 tento blok FB zavoláme trikrát (tzv. Multiple Call).
*   Pri každom volaní k nemu systém priradí iný Instance DB (DB11 pre Dopravník_1, DB12 pre Dopravník_2, DB13 pre Dopravník_3).
*   Jeden kus kódu tak riadi tri rôzne zariadenia nezávisle od seba. Ak v kóde (v samotnom FB) urobíme zmenu, aktualizujú sa naraz všetky tri dopravníky.

**Multi-Instance (Zaborenie blokov):**
Ak naprogramujeme vnútri nášho FB pre Dopravník inštrukciu Časovača (TON), aj ten vyžaduje pamäťový blok. Ak použijeme model *Multi-instance*, pamäť časovača sa vytvorí ako sekcia (premenná) priamo v hlavnom DB Dopravníka. Tým minimalizujeme počet vygenerovaných DB a zjednodušujeme štruktúru projektu (nevzniká neporiadok vo forme desiatok samostatných DB blokov pre časovače).

---

## 4. Lokálne vs. Globálne premenné

Základným pravidlom pre vytváranie univerzálnych (znovu použiteľných) blokov FC a FB je nepoužívať v ich vnútri tzv. globálne premenné (priame I/O adresy ako `I0.0`, alebo premenné z globálnych DB). 

Prečo? Ak natvrdo zaviažeš vnútri FB štart motora na adresu `I0.0`, tento blok bude vedieť zapnúť len tento jeden konkrétny motor a stáva sa univerzálne nepoužiteľným.
Namiesto toho všetky údaje musia do FB/FC prichádzať výlučne cez piny na jeho rozhraní (cez `Input` a `Output`). Takýto blok sa dá jednoducho skopírovať a predať kolegovi na iný projekt.

---

## 📝 Otázky na opakovanie

1. Aká je hlavná a najdôležitejšia odlišnosť medzi Funkciou (FC) a Funkčným blokom (FB)?
2. Vysvetli pojem Instančný dátový blok (Instance DB). Ku ktorému bloku sa viaže a načo slúži?
3. Prečo nie je vhodné umiestniť logiku pre výpočet PID regulátora do hlavného cyklu OB1, ale voláme na to špeciálny Cyclic Interrupt (napr. OB30)?
4. Čo sa stane s hodnotami premenných v sekcii `Temp` po dokončení vykonávania bloku FC a presune na ďalší riadok v OB1?
5. Ak chceš vytvoriť univerzálny blok pre výpočet obvodu kruhu na základe jeho polomeru, použiješ FC alebo FB? Prečo?

---

## 📚 Užitočné zdroje

1. [Siemens Industry Support: What are the differences between FC and FB functions in STEP 7 (TIA Portal)?](https://support.industry.siemens.com/cs/document/109749550/what-are-the-differences-between-the-function-blocks-(fb)-and-the-functions-(fc)-in-step-7-(tia-portal)-?dti=0&lc=en-SK)
2. [TIA Portal Manual: Calling Organization Blocks (OBs)](https://docs.tia.siemens.cloud/r/simatic_s7_1200_manual_collection_enus_20/programming_concepts_organization_blocks)
3. [Siemens Programming Guideline: Reusability and Multi-instances](https://support.industry.siemens.com/cs/document/81318674/programming-guidelines-and-programming-styleguide-for-simatic-s7-1200-and-s7-1500?dti=0&lc=en-SK)