# Insurance Claim Management System

A web-based insurance claim management system built with Flask that allows users to manage policyholders, process claims, analyze risks, and generate reports.

## Features

- Policyholder Management
- Claim Processing
- Risk Analysis
- Report Generation
- Data Persistence
- Modern UI with Bootstrap 5

## Project Structure

```
insurance_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── insurance_data.json    # Data storage file (auto-saved)
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── main.js        # Client-side JavaScript
└── templates/
    ├── base.html          # Base HTML template with common layout
    ├── index.html         # Dashboard / Home page
    ├── policyholders.html # Policyholder management page
    ├── claims.html        # Claims management page
    ├── risk_analysis.html # Risk analysis dashboard
    └── reports.html       # Claims reports page

```

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
```


3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

**1. base.html**
Purpose:
The base template provides a common layout and styling for all pages in the application. Other templates extend this base to keep consistent navigation, styling, and script loading.

Key parts:

Navigation Bar:
Contains links to main sections: Policyholders, Claims, Risk Analysis, and Reports.

Content Block:
{% block content %}{% endblock %} — placeholder for page-specific content.

CSS & JS Includes:
Bootstrap CSS/JS and your custom CSS and JS files are loaded here.

Smooth UI:
Using Bootstrap for responsive and clean UI.

**2. index.html (Welcome page)**
Purpose:
Displays an overview dashboard showing key metrics for the application at a glance.

Key parts:

Cards:
Four Bootstrap cards displaying counts for:

Total Policyholders

Total Claims

Pending Claims

High Risk Policyholders

The data is dynamically inserted using Jinja variables ({{ }}).

This page gives users quick insight into the current state of the system.

**3. policyholders.html**
Purpose:
Manage policyholders — register new ones and view existing entries.

Key parts:

Form to Register Policyholders:
Includes fields for Name, Age, Policy Type, and Sum Insured. Validation errors are displayed as a Bootstrap alert.

Existing Policyholders Table:
Lists all policyholders with their details in a table.

This page is for adding new policyholders and managing/viewing current ones.

**4. claims.html**
Purpose:
Manage insurance claims — file new claims and view/update existing ones.

Key parts:

Form to File New Claim:
Select policyholder, enter claim amount, reason, and status.

Claims Table:
Displays existing claims with ID, policyholder name, amount, date, status (with color-coded badges), and an update button.

JS for Status Update:
Inline JavaScript prompts the user for a new status and sends it via fetch to an API endpoint to update asynchronously.

This page helps users submit new claims and manage ongoing claims.

**5. reports.html**
Purpose:
Show various aggregated reports on claims data.

Key parts:

Monthly Claims Table:
Number of claims per month.

Average Claim by Policy Type Table:
Shows average claim amount grouped by policy type.

Highest Claim Card:
Displays detailed info about the largest claim.

Pending Claims Table:
Lists claims that are still pending.

This page is for data analytics and understanding claim trends.

**6. risk_analysis.html**
Purpose:
Analyze risk by identifying high-risk policyholders and breaking down claims by policy type.

Key parts:

High Risk Policyholders Table:
Shows policyholders with frequent claims and their claim ratios, styled in red to emphasize risk.

Claims by Policy Type Cards:
Each policy type gets a card listing its claims, with amounts and status.

## Data Persistence

The application automatically saves data to `insurance_data.json` when the server stops and loads it when the server starts.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 



