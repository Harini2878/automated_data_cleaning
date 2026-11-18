
from flask import Flask, render_template_string, send_file
import pandas as pd
import os

app = Flask(__name__)

OUTPUT_FILE = "output/clean_dataset.csv"
REPORT_FILE = "output/validation_report.txt"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Data Cleaning Dashboard</title>
    <style>
        body {
            font-family: Arial;
            background: #f1f5f9;
            padding: 30px;
        }
        .container {
            background: white;
            padding: 25px;
            border-radius: 12px;
            max-width: 1000px;
            margin: auto;
        }
        h1 { color: #2563eb; }
        .card {
            background: #e0f2fe;
            padding: 18px;
            border-radius: 8px;
            margin: 15px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th { background: #2563eb; color: white; }
        a {
            display: inline-block;
            background: #16a34a;
            color: white;
            padding: 12px 18px;
            text-decoration: none;
            border-radius: 6px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Automated Data Cleaning Dashboard</h1>
    <p>Your dataset has been cleaned successfully!</p>

    <div class="card">
        <h3>Total Cleaned Records: {{ count }}</h3>
        <h3>Missing Values: {{ missing }}</h3>
        <h3>Duplicate Records: {{ duplicates }}</h3>
    </div>

    <h2>Cleaned Dataset Preview</h2>
    {{ table|safe }}

    <br><br>
    <a href="/download">Download Cleaned CSV</a>

    <h2>Validation Report</h2>
    <pre>{{ report }}</pre>
</div>
</body>
</html>
"""


@app.route("/")
def home():

    if not os.path.exists(OUTPUT_FILE):
        return "Please run main.py first."

    df = pd.read_csv(OUTPUT_FILE)

    count = len(df)
    missing = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    table = df.to_html(index=False, classes="table")

    report = "Report not available."

    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as file:
            report = file.read()

    return render_template_string(
        HTML,
        count=count,
        missing=missing,
        duplicates=duplicates,
        table=table,
        report=report
    )


@app.route("/download")
def download():
    return send_file(OUTPUT_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
