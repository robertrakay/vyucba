---
layout: main
title: Moja úvodná stránka
show_sidebar: true
---

# 👋 Vitaj na stránke

---

## 🎥 Interaktívna prezentácia (Markdown + PowerPoint)

<!-- Markdown prezentácia -->
<div style="width:100%; height:500px; border:1px solid #ccc; margin-bottom:20px;">
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
        fetch('Extra/sprava_o_ustave_2025.md')
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

<!-- Google Slides prezentácia -->
<div style="width:100%; height:500px; border:1px solid #ccc;">
  <iframe src="https://docs.google.com/presentation/d/13y-hdo8QISU0eZM54qNA8ecbagOQfATZ/edit?usp=sharing&ouid=114071380026780541902&rtpof=true&sd=true" width="100%" height="100%" frameborder="0" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
</div>
