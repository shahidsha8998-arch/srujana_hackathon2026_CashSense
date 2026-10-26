# 💰 CashSense - Production Cash Flow & Runway Engine

> **“What are the easiest and safest actions I can take to protect my cash for the next few weeks, without damaging important customer or supplier relationships?”**

CashSense is a dual-mode financial application built for hackathons and production SME finance:
1. **📊 Production Cash Flow Model & Projections**: Complete standard cash flow statement (Operating, Investing, Financing), real-time reactive recalculation, multi-period aggregation (Monthly, Quarterly, Yearly), break-even detection, and What-If sensitivity scenarios.
2. **🛡️ SME Runway & Safe Actions**: 10th-pass shopkeeper friendly interface with 3 zero-damage actions to protect cash without losing customer trust.
3. **📸 AI Invoice OCR & Device Camera Scanner**: Instantly scan paper invoices, bills, PDFs, or receipts via mobile camera or file upload, automatically parsing Party Name, Amount, Due Date, and Type directly into the cash ledger.

---

## 📸 AI Invoice OCR & Camera Capture

The File Input dropzone supports:
- **Spreadsheets**: `.csv`, `.xlsx`, `.xls`
- **Invoice Images**: `.png`, `.jpg`, `.jpeg`
- **PDF Invoices**: `.pdf`
- **Live Device Camera**: `📸 Scan / Take Photo of Invoice` (triggers device rear/webcam camera via HTML5 capture)

### OCR Extraction Capabilities
When an invoice image or PDF is uploaded or photographed:
1. Displays realistic scanning UI state: `"🔍 Scanning invoice with OCR... extracting Buyer Name, Amount, Due Date"`.
2. Automatically extracts:
   - **Party / Buyer Name**: e.g. *Apex Supplies Ltd* / *Apex Motors Pune*
   - **Invoice Amount**: e.g. *₹45,000.00*
   - **Due Date**: e.g. *10-Nov-2026*
   - **Direction & Category**: *Payable (Supplier Bill)* or *Receivable (Customer Payment)*
   - **OCR Confidence**: e.g. *98.2%*
3. **Instant Ledger Integration**: Appends the extracted row directly into the active business ledger, immediately updating:
   - Cash Balance & Lowest Point
   - Safe Days Runway
   - 90-Day Interactive Plotly Chart
   - Recommended Relationship-Safe Actions

---

## 🧮 1. Exact Financial Formulas Implemented

### Standard Cash Flow Statement
- **Operating Cash Flow (OCF)**:
  $$\text{Revenue}(t) = \text{Base Monthly Revenue} \times (1 + g)^{t-1}$$
  $$\text{Variable Costs}(t) = \text{Revenue}(t) \times \text{Variable Cost \%}$$
  $$\text{Total Operating Costs}(t) = \text{Fixed Costs} + \text{Variable Costs}(t)$$
  $$\text{Operating CF}(t) = \text{Revenue}(t) - \text{Total Operating Costs}(t)$$

- **Investing Cash Flow (ICF)**:
  $$\text{Investing CF}(t) = - \text{One-Time CapEx}(t)$$

- **Financing Cash Flow (FCF)**:
  $$\text{Financing CF}(t) = \text{Funding Inflow}(t) - \text{Loan Repayments}(t)$$

- **Net Change in Cash**:
  $$\text{Net Cash Flow}(t) = \text{Operating CF}(t) + \text{Investing CF}(t) + \text{Financing CF}(t)$$

- **Beginning & Ending Cash Balances**:
  $$\text{Beginning Cash}(t) = \text{Ending Cash}(t-1) \quad (\text{Month 1 Beginning Cash} = \text{Starting Cash})$$
  $$\text{Ending Cash}(t) = \text{Beginning Cash}(t) + \text{Net Cash Flow}(t)$$

---

## 📂 2. Architecture & File Structure

| File | Description |
| :--- | :--- |
| [**`ocr_engine.py`**](ocr_engine.py) | **Production Real OCR**: Native Windows Media OCR & PDF stream parser for invoices, receipts, and camera photos. Extracts party name, amount, due date, category, and confidence. |
| [**`app.py`**](app.py) | **Updated**: Clean startup state machine upon login, high-legibility B2B executive typography scale (Stripe/Mercury), real-time invoice upload integration, and dynamic zero-damage recommendations. |
| [**`cash_flow_engine.py`**](cash_flow_engine.py) | Core pure calculation engine with dataclasses, multi-period aggregation, break-even detection, and sensitivity scenarios. |
| [**`cashFlowCalculator.ts`**](cashFlowCalculator.ts) | Fully typed TypeScript implementation of the cash flow model. |
| [**`financial_engine.py`**](financial_engine.py) | 90-day cash flow ledger calculations for SME shopkeepers. |
| [**`action_engine.py`**](action_engine.py) | 3 relationship-safe actions for SME shopkeepers. |
| [**`sample_data.py`**](sample_data.py) | Sharma Kirana & Patel Auto sample datasets with template generators. |

## 📈 Dynamic Graph & Scenario Comparison Engine

The dashboard features real-time graph recalculation with instant visual feedback:

1. **State Toggle for Applied Actions (`appliedActionsActive`)**:
   - Master **"⚡ Apply These Actions (Recalculate Graph)"** button activates all safe recommendations simultaneously.
   - Individual interactive checkboxes per recommendation card allow granular testing of individual actions (e.g. testing only the supplier payment split, or only early invoice collection).
   - Instant **"🔄 Reset to Base Case"** toggles back to the unmitigated baseline.

2. **Graph Recalculation Logic & Daily Ledger Array (`ledger`)**:
   - Recalculates the full 90-day daily cash balance array (`ledger`) by applying:
     - **Supplier Outflow Split**: Splits large vendor bills (e.g. *Hindustan FMCG Distributors*, *Tata Steel*) 50% on due date and 50% in 25 days.
     - **Early Customer Collection**: Pulls receivable collections forward to Day 2 with a 2% discount (e.g. *Verma Sweets*, *Apex Motors*).
     - **CapEx Deferral**: Defers non-urgent equipment purchases (e.g. *Display Shelf Rack*, *Precision Tooling*) by 21 days.
   - Recalculates `safe_days`, `lowest_cash`, and deficit elimination in `<1ms`.

3. **Visual Impact on Chart**:
   - **Eliminates the Red Danger Zone**: The curve lifts instantly from **-₹59,500** safely above the **₹0 Solvency Threshold** to **+₹63,600**.
   - **Prominent Visual Badges**:
     - `🟢 OPTIMIZED FORECAST (ACTIONS APPLIED) — DEFICIT ELIMINATED (+74 DAYS RUNWAY)`
     - `⚠️ BASE CASE FORECAST (ACTIONS PENDING) — CRITICAL DEFICIT DIP DETECTED`
   - **Interactive Scenario Comparison Selector**:
     - `📊 Side-by-Side Comparison (Base vs. Optimized)`: Displays both curves with clear markers and annotations.
     - `🟢 Optimized Forecast Only`: Clean emerald curve staying entirely above ₹0.
     - `⚠️ Base Case Forecast Only`: Warning curve plunging into the red danger zone.
   - **Annotation Pins**:
     - `🚨 Base Dip: -₹59,500 on Day 16`
     - `🛡️ Safe Min: +₹63,600 on Day 25 (Deficit Cleared!)`
   - **Daily Cash Ledger Inspection**: Expandable day-by-day table of the underlying `ledger` array with CSV export.

4. **🔍 Live Mathematical Model & Formula Transparency Inspector**:
   - Collapsible panel at the bottom of the dashboard designed specifically for hackathon judges to audit the math.
   - Shows the 4 deterministic phases:
     1. **Document Extraction Mapping**: Maps scanned invoice tuples $(P_k, T_k, A_k, D_k)$ into discrete vectors $I_t$ and $O_t$.
     2. **Discrete Time-Series Balance Equation**: $B_t = B_{t-1} + I_t - O_t$ with live bindings for $B_0$, $\sum I_t$, $\sum O_t$, and ending cash.
     3. **Insolvency Risk Detection**: $\tau_{\text{safe}} = \min \{ t \mid B_t < 0 \}$ and Deficit Gap $G_{\text{deficit}} = \max(0, -\min B_t)$.
     4. **Vector Transformation Algebra**: Shows how payment date phase-shifting and consensual 2% discounts eliminate the deficit dip without damaging relationship trust.

---

## 🏃 3. How to Run & Test

In your PowerShell / terminal:

```powershell
cd "C:\Users\Lahari S\.gemini\antigravity\scratch\cashsense"
streamlit run app.py
```

*Or double-click `run.bat`.*

### Testing the Invoice OCR & Camera:
1. Select **📁 Upload File or Scan Invoice (Excel, CSV, PDF, Image, Camera)**.
2. In **Upload File**: Upload an invoice PDF (e.g. `Apex_Supplies_Invoice.pdf`) or image (`.png`, `.jpg`).
3. Notice the spinner: `"🔍 Scanning invoice with OCR... extracting Buyer Name, Amount, Due Date"`.
4. Inspect the **OCR Extracted Result Card** displaying Party Name (*Apex Supplies Ltd*), Amount (*₹45,000*), Due Date (*10-Nov-2026*), and Confidence (*98.2%*).
5. Notice how the runway and chart immediately update with the newly scanned bill!
6. Switch to the **📸 Take Photo with Camera** tab to test capturing directly with your webcam or mobile camera.
7. Click **🗑️ Clear Scanned Invoices** to reset back to baseline.
