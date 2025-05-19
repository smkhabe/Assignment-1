from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os

app = Flask(__name__)

# In-memory storage for policyholders and claims
policyholders = {}
claims = []
claim_id_counter = 1
policyholder_id_counter = 1

# ---------------------------
# Data Models
# ---------------------------

# Represents a person who holds an insurance policy
class Policyholder:
    def __init__(self, name, age, policy_type, sum_insured):
        global policyholder_id_counter
        self.id = policyholder_id_counter
        policyholder_id_counter += 1
        self.name = name
        self.age = age
        self.policy_type = policy_type
        self.sum_insured = sum_insured
        self.registration_date = datetime.now().date()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'policy_type': self.policy_type,
            'sum_insured': self.sum_insured,
            'registration_date': self.registration_date.strftime('%Y-%m-%d')
        }

# Represents an insurance claim made by a policyholder
class Claim:
    def __init__(self, policyholder_id, claim_amount, reason, status='Pending'):
        global claim_id_counter
        self.id = claim_id_counter
        claim_id_counter += 1
        self.policyholder_id = policyholder_id
        self.amount = claim_amount
        self.reason = reason
        self.status = status
        self.date = datetime.now().date()
    
    def to_dict(self):
        return {
            'id': self.id,
            'policyholder_id': self.policyholder_id,
            'amount': self.amount,
            'reason': self.reason,
            'status': self.status,
            'date': self.date.strftime('%Y-%m-%d')
        }

# ---------------------------
# Validation Helpers
# ---------------------------

# Validates input data for registering a policyholder
def validate_policyholder_data(data):
    errors = []
    if not data.get('name'):
        errors.append('Name is required')
    if not data.get('age') or not str(data['age']).isdigit() or int(data['age']) <= 0:
        errors.append('Valid age is required')
    if data.get('policy_type') not in ['Health', 'Vehicle', 'Life']:
        errors.append('Valid policy type (Health, Vehicle, Life) is required')
    if not data.get('sum_insured') or not str(data['sum_insured']).replace('.', '').isdigit() or float(data['sum_insured']) <= 0:
        errors.append('Valid sum insured is required')
    return errors

# Validates input data for submitting a claim
def validate_claim_data(data):
    errors = []
    if not data.get('policyholder_id') or not str(data['policyholder_id']).isdigit() or int(data['policyholder_id']) not in policyholders:
        errors.append('Valid policyholder ID is required')
    if not data.get('amount') or not str(data['amount']).replace('.', '').isdigit() or float(data['amount']) <= 0:
        errors.append('Valid claim amount is required')
    if not data.get('reason'):
        errors.append('Claim reason is required')
    return errors

# ---------------------------
# Risk & Reporting Logic
# ---------------------------

# Calculates number of claims made by a policyholder in the past year
def calculate_claim_frequency(policyholder_id):
    one_year_ago = datetime.now().date() - timedelta(days=365)
    return len([claim for claim in claims if claim.policyholder_id == policyholder_id and claim.date >= one_year_ago])

# Calculates total claim amount to sum insured ratio
def calculate_claim_ratio(policyholder_id):
    ph = policyholders.get(policyholder_id)
    if not ph or ph.sum_insured == 0:
        return 0
    total_claims = sum(claim.amount for claim in claims if claim.policyholder_id == policyholder_id)
    return total_claims / ph.sum_insured

# Identifies policyholders that could be classified as high-risk
def identify_high_risk_policyholders():
    high_risk = []
    for ph_id, ph in policyholders.items():
        freq = calculate_claim_frequency(ph_id)
        ratio = calculate_claim_ratio(ph_id)
        if freq > 3 or ratio > 0.8:
            high_risk.append({
                'policyholder': ph.to_dict(),
                'claim_frequency': freq,
                'claim_ratio': ratio
            })
    return high_risk

# Generates various statistical reports based on claims data
def generate_reports():
    monthly_claims = defaultdict(int)
    for claim in claims:
        month_year = claim.date.strftime('%Y-%m')
        monthly_claims[month_year] += 1
    
    policy_type_totals = defaultdict(lambda: {'count': 0, 'total': 0})
    for claim in claims:
        ph = policyholders.get(claim.policyholder_id)
        if ph:
            policy_type_totals[ph.policy_type]['count'] += 1
            policy_type_totals[ph.policy_type]['total'] += claim.amount
    
    avg_by_type = {}
    for policy_type, data in policy_type_totals.items():
        avg_by_type[policy_type] = data['total'] / data['count'] if data['count'] > 0 else 0

    highest_claim = max(claims, key=lambda x: x.amount, default=None)
    pending = [claim for claim in claims if claim.status == 'Pending']
    
    return {
        'monthly_claims': dict(monthly_claims),
        'average_by_type': avg_by_type,
        'highest_claim': highest_claim.to_dict() if highest_claim else None,
        'pending_claims': [claim.to_dict() for claim in pending]
    }

# ---------------------------
# Routes
# ---------------------------

# Home page with summary stats
@app.route('/')
def index():
    pending_claims = len([claim for claim in claims if claim.status == 'Pending'])
    high_risk_count = len(identify_high_risk_policyholders())
    return render_template('index.html', 
                         policyholders=policyholders.values(), 
                         claims=claims,
                         pending_claims=pending_claims,
                         high_risk_count=high_risk_count)

# View/Add policyholders
@app.route('/policyholders', methods=['GET', 'POST'])
def manage_policyholders():
    if request.method == 'POST':
        data = request.form
        errors = validate_policyholder_data(data)
        if errors:
            return render_template('policyholders.html', 
                                 policyholders=policyholders.values(), 
                                 errors=errors)
        
        ph = Policyholder(
            name=data['name'],
            age=int(data['age']),
            policy_type=data['policy_type'],
            sum_insured=float(data['sum_insured'])
        )
        policyholders[ph.id] = ph
        return redirect(url_for('manage_policyholders'))
    
    return render_template('policyholders.html', 
                         policyholders=policyholders.values(), 
                         errors=None)

# View/Add claims
@app.route('/claims', methods=['GET', 'POST'])
def manage_claims():
    if request.method == 'POST':
        data = request.form
        errors = validate_claim_data(data)
        if errors:
            return render_template('claims.html', 
                                 claims=claims, 
                                 policyholders=policyholders, 
                                 errors=errors)
        
        claim = Claim(
            policyholder_id=int(data['policyholder_id']),
            claim_amount=float(data['amount']),
            reason=data['reason'],
            status=data.get('status', 'Pending')
        )
        claims.append(claim)
        return redirect(url_for('manage_claims'))
    
    return render_template('claims.html', 
                         claims=claims, 
                         policyholders=policyholders, 
                         errors=None)

# View risk analysis dashboard
@app.route('/risk-analysis')
def risk_analysis():
    high_risk = identify_high_risk_policyholders()
    claims_by_type = defaultdict(list)
    for claim in claims:
        ph = policyholders.get(claim.policyholder_id)
        if ph:
            claims_by_type[ph.policy_type].append(claim.to_dict())
    
    return render_template('risk_analysis.html', 
                         high_risk=high_risk, 
                         claims_by_type=dict(claims_by_type))

# View generated reports
@app.route('/reports')
def view_reports():
    reports = generate_reports()
    return render_template('reports.html', reports=reports, policyholders=policyholders)

# Update claim status (e.g., Approve or Reject)
@app.route('/api/update-claim-status/<int:claim_id>', methods=['POST'])
def update_claim_status(claim_id):
    data = request.json
    for claim in claims:
        if claim.id == claim_id:
            claim.status = data.get('status', claim.status)
            return jsonify({'success': True, 'claim': claim.to_dict()})
    return jsonify({'success': False, 'error': 'Claim not found'}), 404

# Reorders claim IDs to be sequential starting from 1
def reorder_claim_ids():
    global claims, claim_id_counter
    for i, claim in enumerate(claims, 1):
        claim.id = i
    claim_id_counter = len(claims) + 1

# Reorders policyholder IDs to be sequential starting from 1
def reorder_policyholder_ids():
    global policyholders, policyholder_id_counter, claims
    # Create a mapping of old IDs to new IDs
    id_mapping = {}
    new_policyholders = {}
    
    # First pass: create mapping and assign new IDs
    for i, (old_id, ph) in enumerate(sorted(policyholders.items(), key=lambda x: x[0]), 1):
        id_mapping[old_id] = i
        ph.id = i
        new_policyholders[i] = ph
    
    # Update policyholder dictionary
    policyholders.clear()
    policyholders.update(new_policyholders)
    policyholder_id_counter = len(policyholders) + 1
    
    # Update policyholder_id references in claims
    for claim in claims:
        if claim.policyholder_id in id_mapping:
            claim.policyholder_id = id_mapping[claim.policyholder_id]

# Delete a claim
@app.route('/api/delete-claim/<int:claim_id>', methods=['DELETE'])
def delete_claim(claim_id):
    global claims
    for i, claim in enumerate(claims):
        if claim.id == claim_id:
            deleted_claim = claims.pop(i)
            reorder_claim_ids()  # Reorder IDs after deletion
            return jsonify({'success': True, 'claim': deleted_claim.to_dict()})
    return jsonify({'success': False, 'error': 'Claim not found'}), 404

# Delete a policyholder and their associated claims
@app.route('/api/delete-policyholder/<int:policyholder_id>', methods=['DELETE'])
def delete_policyholder(policyholder_id):
    global policyholders, claims
    
    # Check if policyholder exists
    if policyholder_id not in policyholders:
        return jsonify({'success': False, 'error': 'Policyholder not found'}), 404
    
    # Get the policyholder data before deletion
    deleted_policyholder = policyholders[policyholder_id].to_dict()
    
    # Remove all claims associated with this policyholder
    global claims
    claims = [claim for claim in claims if claim.policyholder_id != policyholder_id]
    
    # Remove the policyholder
    del policyholders[policyholder_id]
    
    # Reorder policyholder IDs after deletion
    reorder_policyholder_ids()
    
    # Reorder claim IDs after removing claims
    reorder_claim_ids()
    
    return jsonify({
        'success': True,
        'policyholder': deleted_policyholder,
        'message': 'Policyholder and associated claims have been deleted'
    })

# Data Persistence
# ---------------------------

# Saves current data to JSON file
def save_data():
    data = {
        'policyholders': [ph.to_dict() for ph in policyholders.values()],
        'claims': [claim.to_dict() for claim in claims],
        'counters': {
            'policyholder_id': policyholder_id_counter,
            'claim_id': claim_id_counter
        }
    }
    with open('insurance_data.json', 'w') as f:
        json.dump(data, f)

# Loads data from saved JSON file if it exists
def load_data():
    global policyholders, claims, policyholder_id_counter, claim_id_counter
    
    if not os.path.exists('insurance_data.json'):
        return
    
    with open('insurance_data.json', 'r') as f:
        data = json.load(f)
    
    policyholders.clear()
    claims.clear()
    
    for ph_data in data.get('policyholders', []):
        ph = Policyholder(
            name=ph_data['name'],
            age=ph_data['age'],
            policy_type=ph_data['policy_type'],
            sum_insured=ph_data['sum_insured']
        )
        ph.id = ph_data['id']
        ph.registration_date = datetime.strptime(ph_data['registration_date'], '%Y-%m-%d').date()
        policyholders[ph.id] = ph
    
    for claim_data in data.get('claims', []):
        claim = Claim(
            policyholder_id=claim_data['policyholder_id'],
            claim_amount=claim_data['amount'],
            reason=claim_data['reason'],
            status=claim_data['status']
        )
        claim.id = claim_data['id']
        claim.date = datetime.strptime(claim_data['date'], '%Y-%m-%d').date()
        claims.append(claim)
    
    counters = data.get('counters', {})
    policyholder_id_counter = counters.get('policyholder_id', 1)
    claim_id_counter = counters.get('claim_id', 1)

# ---------------------------
# Entry Point
# ---------------------------

if __name__ == '__main__':
    # Restore previous session if available
    load_data()
    
    try:
        # Start Flask dev server
        app.run(debug=True)
    finally:
        # Persist data when shutting down
        save_data()
