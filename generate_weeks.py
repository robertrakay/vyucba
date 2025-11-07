import os
import shutil

# 📁 Zoznam predmetov = priečinky v hlavnom adresári
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
    "Extra"
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

# 🧱 Funkcia na vytvorenie tabuľky s odkazmi na týždne
def generate_table(subject):
    rows = []
    for i in range(1, 14):
        url = f"/vyucba/{subject}/Weeks/week{i}/"
        rows.append(f"<tr><td>{i}</td><td><a href='{url}'>Week {i}</a></td></tr>")
    return (
        "<h3>Semester Plan</h3>\n"
        "<table border='1' style='border-collapse:collapse;width:100%;text-align:left;'>\n"
        "<thead><tr><th>Week</th><th>Link</th></tr></thead>\n<tbody>\n"
        + "\n".join(rows)
        + "\n</tbody></table>"
    )

# 🔁 Spracovanie predmetov
for subject in subjects:
    subject_path = os.path.join(subject)

    # 1️⃣ Zmaž staré priečinky "weeks" alebo "Weeks"
    for old_dir in ["weeks", "Weeks"]:
        old_path = os.path.join(subject_path, old_dir)
        if os.path.exists(old_path):
            shutil.rmtree(old_path)
            print(f"🧹 Removed old folder: {old_path}")

    # 2️⃣ Vytvor nový priečinok Weeks/
    weeks_dir = os.path.join(subject_path, "Weeks")
    os.makedirs(weeks_dir, exist_ok=True)

    # 3️⃣ Vytvor 13 týždňov
    for week in range(1, 14):
        file_path = os.path.join(weeks_dir, f"week{week}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(template.format(week=week, subject=subject))
        print(f"✅ Created: {file_path}")

    # 4️⃣ Uprav index.md — ak existuje, doplň tabuľku
    index_path = os.path.join(subject_path, "index.md")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # odstráni staré tabuľky a doplní novú
        start = content.find("<h3>Semester Plan</h3>")
        if start != -1:
            content = content[:start]  # odstráni starú tabuľku

        content += "\n\n" + generate_table(subject)

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🧩 Updated index.md for {subject}")

print("\n🎉 Hotovo! Weeks priečinky boli obnovené a odkazy v tabuľkách doplnené.")
