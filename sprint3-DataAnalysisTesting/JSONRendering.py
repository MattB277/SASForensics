import jinja2
import json

with open("data.json", 'r') as file:
    data = json.load(file)

# Jinja2 HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incident Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        .container {
            border: 1px solid #ccc;
            padding: 20px;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        h1, h2 {
            color: #333;
        }
        .section {
            margin-bottom: 20px;
        }
        .evidence-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        .evidence-table th, .evidence-table td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }
        .evidence-table th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Incident Report</h1>
        <div class="section">
            <h2>Case Details</h2>
            <p><strong>Case Number:</strong> {{ case_number }}</p>
            <p><strong>Incident Type:</strong> {{ incident_type }}</p>
            <p><strong>Date of Incident:</strong> {{ date_of_incident }}</p>
            <p><strong>Incident Address:</strong> {{ incident_address }}</p>
        </div>
        <div class="section">
            <h2>Complainants</h2>
            <ul>
                {% for complainant in complainants %}
                <li>{{ complainant.name }} (Address: {{ complainant.address }})</li>
                {% endfor %}
            </ul>
        </div>
        <div class="section">
            <h2>Summary</h2>
            <p>{{ summary }}</p>
        </div>
        <div class="section">
            <h2>Evidence</h2>
            <table class="evidence-table">
                <thead>
                    <tr>
                        <th>Item Number</th>
                        <th>Description</th>
                        <th>Forensic Disciplines</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in evidence %}
                    <tr>
                        <td>{{ item.item_number }}</td>
                        <td>{{ item.description }}</td>
                        <td>{{ item.forensic_disciplines | join(', ') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <div class="section">
            <h2>Forensic Report</h2>
            <p><strong>Laboratory Number:</strong> {{ forensic_report.laboratory_number }}</p>
            <p><strong>Agency:</strong> {{ forensic_report.agency }}</p>
            <p><strong>Report Date:</strong> {{ forensic_report.report_date }}</p>
            <p><strong>Services Requested:</strong> {{ forensic_report.services_requested | join(', ') }}</p>
        </div>
        <div class="section">
            <h2>Conclusions</h2>
            <p>{{ conclusions }}</p>
        </div>
    </div>
</body>
</html>
"""

# Render HTML with Jinja2
template = jinja2.Template(html_template)
html_output = template.render(data)

# Write the output to an HTML file
output_file = 'incident_report.html'
with open(output_file, 'w') as file:
    file.write(html_output)

print(f"HTML file successfully generated: {output_file}")
