---
title: Adresovanie a Premenné (Názvy, Dátové typy, UDT, DB)
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 3
---

# Adresovanie a Premenné v TIA Portal

Programovanie v TIA Portal opustilo historický prístup absolútneho adresovania (typický pre staršie systémy Simatic S7-300) a prešlo na **symbolické programovanie**. To znamená, že programátor už primárne nepracuje s fyzickými adresami (napr. `I0.0`), ale s čitateľnými názvami premenných (tagmi, napr. `Snimac_Dveri`). Systém si väzbu medzi menom a pamäťovým miestom riadi na pozadí. 

Správna organizácia premenných, voľba dátových typov a štruktúrovanie pamäte pomocou dátových blokov (DB) a užívateľských typov (UDT) odlišuje profesionálny kód od kódu začiatočníka.

---

## 1. Systém adresovania a pamäťové oblasti

V PLC SIMATIC S7 rozlišujeme niekoľko základných pamäťových oblastí, z ktorých každá slúži na iný účel. Absolútna adresa sa vždy skladá z **identifikátora oblasti, veľkosti (Byte/Word/DWord) a čísla**.

### Fyzické Vstupy (I - Input) a Výstupy (Q - Output)
Tieto adresy reprezentujú reálne svorkovnice na PLC alebo rozširujúcich kartách.
*   **Bitové adresovanie:** `I0.0` (Vstupný byte 0, bit 0).
*   **Byte (8 bitov):** `IB0` (Celý nultý byte vstupov).
*   **Word (16 bitov):** `QW2` (Výstupné slovo, zložené z bytov 2 a 3).

### Pamäťové bity (M - Memory/Marker)
Slúžia ako globálna pomocná pamäť pre medzivýsledky. Tieto premenné sú prístupné z ktoréhokoľvek bloku v programe (OB, FC, FB).
*   *Príklad:* `M10.5`, `MW20`, `MD100` (Memory Double Word).
*   *Upozornenie:* V modernom programovaní (S7-1200/1500) sa použitie tzv. "Merkerov" (M-pamäte) **neodporúča**. Nahrádzajú sa Dátovými blokmi (DB), ktoré sú prehľadnejšie a systémovo bezpečnejšie. "Merkery" sa ponechávajú len pre systémové a hodiny (System and Clock Memory).

### Dátové bloky (DB - Data Blocks)
Tvoria jadro ukladania dát v TIA Portal. Predstavujú tabuľky, v ktorých sú premenné uložené štruktúrovane. Adresovanie vyzerá napríklad ako `DB1.DBX0.0` (v DB1, bit nula), avšak vďaka symbolickému prístupu stačí napísať `Data_Motora.Teplota`.

---

## 2. Názvy premenných (Tags) a PLC Tag Table

Definícia všetkých globálnych premenných, ktoré sú viazané na fyzické I/O, sa nachádza v **PLC Tag Table** (Tabuľke premenných).

**Zásady pre názvy premenných (Naming Conventions):**
Dobrá prax vyžaduje, aby meno premennej jednoznačne definovalo jej účel a umiestnenie v stroji.
1.  **Bez medzier a diakritiky:** Namiesto `Snimac dveri č.1` použi CamelCase (`SnimacDveri1`) alebo Snake_Case (`Snimac_Dveri_1`).
2.  **Konzistentné prefixy:** Často sa používa prefix označujúci typ hardvéru, napr. `DI_` pre digitálny vstup, `DQ_` pre digitálny výstup, `AI_` pre analóg. Príklad: `DI_Start_Tlacidlo`.
3.  **Jazyk:** V profesionálnej sfére by všetky názvy tagov a komentáre mali byť písané v **angličtine**.

---

## 3. Štandardné Dátové typy (Data Types)

Každá premenná musí mať definovaný dátový typ, ktorý určuje, koľko miesta v pamäti zaberie a aký druh informácie môže niesť.

*   **Bool (1 bit):** Iba hodnoty 0 / 1 (TRUE/FALSE). Použitie pre stykače, senzory, tlačidlá.
*   **Byte (8 bitov):** Hodnoty 0 až 255. Zriedkavo sa s ním počíta matematicky, skôr sa používa pre maskovanie.
*   **Int (Integer - 16 bitov):** Celé číslo so znamienkom (od -32 768 do +32 767). Používa sa pre počítadlá a jednoduchú matematiku.
*   **DInt (Double Integer - 32 bitov):** Celé číslo (od cca -2 miliárd do +2 miliárd). Štandard pre časovače a presnejšie výpočty.
*   **Real (32 bitov):** Číslo s pohyblivou rádovou čiarkou (desatinné číslo). Používa sa na zobrazenie reálnych fyzikálnych hodnôt (teplota 23.5 °C, tlak, rýchlosť).
*   **Time:** Špeciálny 32-bitový formát pre čas. Ukladá sa v milisekundách, ale zadáva sa vo formáte `T#5s_200ms`.
*   **String:** Textový reťazec (až 254 znakov). Využíva sa pre posielanie textových správ na HMI displeje alebo do nadradených systémov.

---

## 4. Dátové bloky (Data Blocks - DB)

Na rozdiel od fyzických I/O, Dátové bloky sú miesta v pamäti, ktoré si programátor vytvára sám. Sú ekvivalentom globálnych štruktúr z klasického programovania (napr. v jazyku C).

Rozlišujeme dva druhy DB:
1.  **Global DB (Globálny dátový blok):** 
    *   Môže z neho čítať a zapisovať do neho akýkoľvek iný blok v programe (OB, FC, FB). Používa sa na uloženie receptúr, nastavení HMI alebo prenosových dát.
2.  **Instance DB (Instančný dátový blok):**
    *   Je vždy pevne viazaný na jeden konkrétny Funkčný blok (FB). Obsahuje súkromné dáta daného bloku (lokálne pamäte, stavové premenné). Do inštancie by sa nemalo zapisovať "zvonku".

**Optimalizovaný vs. Štandardný prístup (Optimized Block Access):**
Pre modely S7-1200 a S7-1500 by mali byť všetky DB vytvorené ako "Optimized". V tomto režime TIA Portal na pozadí reorganizuje premenné v pamäti tak, aby sa minimalizovali prázdne miesta a zrýchlilo sa čítanie. Programátor už nevidí absolútne adresy (tzv. offsety), pristupuje k dátam výhradne cez symbolické názvy. Tým sa eliminuje riziko prepísania zlých adresových offsetov.

---

## 5. Užívateľské dátové typy (UDT - User Data Types / PLC Data Types)

UDT (v TIA Portal označené ako PLC Data Types) je absolútne kľúčový nástroj pre **objektovo orientované programovanie PLC**. Umožňuje programátorovi vytvoriť si vlastný dátový typ, ktorý sa skladá z viacerých základných typov, a zoskupiť ich do logického celku.

**Príklad z praxe:** Máme v linke 5 rovnakých motorov. Každý motor potrebuje poznať svoj stav, chybu, aktuálnu rýchlosť a počet motohodín.
Namiesto vytvorenia 20 rôznych premenných vytvoríme v priečinku *PLC Data Types* jeden UDT s názvom `typMotor`:
*   `Start` (Bool)
*   `Error` (Bool)
*   `Aktualna_Rychlost` (Real)
*   `Motohodiny` (DInt)

Následne v Globálnom DB vytvoríme premenné `Motor_1`, `Motor_2` až `Motor_5` a všetkým nastavíme dátový typ `typMotor`. Systém automaticky vygeneruje štruktúru pre každý motor. 

**Výhody UDT:**
*   **Konzistencia:** Ak v budúcnosti potrebujeme pridať motoru novú vlastnosť (napr. teplotu), pridáme ju len do štruktúry UDT. Automaticky sa táto zmena aplikuje na všetky motory vo všetkých DB v programe.
*   **Jednoduché odovzdávanie dát:** Namiesto prepájania 10 rôznych vstupov na FC funkciu pripojíme len jeden PIN, na ktorom je celý typ `typMotor`.

---

## 📝 Otázky na opakovanie

1. Aký je rozdiel medzi pamäťovou oblasťou M (Merkery) a Globálnym dátovým blokom (Global DB)? Prečo preferujeme DB?
2. Aký rozsah hodnôt obsiahne dátový typ Int a čo by sa stalo, ak by sme do neho chceli zapísať číslo 40 000? Ktorý typ by sme mali zvoliť?
3. Vysvetli princíp "Optimized Block Access" pri dátových blokoch v S7-1500. Aký to má vplyv na prístup k adresám?
4. Popíš na konkrétnom príklade, prečo by si použil užívateľský dátový typ (UDT) namiesto vytvárania desiatok samostatných premenných v Tag Table.
5. Môžeš do premennej definovanej v PLC Tag table typu Bool s adresou `I0.0` zapísať v programe inštrukciou Cievka `-( ) -` výsledok z logickej operácie? Zdôvodni svoju odpoveď.

---

## 📚 Užitočné zdroje

1. [Siemens Programming Guideline for S7-1200/S7-1500 (Kapitola: Tag naming and UDTs)](https://support.industry.siemens.com/cs/document/81318674/programming-guidelines-and-programming-styleguide-for-simatic-s7-1200-and-s7-1500?dti=0&lc=en-SK)
2. [Siemens FAQ: What are the advantages of using PLC data types (UDT)?](https://support.industry.siemens.com/cs/document/109780823/what-are-the-advantages-of-using-plc-data-types-(udt)-in-step-7-(tia-portal)-?dti=0&lc=en-SK)
3. [TIA Portal Manual: Difference between optimized and standard block access](https://docs.tia.siemens.cloud/r/simatic_s7_1200_manual_collection_enus_20/programming_concepts_optimized_block_access)