---
layout: default        # používa layout zo zložky _layouts/default.html
title: Vyucba - Home   # zobrazí sa v záhlaví webu
show_sidebar: true     # ak máš v layout podporu pre bočný panel
---

{% comment %}
🧱 HLAVNÝ OBSAH STRÁNKY
Tento súbor je zobrazený na https://robertrakay.github.io/vyucba/
a slúži ako úvodná stránka pre všetky predmety.
{% endcomment %}


<!-- 🧩 HLAVNÁ ČASŤ STRÁNKY -->
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
👉 [Subject Template]({{ '/Template/' | relative_url }})

Táto šablóna obsahuje:
- názov predmetu  
- prehľad (overview)  
- 13-týždňovú tabuľku  
- doplnky (code examples, links, assignments, simulator)

---

## 🪶 Markdown návod / Markdown Tutorial

{% comment %}
Tu je dôležitá zmena:
„{{ include MARKDOWN_TUTORIAL.md | markdownify }}“ nefunguje,
pretože include musí byť vo forme Liquid tagu:
{% endcomment %}

{% raw %}{% include MARKDOWN_TUTORIAL.md %}{% endraw %}

👉 Tento súbor nájdeš v `_includes/MARKDOWN_TUTORIAL.md`.

---

## 💡 Tipy

- Všetky cesty používajú relatívne odkazy (`relative_url`), aby fungovali priamo na GitHub Pages.  
- Každý predmet je samostatná podstránka:  
  napr. [Automation & Automation Technology]({{ '/Automation_and_automation_technology/' | relative_url }})  
- Ak chceš zdieľať len jeden predmet, jednoducho pošli link na jeho stránku.

---

*Posledná aktualizácia:* {{ site.time | date: "%d.%m.%Y" }}

</div>
