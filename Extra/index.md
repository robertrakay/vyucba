---
layout: main
title: Moja úvodná stránka
show_sidebar: true
---

# 👋 Vitaj na stránke
Na prepínanie jednotlivých slide-ov použite klávesy ← a →

---

## 🎥 Interaktívna prezentácia (Markdown + PowerPoint)

<!-- 🧩 Remark Markdown prezentácia -->
<div style="width: 100%; height: 500px; border:1px solid #ccc; border-radius:10px; overflow:hidden; margin-bottom: 20px;">
  <iframe srcdoc="
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset='utf-8'>
      <style>html,body{margin:0;height:100%;}</style>
      <script src='https://remarkjs.com/downloads/remark-latest.min.js'></script>
    </head>
    <body>
      <textarea id='source' style='display:none;'></textarea>
      <script>
        fetch('/sprava_o_ustave_2025.md')
          .then(res => res.text())
          .then(md => {
            document.getElementById('source').value = md;
            remark.create({ ratio:'16:9', highlightLanguage:'python', highlightStyle:'monokai' });
          });
      </script>
    </body>
    </html>
  " width="100%" height="100%" frameborder="0"></iframe>
</div>



---

## 📘 Ďalší obsah
Tu môžeš mať napríklad plán semestra, tabuľku alebo odkazy.
