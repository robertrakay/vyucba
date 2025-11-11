---
layout: main
title: Remark.js prezentácia
show_sidebar: true
---

# 👋 Remark.js prezentácia

## 🎥 Interaktívna prezentácia z Markdownu

<div style="width:100%; height:500px; border:1px solid #ccc; border-radius:10px; overflow:hidden;">
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
{% include_relative sprava_o_ustave_2025.md %}
      </textarea>
      <script>
        remark.create({ ratio:'16:9', highlightLanguage:'python', highlightStyle:'monokai' });
      </script>
    </body>
    </html>
  " width="100%" height="100%" frameborder="0"></iframe>
</div>

# 👋 Include google prezentácia
{% include_relative index2.md %}