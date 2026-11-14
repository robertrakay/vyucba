---
title: Týždeň 2 - Úvod do MATLABu
layout: custom_default
parent: Lekárska elektronika
nav_order: 2
show_sidebar: true
---

# Úvod do MATLABu

**Príprava na cvičenie v rozsahu 90 minút**

Cvičenie je postavené na postupe: *vytvorím dáta → uložím ich do matice → vyberiem potrebnú časť → opravím chyby → vypočítam štatistiku → vykreslím graf*. Študenti tak uvidia, ako jednotlivé príkazy spolu súvisia.

Na prvých 90 minút je tém pomerne veľa. Grafické ukážky sú preto rozdelené na povinný základ a bonusové experimenty.

## Ciele cvičenia
Po absolvovaní cvičenia má študent vedieť:
*   vytvoriť a spustiť jednoduchý skript,
*   vytvoriť premennú, vektor a maticu,
*   vybrať a zmeniť prvky matice,
*   identifikovať chýbajúce a zjavne nesprávne hodnoty,
*   doplniť vnútorné chýbajúce hodnoty lineárnou interpoláciou,
*   vypočítať základné štatistiky,
*   vytvoriť čitateľný graf s viacerými priebehmi.

---

## Časový plán

| Čas | Téma | Aktivita |
| :--- | :--- | :--- |
| 0–8 min | Prostredie MATLABu | Ukážka prostredia, vytvorenie skriptu |
| 8–18 min | Premenné a vektory | Spoločné zadávanie krátkych príkazov |
| 18–33 min | Matice a výber dát | Vytvorenie matice, indexovanie, úprava prvkov |
| 33–45 min | Chybné a chýbajúce dáta | `isnan`, logické podmienky, `interp1` |
| 45–52 min | Štatistika | Priemer, medián, minimum, maximum, odchýlka |
| 52–65 min | Úloha 1 — grafy | Sínus, kosínus, formátovanie grafu |
| 65–85 min | Úloha 2 — samostatná práca | Energia študenta počas cvičenia |
| 85–90 min | Kontrola a zhrnutie | Ukážka výsledkov, krátke kontrolné otázky |

---

## 1. Predstavenie prostredia
*(Čas: 0 až 8 minút)*

Ukáž študentom tieto časti:

| Časť prostredia | Na čo slúži |
| :--- | :--- |
| **Command Window** | Okamžité vykonanie príkazu |
| **Workspace** | Prehľad premenných, ich hodnôt a rozmerov |
| **Current Folder** | Pracovný priečinok a súbory |
| **Editor** | Písanie a spúšťanie skriptov |
| **Figure** | Zobrazenie grafov |
| **Help / dokumentácia**| Vyhľadanie syntaxe a príkladov |

### Postup pre študentov
1. Vytvorte pracovný priečinok.
2. Vytvorte nový skript.
3. Uložte ho ako `cvicenie01.m`.
4. Zapíšte a spustite:

```matlab
%% Úvod
clc
clear
close all

disp('Moje prve cvicenie v MATLABe')
```

**Vysvetli rozdiel:**
*   `clc` vymaže text v Command Window.
*   `clear` odstráni premenné z Workspace.
*   `close all` zatvorí grafické okná.
*   `%` začína komentár.
*   `%%` vytvára sekciu skriptu, ktorú možno spustiť samostatne.

**Ukáž vyhľadanie pomoci:**
```matlab
help plot
doc interp1
```

> **Otázka pre študentov:** „Keď použijem `clc`, zostane premenná vo Workspace?“ 
> *Očakávaná odpoveď: áno.*

---

## 2. Premenné a vektory
*(Čas: 8 až 18 minút)*

Začni jednoduchými výpočtami:

```matlab
%% Premenné
napatie = 12;
prud = 0.5;

vykon = napatie * prud
```

**Vysvetli:**
*   `=` priraďuje hodnotu.
*   Bodkočiarka `;` potláča výpis výsledku do Command Window.
*   MATLAB rozlišuje veľké a malé písmená (case-sensitive).
*   Názvy premenných majú byť zrozumiteľné.
*   Desatinné čísla sa zapisujú bodkou: `0.5`.

Potom vytvorte vektory:

```matlab
riadok = [10 20 30 40];
stlpec = [10; 20; 30; 40];

t = 0:0.5:3;
```
**Syntax rozsahu:** `zaciatok:krok:koniec`

**Krátka úloha:** Vytvorte vektor od 0 do 10 s krokom 2. Koľko má prvkov?
```matlab
v = 0:2:10;
numel(v)
```
*(Výsledok: šesť prvkov.)*

Ukáž rozdiel medzi maticovými operáciami a operáciami po prvkoch:
```matlab
v = [1 2 3];

dvojnasobok = 2 * v;
druhe_mocniny = v.^2;
nasobenie_prvkov = v .* v;
```
*Poznámka na tejto hodine:* Stačí zdôrazniť: pri umocňovaní, násobení alebo delení jednotlivých prvkov vo vektore používame bodku pred operátorom: `.^`, `.*` a `./`.

---

## 3. Matice a výber dát
*(Čas: 18 až 33 minút)*

Použi jednoduché meranie dvoch snímačov:

```matlab
%% Matica meraní
% Stĺpce: čas [s], snímač 1 [°C], snímač 2 [°C]

M = [0 20 21;
     1 22 23;
     2 24 25;
     3 26 27];
```

| Riadok | Čas [s] | Snímač 1 [°C] | Snímač 2 [°C] |
| :--- | :--- | :--- | :--- |
| 1 | 0 | 20 | 21 |
| 2 | 1 | 22 | 23 |
| 3 | 2 | 24 | 25 |
| 4 | 3 | 26 | 27 |

*Vysvetlenie pre študentov:* V tomto usporiadaní predstavuje každý riadok jeden okamih merania a každý stĺpec jednu veličinu. Je to praktická dohoda pre namerané dáta; MATLAB nepredpisuje význam riadkov a stĺpcov.
Medzera alebo čiarka oddeľuje prvky v riadku. Bodkočiarka oddeľuje riadky.

**Základ prístupu (indexovanie):**
`M(riadok, stlpec)`
MATLAB indexuje od 1. Dvojbodka `:` na mieste indexu vyberie všetky riadky alebo stĺpce.

```matlab
M(2,3)           % Druhý riadok, tretí stĺpec: 23
M(1,:)           % Celý prvý riadok
M(:,2)           % Celý druhý stĺpec
M(2:4,2:3)       % Vybraná časť matice
M(end,:)         % Posledný riadok
```

**Rozmery a úprava:**
```matlab
size(M)          % Počet riadkov a stĺpcov (vráti vektor)
size(M,1)        % Počet riadkov
size(M,2)        % Počet stĺpcov
numel(M)         % Počet všetkých prvkov

M(2,2) = 22.5;   % Zmena jedného prvku
```

**Vytvorenie matice z vektorov:**
```matlab
cas = (0:3).';               % Stĺpcový vektor
s1 = [20; 22; 24; 26];
s2 = [21; 23; 25; 27];

data = [cas s1 s2];
```
*Príkaz `.'` tu zmení riadkový vektor na stĺpcový (transpozícia).*

### Miniúloha
1. Vyberte tretí riadok.
2. Vyberte hodnoty druhého snímača.
3. Zmeňte hodnotu prvého snímača v poslednom riadku na 28.
4. Vyberte len riadky, kde je čas aspoň 2 sekundy.

*Riešenie posledného bodu:*
```matlab
vyber = data(data(:,1) >= 2,:);
```

---

## 4. Chybné a chýbajúce dáta
*(Čas: 33 až 45 minút)*

Rozlíš dva prípady:
*   `NaN`: chýbajúca alebo nedefinovaná číselná hodnota (Not-a-Number).
*   Napríklad `999`: platné číslo, ktoré je podľa pravidiel nášho merania nesprávne.

Príkaz `isnan` nerozpozná, že číslo 999 je nesprávne. Na také hodnoty potrebujeme vlastnú podmienku.

Spoločná ukážka:
```matlab
%% Oprava dát
cas = (0:6).';
teplota = [20; 21; NaN; 23; 999; 25; 26];

povodne = teplota;

% Pre tento príklad očakávame teplotu od 0 do 50 °C.
chybne = teplota < 0 | teplota > 50;
teplota(chybne) = NaN;

chyba = isnan(teplota);
platne = ~chyba;

teplota(chyba) = interp1(cas(platne), teplota(platne), cas(chyba), 'linear');

[povodne teplota]
```

**Vysvetli masky:**
*   `isnan(teplota)` vytvorí logický vektor (masku, kde sú jednotky na mieste NaN).
*   `~` znamená logickú negáciu (NOT).
*   `|` znamená logické „alebo“ (OR).
*   `teplota(chyba)` vyberie len označené hodnoty.

**Syntax interpolácie:**
`interp1(zname_casy, zname_hodnoty, hladane_casy, 'linear')`

`interp1` odhaduje hodnoty medzi známymi bodmi. V tomto príklade doplní 22 °C a 24 °C. Pre lineárnu interpoláciu potrebujeme aspoň dva platné body s odlišnými časmi.
*Poznámka pri výklade:* Interpolovaná hodnota je odhad, nie nové meranie. Tu opravujeme vnútorné výpadky. Ak chýba prvá alebo posledná hodnota, tento postup ju bez ďalšieho rozhodnutia (extrapolácie) nedoplní.

> **Otázka:** „Prečo chýbajúcu teplotu nenahradíme nulou?“ 
> *Pretože nula je konkrétna teplota a skreslila by graf aj štatistický priemer.*

---

## 5. Štatistické príkazy
*(Čas: 45 až 52 minút)*

Použite opravený vektor:
```matlab
priemer = mean(teplota)
median_hodnot = median(teplota)
minimum = min(teplota)
maximum = max(teplota)
odchylka = std(teplota)
```

| Príkaz | Význam |
| :--- | :--- |
| `mean` | Aritmetický priemer |
| `median`| Medián |
| `min`, `max` | Najmenšia a najväčšia hodnota |
| `std` | Štandardná odchýlka — rozptýlenie hodnôt okolo priemeru |

Ukáž aj výpočet bez dopĺňania výpadkov (s ignorovaním NaN):
```matlab
mean([20 21 NaN 23], 'omitnan')
```

A výpočet po stĺpcoch celej matice:
```matlab
mean(data(:,2:3), 1)
```
*Pri bežnej matici `mean(A,1)` počíta priemery stĺpcov a `mean(A,2)` priemery riadkov. Výberom `data(:,2:3)` zároveň zabránime tomu, aby sme priemerovali aj časový stĺpec.*

---

## 6. Úloha 1 — Sínus, kosínus a grafy
*(Čas: 52 až 65 minút)*

V pôvodnej ukážke treba opraviť (pre študentov):
*   typografické úvodzovky na obyčajné `'...'` alebo `"..."`,
*   umiestniť `hold on` pred druhý `plot`,
*   používať `%` alebo `%%` namiesto `///`,
*   doplniť `ylabel`,
*   umiestniť označenie 90° na `pi/2`, keďže vstup do sin je v radiánoch.
*   `hold on` zachová existujúci priebeh pri pridávaní ďalšieho grafu.

**Spoločný základ:**
```matlab
%% Úloha 1
t = 0:0.1:2*pi;
a = sin(t);
b = cos(t);

figure
plot(t,a,'r<-','MarkerSize',2,'LineWidth',2);
hold on
plot(t,b,'b<-','MarkerSize',2,'LineWidth',2);

grid on
xlabel('Uhol \theta [rad]');
ylabel('Hodnota funkcie [-]');
title('Porovnanie sínusu a kosínusu');

legend('Sínus','Kosínus','Location','best');
text(pi/2,0,'\theta = 90°');

hold off
```

**Rozober formátovací reťazec (`LineSpec`):**

| Zápis | Význam |
| :--- | :--- |
| `r` | Červená farba |
| `b` | Modrá farba |
| `-` | Plná čiara |
| `--` | Prerušovaná čiara |
| `:` | Bodkovaná čiara |
| `<` | Trojuholníková značka smerujúca doľava |
| `o` | Kruhová značka |
| `LineWidth` | Hrúbka čiary |
| `MarkerSize` | Veľkosť značky |

Farbu, typ čiary a značku možno kombinovať v argumente `LineSpec`, napríklad `'b--o'`.

### Úpravy pre študentov
1. Zmeňte farby a značky.
2. Nastavte `MarkerSize` na 6.
3. Zmeňte krok času z `0.1` na `0.5`. Čo sa stane?
4. Pridajte tretí priebeh `c = sin(t - 0.5)`.
5. Doplňte tretiu položku legendy.

### Bonusové ukážky podľa času

**Viac priebehov jedným príkazom:**
```matlab
%% Viac priebehov jedným príkazom
x = 0:pi/100:2*pi;
y1 = sin(x);
y2 = sin(x-0.25);
y3 = sin(x-0.5);

figure
plot(x,y1,x,y2,'--',x,y3,':');
grid on
xlabel('Uhol [rad]');
ylabel('Hodnota [-]');
title('Fázovo posunuté sínusové priebehy');
legend('Bez posunu','Posun 0.25 rad','Posun 0.5 rad');
```

**Farby a značky pri menšom počte bodov:**
```matlab
%% Farby a značky pri menšom počte bodov
x = 0:pi/10:2*pi;

figure
plot(x,sin(x),'g', ...
     x,sin(x-0.25),'b--o', ...
     x,sin(x-0.5),'c*');
grid on
xlabel('Uhol [rad]');
ylabel('Hodnota [-]');
title('Porovnanie štýlov zobrazenia');
legend('Priebeh 1','Priebeh 2','Priebeh 3');
```
*Príklad `tan(sin(x)) - sin(tan(x))` je vhodný ako dobrovoľný experiment. V blízkosti ±π/2 sa vnútorný tangens správa problematicky, takže príklad môže odviesť pozornosť od základov grafov.*

---

## 7. Úloha 2 — Energia študenta počas cvičenia (Samostatná práca)
*(Čas: 65 až 85 minút)*

### Zadanie pre študentov
Počas 90-minútového cvičenia sledujeme fiktívnu energiu troch študentov:
*   **študent A** prišiel oddýchnutý,
*   **študent B** sa postupne prebúdza,
*   **študent C** je myšlienkami už na obede.

Energia je vyjadrená na stupnici 0 až 100 bodov. Dáta sú vymyslené na precvičenie MATLABu.

```matlab
%% Vstupné dáta
t = (0:5:90).';

A = 80 - 0.35*t + 5*sin(t/10);
B = 35 + 0.40*t + 8*sin(t/12);
C = 60 - 0.25*t + 10*cos(t/15);

% Výpadky a chyba merania
B(7) = NaN;
B(8) = NaN;
C(12) = 150;

D = [t A B C];
```

| Stĺpec matice D | Obsah |
| :--- | :--- |
| 1 | Čas [min] |
| 2 | Energia študenta A |
| 3 | Energia študenta B |
| 4 | Energia študenta C |

### Povinné úlohy
1. Zistite rozmer matice `D`.
2. Vyberte celý časový stĺpec a prvých päť riadkov matice.
3. Vyberte riadky od 45. minúty vrátane.
4. Nájdite a doplňte chýbajúce hodnoty študenta B.
5. Hodnoty študenta C mimo rozsahu 0 až 100 označte ako NaN a doplňte interpoláciou.
6. Opravené priebehy zapíšte späť do matice `D`.
7. Pre každého študenta vypočítajte priemer, minimum a maximum.
8. V jednom grafe zobrazte všetky tri opravené priebehy. Doplňte názov, osi, jednotky, legendu a mriežku.

### Otázky k výsledku
*   Kto má najvyššiu priemernú energiu?
*   Kto má najviac energie na konci?
*   Ako chybná hodnota 150 ovplyvní priemer?
*   Prečo je užitočné zachovať pôvodné dáta?

*Bonus:* Do grafu pridajte text „Prestávka?“ pri 45. minúte alebo porovnajte pôvodný a opravený priebeh študenta C.

---

### Vzorové riešenie pre vyučujúceho
Nasledujúci kód nadväzuje na vstupné dáta.

```matlab
%% Výber dát
D_povodne = D;

rozmer = size(D)
cas = D(:,1);
prvych_pat = D(1:5,:);
druha_polovica = D(D(:,1) >= 45,:);

%% Oprava študenta B
energiaB = D(:,3);

chybaB = isnan(energiaB);
platneB = ~chybaB;

energiaB(chybaB) = interp1(cas(platneB), energiaB(platneB), cas(chybaB), 'linear');

D(:,3) = energiaB;
```

```matlab
%% Oprava študenta C
energiaC = D(:,4);

nespravneC = energiaC < 0 | energiaC > 100;
energiaC(nespravneC) = NaN;

chybaC = isnan(energiaC);
platneC = ~chybaC;

energiaC(chybaC) = interp1(cas(platneC), energiaC(platneC), cas(chybaC), 'linear');

D(:,4) = energiaC;

%% Štatistika
energie = D(:,2:4);

priemery = mean(energie,1)
minima = min(energie,[],1)
maxima = max(energie,[],1)

[najvyssi_priemer, student] = max(priemery)
energia_na_konci = energie(end,:)
```

```matlab
%% Graf
figure
plot(cas,D(:,2),'g-o','LineWidth',2,'MarkerSize',4);
hold on
plot(cas,D(:,3),'b--s','LineWidth',2,'MarkerSize',4);
plot(cas,D(:,4),'r:^','LineWidth',2,'MarkerSize',4);

grid on
xlabel('Čas [min]');
ylabel('Energia [body]');
title('Energia študentov počas cvičenia');
legend('Oddýchnutý','Prebúdzajúci sa', 'Myslí na obed','Location','best');

ylim([0 100]);
text(45,95,'Prestávka?');
hold off
```
*Kontrola pre vyučujúceho: Matica má 19 riadkov a 4 stĺpce. Najvyšší priemer má študent A, najvyššiu energiu na konci má študent B. Oprava hodnoty 150 zníži priemer študenta C.*

---

## 8. Záverečná kontrola
*(Čas: 85 až 90 minút)*

Každý študent ukáže graf a odpovie na jednu krátku otázku:
*   Čo vyberie `D(:,3)`?
*   Aký je rozdiel medzi `NaN` a číslom 150?
*   Na čo slúži `hold on`?
*   Čo predstavuje hodnota doplnená interpoláciou?
*   Prečo nepočítame priemer celej matice vrátane času?

**Výstup z hodiny:** jeden uložený skript `cvicenie01.m` s komentármi, vyriešenými úlohami a dvoma hlavnými grafmi.

*Ak sa skupina zdrží pri maticiach, vynechaj bonusové grafické ukážky. Zachovaj čas na druhú úlohu — práve na nej študenti ukážu, či dokážu jednotlivé príkazy použiť samostatne.*

---

## 📚 Dokumentácia k použitým príkazom
*   **MathWorks — Array Indexing:** [https://www.mathworks.com/help/matlab/math/array-indexing.html](https://www.mathworks.com/help/matlab/math/array-indexing.html)
*   **MathWorks — interp1:** [https://www.mathworks.com/help/matlab/ref/double.interp1.html](https://www.mathworks.com/help/matlab/ref/double.interp1.html)
*   **MathWorks — mean:** [https://www.mathworks.com/help/matlab/ref/double.mean.html](https://www.mathworks.com/help/matlab/ref/double.mean.html)
*   **MathWorks — hold:** [https://www.mathworks.com/help/matlab/ref/hold.html](https://www.mathworks.com/help/matlab/ref/hold.html)
*   **MathWorks — plot:** [https://www.mathworks.com/help/matlab/ref/plot.html](https://www.mathworks.com/help/matlab/ref/plot.html)