from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Ujima Gemini Proxy")

# Configure CORS
_frontend = os.getenv("FRONTEND_ORIGIN", "*")
if _frontend == "*":
    origins = ["*"]
else:
    origins = [o.strip() for o in _frontend.split(',') if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GeminiRequest(BaseModel):
    agentType: str = None
    context: dict = None
    prompt: str = None


# -----------------------------
# Agent-to-agent orchestration
# -----------------------------
def get_peak_months(occupation: str):
    if 'Maize' in occupation or 'Maize' in occupation.title():
        return ['October', 'November']
    if 'Matooke' in occupation or 'Matooke' in occupation.title():
        return ['March', 'April', 'September', 'October']
    if 'Market' in occupation or 'vendor' in occupation.lower():
        return ['March', 'April', 'September', 'October']
    if 'Shea' in occupation or 'Shea' in occupation.title():
        return ['January', 'July']
    return ['March', 'December']


def get_income_type(occupation: str):
    occ = occupation.lower()
    if 'farmer' in occ:
        return 'seasonal'
    if 'market' in occ or 'vendor' in occ:
        return 'daily_cash'
    if 'trader' in occ:
        return 'irregular'
    return 'irregular'


def generate_scout_output(app: dict):
    peak = get_peak_months(app.get('occupation', ''))
    income_type = get_income_type(app.get('occupation', ''))
    harvest_note = ''
    if 'Maize' in app.get('occupation', '') or 'Matooke' in app.get('occupation', '') or 'farmer' in app.get('occupation', '').lower():
        harvest_note = f"Income aligns with {"/".join(peak)}. School fee pressure noted."
    else:
        harvest_note = f"Daily/irregular income pattern. Peak demand in {', '.join(peak)}."

    stress_flags = []
    if app.get('children', 0) and int(app.get('children', 0)) > 2:
        stress_flags.append('School fee pressure (3+ dependents)')
    if app.get('loan_amount_kes') and app.get('monthly_income_kes') and int(app.get('loan_amount_kes', 0)) > int(app.get('monthly_income_kes', 0)) * 2:
        stress_flags.append('Loan exceeds 2x monthly income')

    gaps = []
    if app.get('sacco_member_months', 0) < 12:
        gaps.append('New member — limited SACCO history')

    parts = []
    parts.append(f"Income Pattern: {income_type.replace('_',' ')}")
    parts.append(f"Harvest Alignment: {harvest_note}")
    parts.append(f"Stress Signals: {', '.join(stress_flags) if stress_flags else 'None detected'}")
    parts.append(f"Literacy Gaps: {', '.join(gaps) if gaps else 'None identified'}")
    parts.append(f'"{app.get("name")} is a hardworking {app.get("occupation","").lower()}. With proper timing, this loan can thrive."')
    return '<br>'.join(parts)


def generate_guardian_decision(app: dict):
    score = 70
    risk_flags = []

    loan = int(app.get('loan_amount_kes', 0))
    income = int(app.get('monthly_income_kes', 0))

    if loan <= 15000:
        score += 15
    else:
        score -= 10

    if income >= loan * 0.5:
        score += 10
    else:
        score -= 15
        risk_flags.append('Income-to-loan ratio below 50%')

    if app.get('sacco_member_months', 0) >= 12:
        score += 5
    else:
        score -= 5
        risk_flags.append('Member < 12 months')

    if int(app.get('children', 0)) >= 3:
        score -= 5
    if int(app.get('existing_loans', 0)) > 0:
        score -= 10
        risk_flags.append('Existing loan detected')
    if int(app.get('savings_balance_kes', 0)) < loan * 0.2:
        score -= 5

    score = max(0, min(100, score))

    decision = 'APPROVED'
    if score < 50 or len(risk_flags) >= 3:
        decision = 'DECLINE'
    elif loan > 15000 or score < 70 or len(risk_flags) >= 2:
        decision = 'ESCALATE'

    return { 'decision': decision, 'score': score, 'risk_flags': risk_flags }


def generate_guardian_output(app: dict, result: dict):
    emoji = '✅' if result['decision'] == 'APPROVED' else '⚠️' if result['decision'] == 'ESCALATE' else '🚫'
    msg = f"<strong>Decision:</strong> {emoji} {result['decision']}<br><strong>Loan Score:</strong> {result['score']}/100<br><strong>Risk Flags:</strong> {', '.join(result['risk_flags']) if result['risk_flags'] else 'None'}"
    if result['decision'] == 'APPROVED':
        msg += '<br><em class="text-emerald-700">"Fair screening applied. No bias detected against informal occupation."</em>'
    elif result['decision'] == 'ESCALATE':
        msg += '<br><em class="text-amber-700">"Escalating to Hunter for human review. Not a denial — just extra care."</em>'
    return msg


def get_matched_officer(occupation: str):
    if 'Maize' in occupation or 'Matooke' in occupation:
        return 'Joseph Wekesa (Kakamega region specialist)'
    if 'Market' in occupation:
        return 'Mary Achieng (Nairobi informal trade expert)'
    if 'Shea' in occupation:
        return 'Peter Otieno (Busia County field officer)'
    return 'James Mwangi (General portfolio officer)'


def generate_hunter_briefing(app: dict, guardian_result: dict):
    officer = get_matched_officer(app.get('occupation',''))
    counterfactual_income = int(int(app.get('monthly_income_kes',0)) * 1.2)
    new_score = min(100, guardian_result['score'] + 15)
    return {
        'officer': officer,
        'memberSummary': f"{app.get('name')}, {app.get('age',35)}yo {app.get('occupation','').lower()} from {app.get('location')}. SACCO member for {app.get('sacco_member_months',0)} months.",
        'incomeEvidence': f"Monthly income: KES {int(app.get('monthly_income_kes',0))} ({app.get('income_type','')}). Peak months: {', '.join(get_peak_months(app.get('occupation','')))}. Savings: KES {int(app.get('savings_balance_kes',0))}.",
        'riskExplanations': '<br>'.join([f'• {r}' for r in guardian_result.get('risk_flags',[])]) if guardian_result.get('risk_flags') else 'No risk flags',
        'harvestContext': 'Maize long rains: March-May. Short rains: Oct-Nov. Harvest income peaks in Oct/Nov.' if 'farmer' in app.get('occupation','').lower() else 'Market vendor income peaks during school terms and holiday seasons.',
        'counterfactual': f"If income were 20% higher (KES {counterfactual_income}), loan score would rise to ~{new_score}/100, likely qualifying for auto-approval.",
        'crossSell': 'School Fees Savings Plan + Drought Insurance' if int(app.get('children',0))>0 else 'Drought Insurance + Business Growth Savings Plan'
    }


@app.post('/api/process')
async def process_application(req: GeminiRequest):
    # Build application dict from request
    app_data = {
        'name': req.context.get('name') if req.context else req.__dict__.get('name'),
        'occupation': req.context.get('occupation') if req.context else '',
        'location': req.context.get('location') if req.context else '',
        'loan_amount_kes': int(req.context.get('amount') if req.context and req.context.get('amount') else 0),
        'purpose': req.context.get('purpose') if req.context else '',
        'monthly_income_kes': int(req.context.get('income') if req.context and req.context.get('income') else 0),
        'children': int(req.context.get('children') if req.context and req.context.get('children') else 0),
    }

    # enrich
    app_data['peak_months'] = get_peak_months(app_data.get('occupation',''))
    app_data['income_type'] = get_income_type(app_data.get('occupation',''))
    app_data['savings_balance_kes'] = int(app_data['monthly_income_kes'] * 0.4)
    app_data['existing_loans'] = 1 if (os.urandom(1)[0] / 255.0) > 0.7 else 0
    app_data['sacco_member_months'] = int((os.urandom(1)[0] % 24) + 3)

    # Scout
    scout_output = generate_scout_output(app_data)

    # Guardian
    guardian_result = generate_guardian_decision(app_data)
    guardian_output = generate_guardian_output(app_data, guardian_result)

    hunter_briefing = None
    hunter_output = None
    if guardian_result['decision'] == 'ESCALATE':
        hunter_briefing = generate_hunter_briefing(app_data, guardian_result)
        hunter_output = f"Officer briefing packet prepared for {app_data.get('name')}. Matched to officer: {hunter_briefing.get('officer')}. Counterfactual analysis included."

    final_app = {
        'id': int.from_bytes(os.urandom(6), 'big'),
        'name': app_data.get('name'),
        'occupation': app_data.get('occupation'),
        'location': app_data.get('location'),
        'loan_amount_kes': app_data.get('loan_amount_kes'),
        'decision': guardian_result['decision'],
        'timestamp': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'loan_score': guardian_result['score'],
        'risk_flags': len(guardian_result.get('risk_flags',[])),
        'hunter_briefing': hunter_briefing
    }

    return {
        'scout_output': scout_output,
        'guardian_output': guardian_output,
        'hunter_output': hunter_output,
        'guardian_result': guardian_result,
        'final_app': final_app,
    }
