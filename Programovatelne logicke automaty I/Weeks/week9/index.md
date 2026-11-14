---
title: HMI - Faceplate a Knižnice
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 9
---

# HMI - Faceplates a Knižnice (Libraries)

V priemyselnej automatizácii sa neustále opakujú tie isté prvky: motory, čerpadlá, ventily, PID regulátory. Kresliť pre každý z 50 motorov na linke rovnakú grafiku, tlačidlá a popisy je mimoriadne neefektívne a pri neskorších zmenách (napríklad pridaní jedného tlačidla pre všetky motory) priam katastrofálne z hľadiska času. TIA Portal tento problém rieši pomocou konceptu **Faceplates (Grafické typy)** a **Libraries (Knižnice)**.

Tento prístup úzko súvisí s objektovo orientovaným programovaním v PLC (používanie UDT dátových typov a FB blokov). Spolu tvoria najvyššiu úroveň štandardizácie programu.

---

## 1. Čo je to Faceplate?

**Faceplate** (v TIA Portal označovaný ako Faceplate Type) je **znovu použiteľný grafický blok**. Predstav si ho ako "okno v okne". 
Vytvoríš si ho iba raz (nakreslíš do neho čerpadlo, I/O polia pre rýchlosť, tlačidlá Štart/Stop a stavové kontrolky) a následne tento Faceplate vložíš na obrazovku 50-krát.

Každý vložený Faceplate sa nazýva **Inštancia (Instance)**.

**Kľúčové výhody:**
1.  **Centrálna úprava (Central Modification):** Ak zákazník po roku prevádzky požiada, aby sa farba zapnutého motora zmenila zo zelenej na modrú, otvoríš iba pôvodný Faceplate Type, zmeníš farbu, uložíš a TIA Portal automaticky aktualizuje všetkých 50 motorov vo všetkých obrazovkách projektu.
2.  **Zapuzdrenie (Encapsulation):** Vo vnútri Faceplatu nemôžeš priamo použiť HMI tagy z projektu. Faceplate má svoje vlastné **Rozhranie (Interface)**. Až keď vložíš inštanciu na obrazovku, pripojíš k jej rozhraniu konkrétne premenné.

---

## 2. Prepojenie PLC a HMI (UDT a Faceplate)

Skutočná sila Faceplatu sa prejaví vtedy, ak ho prepojíme s Užívateľským dátovým typom (UDT) z PLC.
Ak na pripojenie jedného motora do Faceplatu potrebujeme preniesť 15 premenných (Štart, Stop, Porucha, Rýchlosť_Aktualna, Rýchlosť_Žiadaná...), bolo by nepraktické prepájať 15 samostatných pinov.

**Profi postup (Best Practice):**
1.  **V PLC:** Vytvoríme štruktúru `UDT_Motor`, ktorá obsahuje všetky tieto premenné. V DB vytvoríme 50 motorov s typom `UDT_Motor`.
2.  **Vo Faceplate:** V jeho rozhraní (Interface) vytvoríme iba jeden jediný pin s názvom "Data" a ako dátový typ mu priradíme nami vytvorené `UDT_Motor`.
3.  **Na obrazovke:** Vložíme Faceplate a na jeho jediný pin "Data" pripojíme z HMI Tagov napr. `DB_Motory.Motor_1`.
Softvér na pozadí sám správne rozvetví všetky potrebné bity a čísla priamo do grafiky vo vnútri Faceplatu.

---

## 3. Typy Knižníc (Libraries)

Aby sme mohli Faceplates, ale aj PLC bloky (FB, FC, UDT) ukladať a prenášať, TIA Portal využíva systém Knižníc. Rozlišujeme dve základné úrovne.

### Project Library (Projektová knižnica)
Je viazaná výlučne na jeden konkrétny TIA Portal projekt (súbor .ap18, .ap19 atď.). 
Obsahuje dva priečinky:
*   **Types (Typy):** Sem patria objekty, ktoré sa dajú verziovať a sú prepojené so svojimi inštanciami v projekte (Faceplates, UDT, FB bloky). Ak zmeníš *Type* v knižnici, systém ti ponúkne aktualizáciu všetkých inštancií v projekte.
*   **Master Copies (Kópie):** Sem patria hlúpe, "mŕtve" kópie. Sú to len výstrižky. Ak si sem hodíš nejakú nakreslenú HMI obrazovku a neskôr ju vložíš do projektu, stratí väzbu na knižnicu. Zmena v knižnici ju už spätne neaktualizuje. (Používa sa na hardvérové konfigurácie alebo celé foldre).

### Global Library (Globálna knižnica)
Zatiaľ čo Project Library zanikne so zmazaním projektu, **Global Library** je samostatný súbor (s príponou `.al18`, `.al19`), ktorý leží na disku počítača alebo na firemnom serveri.
*   Slúži na zdieľanie štandardov medzi viacerými programátormi v tíme.
*   Typický postup: Skúsený inžinier vytvorí štandardný `UDT_Ventil`, blok `FB_Ventil` a grafiku `Faceplate_Ventil`. Všetko to uloží do Globálnej knižnice. Títo knižnicu si stiahnu 10 junior programátori, pripoja ju k svojim novým projektom a používajú overené bloky (bez toho, aby ich museli programovať od nuly).
*   *Upozornenie:* Aby si mohol do Globálnej knižnice niečo vložiť, musíš ju mať otvorenú v režime zápisu (Remove Write Protection). Mnoho firemných knižníc sa otvára len na čítanie (Read-Only), aby ich niekto omylom neprepísal.

---

## 4. Tvorba a editácia Faceplatu (Verziovanie)

Pretože objekty v priečinku *Types* (teda aj Faceplates) slúžia ako šablóny, TIA Portal ich prísne chráni pred náhodnou úpravou. Nemôžeš ich len tak otvoriť a prepísať. Funguje tu striktný systém verziovania.

1.  **Edit type (Úprava typu):** Ak chceš Faceplate upraviť, musíš v knižnici kliknúť pravým tlačidlom na jeho verziu (napr. V 1.0.0) a vybrať "Edit Type". 
2.  **In testing (V testovaní):** Otvorí sa ti editor. Pôvodná verzia zostáva nedotknutá v ostrej prevádzke. Ty pracuješ na testovacej vrstve.
3.  **Release version (Vydanie verzie):** Keď zmeny dokončíš a otestuješ, musíš typ vydať ("Release"). Systém ťa vyzve, aby si mu pridelil nové číslo verzie (napríklad V 1.0.1, V 1.1.0 pre väčšiu zmenu, alebo V 2.0.0 pri úplnej prestavbe funkčnosti).
4.  **Update Instances (Aktualizácia v projekte):** Následne sa ťa TIA Portal opýta, či chceš všetky existujúce Faceplaty na obrazovkách tvojho projektu "upgradovať" na túto novú verziu. Môžeš to urobiť hneď, alebo nechať niektoré stroje bežať na starej verzii a iné na novej.

Tento systém chráni firemné štandardy. Ak do projektu importuješ aktualizovaný `FB_Motor` V2.0 z Globálnej knižnice a zistíš, že obsahuje chybu, môžeš v Project knižnici kedykoľvek kliknúť pravým a zvoliť downgrade inštancií späť na stabilnú verziu V1.0.

---

## 📝 Otázky na opakovanie

1. Aký je najväčší benefit prenesenia celej štruktúry `UDT` (Užívateľský dátový typ) do rozhrania (Interface) Faceplatu, v porovnaní s mapovaním každej boolovskej a analógovej premennej zvlášť?
2. Vysvetli zásadný rozdiel medzi *Project Library* a *Global Library*. Ktorú použiješ, ak chceš poslať svoj naprogramovaný motorový blok kolegovi, ktorý pracuje na inom projekte?
3. Čo sa stane, ak vložíš objekt z priečinka *Master Copies* (napríklad nakreslené logo) do troch rôznych obrazoviek a neskôr v Knižnici toto logo prefarbíš? Prefarbia sa aj logá na obrazovkách? Zdôvodni.
4. Aký je účel číslovania verzií (Versioning) pri objektoch v sekcii *Types*?
5. Môžeš vo vnútri Faceplatu priamo nastaviť animáciu na premennú (Tag), ktorá sa nachádza vonku v HMI Tag tabuľke projektu? Ak nie, ako sa to správne rieši?

---

## 📚 Užitočné zdroje

1. [Siemens Industry Online Support: Creating Faceplates in WinCC (TIA Portal)](https://support.industry.siemens.com/cs/document/68014632/how-do-you-create-faceplates-with-wincc-(tia-portal)-?dti=0&lc=en-SK)
2. [TIA Portal Manual: Working with libraries](https://docs.tia.siemens.cloud/r/simatic_wincc_unified_v18_manual_enus_20/hmi_working_with_libraries)
3. [Siemens Application Example: Basic principles for creating HMI faceplates](https://support.industry.siemens.com/cs/document/109477038/hmi-design-masterclass-basic-principles-for-creating-hmi-faceplates?dti=0&lc=en-SK)