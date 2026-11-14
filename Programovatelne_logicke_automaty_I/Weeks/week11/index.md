---
title: Diagnostika, Pamäť a Správa projektov (Retain, Snapshot, SD)
layout: custom_default
parent: Programovateľné logické automaty I
nav_order: 11
---

# Diagnostika, Pamäť a Správa projektov v TIA Portal

Napísať kód, ktorý riadi stroj za ideálnych podmienok, je len polovica práce automatizéra. Druhá polovica spočíva v tom, ako sa stroj zachová pri poruche hardvéru, pri výpadku napájania alebo pri servisnom zásahu. Schopnosť rýchlo diagnostikovať chybu (Debugging), správne zálohovať dáta a udržiavať poriadok v softvérových verziách je to, čo odlišuje profesionála od začiatočníka.

---

## 1. Diagnostika PLC a HMI (Best Practices)

Zastavenie modernej výrobnej linky stojí firmu stovky až tisíce eur za minútu. Ak sa PLC z nejakého dôvodu prepne do režimu **STOP**, údržbár musí do minúty vedieť, prečo sa to stalo.

### Diagnostic Buffer (Diagnostický zásobník)
Základný kameň každej diagnostiky v systémoch Siemens. Je to kruhová pamäť (Ring buffer) priamo v PLC, ktorá zaznamenáva všetky systémové udalosti s presnou časovou pečiatkou.
*   **Ako to funguje:** Ak PLC spadne, programátor sa pripojí (Go Online), otvorí *Online & Diagnostics* a pozrie si *Diagnostic Buffer*. 
*   **Čo obsahuje:** Vidí tu napríklad: *"Event 1 of 50: I/O access error, writing to QW200"*. Systém mu presne povie, na ktorom riadku a v ktorom bloku došlo k chybe (napr. pokus o zápis na neexistujúcu hardvérovú adresu).
*   **Best Practice:** Diagnostický zásobník prežíva výpadok napájania. Aj keď PLC zhasne a znova sa zapne, história chýb tam zostáva uložená.

### Ošetrenie chýb pomocou špeciálnych OB (Error Interrupts)
Ak hardvérová karta na linke zhorí (alebo sa odpojí PROFINET kábel), štandardné PLC to vyhodnotí ako fatálnu chybu a okamžite zastaví hlavný program (padne do stavu STOP).
*   **Best Practice:** Do programu (do zložky Program Blocks) je nutné vložiť prázdne organizačné bloky, napr. **OB82 (Diagnostic Error Interrupt)** a **OB86 (Rack or Station Failure)**. Ak nastane porucha hardvéru, operačný systém PLC zavolá tieto bloky namiesto prechodu do režimu STOP. Stroj síce nahlási chybu (začne svietiť červená ERROR LED na PLC), ale kód beží ďalej, čo umožní programátorovi riadene zastaviť linku (napr. najprv vypnúť ohrevy a uvoľniť tlaky).

### HMI System Diagnostics
V TIA Portal (od verzie WinCC V13) existuje pripravený grafický objekt s názvom **System Diagnostic View**. 
Programátor ho len "pretiahne" myšou na servisnú obrazovku panela. Bez toho, aby napísal jediný riadok kódu, tento objekt na HMI zobrazuje reálne hardvérové chyby z PLC (napr. "Odpojený frekvenčný menič na adrese IP 192.168.0.5"). Ušetrí to desiatky hodín programovania ručných alarmov pre Profinet sieť.

---

## 2. Práca s SD kartou pre PLC (SIMATIC Memory Card)

Siemens PLC využívajú špeciálne pamäťové karty s označením **SMC (SIMATIC Memory Card)**. Sú to priemyselné SD karty s upraveným súborovým systémom, odolné voči EMC a častým prepisom. 

**Kritické varovanie z praxe!** 
SMC kartu **nikdy nesmieš formátovať cez štandardný prieskumník vo Windows** (FAT32/NTFS)! Formátovanie zničí jej skrytý systémový sektor a stane sa z nej predražená nefunkčná SD karta, ktorú už PLC neprečíta. Zmazať súbory z nej smieš len cez TIA Portal alebo priamym vymazaním obsahu vo vnútri priečinkov vo Windows.

### Funkcie SMC karty:
1.  **S7-1500 (Nutnosť):** PLC radu S7-1500 nemajú vnútornú "Load" pamäť na program. Bez vloženej SMC karty do tohto CPU nenahráš žiadny program, CPU ani nenabehne.
2.  **S7-1200 (Rozšírenie):** S7-1200 má vlastnú vnútornú pamäť. Karta sa tam vkladá voliteľne pre dva účely:
    *   **Program Card (Transfer):** Ak pošleš kartu zákazníkovi do Číny, on ju zasunie do prázdneho S7-1200, zapne ho a PLC si program samo "vytiahne" z karty. (Zákazník nepotrebuje TIA Portal).
    *   **Data Log (Archivácia):** Využíva sa na ukladanie nameraných dát (napr. teplôt a tlaku za posledný mesiac) do CSV súborov. V SCL kóde sa využívajú inštrukcie `DataLogCreate` a `DataLogWrite`, ktoré cyklicky zapisujú dáta priamo na túto kartu.

---

## 3. Online / Offline Comparison (Porovnávanie projektov)

Základným problémom tímovej práce alebo údržby je rozdiel medzi tým, čo má programátor v notebooku (**Offline projekt**) a tým, čo reálne beží v stroji (**Online kód**).
Predstav si, že nočná zmena údržbárov obišla pokazený snímač priamym drôtom a urobili rýchlu úpravu v kóde. Ak na druhý deň ranná zmena nahrá svoj Offline projekt do PLC (Download to device), prepíšu nočnú úpravu a stroj narazí.

### Indikátory v TIA Portal (Compare function)
Po kliknutí na funkciu "Go Online" sa v strome projektu rozsvietia farebné ikony:
*   🟢 **Zelený kruh:** Zhodné. Kód a premenné u teba v PC sú na bit presne rovnaké ako v PLC.
*   🔵 **Modrý a Oranžový znak:** Rozdiel. V tvojom notebooku je iný kód než v PLC (niekto niečo zmenil).
*   🔴 **Červený znak:** Chyba alebo konflikt verzií.

### Detailné porovnanie (Detailed Compare)
Ak vidíš modrý/oranžový znak na nejakom bloku (napr. FB_Motor), môžeš naň kliknúť pravým a zvoliť **Quick Compare**. TIA Portal otvorí rozdelenú obrazovku: vľavo vidíš svoj offline kód, vpravo online kód z PLC a farebne ti vyznačí presne ten jeden riadok SCL alebo LAD, ktorý sa líši. Následne sa rozhodneš, či stiahneš kód z PLC k sebe (Upload), alebo pošleš svoj kód do PLC (Download).

---

## 4. Snapshot premenných (Snímok aktuálnych hodnôt)

**Problém z praxe:**
Aktivoval si stroj. Hodinu si ladil PID regulátor, upravoval maximálne limity rýchlosti čerpadla, ukladal nastavenia snímačov. Tieto zmeny sa zapísali do Dátových blokov (DB) priamo v PLC – do stĺpca **Monitor Value (Aktuálna hodnota)**. 
V tvojom Offline projekte v PC však svietia pôvodné nuly v stĺpci **Start Value (Počiatočná hodnota)**. 
Ak by si teraz spravil bežný Download (nahrávanie celého projektu), TIA Portal pošle do stroja tvoje offline počiatočné hodnoty (teda nuly) a celá tvoja hodinová práca ladenia sa prepíše a vymaže!

**Riešenie: Funkcia Snapshot**
1.  Otvoríš Data Block (DB) v režime Online (klikneš na ikonu okuliarov so zelenou šípkou).
2.  Hore v lište klikneš na ikonu fotoaparátu – **Snapshot**. Tento nástroj "odfotí" aktuálne (Monitor) hodnoty priamo z bežiaceho stroja a uloží ich do dočasného stĺpca Snapshot.
3.  Následne klikneš na druhú ikonu: **"Copy snapshots to start values"** (Skopírovať snímky do počiatočných hodnôt).
4.  Odpojíš sa od PLC (Go Offline) a celý projekt uložíš. Od tohto momentu má tvoj projekt v PC natrvalo uložené presne tie vyladené PID konštanty a nastavenia, aké mal reálny stroj.

---

## 5. Retain Variables (Zálohované premenné)

Základným fyzikálnym faktom PLC pamäte (Work Memory, zvyčajne typ RAM) je, že **pri výpadku prúdu sa vymaže**. Keď sa po hodine prúd vráti a PLC naštartuje, všetky obyčajné (Non-Retain) premenné dostanú svoje defaultné (Start) hodnoty – zvyčajne hodnotu `0` alebo `FALSE`.

Pre mnohé údaje je to však katastrofa (receptúry na pečenie chleba, celkové počítadlo odpracovaných motohodín čerpadla, počet vyrobených kusov za smenu). Tieto musia prežiť!

### Nastavenie Retain (Zálohovanie)
Vo vlastnostiach akejkoľvek premennej v Dátovom bloku (DB) alebo v PLC Tag table môžeš zaškrtnúť políčko v stĺpci **Retain**. 
Keď premennú označíš ako Retain, PLC ju fyzicky neukladá len do bežnej RAM, ale do špeciálnej **NVRAM (Non-Volatile RAM)**, ktorú udržuje záložná batéria (Superkondenzátor). Po výpadku napájania a reštarte si PLC prečíta túto NVRAM a načíta si poslednú známu hodnotu.

**Best Practices pre použitie Retain:**
1.  **Nepoužívaj to všade!** NVRAM je drahá a má obmedzenú kapacitu (napr. iba 10 KByte u základných CPU S7-1200). Ak označíš 5 obrovských inštancií na Retain, CPU ti vyhlási chybu nedostatku pamäte.
2.  **Nikdy nedávaj Retain na výkonné bity!** Ak by si označil bit "Zapni_Motor" ako Retain, tak po výpadku elektriny a jej následnom nahodení by sa motor okamžite zapol bez povelu operátora! Výkonné (štartovacie) premenné a dočasné signály musia byť vždy Non-Retain, aby sa po resete vynulovali (Fall-back to Safe State).
3.  **Čo má byť Retain?** Nastavenia užívateľa z HMI panelu, alarmové limity (Min/Max teplota), časovače motohodín a počítadlá cyklov, výrobné šarže.

---
## 6. Vstavaný Webový Server (Diagnostika bez TIA Portal)

V priemyselnej praxi sa často stáva, že údržbár nemá k dispozícii notebook s nainštalovaným a licencovaným systémom TIA Portal (ktorý má desiatky gigabajtov), no potrebuje rýchlo zistiť, prečo stroj stojí. Tu prichádza na rad **Web Server** integrovaný priamo v CPU S7-1200 a S7-1500.

### Aktivácia a Prístup
1. V hardvérovej konfigurácii CPU (v TIA Portal) je nutné v sekcii *Web server* zaškrtnúť **Enable web server on this module**.
2. Z bezpečnostných dôvodov je potrebné vytvoriť užívateľské konto (User name / Password) a prideliť mu práva (napr. len na čítanie, alebo aj na zápis premenných a sťahovanie logov).
3. Po nahratí konfigurácie do PLC stačí do bežného webového prehliadača (Chrome, Edge) v PC alebo v smartfóne zadať IP adresu PLC (napr. `https://192.168.0.1`).

### Možnosti Web Servera
*   **Diagnostic Buffer:** Plnohodnotné zobrazenie diagnostického zásobníka s chybami (rovnako ako v TIA Portal).
*   **Watch Tables:** Možnosť prezerať si aktuálne stavy vstupov, výstupov a premenných z dátových blokov.
*   **DataLogs a Užívateľské stránky:** Umožňuje stiahnutie CSV súborov s historickými dátami priamo na USB/Disk PC. Pokročilí programátori (napr. pomocou HTML/JS) môžu do PLC nahrať vlastné vizualizačné webové stránky, ktoré priamo čítajú dáta z PLC (User-defined pages).

---

## 7. Nástroj TRACE (Osciloskop priamo v PLC)

Bežná *Watch Table* v TIA Portal dokáže zobraziť hodnotu premennej vizuálne asi dvakrát za sekundu. Ak však potrebuješ diagnostikovať prúdovú špičku motora, ktorá trvá 50 milisekúnd, alebo jemné kmitanie tlaku v hydraulike, vo Watch tabuľke si to okom nikdy nevšimneš.

Na to slúži **TRACE**. Je to softvérový osciloskop, ktorý beží priamo v hardvéri PLC.

### Princíp fungovania a nastavenie
1.  **Konfigurácia (Traces):** V strome projektu vytvoríš nový Trace. Pridáš do neho premenné, ktoré chceš sledovať (napr. analógový vstup tlaku a výstup PWM).
2.  **Vzorkovanie (Sampling):** Nastavíš, ako často má PLC hodnotu uložiť. Zvyčajne sa nastavuje *OB1 (Main cycle)* – PLC zaznamená hodnotu v každom jednom obehnutí programu (napr. každých 5 milisekúnd).
3.  **Spúšťač (Trigger):** Definuješ udalosť, ktorá spustí nahrávanie. Ak by TRACE nahrával neustále, okamžite by zaplnil pamäť. Trigger môže byť napríklad: *„Začni nahrávať presne vtedy, keď premenná I0.0 (Štart lisu) prejde z 0 na 1, a nahraj aj 100 vzoriek pred touto udalosťou (Pre-trigger)“*.
4.  **Zobrazenie a Analýza:** PLC nahrá dáta do svojej pamäte, a po dokončení si ich TIA Portal stiahne a vykreslí do detailného grafu, kde môžeš zoomovať a merať časové rozdiely medzi signálmi (napr. reakčný čas ventilu).

---

## 8. Záchrana strateného projektu (Upload device as new station)

Najhoršia nočná mora údržbára: Stroj stojí, originálny autor programu nedvíha telefón a ty nemáš k dispozícii zdrojový `.ap18` súbor (Offline projekt). Našťastie, moderné systémy (od firmvéru S7-1200 V4.0 a všetky S7-1500) obsahujú priamo v pamäti CPU kompletný projekt **vrátane názvov premenných a komentárov v blokoch**. 

*(Poznámka: Pri starých S7-300 si po uploade získal len holý kód bez komentárov s absolútnymi adresami typu M0.0, čo sa čítalo ako "rozsypaný čaj".)*

### Postup záchrany (Upload):
1.  Otvoríš TIA Portal a vytvoríš úplne nový, prázdny projekt. Nevkladáš do neho žiadne PLC.
2.  Klikneš do horného menu na **Online -> Upload device as new station (Hardware and Software)**.
3.  Vyhľadáš PLC v sieti cez Profinet a potvrdíš.
4.  TIA Portal "vysaje" z PLC kompletnú hardvérovú konfiguráciu (vrátane I/O kariet), všetky programové bloky (OB, FC, FB), dátové bloky (DB) s aktuálnymi hodnotami, HMI tagy a všetky komentáre k sieti (Networks). Získaš tak takmer 100 % identickú kópiu pôvodného vývojárskeho projektu a môžeš stroj okamžite diagnostikovať a upravovať.

---

## 9. Detailná architektúra pamäte v Siemens PLC

Aby programátor pochopil, prečo sa mu projekt niekedy nevojde do PLC, musí rozlišovať tri úplne odlišné pamäťové zóny:

1.  **Load Memory (Nahrávacia pamäť / Flash / SMC karta):** 
    Toto je "pevný disk" PLC. Je to nevolatilná pamäť (nevznikne jej strata pri výpadku prúdu). Ukladá sa sem celý projekt (program, komentáre, konfigurácia) presne tak, ako bol stiahnutý z PC. U modelov S7-1500 sa táto pamäť nachádza výlučne na vloženej SD karte (SMC).
2.  **Work Memory (Pracovná pamäť / RAM):** 
    Toto je rýchla "operačná pamäť". Operačný systém PLC do nej pred štartom prekopíruje z *Load Memory* len tie časti kódu a dát, ktoré nevyhnutne potrebuje pre vykonávanie cyklu (čistý strojový kód bez komentárov). Work Memory je integrovaná priamo v CPU a **nedá sa rozšíriť**. Ak PLC hlási, že má plnú Work Memory, nepomôže ti kúpiť väčšiu SD kartu – musíš kúpiť silnejší model CPU (napr. vymeniť CPU 1511 za 1515) alebo radikálne optimalizovať kód.
3.  **Retain Memory (Zálohovaná pamäť / NVRAM):** 
    Malá, na výpadky napájania nezávislá pamäť (zabezpečená superkondenzátorom alebo batériou). Udržiava premenné, ktoré boli v dátových blokoch označené ako *Retain* (napr. počítadlá kusov). Kapacita je zvyčajne veľmi malá (okolo 10 kByte pri S7-1200 a do 500 kByte pri S7-1500).

---

## 10. Referenčné projekty (Reference Projects)

Máš súbor `Stroj_V1.ap18` a kolega ti pošle súbor `Stroj_V2_Final.ap18`. Potrebuješ zistiť, či a aké zmeny v kóde urobil, aby si si omylom neprepísal svoje úpravy. TIA Portal nevie mať otvorené dva plnohodnotné projekty súčasne.

**Riešenie:**
1. Otvoríš si svoj hlavný projekt (`Stroj_V1`).
2. Zobrazíš si panel **Reference projects** (zvyčajne skrytý v ľavom dolnom rohu).
3. Tu otvoríš kolegov projekt (načíta sa len na čítanie - Read Only).
4. Teraz môžeš pretiahnuť kolegov programový blok (napr. FC_Pohon) priamo na tvoj blok s rovnakým názvom a zvoliť **Quick Compare**. Systém ti presne ukáže rozdiel v kóde (napr. kolega zmenil konštantu na riadku 45). Z Referenčného projektu si môžeš tiež metódou Drag&Drop jednoducho kopírovať HMI obrazovky, UDT štruktúry alebo celé bloky do tvojho aktívneho projektu.

## 📝 Otázky na opakovanie

1. Aký je rozdiel medzi stĺpcami *Start value (Počiatočná hodnota)* a *Monitor value (Aktuálna hodnota)* v dátovom bloku (DB) a prečo je dôležité pred nahrávaním úprav do stroja používať nástroj **Snapshot**?
2. Prečo je kriticky nebezpečné pre personál údržby, ak programátor označí bit pre štart lisu do kategórie **Retain** premenných?
3. Čo sa stane so SIMATIC Memory Card (SMC), ak sa ju programátor pokúsi sformátovať cez prieskumníka (Tento Počítač) vo Windows na formát NTFS/FAT32?
4. Tvoj kód pre HMI panel vykazuje chyby komunikácie, pretože frekvenčný menič na linke bol odpojený. Aký prázdny blok by si vložil do PLC programu, aby PLC nepadlo do stavu STOP z dôvodu výpadku I/O stanice?
5. Pred nahraním tvojich zmien do PLC sa ikona pri funkcii *Go Online* na bloku s motorom sfarbila namodro/oranžovo. Čo ti týmto systém TIA Portal hovorí a ako by si mal postupovať predtým, než klikneš na *Download*?

---

## 📚 Užitočné zdroje

1. [Siemens Industry Online Support: How do you read out the diagnostic buffer in STEP 7 (TIA Portal)?](https://support.industry.siemens.com/cs/document/90467140/how-do-you-read-out-the-diagnostic-buffer-in-step-7-(tia-portal)-?dti=0&lc=en-SK)
2. [TIA Portal Manual: Using SIMATIC Memory Cards](https://docs.tia.siemens.cloud/r/simatic_s7_1500_system_manual_enus_20/hmi_using_memory_cards)
3. [Siemens Industry Online Support: What should you watch out for when downloading the hardware/software and copying the actual values to the start values?](https://support.industry.siemens.com/cs/document/99062590/what-should-you-watch-out-for-when-downloading-the-hardware-software-and-copying-the-actual-values-to-the-start-values-(snapshot)-in-step-7-(tia-portal)-?dti=0&lc=en-SK)