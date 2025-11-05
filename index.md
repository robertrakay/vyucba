---
layout: default
title: Vyucba - Home
show_sidebar: true
---
<div id="side-panel" style="float:left;width:220px;height:100vh;background:#f1f1f1;padding:10px;box-sizing:border-box;position:fixed;">
  <h3>Subjects</h3>
  <ul style="list-style:none;padding:0;">
    <li><a href="{{ '/' | relative_url }}">🏠 Home</a></li>
    <li><a href="{{ '/Automation_and_automation_technology/' | relative_url }}">Automation & Automation Technology</a></li>
    <li><a href="{{ '/Cybernetics_and_Informatics/' | relative_url }}">Cybernetics & Informatics</a></li>
    <li><a href="{{ '/Electrotechnics_and_electrical_engineering/' | relative_url }}">Electrotechnics & Electrical Engineering</a></li>
    <li><a href="{{ '/Lekárska_elektronika/' | relative_url }}">Lekárska elektronika</a></li>
    <li><a href="{{ '/Logické_riadiace_systémy/' | relative_url }}">Logické riadiace systémy</a></li>
    <li><a href="{{ '/Mechatronics_-_Microprocessors/' | relative_url }}">Mechatronics - Microprocessors</a></li>
    <li><a href="{{ '/Základy_programovania_-_Programming_Technics/' | relative_url }}">Základy programovania</a></li>
  </ul>
</div>

<div style="margin-left:240px;padding:20px;">

# 🎓 Vyucba – Teaching Repository

Vitaj!  
Tento repozitár obsahuje moje výučbové materiály pre jednotlivé predmety.  
Každý predmet má vlastnú sekciu, vlastný web a obsah (poznámky, úlohy, kódy, simulátory).

---

## 📘 Predmety / Subjects
Vyber si predmet, ktorý chceš zobraziť z navigácie vľavo.  
Každý predmet má rovnakú štruktúru:
- **01_Instructions** – pokyny k cvičeniam  
- **02_CodeExamples** – ukážky kódov  
- **03_Assignment** – zadania  
- **04_Notes** – poznámky  

---

## 🧩 Šablóna predmetu / Subject Template

Ak vytváraš nový predmet, použi túto šablónu:
👉 [Subject Template]({{ '/TEMPLATE_subject_index.md' | relative_url }})

Táto šablóna obsahuje:
- názov predmetu
- prehľad (overview)
- 13-týždňovú tabuľku
- doplnky (code examples, links, assignments, simulator)

---

## 🪶 Markdown návod / Markdown Tutorial

Ak chceš pridávať poznámky, úlohy alebo kódy v Markdown formáte, pozri:
{% include MARKDOWN_TUTORIAL.md %}

---

## 💡 Tipy

- Všetky cesty používajú relatívne odkazy (`relative_url`), aby fungovali priamo na GitHub Pages.  
- Každý predmet je samostatná podstránka:  
  napr. [Automation & Automation Technology]({{ '/Automation_and_automation_technology/' | relative_url }})  
- Ak chceš zdieľať len jeden predmet, jednoducho pošli link na jeho stránku.

---

*Posledná aktualizácia:* {{ site.time | date: "%d.%m.%Y" }}

</div>
