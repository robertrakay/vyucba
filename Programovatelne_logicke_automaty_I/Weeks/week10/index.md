---
title: Pokročilé signály a regulácia (Analóg, HSC, PWM, PID)
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 10
---

# Pokročilé spracovanie signálov a regulácia v TIA Portal

Kým digitálne vstupy a výstupy (1/0) reprezentujú stavy stroja (zapnutý/vypnutý, senzor vidí/nevidí), reálny svet je spojitý. Rýchlosť, teplota, poloha, tlak a prietok vyžadujú pokročilé metódy spracovania dát, presné časovanie a spätnú väzbu. V tejto kapitole sa zameriame na to, ako PLC S7-1200 a S7-1500 komunikujú s fyzikálnym svetom.

---

## 1. Analógové signály (A/D a D/A prevodníky)

Analógové senzory prevádzajú fyzikálne veličiny (napr. teplotu 0-100 °C) na štandardizované elektrické signály. Tieto signály následne vstupujú do A/D (Analógovo-digitálneho) prevodníka v PLC.

### Priemyselné štandardy signálov
*   **Napäťové (0 – 10 V):** Jednoduchšie na meranie (paralelné pripojenie), ale veľmi náchylné na elektromagnetické rušenie (EMC) a úbytky napätia na dlhých kábloch.
*   **Prúdové (4 – 20 mA):** Priemyselný štandard. Sú imúnne voči úbytkom napätia na dĺžke kábla. Rozsah začína od 4 mA (tzv. "živá nula") z dôležitého bezpečnostného dôvodu: ak prúd klesne na 0 mA, PLC okamžite vie, že došlo k pretrhnutiu kábla (Wire break).
*   **Odporové (PT100 / Ni1000):** Teplotné snímače, ktoré menia svoj odpor v závislosti od teploty. PLC karty pre RTD (Resistance Temperature Detector) dokážu tento odpor priamo merať a v programe priamo vracajú hodnotu v stupňoch Celzia (napr. hodnota 235 = 23,5 °C).

### "Magické" číslo 27648 a spracovanie v programe
Siemens PLC (na rozdiel od Arduina, ktoré má 10-bitový prevodník vracajúci 0-1023) prevádza nominálny rozsah analógového signálu (napr. 0-10V) na celočíselnú (Integer) hodnotu od **0 do 27648**.
*   *Prečo nie 32767 (čo je maximum pre 16-bitový Integer)?* Zvyšný rozsah od 27649 do 32767 je ponechaný ako rezerva (Overrange) pre diagnostiku. Ak senzor nameria napätie 11 V, PLC zistí pretečenie a dokáže vyhodiť chybu merania bez toho, aby pretiekla premenná.

### Inštrukcie NORM_X a SCALE_X
V starších systémoch (S7-300) sa na prepočet požívali zložité funkcie (FC105). V TIA Portal sa používa elegantná dvojica inštrukcií:
1.  **NORM_X (Normalizácia):** Zoberie hrubú hodnotu z prevodníka (napr. Int 0 - 27648) a prevedie ju na percentuálnu hodnotu Real od 0.0 do 1.0.
2.  **SCALE_X (Škálovanie):** Zoberie normalizovanú hodnotu (0.0 - 1.0) a roztiahne ju na reálne fyzikálne jednotky stroja (napr. 0.0 °C - 150.0 °C).

**Príklad v SCL:**
```scl
// 1. Normalizácia surového signálu z adresy IW64 (Senzor 0-10V)
#Norm_Hodnota := NORM_X(MIN := 0, 
                        VALUE := "AI_Senzor_Tlaku", 
                        MAX := 27648); // Výsledok je Real (napr. 0.5 pre stredný tlak)

// 2. Škálovanie na reálny tlak v baroch (Senzor má rozsah 0 - 10.0 bar)
#Tlak_V_Baroch := SCALE_X(MIN := 0.0, 
                          VALUE := #Norm_Hodnota, 
                          MAX := 10.0);

```

Pre **Analógové výstupy** (ovládanie frekvenčného meniča 0-10V) je postup presne opačný: Najprv `NORM_X` z (0.0 - 50.0 Hz) na (0.0 - 1.0), a potom `SCALE_X` z (0.0 - 1.0) na (0 - 27648).

---

## 2. Signály HSC (High-Speed Counter) a Enkodéry

Štandardný OB1 cyklus PLC trvá napríklad 10 ms (100 Hz). Ak chceme merať presnú polohu motora alebo dĺžku odrezaného materiálu, používame tzv. **Inkrementálny rotačný snímač (Enkodér)**.
Ak má enkodér rozlíšenie 1000 pulzov na otáčku a hriadeľ sa točí rýchlosťou 600 RPM (10 otáčok za sekundu), enkodér vygeneruje **10 000 pulzov za sekundu (10 kHz)**.
Program v OB1 nedokáže tieto pulzy zachytiť, pretože za jeden jeho 10 ms cyklus sa fyzicky odohrá 100 pulzov – PLC zistí iba to, že vstup je 1, ale "nevidí", čo sa dialo medzi tým.

### Princíp hardvérového čítača (HSC)

Tento problém rieši **High-Speed Counter (HSC)**. Je to kus nezávislého hardvéru (mikročipu) priamo na vstupnej karte PLC, ktorý číta pulzy bleskovou rýchlosťou (až do 100 kHz alebo 1 MHz, v závislosti od CPU) úplne nezávisle od softvérového cyklu OB1. V OB1 si programátor prečíta len finálne číslo, koľko pulzov čítač napočítal.

### Ako to funguje v TIA Portal

1. **Hardvérová konfigurácia (Device Configuration):** V nastaveniach samotného CPU musíme povoliť HSC kanál (napr. HSC 1), zvoliť režim čítania (A/B phases) a vyhradiť mu fyzické vstupy (napr. I0.0 pre kanál A, I0.1 pre kanál B). Enkodér z fázového posunu kanálov A a B dokáže okrem rýchlosti určiť aj smer otáčania.
2. **Volanie inštrukcie CTRL_HSC:**
V kóde sa používa špeciálny systémový blok `CTRL_HSC` (Control High Speed Counter). Tento blok neslúži na samotné "sčítavanie" (to robí hardvér), ale na *ovládanie* čítača.
* Používa sa napríklad na **vynulovanie (Reset)** hodnoty čítača, keď stroj narazí na koncový referenčný spínač (Home position).
* Aktuálna hodnota (poloha) sa dá na moderných CPU sčítať aj tak, že sa čítač jednoducho namapuje do I/O pamäte ako Input Double Word (napr. `%ID1000`), a túto adresu môžeme v programe kedykoľvek prečítať a porovnávať.



---

## 3. Výstup PWM (Pulse Width Modulation)

**Pulzno-šírková modulácia (PWM)** je metóda, ako pomocou digitálneho (dvojstavového) výstupu riadiť analógovú veličinu – najčastejšie výkon, otáčky malých DC motorov, alebo teplotu ohrevných telies (cez Solid State Relé - SSR).

Namiesto toho, aby sme na ohrievač posielali zložité spojité analógové napätie od 0V do 230V, posielame naň vždy plné napätie, ale vo veľmi rýchlych impulzoch.
Pomer medzi časom, kedy je výstup zapnutý, a celkovou dĺžkou periódy sa nazýva **Strieda signálu (Duty Cycle)**.

* **0 % Duty Cycle:** Výstup je trvalo vypnutý. (Výkon 0 %)
* **50 % Duty Cycle:** Výstup sa rýchlo prepína – polovicu času svieti, polovicu nesvieti. Zotrvačnosťou systému (tepelnou alebo mechanickou) sa to prejaví ako 50% výkon.
* **100 % Duty Cycle:** Výstup je trvalo zapnutý.

### Implementácia v TIA Portal (Pulse Generators)

Rovnako ako HSC na vstupoch, klasické reléové výstupy nestíhajú kmitať s frekvenciou kilohertzov. Pre PWM je **nutné použiť PLC s tranzistorovými výstupmi (Solid-state, DC/DC/DC modely)**, ktoré dokážu kmitať miliónkrát bez opotrebenia kontaktov.

1. **Aktivácia (Device Config):** V nastaveniach CPU povolíme *Pulse generator (PTO/PWM)*. Tu nastavíme periódu signálu (napr. 10 ms pre rýchly priebeh, alebo aj 2 sekundy pre pomalé SSR relé riadiace kúrenie pece).
2. **Inštrukcia CTRL_PWM:** Tento blok sa vyvoláva v programe. Parametrom `ENABLE` zapíname/vypíname generovanie.
3. **Zápis striedy (Duty Cycle):** Odošle sa do dedikovaného výstupného slova (QW). V závislosti od konfigurácie hardvéru má hodnotu napríklad od 0 do 100 (v percentách) alebo jemnejšiu od 0 do 27648, podobne ako analóg.

---

## 4. Uzavreté regulačné slučky (PID Regulátor)

Keď už vieme prečítať analógový senzor (napr. merať teplotu pece) a vieme ovládať akčný člen (napr. ohrievač cez PWM alebo analógový ventil), potrebujeme do systému vniesť **mozog, ktorý ich prepojí a udrží na požadovanej hodnote**. K tomu slúži **PID regulátor**.

Základným problémom riadenia on/off (termostat) je, že systém zotrváva v osciláciách a "prestrelí" cieľovú teplotu. PID (Proporcionálno-Integračno-Derivačný) regulátor neustále sleduje tzv. **Regulačnú odchýlku (Error)**, čo je rozdiel medzi želanou hodnotou (Setpoint) a skutočnou hodnotou nameranou snímačom (Feedback/Process Value).

* **P-zložka (Proporcionálna):** Reaguje na okamžitú veľkosť chyby. Čím ďalej sme od cieľa, tým viac pridá plyn (otvorí ventil).
* **I-zložka (Integračná):** Pamätá si históriu. Ak sme blízko cieľa, ale dlhodobo ho nevieme dosiahnuť (napríklad tepelné straty kompenzujú P-zložku), I-zložka túto malú dlhodobú chybu sčíta (zintegruje) a posunie výkon vyššie, kým sa chyba nezrovná na absolútnu nulu.
* **D-zložka (Derivačná):** Pozerá do budúcnosti. Reaguje na rýchlosť zmeny. Ak sa teplota blíži k cieľu príliš rýchlo, D-zložka "stúpi na brzdu", aby predišla prestreleniu. (Často sa pri teplotných systémoch vypína, používa sa pri polohe alebo rýchlosti).

### PID_Compact v TIA Portal (Technology Objects)

V TIA Portal sa PID realizuje pomocou tzv. **Technology Object (TO)**. Je to špeciálny systémový modul, ktorý okrem kódu obsahuje aj vlastnú diagnostickú a nastavovaciu obrazovku.

**Kľúčové pravidlo - Cyclic Interrupt (OB30)!**
PID matematické algoritmy (najmä integrály a derivácie) vyžadujú na svoj výpočet **absolútne presný a nemenný časový krok** (napr. $dt = 100 ms$).
Regulátor `PID_Compact` preto **NIKDY nesmie byť volaný v hlavnom cykle OB1**, pretože čas obehu OB1 kolíše. Musí sa umiestniť do *Cyclic Interrupt OB* (napr. OB30), ktorému v hardvéri nastavíme spúšťanie presne každých 100 ms.

**Ako sa konfiguruje PID_Compact:**

1. **Vstupy:**
* `Setpoint` (Žiadaná hodnota, napr. 200.0 °C)
* `Input` (Analógová meraná hodnota, napr. vrátená z inštrukcie SCALE_X)


2. **Výstupy:**
* `Output` (Analógový výstup, ktorý sa prepojí do inštrukcie NORM_X a pošle do ventilu).
* `Output_PWM` (Priamy bitový výstup, ktorý automaticky pulzuje a môže ovládať striedu PWM priamo).


3. **Ladenie (Tuning):** TIA Portal disponuje excelentnou funkciou *Auto-Tuning* (Pre-tuning a Fine-tuning). Otvoríš si okno PID a spustíš automatické meranie. Regulátor sám "vykopne" skokovú zmenu na výstupe, sleduje, ako rýchlo systém a senzory zareagujú, a sám si vypočíta matematické konštanty pre P, I, a D, čím ušetrí inžinierovi hodiny ručného ladenia.

---

## 📝 Otázky na opakovanie

1. Aká konštanta (Integer) reprezentuje v siemenských analógových prevodníkoch maximálnu nominálnu hodnotu (napr. pri 10 V alebo 20 mA) a prečo konštruktéri nevyužili plný rozsah 32767?
2. Máš 16-bitové číslo z analógového senzora vzdialenosti. Popíš krok za krokom (použitie a parametre inštrukcií), ako z tohto čísla získaš v programe hodnotu vzdialenosti v milimetroch.
3. Prečo nemôžeme na meranie vysokých otáčok z inkrementálneho snímača (Enkodéra) použiť bežný digitálny vstup a obyčajné počítadlo (CTU) vo vnútri OB1? Čo je to HSC?
4. Ak potrebuješ PID regulátorom udržiavať konštantnú teplotu vody, prečo nesmieš blok `PID_Compact` vložiť priamo do hlavného programu OB1? Kde ho musíš zavolať?
5. Vysvetli pojem *Strieda signálu (Duty Cycle)* pri PWM. Ako sa prejaví na ohrievacom telese s pomalou zotrvačnosťou, ak na výstup zapíšeme Duty Cycle 25 %?

---

## 📚 Užitočné zdroje

1. [Siemens Industry Online Support: How do you standardize and destandardize analog values with STEP 7 (TIA Portal)?](https://support.industry.siemens.com/cs/document/39334504/for-an-s7-1200-s7-1500-controller-in-step-7-(tia-portal)-how-do-you-scale-integer-values-in-real-numbers-and-vice-versa-for-analog-inputs-and-outputs-?dti=0&lc=en-SK)
2. [Siemens TIA Portal Manual: Principle of High-Speed Counters (HSC)](https://www.google.com/search?q=https://docs.tia.siemens.cloud/r/simatic_s7_1200_manual_collection_enus_20/technology_hsc_principle)
3. [Siemens Application Example: Control loop optimization with PID_Compact](https://www.google.com/search?q=https://support.industry.siemens.com/cs/document/109793135/control-loop-optimization-with-pid_compact-v2-2%3Fdti%3D0%26lc%3Den-SK)
4. [Control.com: Understanding PID Control and the Mathematics behind it](https://www.google.com/search?q=https://control.com/technical-articles/introduction-to-pid-control-proportional-integral-derivative/)

```