# Ujima Loan Pride — Multi-Agent SACCO Loan Intelligence Dashboard

A modern loan application platform for SACCO (Savings and Credit Cooperative Organization) members in informal sectors, powered by an ethical AI agent pipeline that ensures fair screening without bias against informal occupations.

---

## 🎯 Project Overview

**Ujima Loan Pride** is a web-based dashboard designed to streamline loan applications for members of cooperative societies. The system employs three specialized AI agents (Scout, Guardian, Hunter) to analyze loan requests, screen applicants fairly, and prepare briefing packets for human loan officers.

**Key Philosophy:** No discrimination against informal occupation, gender, or rural location. Fair screening only.

---

## 📋 Features

### 1. **Real-Time KPI Dashboard**
- Revenue YTD tracking
- Total disbursed funds
- Active borrowers count
- Repayment rate monitoring

### 2. **Interactive Charts**
- Revenue trend (line chart)
- Revenue mix breakdown (donut chart)
- Borrowers by occupation distribution (bar chart)

### 3. **Loan Application Form**
A comprehensive form for members to request loans with fields:
- Full name
- Occupation (6 predefined options)
- Location
- Loan amount (KES)
- Purpose
- Monthly income
- Number of dependents

### 4. **Multi-Agent Pipeline**
Three-stage AI-powered review system:

#### **Scout Agent** — Financial Literacy Coach
- Analyzes income patterns and harvest cycles
- Identifies seasonal income peaks
- Detects financial literacy gaps
- Provides context on stress signals

#### **Guardian Agent** — Loan Triage
- Applies fair screening (no bias against informal work)
- Calculates loan risk score (0–100)
- Flags potential issues
- Makes initial decision: APPROVED, ESCALATE, or DECLINE

#### **Hunter Agent** — Human-in-Loop Coordinator
- Generates officer briefing packets
- Matches applicant to regional specialist
- Provides counterfactual income analysis
- Suggests cross-sell opportunities (insurance, savings plans)
- Delivers 2-minute briefing format

### 5. **Recent Applications Table**
- Displays all processed applications
- Shows member name, occupation, loan amount
- Decision status (Approved ✅ | Escalated ⚠️ | Declined 🚫)
- Action links to view briefing packets

### 6. **Response Modal**
- Swahili/Sheng language feedback to applicants
- Agent pipeline summary
- Clear decision communication

### 7. **Officer Briefing Modal**
- Comprehensive packet for human review
- Member summary and income evidence
- Risk flag explanations
- Harvest calendar context
- Counterfactual income analysis
- Cross-sell suggestions

---

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Safari, Firefox, Edge)
- Internet connection (for CDN resources)
- Google Gemini API key (optional—defaults to mock mode)

### Setup

1. **Clone or download the project**
   ```bash
   cd ujima\ loan
   ```

2. **Add your Google Gemini API key** (optional)
   - Open `index.html`
   - Find the line: `const GEMINI_API_KEY = "..."`
   - Replace with your actual API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. **Open in browser**
   ```bash
   # On macOS
   open index.html
   
   # On Linux
   xdg-open index.html
   
   # On Windows
   start index.html
   ```

---

## 📱 How to Use

### Submitting a Loan Application

1. **Tap "Apply for Loan"** button in header to jump to form
2. **Fill in all form fields:**
   - Name, occupation, location
   - Desired loan amount (KES 1,000–500,000)
   - Loan purpose
   - Monthly income
   - Number of children
3. **Click "Submit to Agent Pipeline"**
4. **Monitor pipeline:**
   - Scout analyzes income pattern
   - Guardian screens for fairness
   - Hunter (if escalated) prepares briefing
5. **View decision** in response modal (Swahili language)
6. **Form auto-resets** for next submission

### Loading Test Profiles

Use the **"Load Test Profile"** section to quickly populate the form with sample data:
- **Grace Akinyi** — Maize farmer requesting KES 28,000
- **Amina Hassan** — Market vendor requesting KES 12,000
- **Zawadi Ochieng** — Shea butter trader requesting KES 8,000

### Viewing Officer Briefings

- Click **"View Packet"** on any escalated application
- Read 2-minute briefing designed for loan officers
- Includes assigned officer, income evidence, risk analysis, and counterfactual scenarios

---

## 🏗️ Architecture

### File Structure
```
ujima loan/
├── index.html          # Single-page application (HTML + CSS + JS)
└── README.md           # Documentation (this file)
```

### Technology Stack
- **Frontend:** HTML5, Tailwind CSS, Chart.js
- **Language:** Vanilla JavaScript
- **APIs:** Google Generative AI (Gemini) — optional integration
- **Charts:** Chart.js 4.x for data visualization
- **Icons:** Heroicons (SVG)
- **Fonts:** Inter (Google Fonts via CDN)

### Data Flow

```
User Form Input
    ↓
[processApplication()]
    ↓
Scout Agent Analysis → Income & Harvest Pattern Recognition
    ↓
Guardian Agent Screening → Loan Score (0-100) + Risk Flags
    ↓
Decision: APPROVED / ESCALATE / DECLINE
    ↓
If ESCALATE:
    Hunter Agent → Officer Briefing Packet
    ↓
Response Modal + Table Update
    ↓
Form Auto-Reset
```

---

## 🤖 Agent Logic Details

### Scout Agent
Analyzes occupational income patterns:
- **Seasonal farmers** → Identifies harvest months (e.g., Oct/Nov for maize)
- **Daily income vendors** → Notes peak market seasons
- **Irregular traders** → Flags income variability
- **Output:** Income type, peak months, financial literacy gaps

### Guardian Agent Scoring
```
Base Score: 70

+ 15 pts if loan_amount ≤ 15,000 KES
- 10 pts if loan_amount > 15,000 KES

+ 10 pts if monthly_income ≥ 50% of loan_amount
- 15 pts if monthly_income < 50% of loan_amount

+ 5 pts if SACCO member ≥ 12 months
- 5 pts if SACCO member < 12 months

- 5 pts if children ≥ 3
- 10 pts if existing_loans > 0
- 5 pts if savings < 20% of loan_amount

Final: 0–100 (clamped)

Decision Logic:
- APPROVED:  score ≥ 70 AND risk_flags < 2
- ESCALATE: 50 ≤ score < 70 OR 2 ≤ risk_flags < 3
- DECLINE:  score < 50 OR risk_flags ≥ 3
```

### Hunter Agent (Escalation Only)
Generates briefing packets including:
1. **Officer Assignment** — Regional specialist matched by occupation
2. **Member Summary** — Age, occupation, tenure, location
3. **Income Evidence** — Monthly amount, income type, peak months, savings
4. **Risk Explanations** — Detailed breakdown of each flag
5. **Harvest Context** — Seasonal calendars for agricultural/vendor occupations
6. **Counterfactual Analysis** — "If income were 20% higher, score would be ~X"
7. **Cross-Sell Opportunities** — Suggest insurance or savings products

---

## 📊 Dashboard Components

### KPI Cards (4 columns)
- **Revenue YTD:** KES 4.8M (↑12% vs last quarter)
- **Total Disbursed:** KES 2.1M across 314 members
- **Active Borrowers:** 314 (↑8 new this month)
- **Repayment Rate:** 94.2% (above SASRA target)

### Charts
1. **Revenue Trend** — 6-month line chart (Jan–Jun 2026)
2. **Revenue Mix** — Donut chart (Interest 65%, Fees 20%, Penalties 5%, Other 10%)
3. **Borrowers by Occupation** — Bar chart (6 occupation categories)

### Applications Table
Columns:
- **Member** — Name + location
- **Occupation** — Job category
- **Amount** — Loan requested (KES)
- **Decision** — Badge (Approved/Escalated/Declined)
- **Action** — "View Packet" link (escalated only)

---

## 🔧 Form Fields

| Field | Type | Required | Constraints | Example |
|-------|------|----------|-------------|---------|
| Full Name | Text | ✅ | Any | Grace Akinyi |
| Occupation | Select | ✅ | 6 options | Maize Farmer |
| Location | Text | ✅ | Any | Kakamega |
| Loan Amount | Number | ✅ | 1,000–500,000 KES | 28,000 |
| Purpose | Textarea | ✅ | Any | School fees |
| Monthly Income | Number | ✅ | ≥ 0 | 15,000 |
| Children | Number | ✅ | 0–10 | 2 |

### Occupation Options
1. Maize Farmer
2. Matooke Farmer
3. Market Vendor (vegetables)
4. Shea Butter Trader
5. Matatu Owner
6. Tailor

---

## 🛡️ Ethical Guardrails

The system enforces fair lending practices:

1. **No Occupation Bias**
   - Informal work (farming, vending, trading) is never penalized
   - Same evaluation criteria for formal and informal sectors

2. **No Gender Discrimination**
   - Identical screening regardless of applicant gender
   - Historical bias removed from algorithms

3. **No Location Penalty**
   - Rural borrowers evaluated fairly alongside urban members
   - Regional income seasonality factored in

4. **Transparent Scoring**
   - All risk flags explained to loan officer
   - Counterfactual scenarios provided
   - No black-box decisions

5. **Human-in-Loop Design**
   - Escalations require human officer review
   - AI assists, does not replace, human judgment

---

## 🔌 API Integration (Secure Backend)

### Architecture
The API key is now **secured on the backend** using a Vercel serverless function. The client-side code no longer exposes any sensitive credentials.

```
Client (index.html)
  ↓ fetch request (no API key)
Backend (api/gemini.js)
  ↓ (uses process.env.GEMINI_API_KEY)
Google Gemini API
```

### Setup Instructions

#### Step 1: Get Your Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key (you'll need this for Vercel environment variables)

#### Step 2: Deploy to Vercel

**Option A: Using Vercel CLI (Recommended)**

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Navigate to project folder
cd "ujima loan"

# 3. Login to Vercel
vercel login

# 4. Deploy
vercel

# 5. Add environment variable when prompted
# Or go to Vercel dashboard → Project Settings → Environment Variables
# Add: GEMINI_API_KEY = your_actual_key_here
```

**Option B: Using Vercel Web Dashboard**

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project" → Select your repository
4. **Before deploying:**
   - Go to Settings → Environment Variables
   - Add `GEMINI_API_KEY` = your actual API key
   - Select "Production" environment
5. Click Deploy

#### Step 3: Verify Deployment
- Visit your Vercel URL
- Submit a test loan application
- Check the application processes without errors
- Monitor your Google API dashboard for successful calls

### Environment Variables (.env.local for local testing)

Create a `.env.local` file in the project root (already in `.gitignore`):

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Important:** Never commit `.env.local` to git!

### File Structure
```
ujima loan/
├── index.html              # Client code (NO API keys here)
├── api/
│   └── gemini.js          # Backend function (uses env variables)
├── README.md              # This file
├── .gitignore             # Prevents committing secrets
└── .env.local             # Local testing only (ignored by git)
```

### How It Works

1. **Client submits form** → `processApplication()` is called
2. **Agent pipeline runs** → `callGeminiAPI()` makes a request to `/api/gemini`
3. **Backend function** (`api/gemini.js`) receives the request
4. **Backend safely calls Gemini API** using environment variable `GEMINI_API_KEY`
5. **Response returned to client** for display

### Security Checklist
- ✅ API key stored in Vercel environment variables (encrypted)
- ✅ API key NOT hardcoded in source code
- ✅ API key NOT exposed in browser DevTools
- ✅ Backend only accepts POST requests
- ✅ `.env.local` never committed to git
- ✅ All communication uses HTTPS (automatic on Vercel)

### Fallback Behavior
If the backend is unavailable or API key is missing:
- System gracefully falls back to mock responses
- Users still see agent pipeline simulation
- No errors break the application

### Monitoring & Troubleshooting

**Check API Usage:**
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- View API usage metrics
- Set quotas to prevent unexpected charges

**Debug Backend Issues:**
1. Go to Vercel dashboard → your project
2. Click "Deployments" → latest deployment
3. Click "Functions" tab
4. View logs for `api/gemini`

**Common Issues:**

| Issue | Solution |
|-------|----------|
| "API key not configured" | Add `GEMINI_API_KEY` to Vercel env vars |
| 401 Unauthorized | Verify API key is correct in env var |
| 429 Too Many Requests | Check rate limits; upgrade Gemini plan if needed |
| Function timeout | Increase function timeout in vercel.json (if needed) |

### Upgrading from Client-Side to Backend

If you had the old client-side code:
1. **Remove** the hardcoded API key from `index.html`
2. **Update** `callGeminiAPI()` to fetch from `/api/gemini`
3. **Create** `api/gemini.js` with the backend code
4. **Add** `GEMINI_API_KEY` to Vercel environment variables
5. **Test** locally with `.env.local` before deploying

---

## 🐍 FastAPI Backend (Local & Production)

This project includes an optional FastAPI proxy that securely stores the `GEMINI_API_KEY` on the server side and forwards requests from the frontend to Google Gemini.

Files added:
- `backend/main.py` — FastAPI app with `POST /api/gemini` endpoint
- `backend/requirements.txt` — Python dependencies
- `.env.example` — example environment variables file

Quick local setup:

1. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\\Scripts\\activate     # Windows PowerShell
pip install -r backend/requirements.txt
```

2. Create a `.env` file in project root (or set env vars in your host):

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
FRONTEND_ORIGIN=http://localhost:5500
```

3. Run the FastAPI server (development):

```bash
# from project root
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

4. Open the frontend (`index.html`) in your browser. The client already calls `/api/gemini` so when the backend runs on the same host or a reverse proxy, requests will be forwarded securely.

Notes for production:
- Deploy the FastAPI app to your host (Render, Fly, or a VPS) and set `GEMINI_API_KEY` in provider environment variables.
- If serving frontend separately, set `FRONTEND_ORIGIN` to the frontend origin and ensure CORS is configured.


## 📲 Responsive Design

- **Desktop:** Full grid layout (KPIs, charts, form, pipeline, table)
- **Tablet:** Optimized column wrapping
- **Mobile:** Single-column stacked layout with smooth scrolling

---

## 🎨 Design System

### Colors (Tailwind)
- **Ujima (Primary):** Green (#10b981)
  - 50: #f0fdf4, 100: #dcfce7, 500: #10b981, 600: #059669, 700: #047857, 900: #064e3b
- **Pride (Accent):** Amber (#f59e0b)
  - 500: #f59e0b, 600: #d97706
- **Neutral:** Slate (grays)

### Typography
- **Font Family:** Inter (Google Fonts)
- **Headlines:** Semibold (600)
- **Body:** Regular (400)
- **Small Text:** 0.75rem (12px)

### Animations
- `pulse-ring` — Expanding pulse for active agents
- `fade-in-up` — Entrance animation for modals
- `slide-in` — Slide animation for table rows
- `blink` — Typing cursor blink

---

## 📝 Customization Guide

### Change Occupation Options
Edit the `<select id="app-occupation">` element:
```html
<option value="Your Occupation">Your Occupation Label</option>
```

### Modify Loan Amount Limits
In the `<input id="app-amount">` element:
```html
<input min="1000" max="500000" />  <!-- Change min/max -->
```

### Adjust Agent Scoring
Find `generateGuardianDecision()` function and modify point values:
```javascript
if (app.loan_amount_kes <= 15000) score += 15;  // Change points here
```

### Change Colors
Update Tailwind config in `<style>` block:
```javascript
colors: {
  ujima: { 500: '#10b981', /* ... */ },
  pride: { 500: '#f59e0b', /* ... */ }
}
```

### Modify Swahili Responses
Edit `generateSwahiliResponse()` function to customize decision messages.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Charts not showing | Check browser console for errors; ensure Chart.js loaded |
| Form not submitting | Verify all required fields filled; check browser console |
| API errors | Confirm Gemini API key is valid; check rate limits |
| Slow pipeline | Normal—agents simulate processing delays for UX; adjust in `callGeminiAPI()` |
| Modal not closing | Ensure JavaScript enabled; click backdrop to close |

---

## 📄 License & Credits

**Project:** Ujima Loan Pride  
**Purpose:** Financial Inclusion for Informal Sectors  
**Date:** June 2026  
**Region Focus:** Western Kenya (Kakamega, Busia, Mt. Elgon)

---

## 🤝 Contributing

Suggestions for improvement:
- Add SMS notifications for decision updates
- Integrate with mobile money (M-Pesa, Airtel Money)
- Export briefing packets as PDF
- Multi-language support (Swahili, Luhya, Luo, Kikuyu)
- Bulk upload for agent onboarding
- Mobile app wrapper (React Native, Flutter)

---

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review agent pipeline logs in browser console
3. Validate form inputs match constraints
4. Ensure API key configured (if using live Gemini)

---

**Last Updated:** June 3, 2026  
**Version:** 1.0

