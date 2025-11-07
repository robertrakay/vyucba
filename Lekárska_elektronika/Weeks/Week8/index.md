🧑‍🏫 Pokyny pre učiteľa – 2. cvičenie (Pilotné meranie s Biopluxom)
🎯 Cieľ cvičenia

Umožniť študentom vykonať prvé meranie s Bioplux systémom, overiť funkčnosť pripojenia senzorov, a získať základné skúsenosti so záznamom fyziologických signálov.
Cieľom nie je presná analýza, ale zvládnutie praktických krokov:

inštalácia a spustenie softvéru OpenSignals

pripojenie senzorov

kalibrácia a kontrola signálu

záznam a export dát

📚 Priebeh hodiny (90 min)
Čas	Aktivita
0–10 min	Krátky úvod (účel pilotného merania, bezpečnostné zásady)
10–25 min	Príprava zariadenia – zapojenie Bioplux, spárovanie s PC, kontrola Bluetooth spojenia
25–45 min	Umiestnenie elektród a senzorov (EMG, EKG, GSR, podľa výberu skupiny)
45–70 min	Pilotné meranie – záznam počas 2 jednoduchých situácií (napr. pokoj vs. aktivita)
70–80 min	Export dát do .csv, uloženie názvom tímu
80–90 min	Zhrnutie: čo fungovalo / nefungovalo, otázky pre ďalšie meranie
🧩 Úlohy pre učiteľa

Pripraviť pred cvičením dve sady zariadení Bioplux, skontrolovať nabitie batérií.

Uistiť sa, že každý tím má prístup k OpenSignals (r)evolution a funkčný Bluetooth port.

Upozorniť študentov na:

Správne čistenie kože pred aplikáciou elektród (vlhčený obrúsok).

Označenie miesta pripojenia elektród (pre zopakovanie pri 3. cvičení).

Zákaz pripojovania viac zariadení na jeden účet (pád komunikácie).

Asistovať pri spárovaní a kontrole signálu (skontrolovať nulovú líniu a amplitúdu).

V prípade nefunkčných senzorov poskytnúť syntetické dáta pre MATLAB spracovanie.

🧠 Hodnotenie

Nie je známkované, len overenie funkčnosti:

Tím dokázal získať meranie? ✅

Dáta boli uložené v správnom formáte (.csv)? ✅

Tím popísal priebeh a problémy? ✅

👩‍🔬 Pokyny pre študentov – 2. cvičenie (Pilotné meranie)
🎯 Cieľ

Získať prvé vlastné fyziologické meranie pomocou Bioplux systému a pripraviť dáta pre spracovanie v MATLABe.

🧰 Postup krok za krokom
1. Príprava zariadenia

Zapni Bioplux jednotku a pripoj ju k notebooku cez Bluetooth.

Spusť OpenSignals (r)evolution).

Uisti sa, že senzor, ktorý chceš použiť, je rozpoznaný (zelená ikonka).

2. Pripojenie senzorov

Vyber si jeden typ merania:

EMG – svalová aktivita

EKG – srdcová aktivita

GSR – kožná vodivosť

Pri pripájaní:

Vyčisti pokožku alkoholovým obrúskom.

Pripoj elektródy podľa odporúčania vyučujúceho.

Skontroluj, či nie sú elektródy obrátené alebo voľné.

3. Pilotné meranie

Spusti záznam (ikona REC).

Meraj 60 sekúnd v pokoji, potom 30 sekúnd aktivity (napr. zatínanie ruky, dýchanie, stresový podnet).

Po skončení merania zastav záznam a pozoruj priebeh signálu.

4. Export dát

Ulož záznam ako .csv (File → Export → CSV).

Názov súboru: Tím1_EMG_pilot.csv

Prenes dáta na školský disk / do Moodle.

5. Diskusia v tíme

Čo fungovalo dobre?

Kde nastal problém (signál, spojenie, elektródy)?

Aký typ signálu by ste chceli skúmať ďalej?

📦 Výstup z cvičenia

Každý tím odovzdá:

Súbor .csv s názvom merania

Krátky zápis (3–5 viet):

aký signál merali

ako prebiehalo meranie

aké problémy sa vyskytli

⚙️ Odporúčania pre správne vykonanie meraní
🧩 Technické odporúčania

Pred meraním nechajte zariadenie 1–2 minúty stabilizovať (zníži drift).

Elektrody pripevniť pevne, ale nie príliš – kontakt musí byť rovnomerný.

Vyhnite sa pohybu káblov, tie spôsobujú artefakty.

Zemniaca (referenčná) elektróda musí byť umiestnená mimo aktívnej oblasti.

Pri meraní EKG sa odporúča sedieť v kľude, opretý chrbát.

Pri meraní EMG dbať na to, aby sval nebol pod napätím mimo aktívnej fázy.

Bluetooth spojenie testujte pred každým meraním – strata signálu = neúplné dáta.

Vetranie a vlhkosť: potenie môže ovplyvniť GSR aj EMG signály.

🧠 Organizačné odporúčania

Každý tím má 1 zodpovedného operátora (riadi meranie, zapisuje poznámky).

Všetky merania robte na tom istom mieste na tele počas celého semestra.

Pri nefunkčnom senzore použite syntetické dáta (vyučujúci poskytne).

Každý člen tímu by si mal vyskúšať aspoň jedno meranie.

Skupiny môžu navzájom porovnať svoje priebehy – odlišnosti sú bežné.

Po skončení merania odpojte senzor a vyčistite elektródy (izopropanol, obrúsok).

📋 Bezpečnostné zásady

Bioplux používa nízke napätie a galvanické oddelenie – bezpečné, no vždy iba na neporušenú kožu.

Elektródy nikdy neumiestňujte v blízkosti srdca pri inom zapojení ako odporúča učiteľ.

Nemerajte osoby s kardiostimulátorom alebo kožnými poraneniami.

Po meraní odpojte všetky káble pred uložením zariadenia.
