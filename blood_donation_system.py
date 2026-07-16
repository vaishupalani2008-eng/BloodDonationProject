"""
BLOOD DONATION CAMP MANAGEMENT SYSTEM — Core Logic
A mini project in Python for CS students.

This file contains:
  - Data storage & eligibility logic
  - HTML report generator (professional camp report, with bar charts)
  - The CLI menu functions (register_donor, view_donors, etc.)

Run app.py (in the same folder) to actually start the program —
this file is imported by app.py and is not meant to be run directly.
"""

import json
import os
import webbrowser
from datetime import datetime

DATA_FILE = "donors.json"
REPORT_FILE = "report.html"

# ---------------------------------------------------------
# Reference data (from blood camp guidelines)
# ---------------------------------------------------------
BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

STATE_ANNUAL_UNITS = {
    "Maharashtra": 2168000,
    "Uttar Pradesh": 1600000,
    "Tamil Nadu": 953000,
    "Karnataka": 800000,
    "Gujarat": 800000,
    "Haryana": 592000,
    "Delhi": 400000,
    "Madhya Pradesh": 170000,
}

ELIGIBILITY = [
    ("Age", "18 - 65 years"),
    ("Weight", "45 - 50 kg"),
    ("Hemoglobin level", "&ge; 12.5 g/dL"),
    ("Gap between donations (Male)", "90 days (3 months)"),
    ("Gap between donations (Female)", "120 days (4 months)"),
    ("Units per donation", "1 unit"),
]

EXCLUSIONS = ["Pregnant or breastfeeding", "Fever or other illness"]

AVOID_ITEMS = [
    "Fasting",
    "Fatty foods",
    "Alcohol",
    "Smoking",
    "Aspirin / Painkillers",
    "Dehydration",
    "Sleeping less than sufficient hours",
]

POST_DONATION_CARE = [
    "Rest for 10-15 minutes at the camp before leaving",
    "Keep the bandage on for at least 4-6 hours",
    "Drink extra fluids over the next 24-48 hours",
    "Avoid heavy lifting or strenuous exercise for the rest of the day",
    "Eat iron-rich foods (leafy greens, legumes, lean meat) over the next few days",
    "If feeling dizzy, sit or lie down with feet elevated until it passes",
]

# Blood group compatibility: who each donor type can give to
BLOOD_COMPATIBILITY = [
    ("O-", "All blood types (universal donor)"),
    ("O+", "O+, A+, B+, AB+"),
    ("A-", "A-, A+, AB-, AB+"),
    ("A+", "A+, AB+"),
    ("B-", "B-, B+, AB-, AB+"),
    ("B+", "B+, AB+"),
    ("AB-", "AB-, AB+"),
    ("AB+", "AB+ only (universal recipient)"),
]

# ---------------------------------------------------------
# Camp organizer / contact person details
# Edit these values for your own camp.
# ---------------------------------------------------------
CAMP_DETAILS = {
    "camp_name": "City Blood Donation Camp",
    "organizer": "Dr. Anjali Mehta",
    "designation": "Camp Coordinator",
    "phone": "+91 98765 43210",
    "email": "bloodcamp@example.org",
    "venue": "Community Health Center, Main Hall",
    "date": "2026-07-20",
}


# ---------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------
def load_donors():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_donors(donors):
    with open(DATA_FILE, "w") as f:
        json.dump(donors, f, indent=4)


# ---------------------------------------------------------
# Eligibility & Exclusion Logic
# ---------------------------------------------------------
def check_eligibility(age, weight, hemoglobin, gender, last_donation_date, pregnant_or_bf, has_fever):
    """Returns (eligible: bool, reasons: list[str])"""
    reasons = []

    if not (18 <= age <= 65):
        reasons.append("Age must be between 18 and 65 years.")

    if weight < 45:
        reasons.append("Weight must be at least 45 kg.")

    if hemoglobin < 12.5:
        reasons.append("Hemoglobin level must be >= 12.5 g/dL.")

    if pregnant_or_bf:
        reasons.append("Excluded: pregnant or breastfeeding.")

    if has_fever:
        reasons.append("Excluded: currently has fever/illness.")

    if last_donation_date:
        last_date = datetime.strptime(last_donation_date, "%Y-%m-%d")
        gap_days = (datetime.now() - last_date).days
        required_gap = 90 if gender.lower() == "male" else 120
        if gap_days < required_gap:
            wait_more = required_gap - gap_days
            reasons.append(
                f"Must wait {required_gap} days between donations "
                f"({wait_more} more day(s) needed)."
            )

    eligible = len(reasons) == 0
    return eligible, reasons


# ---------------------------------------------------------
# Core Menu Actions
# ---------------------------------------------------------
def register_donor_data(name, age, weight, hemoglobin, gender, phone, blood_type,
                         last_donation, pregnant_or_bf, has_fever, location=""):
    """Core registration logic, reusable by both the CLI and the web app.
    Returns (donor_dict, eligible, reasons)."""
    eligible, reasons = check_eligibility(
        age, weight, hemoglobin, gender, last_donation, pregnant_or_bf, has_fever
    )

    donor = {
        "name": name,
        "age": age,
        "weight": weight,
        "hemoglobin": hemoglobin,
        "gender": gender,
        "phone": phone,
        "blood_type": blood_type,
        "location": location,
        "last_donation": last_donation,
        "eligible": eligible,
        "registered_on": datetime.now().strftime("%Y-%m-%d"),
    }

    donors = load_donors()
    donors.append(donor)
    save_donors(donors)

    return donor, eligible, reasons


def register_donor():
    print("\n--- New Donor Registration ---")
    name = input("Name: ").strip()
    age = int(input("Age: "))
    weight = float(input("Weight (kg): "))
    hemoglobin = float(input("Hemoglobin level (g/dL): "))
    gender = input("Gender (Male/Female): ").strip()
    phone = input("Phone number: ").strip()
    location = input("City / Area (for donors to be found nearby): ").strip()
    blood_type = input(f"Blood type {BLOOD_TYPES}: ").strip().upper()

    last_donation = input("Last donation date (YYYY-MM-DD) or leave blank if first time: ").strip()
    last_donation = last_donation if last_donation else None

    pregnant_or_bf = input("Pregnant or breastfeeding? (y/n): ").strip().lower() == "y"
    has_fever = input("Currently has fever or other illness? (y/n): ").strip().lower() == "y"

    donor, eligible, reasons = register_donor_data(
        name, age, weight, hemoglobin, gender, phone, blood_type,
        last_donation, pregnant_or_bf, has_fever, location
    )

    print("\n--- Result ---")
    if eligible:
        print(f"✅ {name} is ELIGIBLE to donate blood ({blood_type}).")
    else:
        print(f"❌ {name} is NOT eligible to donate. Reasons:")
        for r in reasons:
            print(f"   - {r}")


def view_donors():
    donors = load_donors()
    if not donors:
        print("\nNo donor records found.")
        return
    print(f"\n--- Registered Donors ({len(donors)}) ---")
    for i, d in enumerate(donors, 1):
        status = "Eligible" if d["eligible"] else "Not Eligible"
        phone = d.get("phone", "N/A")
        print(f"{i}. {d['name']} | {d['blood_type']} | Age {d['age']} | {phone} | {status}")


def get_inventory():
    """Returns a dict of blood_type -> unit count, from eligible donors."""
    donors = load_donors()
    inventory = {bt: 0 for bt in BLOOD_TYPES}
    for d in donors:
        if d["eligible"] and d["blood_type"] in inventory:
            inventory[d["blood_type"]] += 1
    return inventory


def blood_inventory_report():
    inventory = get_inventory()
    print("\n--- Blood Inventory (units collected from eligible donors) ---")
    for bt, units in inventory.items():
        print(f"{bt:4s} : {units} unit(s)")


def state_statistics():
    print("\n--- State-wise Annual Blood Requirement (units) ---")
    for state, units in sorted(STATE_ANNUAL_UNITS.items(), key=lambda x: -x[1]):
        print(f"{state:20s} : {units:,} units/year")
    total = sum(STATE_ANNUAL_UNITS.values())
    print(f"\nTotal across listed states: {total:,} units/year")


def show_avoid_list():
    print("\n--- Things Donors Should Avoid Before/After Donation ---")
    for item in AVOID_ITEMS:
        print(f" - {item}")


def find_nearby_donors(blood_type="", location_query=""):
    """Returns eligible donors matching the given blood type (exact) and/or
    location query (substring match, case-insensitive). Either can be left blank
    to skip that filter. Reusable by both the CLI and the web app."""
    donors = load_donors()
    blood_type = blood_type.strip().upper()
    location_query = location_query.strip().lower()

    matches = []
    for d in donors:
        if not d.get("eligible"):
            continue
        if blood_type and d.get("blood_type", "").upper() != blood_type:
            continue
        if location_query and location_query not in d.get("location", "").lower():
            continue
        matches.append(d)
    return matches


def search_by_blood_type():
    bt = input("\nEnter blood type to search (e.g. O+): ").strip().upper()
    location = input("Filter by city/area (leave blank for all locations): ").strip()
    matches = find_nearby_donors(blood_type=bt, location_query=location)
    if not matches:
        print(f"No eligible donors found for {bt}" + (f" near '{location}'." if location else "."))
        return
    print(f"\nEligible donors with {bt}" + (f" near '{location}':" if location else ":"))
    for d in matches:
        loc = d.get("location") or "Location not provided"
        print(f" - {d['name']} | {loc} | {d.get('phone', 'N/A')} (Age {d['age']})")


# ---------------------------------------------------------
# HTML Report Generator
# ---------------------------------------------------------
def eligibility_rows():
    return "\n".join(
        f'<tr><td class="label">{label}</td><td class="value">{value}</td></tr>'
        for label, value in ELIGIBILITY
    )


def blood_type_cells(inventory):
    """Vertical bar chart: one bar per blood type, height proportional to units on hand."""
    max_units = max(inventory.values()) if inventory and max(inventory.values()) > 0 else 1
    bars = []
    for bt in BLOOD_TYPES:
        count = inventory.get(bt, 0)
        height_pct = round((count / max_units) * 100) if max_units else 0
        height_pct = max(height_pct, 4)  # keep a sliver visible even at 0
        bars.append(f"""
        <div class="vbar-col">
          <div class="vbar-value">{count}</div>
          <div class="vbar-track"><div class="vbar-fill" style="height:{height_pct}%"></div></div>
          <div class="vbar-label">{bt}</div>
        </div>""")
    return "\n".join(bars)


def exclusion_rows():
    return "\n".join(f'<li>{item}</li>' for item in EXCLUSIONS)


def avoid_rows():
    return "\n".join(f'<li>{item}</li>' for item in AVOID_ITEMS)


def post_care_rows():
    return "\n".join(f'<li>{item}</li>' for item in POST_DONATION_CARE)


def compatibility_rows():
    return "\n".join(
        f'<tr><td class="label">{donor_type}</td><td class="value" style="text-align:left; font-weight:500; color:var(--ink);">{can_give_to}</td></tr>'
        for donor_type, can_give_to in BLOOD_COMPATIBILITY
    )


def demographic_stats():
    """Returns dict with gender counts and age-bracket counts among eligible donors."""
    donors = load_donors()
    eligible = [d for d in donors if d.get("eligible")]

    gender_counts = {"Male": 0, "Female": 0}
    for d in eligible:
        g = d.get("gender", "").strip().capitalize()
        if g in gender_counts:
            gender_counts[g] += 1

    brackets = [("18-25", 18, 25), ("26-35", 26, 35), ("36-50", 36, 50), ("51-65", 51, 65)]
    age_counts = {label: 0 for label, _, _ in brackets}
    for d in eligible:
        age = d.get("age", 0)
        for label, lo, hi in brackets:
            if lo <= age <= hi:
                age_counts[label] += 1
                break

    return gender_counts, age_counts


def horizontal_bar_rows(data, bar_class="bar-fill"):
    """Generic horizontal bar chart rows for a dict of label -> count."""
    max_val = max(data.values()) if data and max(data.values()) > 0 else 1
    rows = []
    for label, count in data.items():
        pct = round((count / max_val) * 100) if max_val else 0
        rows.append(f"""
        <tr>
          <td class="state-name">{label}</td>
          <td class="state-bar-cell">
            <div class="bar-track"><div class="{bar_class}" style="width:{pct}%"></div></div>
          </td>
          <td class="state-units">{count}</td>
        </tr>""")
    return "\n".join(rows)


def demographic_rows():
    gender_counts, age_counts = demographic_stats()
    gender_html = horizontal_bar_rows(gender_counts, bar_class="bar-fill bar-fill-gender")
    age_html = horizontal_bar_rows(age_counts, bar_class="bar-fill bar-fill-age")
    return gender_html, age_html




def state_rows():
    max_units = max(STATE_ANNUAL_UNITS.values())
    rows = []
    for name, units in sorted(STATE_ANNUAL_UNITS.items(), key=lambda x: -x[1]):
        pct = round(units / max_units * 100)
        rows.append(f"""
        <tr>
          <td class="state-name">{name}</td>
          <td class="state-bar-cell">
            <div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>
          </td>
          <td class="state-units">{units:,}</td>
        </tr>""")
    return "\n".join(rows)


def donor_rows():
    donors = load_donors()
    if not donors:
        return '<tr><td colspan="9" style="text-align:center; opacity:0.6;">No donors registered yet.</td></tr>'
    rows = []
    for d in donors:
        status_class = "eligible" if d["eligible"] else "not-eligible"
        status_text = "Eligible" if d["eligible"] else "Not Eligible"
        last_don = d.get("last_donation") or "First time"
        rows.append(f"""
        <tr>
          <td class="label">{d['name']}</td>
          <td class="value" style="text-align:left;">{d['blood_type']}</td>
          <td class="value" style="text-align:left;">{d['age']}</td>
          <td class="value" style="text-align:left;">{d.get('gender', 'N/A')}</td>
          <td class="value" style="text-align:left;">{d.get('location') or 'N/A'}</td>
          <td class="value" style="text-align:left;">{d.get('weight', 'N/A')} kg</td>
          <td class="value" style="text-align:left;">{d.get('hemoglobin', 'N/A')} g/dL</td>
          <td class="value" style="text-align:left;">{d.get('phone', 'N/A')}</td>
          <td class="value" style="text-align:left;"><span class="status-badge {status_class}">{status_text}</span></td>
        </tr>""")
    return "\n".join(rows)


def build_html():
    inventory = get_inventory()
    total_eligible = sum(inventory.values())
    total_states = len(STATE_ANNUAL_UNITS)
    donor_count = len(load_donors())
    generated_on = datetime.now().strftime("%d %B %Y, %I:%M %p")
    report_id = "BDC-" + datetime.now().strftime("%Y%m%d-%H%M")
    gender_chart, age_chart = demographic_rows()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Blood Donation Camp — Official Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --navy: #0B3D5C;
    --navy-deep: #082A40;
    --teal: #0E7C7B;
    --clinical-red: #A61C3C;
    --paper: #F6F8FA;
    --line: #DCE3E8;
    --ink: #1B2430;
    --muted: #5A6B78;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: 'Inter', sans-serif; font-size: 15px; }}

  /* ---------- MASTHEAD ---------- */
  .masthead {{
    background: var(--navy-deep);
    color: #EAF1F5;
    padding: 36px 40px 28px;
    border-bottom: 3px solid var(--clinical-red);
  }}
  .masthead-top {{
    display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;
  }}
  .org-mark {{ display: flex; align-items: center; gap: 12px; }}
  .org-mark .crest {{
    width: 40px; height: 40px; border-radius: 50%; border: 2px solid var(--clinical-red);
    display: flex; align-items: center; justify-content: center; font-size: 18px; color: var(--clinical-red); flex-shrink: 0;
  }}
  .org-mark-text .eyebrow {{
    font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: 2px;
    text-transform: uppercase; color: #9FB6C4;
  }}
  h1 {{
    font-family: 'Source Serif 4', serif; font-weight: 600; font-size: clamp(24px, 3.4vw, 32px);
    margin: 2px 0 0; letter-spacing: 0.2px;
  }}
  .doc-meta {{
    text-align: right; font-family: 'IBM Plex Mono', monospace; font-size: 11.5px; color: #9FB6C4; line-height: 1.7;
  }}
  .doc-meta strong {{ color: #EAF1F5; }}

  .stat-strip {{
    display: flex; gap: 0; margin-top: 26px; border: 1px solid rgba(255,255,255,0.14); border-radius: 4px; overflow: hidden;
  }}
  .stat-cell {{
    flex: 1; padding: 14px 18px; border-right: 1px solid rgba(255,255,255,0.14);
  }}
  .stat-cell:last-child {{ border-right: none; }}
  .stat-cell .num {{ font-family: 'IBM Plex Mono', monospace; font-size: 24px; font-weight: 600; color: #EAF1F5; }}
  .stat-cell .lbl {{
    font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #9FB6C4; margin-top: 2px;
  }}

  /* ---------- LAYOUT ---------- */
  .wrap {{ max-width: 1040px; margin: 0 auto; padding: 32px 40px 60px; }}

  .section {{
    background: white; border: 1px solid var(--line); border-radius: 4px; margin-bottom: 20px;
  }}
  .section-header {{
    display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
    padding: 16px 22px; border-bottom: 1px solid var(--line); background: #FBFCFD;
  }}
  .section-header h2 {{
    font-family: 'Source Serif 4', serif; font-weight: 600; font-size: 17px; margin: 0; color: var(--navy);
  }}
  .section-header .tag {{
    font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; text-transform: uppercase;
    letter-spacing: 1px; color: var(--muted);
  }}
  .section-body {{ padding: 18px 22px 20px; }}

  .grid-two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  @media (max-width: 720px) {{ .grid-two {{ grid-template-columns: 1fr; }} }}

  table {{ width: 100%; border-collapse: collapse; }}
  th {{
    text-align: left; padding: 8px 6px; font-family: 'IBM Plex Mono', monospace; font-size: 10.5px;
    text-transform: uppercase; letter-spacing: 1px; color: var(--muted); border-bottom: 1px solid var(--line);
  }}
  td {{ padding: 9px 6px; font-size: 14px; border-bottom: 1px solid var(--line); }}
  tr:last-child td {{ border-bottom: none; }}
  td.label {{ color: var(--ink); font-weight: 500; }}
  td.value {{ text-align: right; font-family: 'IBM Plex Mono', monospace; font-weight: 600; color: var(--navy); }}

  /* blood type vertical bar chart */
  .vbar-chart {{
    display: flex; align-items: flex-end; gap: 10px; height: 160px; padding: 10px 6px 0;
    border-bottom: 1px solid var(--line);
  }}
  .vbar-col {{
    flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%;
  }}
  .vbar-value {{
    font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 600; color: var(--navy); margin-bottom: 4px;
  }}
  .vbar-track {{
    width: 100%; max-width: 34px; height: 100%; display: flex; align-items: flex-end;
    background: var(--paper); border: 1px solid var(--line); border-radius: 2px 2px 0 0; overflow: hidden;
  }}
  .vbar-fill {{ width: 100%; background: linear-gradient(180deg, var(--teal), var(--navy)); }}
  .vbar-label {{
    margin-top: 8px; font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 600; color: var(--clinical-red);
  }}

  ul.plain {{ list-style: none; margin: 0; padding: 0; }}
  ul.plain li {{ margin: 8px 0; }}
</style>
</head>
<body>
  <div class="masthead">
    <div class="org-mark">
      <div class="crest">BD</div>
      <div class="org-mark-text">
        <div class="eyebrow">Blood Donation Camp</div>
        <h1>Official Report</h1>
      </div>
    </div>
    <div class="doc-meta">
      Generated: {generated_on}<br>
      Report ID: {report_id}<br>
      Eligible units: {total_eligible} &middot; Total donors: {donor_count}
    </div>
  </div>

  <div class="wrap">
    <div class="section">
      <div class="section-header"><h2>Inventory Summary</h2><span class="tag">Eligible units by blood group</span></div>
      <div class="section-body">
        <div class="grid-two">
          <div>
            <h3>Units on Hand</h3>
            <ul class="plain">
              {''.join(f'<li>{bt}: {inventory.get(bt, 0)} unit(s)</li>' for bt in BLOOD_TYPES)}
            </ul>
          </div>
          <div>
            <h3>Blood Inventory Chart</h3>
            <div class="vbar-chart">
              {''.join(
                f'<div class="vbar-col"><div class="vbar-value">{inventory.get(bt, 0)}</div><div class="vbar-track"><div class="vbar-fill" style="height:{max(round(inventory.get(bt, 0) / max(inventory.values()) * 100), 4)}%"></div></div><div class="vbar-label">{bt}</div></div>'
                for bt in BLOOD_TYPES
              )}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-header"><h2>Donor Demographics</h2><span class="tag">Eligible donors by gender and age</span></div>
      <div class="section-body">
        <table>
          <thead><tr><th>Category</th><th>Count</th></tr></thead>
          <tbody>
            {gender_chart}
          </tbody>
        </table>
        <table>
          <thead><tr><th>Category</th><th>Count</th></tr></thead>
          <tbody>
            {age_chart}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</body>
</html>"""


def generate_html_report():
    """Generate the official report HTML file and open it in the browser."""
    html = build_html()
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    report_path = os.path.abspath(REPORT_FILE)
    print(f"\n✅ {REPORT_FILE} generated at {report_path}")
    try:
        webbrowser.open(f"file://{report_path}")
    except Exception:
        print("Unable to open the report in the browser automatically.")
