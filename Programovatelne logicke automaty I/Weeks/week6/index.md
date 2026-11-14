```markdown
---
title: SCL Jazyk (Structured Control Language)
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 6
---

# SCL Jazyk (Structured Control Language)

V prostredí Siemens TIA Portal sa pre programovanie logických automatov S7-1200 a S7-1500 využíva niekoľko jazykov definovaných medzinárodnou normou **IEC 61131-3**. Kým grafické jazyky ako LAD (Ladder Logic) a FBD (Function Block Diagram) excelujú pri riadení binárnej logiky (zapínanie motorov, blokovania, vyhodnocovanie snímačov), pri komplexnejších úlohách narážajú na svoje limity. 

Na zložité matematické výpočty, hromadné spracovanie dát v poliach (Arrays), manipuláciu s textom (Strings) a zložité stavové automaty sa využíva textový jazyk **SCL (Structured Control Language)**. V norme IEC je tento jazyk známy pod skratkou **ST (Structured Text)**. V moderných projektoch sa architektúra programu často kombinuje – grafické jazyky tvoria hlavnú kostru a volanie blokov, zatiaľ čo vnútorná logika špecifických výpočtových blokov je napísaná v SCL.

---

## 1. Základná syntax a pravidlá zápisu

SCL je vyšší programovací jazyk, ktorý je syntakticky veľmi blízky jazyku Pascal. Pri písaní kódu je nutné dodržiavať striktné pravidlá kompilátora.

### Priradenie verzus Porovnanie
Toto je najkritickejší rozdiel oproti iným programovacím jazykom (ako C++ alebo Python) a najčastejší zdroj chýb u začiatočníkov.
*   **Priradenie hodnoty (`:=`):** Slúži na zápis (uloženie) hodnoty do premennej. Príkaz hovorí: "Vezmi hodnotu na pravej strane a ulož ju do premennej na ľavej strane."
    *   `#Aktualna_Rychlost := 50.0;`
*   **Porovnanie (`=`):** Slúži výhradne na testovanie rovnosti v podmienkových príkazoch (IF, WHILE). Nevykonáva žiadny zápis.
    *   `IF #Aktualna_Rychlost = 50.0 THEN ...`

### Prístup k premenným v TIA Portal
SCL vizuálne rozlišuje, odkiaľ premenná pochádza, pomocou prefixov:
*   **Lokálne premenné (`#`):** Týka sa premenných definovaných priamo v rozhraní daného bloku (Input, Output, Temp, Static). Príklad: `#VstupnaTeplota`.
*   **Globálne premenné (`"`):** Názvy obalené v úvodzovkách odkazujú na globálne Tagy (fyzické I/O) alebo na Globálne dátové bloky. Príklad: `"DB_Parametre".MaxRychlost` alebo `"I0.0"`.

### Ukončenie príkazu a Komentáre
*   Každý vykonávací príkaz (priradenie, volanie funkcie) musí byť ukončený **bodkočiarkou (`;`)**. Zabudnutie bodkočiarky spôsobí syntaktickú chybu na nasledujúcom riadku.
*   **Jednoriadkový komentár:** Začína dvomi lomkami `// Toto je komentár`.
*   **Viacriadkový komentár:** Uzatvára sa do zátvoriek s hviezdičkou `(* Tento text je na viac riadkov *)`.

---

## 2. Matematika a Logické operácie

V SCL je možné písať zložité matematické rovnice priamo do jedného riadku, čo je neporovnateľne prehľadnejšie než radenie desiatok matematických blokov v LAD.

### Aritmetika a Bitová logika
*   **Základné operátory:** `+`, `-`, `*`, `/`, `MOD` (zvyšok po delení).
*   **Zátvorky:** Riadia prioritu operácií rovnako ako v bežnej algebre.
    *   `#Vysledok := (#A + #B) * ("DB_Data".Konstanta / 100.0);`
*   **Bitové operátory:** `AND`, `OR`, `XOR`, `NOT`. Tieto operátory neslúžia len pre boolovské premenné, ale aj na maskovanie bitov vo vnútri Byte alebo Word štruktúr (tzv. Bitwise operations).

### Vstavané matematické funkcie
TIA Portal SCL obsahuje knižnicu hotových funkcií pre komplexnú matematiku:
*   `ABS(#Hodnota)` – Absolútna hodnota.
*   `SQRT(#Hodnota)` – Druhá odmocnina.
*   `SIN(#Uhol)`, `COS(#Uhol)` – Trigonometrické funkcie (očakávajú hodnotu v radiánoch).
*   `LN(#Hodnota)`, `EXP(#Hodnota)` – Prirodzený logaritmus a exponenciála.

---

## 3. Podmienkové vetvenie (Control Statements)

Podmienky umožňujú programu rozhodovať sa na základe aktuálnych stavov senzorov alebo premenných.

### Štruktúra IF ... ELSIF ... ELSE
Vyhodnocuje výrazy zhora nadol. Hneď ako je nájdená prvá splnená podmienka (TRUE), kód vo vnútri sa vykoná a celý zvyšok bloku IF sa preskočí.

```scl
IF #Teplota_Motora > 90.0 THEN
    #Alarm_Prehriatie := TRUE;
    #Motor_Start := FALSE;
    #Chladenie := TRUE;
    
ELSIF #Teplota_Motora > 70.0 THEN
    // Varovanie, ale motor beží ďalej
    #Alarm_Prehriatie := FALSE; 
    #Chladenie := TRUE;
    
ELSE
    // Normálna prevádzka
    #Alarm_Prehriatie := FALSE;
    #Chladenie := FALSE;
END_IF;

```

*⚠️ Dôležité pravidlo:* V štruktúre IF sa nepoužívajú inštrukcie Set/Reset. Ak v podmienke nastavíš boolovskú premennú na TRUE, musíš zabezpečiť jej nastavenie na FALSE v bloku `ELSE`. Inak si premenná zapamätá stav TRUE natrvalo, aj keď podmienka už dávno neplatí.

### Štruktúra CASE ... OF (Stavové automaty)

Zatiaľ čo `IF` je ideálny pre logiku, `CASE` je nenahraditeľný pre tvorenie sekvencií krokov stroja. Testuje celočíselnú premennú (Int/DInt) a na základe jej hodnoty vykoná príslušný blok kódu.

```scl
CASE #Krok_Stroja OF
    0:  // Krok 0: Čakanie na štart
        #Ventil_A := FALSE;
        IF #Tlacidlo_Start AND ("DB_Senzory".Tlak_OK) THEN
            #Krok_Stroja := 10; // Prechod na ďalší krok
        END_IF;
        
    10: // Krok 10: Napúšťanie
        #Ventil_A := TRUE;
        IF #Senzor_Hladiny = TRUE THEN
            #Krok_Stroja := 20;
        END_IF;
        
    20: // Krok 20: Ukončenie
        #Ventil_A := FALSE;
        #Krok_Stroja := 0; // Slučka sa uzatvára späť na začiatok
        
    ELSE 
        // Tento kód sa vykoná, ak sa premenná dostane do nedefinovaného stavu
        #Krok_Stroja := 0; 
END_CASE;

```

---

## 4. Cykly (Loops) a hromadné spracovanie dát

Cykly sú hlavnou doménou SCL. Umožňujú vykonať rovnakú operáciu stokrát pomocou troch riadkov kódu. Najčastejšie sa používajú na prehľadávanie, sčítavanie alebo triedenie dát v štruktúre Array.

**⚠️ Varovanie (Watchdog Error):** PLC nefunguje ako bežný počítač. Celý užívateľský program (vrátane cyklov) sa musí stihnúť vykonať v rámci jedného Scan Cyklu (zvyčajne do 150 ms). Ak v SCL napíšeš nekonečnú slučku, z ktorej program nedokáže vyskočiť, PLC vyhlási "Cycle time exceeded" a hardvérovo sa prepne do režimu STOP, čím zastaví celú výrobnú linku.

### FOR ... DO (Pevný počet opakovaní)

Používa sa vtedy, keď presne vieme, koľkokrát sa má cyklus vykonať. Indexová premenná sa automaticky inkrementuje.

Príklad: Máme pole 50 snímačov typu Real. Chceme nájsť najvyššiu zaznamenanú teplotu.

```scl
#Max_Teplota := 0.0; // Inicializácia pred hľadaním

FOR #Index := 1 TO 50 BY 1 DO
    // Zistíme, či je aktuálny snímač teplejší než naše doterajšie maximum
    IF "DB_Data".Senzor[#Index] > #Max_Teplota THEN
        #Max_Teplota := "DB_Data".Senzor[#Index];
        #ID_Najvyzsieho_Senzora := #Index; // Zapamätáme si aj to, ktorý to bol
    END_IF;
END_FOR;

```

### WHILE ... DO (Cyklus závislý od podmienky)

Vykonáva sa dovtedy, kým je podmienka TRUE. Používa sa vtedy, keď nevieme presný počet opakovaní, napríklad pri hľadaní prvej prázdnej pozície v zásobníku.

```scl
#Index := 1;
#Najdene := FALSE;

WHILE (#Index <= 100) AND (NOT #Najdene) DO
    IF "DB_Zasobnik".Pozicia[#Index].Prazdna = TRUE THEN
        #Prva_Volna_Pozicia := #Index;
        #Najdene := TRUE; // Splnenie podmienky pre vyskočenie z cyklu
    END_IF;
    
    #Index := #Index + 1; // Manuálna inkrementácia!
END_WHILE;

```

---

## 5. Práca s textovými reťazcami (Strings)

Spracovanie textu v LAD je takmer nemožné. V SCL je to naopak natívna záležitosť. Využíva sa to na komunikáciu s nadradenými IT systémami (MES, ERP), čítanie z čítačiek čiarových kódov (Barcode scanners) alebo generovanie výpisov pre HMI.

* `CONCAT` (Spojenie reťazcov): Spojí dva Stringy do jedného.
* `LEFT`, `RIGHT`, `MID`: Vystrihne určený počet znakov zľava, sprava alebo zo stredu textu.
* `LEN`: Vráti dĺžku aktuálneho reťazca (počet znakov).
* `FIND`: Nájde pozíciu konkrétneho znaku v rámci textu (napríklad hľadá znak čiarky `,` pri spracovaní CSV súboru).

**Príklad použitia:**
Snímač načítal čiarový kód v tvare `"PROD-1234-OK"`. My z neho potrebujeme získať len číslo šarže (1234).

```scl
// Orezanie prvých 5 znakov ("PROD-")
#Docasny_Text := RIGHT(IN := #Nacitany_Barcode, L := LEN(#Nacitany_Barcode) - 5);
// Teraz máme "1234-OK". Orezanie posledných 3 znakov ("-OK")
#Vysledna_Sarza := LEFT(IN := #Docasny_Text, L := LEN(#Docasny_Text) - 3);
// Výsledok vo #Vysledna_Sarza je text "1234".

```

---

## 6. Volanie inštancií, Časovačov a iných blokov v SCL

Ak chceme v SCL použiť časovač (napr. Timer On-Delay - `TON`), musíme ho v hlavičke nášho bloku (sekcia Static) deklarovať ako inštanciu typu `TON_TIME` (alebo `IEC_TIMER`). To isté platí pre volanie iných Funkčných blokov (FB), ktoré vyžadujú vlastnú pamäť.

Kód v SCL sa nerealizuje spájaním čiar, ale priraďovaním hodnôt do vstupných a výstupných parametrov konkrétnej inštancie bloku.

```scl
// Volanie časovača
#Instancia_TON(IN := #Spustacia_Podmienka, 
               PT := T#2s500ms);

// Vyhodnotenie výstupu časovača na ďalšom riadku
IF #Instancia_TON.Q = TRUE THEN
    #Pohyb_Povolil := TRUE;
END_IF;

// Volanie internej funkcie (FC) so zápisom jej výstupu (=>)
"FC_Prevod_Teploty"(Vstup_Analog := "I_Analog_1",
                    Korekcia := 1.5,
                    Teplota_Real => #Teplota_Stroja);

```

Všimnite si kľúčový rozdiel: Vstupom bloku sa dáta posielajú cez znak priradenia `:=`. Zatiaľ čo výstup bloku, ktorý chceme zapísať do našej premennej, sa prepája pomocou operátora šípky `=>`.

---

## 📝 Otázky na opakovanie

1. **Syntax:** Aký operátor sa v SCL používa na priradenie hodnoty premennej a aký na porovnanie dvoch hodnôt v podmienke?
2. **Bezpečnosť cyklov:** Čo je to Watchdog Timer a prečo je chybne napísaný cyklus `WHILE ... DO` pre priemyselné PLC oveľa nebezpečnejší než pre bežný PC program?
3. **Logika podmienok:** Prečo je pri návrhu sekvenčného riadenia (krok za krokom) vhodnejšie zvoliť štruktúru `CASE ... OF` namiesto množstva `IF ... ELSIF` podmienok?
4. **Práca s textom:** Opíš scenár z priemyselnej praxe, pri ktorom by si nevyhnutne musel použiť inštrukcie `CONCAT`, `MID` alebo `LEFT`.
5. **Volanie blokov:** Aký je rozdiel medzi operátormi `:=` a `=>` pri volaní bloku (napr. FC) vo vnútri SCL kódu?

---

## 📚 Užitočné zdroje

1. [Siemens TIA Portal Manual: SCL (Structured Control Language) Programming overview](https://www.google.com/search?q=https://docs.tia.siemens.cloud/r/simatic_s7_1200_manual_collection_enus_20/programming_concepts_scl)
2. [Siemens Industry Online Support: Examples for SCL Programming in STEP 7 (TIA Portal)](https://www.google.com/search?q=https://support.industry.siemens.com/cs/document/59643194/examples-for-scl-programming-in-step-7-(tia-portal)-%3Fdti%3D0%26lc%3Den-SK)
3. [RealPars: Structured Text (ST) PLC Programming Basics](https://realpars.com/structured-text/)

```

```