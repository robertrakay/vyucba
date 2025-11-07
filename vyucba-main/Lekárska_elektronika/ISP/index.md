Nižšie máš návrh 8 tém rozdelených podľa náročnosti – 4 základné a 4 pokročilé.
Všetky možno spracovať len s Matlabom, Pythonom alebo Jupyterom a syntetickými alebo verejnými dátami (napr. PhysioNet, Kaggle, UCI datasets).

#🎓 ZÁKLADNÉ TÉMY (úroveň: samostatná práca, analytický projekt)
#🔹 1. Simulation of Wearable Heart Rate Sensor Data
##Cieľ:

Vytvoriť syntetický dataset simulujúci merania tepu zo smart náramku počas dňa.

##Úlohy:

Vygenerovať časovú sériu HR (60–160 bpm) s náhodnými zmenami.

Pridať simulované fázy: spánok, chôdza, cvičenie.

Vizualizovať HR trend a porovnať s reálnym záznamom z verejnej databázy (napr. PhysioNet).

Exportovať ako .csv a popísať význam zmien.

Výstup:

MATLAB alebo Python skript + krátky report (graf + interpretácia).

#🔹 2. Synthesis and Analysis of Accelerometer Data (ADXL345 simulation)
Cieľ:

Simulovať dáta z akcelerometra počas 3 typov aktivít – pokoj, chôdza, beh.

Úlohy:

Generovať 3D signál (X,Y,Z) s rôznym rozsahom a frekvenciou.

Vykresliť v 3D grafe trajektóriu pohybu.

Použiť FFT alebo RMS analýzu na rozlíšenie aktivít.

Výstup:

MATLAB/Python script + 2 grafy + interpretácia.

#🔹 3. Stress Level Estimation from Synthetic GSR Data
##Cieľ:

Vytvoriť a analyzovať umelý signál galvanickej reakcie kože pri rôznych stresových úrovniach.

##Úlohy:

Generovať 3 úseky GSR: pokoj, mierny stres, vysoký stres.

Určiť priemernú vodivosť a trend.

Vizualizovať zmeny a vysvetliť fyziologický význam.

Výstup:

Grafy v MATLABe + krátky opis.

#🔹 4. Comparison of Synthetic Biosignals – EKG vs. PPG
##Cieľ:

Porovnať dve synteticky vytvorené merania srdcovej činnosti.

##Úlohy:

Vytvoriť EKG signál s R-vlnami a PPG vlnu (napr. sinus + modifikácie).

Vypočítať HR (srdcovú frekvenciu) z oboch.

Vizualizovať priebeh a fázový posun medzi EKG a PPG.

Výstup:

MATLAB/Python skript + 1 porovnávací graf + diskusia.

#🚀 POKROČILÉ TÉMY (úroveň: výskumný miniprojekt s AI alebo modelovaním)
#🔹 5. Activity Recognition from Synthetic Wearable Sensor Data (AI-based)
Cieľ:

Vytvoriť syntetické dáta akcelerometra pre rôzne aktivity (napr. sedenie, chôdza, beh, ležanie) a klasifikovať ich pomocou AI.

Úlohy:

Generovať datasety (3 osi, 1000 vzoriek/aktivita).

Použiť jednoduchý klasifikátor (k-NN, Decision Tree, alebo Neural Network).

Zhodnotiť presnosť modelu.

Výstup:

Python Jupyter notebook (Scikit-learn alebo MATLAB Classification Learner) + report.

#🔹 6. Smart Health Monitoring Dashboard (synthetic wearable data)
Cieľ:

Navrhnúť interaktívny MATLAB/Python dashboard pre vizualizáciu signálov z nositeľných senzorov.

Úlohy:

Použiť syntetické dáta (HR, GSR, acc).

Implementovať vizuálne indikátory: „Low“, „Normal“, „High“ stav.

Automaticky vyhodnocovať priemerné hodnoty.

Výstup:

MATLAB App Designer alebo Streamlit dashboard.

#🔹 7. Machine Learning Prediction of Stress from Physiological Data
Cieľ:

Použiť dostupné dataset-y (napr. WESAD – Wearable Stress and Affect Dataset) alebo ich zjednodušenú syntetickú verziu.

Úlohy:

Spracovať 3 fyziologické vstupy (HR, GSR, temp).

Vytvoriť model predikcie stresu (binárna klasifikácia).

Vizualizovať confusion matrix, ROC krivku.

Výstup:

Python Jupyter Notebook + krátka diskusia.

#🔹 8. Simulation of Wearable Sensor Network for Biomechanical Analysis
Cieľ:

Simulovať sieť 2–3 senzorov (napr. ADXL345, gyroskop, DHT11) na meranie pohybu končatiny.

Úlohy:

Generovať súbežné 3D dáta (pohyb v ramene a zápästí).

Vypočítať uhol ohybu, rýchlosť, teplotu prostredia.

Vizualizovať pohyb v čase.

Diskutovať o možnostiach reálneho nasadenia vo fyzioterapii.

Výstup:

MATLAB/Python projekt s grafmi a krátkou prezentáciou výsledkov.

#📦 Odporúčaná štruktúra výstupu pre všetky zadania

Každé zadanie by malo obsahovať:

Názov projektu + ciele

Použité metódy a nástroje (Matlab/Python/AI)

Popis syntetických dát alebo datasetu

Grafické výstupy / dashboard / model

Analýzu výsledkov a zhodnotenie

Krátke video alebo PDF prezentáciu (voliteľné)

#💡 Tip pre učiteľa

Základné témy = vhodné ako samostatné semestrálne práce (4–6 strán + grafy)

Pokročilé témy = možné využiť ako dlhodobejší výskumný miniprojekt

Možno pridať aj rozšírenie: študenti si porovnajú syntetické a verejné reálne dáta

Odovzdanie: .zip (projekt + PDF report)
