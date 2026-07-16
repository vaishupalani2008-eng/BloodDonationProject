"""
BLOOD DONATION CAMP MANAGEMENT SYSTEM — Pie Chart Report
A companion file to blood_donation_system.py and app.py.

Generates a standalone HTML page with real, interactive pie charts
(Chart.js) for:
  - Blood type distribution
  - Gender distribution
  - Age bracket distribution

Reads live data from donors.json (created by app.py / blood_donation_system.py).

Run:
    python pie_chart_report.py

This writes pie_report.html and opens it in your browser automatically.
"""

import json
import os
import webbrowser
from datetime import datetime

import blood_donation_system as core

REPORT_FILE = "pie_report.html"

# A small, distinct color set reused across all three charts
COLORS = [
    "#0B3D5C",  # navy
    "#0E7C7B",  # teal
    "#A61C3C",  # clinical red
    "#FFB703",  # gold
    "#6A4C93",  # violet
    "#2E8B57",  # sea green
    "#D9822B",  # amber
    "#5A6B78",  # muted grey
]


def build_pie_report():
    inventory = core.get_inventory()
    gender_counts, age_counts = core.demographic_stats()
    donor_count = len(core.load_donors())
    generated_on = datetime.now().strftime("%d %B %Y, %I:%M %p")

    # Filter out zero-value blood types so the pie isn't cluttered with empty slices
    bt_labels = [bt for bt, count in inventory.items() if count > 0]
    bt_values = [inventory[bt] for bt in bt_labels]
    if not bt_labels:
        bt_labels, bt_values = ["No data yet"], [1]

    gender_labels = list(gender_counts.keys())
    gender_values = list(gender_counts.values())
    if sum(gender_values) == 0:
        gender_labels, gender_values = ["No data yet"], [1]

    age_labels = list(age_counts.keys())
    age_values = list(age_counts.values())
    if sum(age_values) == 0:
        age_labels, age_values = ["No data yet"], [1]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Blood Donation Camp — Pie Chart Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --navy: #0B3D5C; --navy-deep: #082A40; --teal: #0E7C7B;
    --clinical-red: #A61C3C; --paper: #F6F8FA; --line: #DCE3E8;
    --ink: #1B2430; --muted: #5A6B78;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: 'Inter', sans-serif; }}

  .masthead {{
    background: var(--navy-deep); color: #EAF1F5; padding: 30px 40px;
    border-bottom: 3px solid var(--clinical-red);
  }}
  .eyebrow {{
    font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; letter-spacing: 2px;
    text-transform: uppercase; color: #9FB6C4;
  }}
  h1 {{ font-family: 'Source Serif 4', serif; font-weight: 700; font-size: 26px; margin: 4px 0 0; }}
  .meta {{ font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #9FB6C4; margin-top: 10px; }}

  .wrap {{
    max-width: 1080px; margin: 0 auto; padding: 32px 24px 60px;
    display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 22px;
  }}
  .card {{ background: white; border: 1px solid var(--line); border-radius: 4px; padding: 20px 22px 26px; }}
  .card h2 {{ font-family: 'Source Serif 4', serif; font-size: 17px; margin: 0 0 4px; color: var(--navy); }}
  .card .tag {{
    font-family: 'IBM Plex Mono', monospace; font-size: 10.5px; text-transform: uppercase;
    letter-spacing: 1px; color: var(--muted); display: block; margin-bottom: 14px;
  }}
  .chart-holder {{ position: relative; height: 280px; }}

  footer {{
    text-align: center; font-family: 'IBM Plex Mono', monospace; font-size: 11px;
    color: var(--muted); padding: 20px 0 40px;
  }}
</style>
</head>
<body>

  <div class="masthead">
    <div class="eyebrow">Blood Donation Camp</div>
    <h1>{core.CAMP_DETAILS['camp_name']} — Pie Chart Report</h1>
    <div class="meta">Generated {generated_on} &middot; {donor_count} donor(s) on record</div>
  </div>

  <div class="wrap">

    <div class="card">
      <h2>Blood Type Distribution</h2>
      <span class="tag">Units on hand, by group</span>
      <div class="chart-holder"><canvas id="bloodTypeChart"></canvas></div>
    </div>

    <div class="card">
      <h2>Gender Distribution</h2>
      <span class="tag">Eligible donors</span>
      <div class="chart-holder"><canvas id="genderChart"></canvas></div>
    </div>

    <div class="card">
      <h2>Age Bracket Distribution</h2>
      <span class="tag">Eligible donors</span>
      <div class="chart-holder"><canvas id="ageChart"></canvas></div>
    </div>

  </div>

  <footer>Blood Donation Camp Management System &middot; Pie Chart Report &middot; Generated with Python + Chart.js</footer>

  <script>
    const colors = {json.dumps(COLORS)};

    function makePie(canvasId, labels, values) {{
      new Chart(document.getElementById(canvasId), {{
        type: 'pie',
        data: {{
          labels: labels,
          datasets: [{{
            data: values,
            backgroundColor: colors.slice(0, labels.length),
            borderColor: '#ffffff',
            borderWidth: 2
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ font: {{ family: 'Inter', size: 12 }} }} }}
          }}
        }}
      }});
    }}

    makePie('bloodTypeChart', {json.dumps(bt_labels)}, {json.dumps(bt_values)});
    makePie('genderChart', {json.dumps(gender_labels)}, {json.dumps(gender_values)});
    makePie('ageChart', {json.dumps(age_labels)}, {json.dumps(age_values)});
  </script>

</body>
</html>
"""


def generate_pie_report():
    html = build_pie_report()
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    report_path = os.path.abspath(REPORT_FILE)
    print(f"\n✅ {REPORT_FILE} generated at {report_path}")
    print("Opening it in your default browser...")
    webbrowser.open(f"file://{report_path}")


if __name__ == "__main__":
    generate_pie_report()