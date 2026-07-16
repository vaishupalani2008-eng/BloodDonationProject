"""
BLOOD DONATION CAMP MANAGEMENT SYSTEM — Web App
A mini project in Python for CS students.

This is the file you actually run. It imports everything it needs
from blood_donation_system.py (must be in the same folder).

Run as a web app (default):
    python app.py
    then open http://127.0.0.1:5000

Run as a terminal menu instead:
    python app.py --cli
"""

import sys
from flask import Flask, request
from blood_donation_system import *

# ---------------------------------------------------------
# Flask Web App
# ---------------------------------------------------------
app = Flask(__name__)

FORM_STYLE = """
<style>
  :root {
    --navy: #0B3D5C; --navy-deep: #082A40; --teal: #0E7C7B;
    --clinical-red: #A61C3C; --paper: #F6F8FA; --line: #DCE3E8;
    --ink: #1B2430; --muted: #5A6B78;
  }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--paper); color:var(--ink); font-family:'Inter',sans-serif; font-size:15px; }
  .masthead { background:var(--navy-deep); color:#EAF1F5; padding:28px 40px; border-bottom:3px solid var(--clinical-red); }
  .masthead h1 { font-family:'Source Serif 4',serif; font-weight:600; font-size:24px; margin:0; }
  .masthead .eyebrow { font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:2px; text-transform:uppercase; color:#9FB6C4; }
  .masthead nav { margin-top:14px; }
  .masthead nav a { color:#EAF1F5; text-decoration:none; font-size:13px; margin-right:20px; border-bottom:1px solid transparent; }
  .masthead nav a:hover { border-bottom:1px solid var(--clinical-red); }
  .wrap { max-width:640px; margin:0 auto; padding:32px 24px 60px; }
  .section { background:white; border:1px solid var(--line); border-radius:4px; }
  .section-header { padding:16px 22px; border-bottom:1px solid var(--line); background:#FBFCFD; }
  .section-header h2 { font-family:'Source Serif 4',serif; font-weight:600; font-size:17px; margin:0; color:var(--navy); }
  .section-body { padding:22px; }
  label { display:block; font-family:'IBM Plex Mono',monospace; font-size:11px; text-transform:uppercase; letter-spacing:1px; color:var(--muted); margin:14px 0 6px; }
  label:first-child { margin-top:0; }
  input[type=text], input[type=number], input[type=date], select {
    width:100%; padding:10px 12px; border:1px solid var(--line); border-radius:3px; font-family:'Inter',sans-serif; font-size:14px; background:white;
  }
  input:focus, select:focus { outline:2px solid var(--teal); outline-offset:1px; border-color:var(--teal); }
  .row2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  .checkbox-row { display:flex; align-items:center; gap:8px; margin-top:16px; }
  .checkbox-row input { width:auto; }
  .checkbox-row label { margin:0; text-transform:none; letter-spacing:0; font-size:14px; color:var(--ink); }
  button {
    margin-top:24px; width:100%; padding:12px; background:var(--navy); color:white; border:none;
    border-radius:3px; font-family:'Inter',sans-serif; font-weight:600; font-size:14.5px; cursor:pointer;
  }
  button:hover { background:var(--navy-deep); }
  .result-banner { padding:16px 22px; border-radius:4px; margin-bottom:20px; font-size:14.5px; }
  .result-banner.ok { background:#EAF5EC; border:1px solid #C7E4CC; color:#1B6B34; }
  .result-banner.no { background:#FAECEE; border:1px solid #F0CBD1; color:var(--clinical-red); }
  .result-banner ul { margin:8px 0 0; padding-left:18px; }
  a.button-link {
    display:inline-block; margin-top:16px; padding:10px 18px; background:var(--teal); color:white;
    text-decoration:none; border-radius:3px; font-size:14px; font-weight:600;
  }
</style>
"""


def page_shell(body_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Blood Donation Camp — Web App</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
{FORM_STYLE}
</head>
<body>
  <div class="masthead">
    <div class="eyebrow">Blood Donation Camp</div>
    <h1>{CAMP_DETAILS['camp_name']}</h1>
    <nav>
      <a href="/">Dashboard</a>
      <a href="/register">Register Donor</a>
    </nav>
  </div>
  <div class="wrap">
    {body_html}
  </div>
</body>
</html>"""


@app.route("/")
def dashboard():
    # Reuses the same build_html() report used by the CLI's "Generate HTML Report" option.
    return build_html()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = int(request.form.get("age", 0))
        weight = float(request.form.get("weight", 0))
        hemoglobin = float(request.form.get("hemoglobin", 0))
        gender = request.form.get("gender", "").strip()
        phone = request.form.get("phone", "").strip()
        blood_type = request.form.get("blood_type", "").strip().upper()
        last_donation = request.form.get("last_donation", "").strip() or None
        pregnant_or_bf = request.form.get("pregnant_or_bf") == "on"
        has_fever = request.form.get("has_fever") == "on"

        donor, eligible, reasons = register_donor_data(
            name, age, weight, hemoglobin, gender, phone, blood_type,
            last_donation, pregnant_or_bf, has_fever
        )

        if eligible:
            banner = f"""<div class="result-banner ok">
                <strong>{name} is ELIGIBLE to donate blood ({blood_type}).</strong>
            </div>"""
        else:
            reasons_html = "".join(f"<li>{r}</li>" for r in reasons)
            banner = f"""<div class="result-banner no">
                <strong>{name} is NOT eligible to donate.</strong>
                <ul>{reasons_html}</ul>
            </div>"""

        body = f"""
        {banner}
        <a class="button-link" href="/register">Register Another Donor</a>
        <a class="button-link" href="/" style="background:var(--navy); margin-left:10px;">View Dashboard</a>
        """
        return page_shell(body)

    # GET: show the registration form
    blood_type_options = "".join(f"<option value='{bt}'>{bt}</option>" for bt in BLOOD_TYPES)
    body = f"""
    <div class="section">
      <div class="section-header"><h2>New Donor Registration</h2></div>
      <div class="section-body">
        <form method="POST" action="/register">
          <label>Full Name</label>
          <input type="text" name="name" required>

          <div class="row2">
            <div>
              <label>Age</label>
              <input type="number" name="age" min="1" max="120" required>
            </div>
            <div>
              <label>Gender</label>
              <select name="gender" required>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
          </div>

          <div class="row2">
            <div>
              <label>Weight (kg)</label>
              <input type="number" step="0.1" name="weight" required>
            </div>
            <div>
              <label>Hemoglobin (g/dL)</label>
              <input type="number" step="0.1" name="hemoglobin" required>
            </div>
          </div>

          <div class="row2">
            <div>
              <label>Blood Type</label>
              <select name="blood_type" required>{blood_type_options}</select>
            </div>
            <div>
              <label>Phone Number</label>
              <input type="text" name="phone" required>
            </div>
          </div>

          <label>Last Donation Date (leave blank if first time)</label>
          <input type="date" name="last_donation">

          <div class="checkbox-row">
            <input type="checkbox" name="pregnant_or_bf" id="pregnant_or_bf">
            <label for="pregnant_or_bf">Pregnant or breastfeeding</label>
          </div>
          <div class="checkbox-row">
            <input type="checkbox" name="has_fever" id="has_fever">
            <label for="has_fever">Currently has fever or other illness</label>
          </div>

          <button type="submit">Check Eligibility &amp; Register</button>
        </form>
      </div>
    </div>
    """
    return page_shell(body)


# ---------------------------------------------------------
# HTML Report Generator
# ---------------------------------------------------------
def generate_html_report():
    """Generate and open the dashboard HTML report."""
    import webbrowser
    html = build_html()
    report_file = "report.html"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)
    report_path = os.path.abspath(report_file)
    print(f"\n✅ {report_file} generated at {report_path}")
    print("Opening it in your default browser...")
    webbrowser.open(f"file://{report_path}")


# ---------------------------------------------------------
# Command-line Menu (optional mode: run with --cli)
# ---------------------------------------------------------
def main_cli():
    menu = """
=====================================
   BLOOD DONATION CAMP MANAGEMENT
=====================================
1. Register New Donor (Eligibility Check)
2. View All Donors
3. Blood Inventory Report
4. State-wise Annual Statistics
5. Things to Avoid Before Donating
6. Search Donors by Blood Type
7. Generate HTML Report (report.html)
8. Exit
"""
    while True:
        print(menu)
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            register_donor()
        elif choice == "2":
            view_donors()
        elif choice == "3":
            blood_inventory_report()
        elif choice == "4":
            state_statistics()
        elif choice == "5":
            show_avoid_list()
        elif choice == "6":
            search_by_blood_type()
        elif choice == "7":
            generate_html_report()
        elif choice == "8":
            print("Goodbye! Thank you for supporting blood donation.")
            break
        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------
if __name__ == "__main__":
    if "--cli" in sys.argv:
        main_cli()
    else:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print("Starting web app...")
        print(f"  This Computer:  http://127.0.0.1:5000")
        print(f"  Other Devices:  http://{local_ip}:5000")
        print("(Use 'python app.py --cli' for the terminal menu instead.)")
        app.run(host='0.0.0.0', debug=True)