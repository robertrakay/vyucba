---
layout: subject
title: Jupyter Notebook
---
# 🧮 Jupyter Notebook

Jupyter Notebook je interaktívne prostredie pre **Python výpočty, vizualizácie a experimenty**.

---

## 🔗 Odkazy

- 🌐 [Try Jupyter Online](https://jupyter.org/try-jupyter)
- 📘 [Jupyter Documentation](https://docs.jupyter.org/)
- 🧩 [Google Colab (alternatíva)](https://colab.research.google.com/)

---

## 🧩 Postup

1. Otvor [JupyterLab Online](https://jupyter.org/try-jupyter/lab/).
2. Klikni na **Notebook → Python 3 (ipykernel)**.
3. Do bunky vlož napríklad:

   ```python
   import matplotlib.pyplot as plt
   import numpy as np

   x = np.linspace(0, 2*np.pi, 100)
   y = np.sin(x)

   plt.plot(x, y)
   plt.title("Jednoduchý sínusový priebeh")
   plt.show()
