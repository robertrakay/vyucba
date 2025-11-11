---
layout: custom_default
title: Moja úvodná stránka
show_sidebar: true
---

# 👋 Vitaj na stránke
Na prepínanie jednotlivých slide-ov použite klávesy ← a →


---

## 🎥 Interaktívna prezentácia (Markdown + PowerPoint)

<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between;">

  <!-- 🧩 Remark Markdown prezentácia -->
  <div id="remark-container" style="flex: 1 1 48%; min-width: 320px; height: 500px; border:1px solid #ccc; border-radius:10px; overflow:hidden;">
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

  <!-- 🧭 PowerPoint prezentácia z OneDrive/SharePoint -->
  <div id="ppt-container" style="flex: 1 1 48%; min-width: 320px; height: 500px; border:1px solid #ccc; border-radius:10px; overflow:hidden;">
    <iframe 
      src="https://tukesk-my.sharepoint.com/:p:/g/personal/robert_rakay_tuke_sk/Eb-3M2aTts9EjZtbXeYWJUgBaloJrpz8Wavu6W1h5sXRMw?e=OdbHy1&em=2"
      width="100%" 
      height="100%" 
      frameborder="0" 
      scrolling="no"
      allowfullscreen="true"
      mozallowfullscreen="true"
      webkitallowfullscreen="true">
    </iframe>
  </div>

</div>

---

## 📘 Ďalší obsah
Tu môžeš mať napríklad plán semestra, tabuľku alebo odkazy.
