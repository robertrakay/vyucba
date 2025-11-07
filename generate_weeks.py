import os

# Zoznam priečinkov – každý názov zodpovedá jednému predmetu
subjects = [
    "Automation_and_automation_technology",
    "Cybernetics_and_Informatics",
    "Electrotechnics_and_electrical_engineering",
    "Lekárska_elektronika",
    "Logické_riadiace_systémy",
    "Mechatronics_-_Microprocessors",
    "Základy_programovania_-_Programming_Technics",
    "Projektová_Dokumentácia",
    "Digitalizácia_Priemyslu",
    "Prostriedky_Priemyselnej_Automatizácie",
    "Bezpečnostné_Systémy",
    
]

# 🧩 YAML šablóna pre každý týždeň
template = """---
layout: subject
title: Week {week}
permalink: /{subject}/weeks/week{week}/
show_sidebar: false
---
# Week {week}
Week info coming soon.
"""

# 🏗️ Vytvorenie priečinkov a súborov
for subject in subjects:
    weeks_dir = os.path.join(subject, "Weeks")
    os.makedirs(weeks_dir, exist_ok=True)
    for week in range(1, 14):
        file_path = os.path.join(weeks_dir, f"week{week}.md")
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(template.format(week=week, subject=subject))
            print(f"✅ Created: {file_path}")
        else:
            print(f"⚠️ Skipping (exists): {file_path}")
