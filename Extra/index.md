---
layout: custom_default
title: Moja úvodná stránka
show_sidebar: true
---

# 👋 Vitaj na stránke
Tu bude bežný text alebo obsah stránky.

---

## 🎥 Interaktívna prezentácia

<div id="remark-container" style="height:500px; border:1px solid #ccc; border-radius:10px; overflow:hidden;">
  <iframe id="remark-frame" srcdoc="
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset='utf-8'>
    <style>
      html, body { margin: 0; height: 100%; }
    </style>
    <script src='https://remarkjs.com/downloads/remark-latest.min.js'></script>
  </head>
  <body>
    <textarea id='source' style='display:none;'>


class: center, middle, inverse
# 👨‍🏫 Predmet: Automatizácia
Úvodná prezentácia

---

# 🏭 Priemysel 4.0
Integrácia IoT, AI a robotiky

---

# 🤖 Príklady
- Riadiace systémy
- Vizualizácia
- OEE monitoring

---

# ✅ Ďakujem!
Stlač **šípku doprava ⬅️➡️** pre prechod medzi snímkami.


{% include_relative sprava_o_ustave_2025.md %}


    </textarea>
    <script>
      var slideshow = remark.create({
        ratio: '16:9',
        highlightLanguage: 'python',
        highlightStyle: 'monokai'
      });
    </script>
  </body>
  </html>
  " width="100%" height="100%" frameborder="0"></iframe>
</div>

---

## Ďalší obsah
Tu môžeš mať napríklad plán semestra, tabuľku alebo odkazy.
