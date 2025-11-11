---
layout: main
title: Moja úvodná stránka
show_sidebar: true
---

# 👋 Vitaj na stránke
Na prepínanie jednotlivých slide-ov použite klávesy ← a →

---

## 🎥 Interaktívna prezentácia (Markdown + PowerPoint)

<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between;">

  <!-- 🧩 Remark Markdown prezentácia -->
  <div style="flex: 1 1 48%; min-width: 320px; height: 500px; border:1px solid #ccc; border-radius:10px; overflow:hidden;">
    <iframe srcdoc="
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset='utf-8'>
        <style>html,body{margin:0;height:100%;}</style>
        <script src='https://remarkjs.com/downloads/remark-latest.min.js'></script>
      </head>
      <body>
        <textarea id='source' style='display:none;'>
# Tu vlož obsah svojho Markdownu
{% include_relative sprava_o_ustave_2025.md %}
        </textarea>
        <script>
          remark.create({ ratio:'16:9', highlightLanguage:'python', highlightStyle:'monokai' });
        </script>
      </body>
      </html>
    " width="100%" height="100%" frameborder="0"></iframe>
  </div>

  <!-- 🧭 PowerPoint prezentácia z SharePoint -->
  <div style="flex: 1 1 48%; min-width: 320px; height: 500px; border:1px solid #ccc; border-radius:10px; overflow:hidden;">
    <iframe 
      src="https://view.officeapps.live.com/op/embed.aspx?src=https%3A%2F%2Ftukesk.sharepoint.com%2F%3A%2Fp%3A%2Fr%2Fsites%2FUAMaR%2FZdielane%2520dokumenty%2FGeneral%2Fsprava%25202025%2520UAMRaVT%2520v1%2520public.pptx&wdStartOn=1&wdEmbedCode=0&wdPrint=0&wdDownload=0&wdInConfigurator=0" 
      width="100%" 
      height="100%" 
      frameborder="0" 
      allowfullscreen>
    </iframe>
  </div>

</div>

---

## 📘 Ďalší obsah
Tu môžeš mať napríklad plán semestra, tabuľku alebo odkazy.
