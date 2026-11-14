---
title: Vizualizácia na HMI (Základy)
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 7
---

# Vizualizácia na HMI (Základy tvorby obrazoviek)

Programovateľný logický automat (PLC) riadi stroj neviditeľne na pozadí. Aby mohol operátor stroj ovládať, zadávať parametre výroby a vidieť aktuálny stav, využíva sa **HMI panel (Human Machine Interface)**. V prostredí TIA Portal je obrovskou výhodou, že programovanie PLC a tvorba HMI vizualizácie prebiehajú v jednom softvéri a zdieľajú spoločnú databázu premenných (Tags). Vývojárske prostredie pre HMI panely Siemens sa nazýva **WinCC (Windows Control Center)**.

---

## 1. Architektúra HMI v TIA Portal

Pred samotným kreslením obrazoviek je nutné pochopiť, ako HMI panel komunikuje s PLC a aké typy HMI systémov existujú.

### Typy HMI systémov
*   **Basic Panels:** Základná rada panelov (napr. KTP400, KTP700 Basic). Určené pre jednoduché aplikácie, obmedzený počet objektov a alarmov. Nepodporujú pokročilé skriptovanie (VBS).
*   **Comfort Panels:** Profesionálna rada pre náročné aplikácie. Vyššie rozlíšenie, podpora archivácie dát (datalogging), prehrávanie videí z kamier, skriptovanie vo VBScript (Visual Basic) a tvorba pokročilých Faceplate.
*   **WinCC Advanced (PC Runtime):** HMI nebeží na fyzickom dotykovom paneli, ale ako aplikácia na štandardnom priemyselnom PC (IPC) so systémom Windows.

### HMI Tags (Prepojenie s PLC)
HMI panel nepracuje s PLC nepretržite, ale v cykloch (zvyčajne každých 100 ms až 1 sekunda). PLC kód by **nikdy** nemal byť časovo závislý od odozvy HMI.
*   Ak na PLC vytvoríš premennú (napr. `"DB_Motor".Start`), môžeš ju jednoducho myšou pretiahnuť (Drag & Drop) na obrazovku HMI. TIA Portal na pozadí automaticky vytvorí **HMI Tag**, zriadi komunikačné spojenie medzi HMI a PLC a priradí objektu správnu adresu.

---

## 2. Navigácia a základné grafické objekty

Dobrá HMI obrazovka musí byť intuitívna. Operátor musí na prvý pohľad vidieť, kde sa nachádza, čo je v norme a kde je problém. Zlaté pravidlo priemyselného dizajnu znie: **Menej je viac. Vyhýbaj sa krikľavým farbám pre bežné stavy (využívaj šedú) a farby ako červená (alarm) a zelená/žltá (aktívny stav) používaj len na upozornenie.**

### Screens a Screen Management (Obrazovky)
Základom vizualizácie sú obrazovky (Screens). 
*   **Start Screen:** Hlavná obrazovka, ktorá sa zobrazí po štarte panelu (zvyčajne prehľad celého stroja).
*   **Templates (Šablóny):** Slúžia na to, aby si nemusel na každú obrazovku kresliť to isté. Do Template sa zvyčajne vkladá logo firmy, aktuálny čas, meno prihláseného operátora a navigačné tlačidlá (Hlavné menu, Alarmy, Nastavenia). Akákoľvek zmena v Template sa okamžite prejaví na všetkých obrazovkách, ktoré ho využívajú.

### Basic Objects (Základné objekty)
Slúžia prevažne na statickú vizualizáciu bez interakcie operátora.
*   **Text field:** Statické popisy.
*   **Graphic view:** Vloženie obrázka stroja (.png, .jpg).

### Elements (Aktívne prvky)
Tieto prvky už vyžadujú prepojenie s premennými z PLC (HMI Tags).
*   **I/O Field:** Najčastejšie používaný prvok. Zobrazuje hodnoty z PLC (Output režim - napr. aktuálna teplota) alebo umožňuje operátorovi hodnotu zapísať (Input režim - napr. nastavenie požadovanej teploty stroja).
*   **Button (Tlačidlo):** Spúšťa akcie (Events), napr. prepnutie obrazovky, zapnutie motora, potvrdenie alarmu.
*   **Symbolic I/O field:** Rozbaľovacie menu (Drop-down zoznam). Umožňuje výber z vopred definovaného zoznamu textov (napríklad výber receptúry).
*   **Bar (Stĺpcový graf):** Vizuálne ukazuje zaplnenie nádrže alebo tlak. Intuitívnejšie než holé číslo.

---

## 3. Dynamizácia objektov (Animations)

Statický obdĺžnik je na HMI zbytočný, kým nezmení farbu alebo veľkosť podľa stavu stroja. **Dynamizácia (Animations)** oživuje grafiku. Na objektoch ju nastavujeme v spodnom menu v záložke `Properties -> Animations`.

### Display Animations (Vzhľad)
*   **Appearance (Vzhľad):** Zmení farbu pozadia, farbu textu alebo blikanie (Flashing) na základe hodnoty premennej. *Príklad: Ak má bit `Motor_Bezi` hodnotu 0, čerpadlo je šedé. Ak má hodnotu 1, čerpadlo je zelené.*
*   **Visibility (Viditeľnosť):** Objekt sa zobrazí alebo zmizne v závislosti od premennej. *Príklad: Tlačidlo "Otvoriť kryt" sa zobrazí len vtedy, ak je premenná `Stroj_Zastaveny` TRUE.*

### Movement Animations (Pohyb)
*   **Horizontal / Vertical Movement:** Zabezpečuje fyzický posun objektu po obrazovke (v osi X alebo Y). Využíva sa na zobrazenie pohybu portálu žeriavu alebo výšky lisovacieho nástroja na základe analógovej hodnoty z PLC.
*   **Direct movement:** Umožňuje posun v oboch osiach (X a Y) súčasne.

---

## 4. Udalosti (Events) a Akcie

Kým animácie definujú, čo grafika ukazuje operátorovi, udalosti (Events) definujú, **čo panel urobí, keď naň operátor klikne**. Udalosti sa typicky programujú na Tlačidlách (Buttons).

Každé tlačidlo má udalosti, ktoré viažu na akcie prstov operátora:
*   **Click / Tap:** Vykoná funkciu okamžite pri ťuknutí na tlačidlo.
*   **Press (Stlačenie):** Akcia sa vykoná v momente dotyku obrazovky.
*   **Release (Pustenie):** Akcia sa vykoná až po uvoľnení prsta z obrazovky. (Toto je dôležité bezpečnostné pravidlo pri JOGovaní strojov).

### Najčastejšie priraďované systémové funkcie na Tlačidlách:
TIA Portal (WinCC) má obrovskú knižnicu predprogramovaných systémových funkcií, ktoré sa dajú priradiť pod udalosť (napríklad pod `Press`):
*   `ActivateScreen(Screen_Name)`: Prepne HMI na zadanú obrazovku.
*   `SetBit(Tag)`: Nastaví bit v PLC na TRUE a drží ho natrvalo v stave 1.
*   `ResetBit(Tag)`: Nastaví bit v PLC na FALSE.
*   `InvertBit(Tag)`: Zmení stav na opačný (0 na 1, 1 na 0).
*   **`SetBitWhileKeyPressed(Tag)`:** Z bezpečnostného hľadiska **kriticky dôležitá funkcia**. Zabezpečí, že bit (napríklad manuálny posun vozíka) je v PLC nastavený na 1 len kým operátor fyzicky drží prst na tlačidle HMI. Akonáhle prst pustí, bit padne na 0. (Nepoužívať na to Set pod `Press` a Reset pod `Release`, pretože pri výpadku spojenia panelu môže ostať bit zaseknutý v 1!).

---

## 📝 Otázky na opakovanie

1. Aký je rozdiel medzi objektom *I/O Field* a objektom *Text Field*? Na čo slúži režim Input/Output v *I/O Field*?
2. Vysvetli význam *Template (Šablóny)* pri tvorbe HMI projektu s viacerými obrazovkami (Screens).
3. Prečo je z hľadiska priemyselnej praxe nevhodné urobiť celú vizualizáciu vo farbách dúhy, aj keď to softvér umožňuje?
4. Ktorú animáciu (Animation) použiješ, ak chceš, aby symbol ventilu svietil na zeleno pri otvorení a zmenil farbu na červenú pri poruche?
5. Vysvetli rozdiel medzi HMI funkciami `SetBit` a `SetBitWhileKeyPressed`. Ktorú z nich použiješ na manuálne roztočenie motora (tzv. JOG), a prečo?

---

## 📚 Užitočné zdroje

1. [Siemens HMI Design Workbook - Pravidlá dizajnu pre priemysel (HMI Design Masterclass)](https://support.industry.siemens.com/cs/document/109773423/hmi-design-workbook-for-wincc-(tia-portal)-?dti=0&lc=en-SK)
2. [TIA Portal Manual: Basics of Screen Configuration](https://docs.tia.siemens.cloud/r/simatic_wincc_unified_v18_manual_enus_20/hmi_basics_of_screen_configuration)
3. [Siemens Industry Online Support: Example Blocks for WinCC (TIA Portal) and STEP 7 (TIA Portal) (for S7-1200 and S7-1500)](https://support.industry.siemens.com/cs/document/109476800/example-blocks-for-wincc-(tia-portal)-and-step-7-(tia-portal)-in-scl-?dti=0&lc=en-SK)