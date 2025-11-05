---
layout: default
title: Vyucba - Home
show_sidebar: true
---

{% comment %}
🧱 HLAVNÁ STRÁNKA
Zobrazí sa na https://robertrakay.github.io/vyucba/
Používa layout _layouts/default.html (ktorý vkladá sidebar automaticky)
{% endcomment %}

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
👉 [Subject Template]({{ '/Template/' | relative_url }})

Táto šablóna obsahuje:
- názov predmetu  
- prehľad (overview)  
- 13-týždňovú tabuľku  
- doplnky (code examples, links, assignments, simulator)

---

## 🪶 Markdown návod / Markdown Tutorial

{% capture tutorial %}{% include MARKDOWN_TUTORIAL.md %}{% endcapture %}
{{ tutorial | markdownify }}

---

## 💡 Tipy

- Všetky cesty používajú relatívne odkazy (`relative_url`), aby fungovali priamo na GitHub Pages.  
- Každý predmet je samostatná podstránka, napr.:  
  [Automation & Automation Technology]({{ '/Automation_and_automation_technology/' | relative_url }})  
- Ak chceš zdieľať len jeden predmet, jednoducho pošli link na jeho stránku.

---

*Posledná aktualizácia:* {{ site.time | date: "%d.%m.%Y" }}
