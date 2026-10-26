"""
financial_engine.py - Core cash flow calculations for CashSense.
Computes daily 90-day cash projections, runway (safe days left),
danger zones, and Indian Rupee formatting.
"""

from datetime import date, timedelta
import pandas as pd
import numpy as np

def format_inr(number):
    """
    Format numbers according to the Indian Rupee numbering system (e.g., ₹1,45,000).
    Handles negative numbers cleanly.
    """
    if number is None or pd.isna(number):
        return "₹0"
    
    is_negative = number < 0
    num = abs(int(round(number)))
    
    s = str(num)
    if len(s) <= 3:
        formatted = s
    else:
        last_three = s[-3:]
        remaining = s[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted = ",".join(groups) + "," + last_three
        
    return f"-₹{formatted}" if is_negative else f"₹{formatted}"

def standardize_dataframe(df):
    """
    Standardizes uploaded CSV or Excel data columns into CashSense format.
    Flexible matching for common Indian SME accounting column headers.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["Date", "Party", "Type", "Amount", "Category", "Notes"])
    
    clean_df = df.copy()
    
    # Normalize column names to lowercase stripped
    col_map = {col: str(col).strip().lower() for col in clean_df.columns}
    
    # Find matching columns
    date_col = next((c for c, l in col_map.items() if any(k in l for k in ["date", "tarikh", "day"])), None)
    party_col = next((c for c, l in col_map.items() if any(k in l for k in ["party", "name", "customer", "vendor", "supplier", "account", "description", "details"])), None)
    type_col = next((c for c, l in col_map.items() if any(k in l for k in ["type", "in/out", "inout", "flow", "direction", "cr/dr", "dr/cr", "credit/debit"])), None)
    amt_col = next((c for c, l in col_map.items() if any(k in l for k in ["amount", "rupees", "rs", "inr", "value", "total"])), None)
    notes_col = next((c for c, l in col_map.items() if any(k in l for k in ["notes", "remark", "memo", "category", "purpose"])), None)
    
    result = pd.DataFrame()
    
    # Process Date
    if date_col:
        result["Date"] = pd.to_datetime(clean_df[date_col], errors="coerce").dt.date
    else:
        # Default starting from today
        result["Date"] = [date.today() + timedelta(days=i) for i in range(len(clean_df))]
        
    # Drop rows where date is NaT
    result = result.dropna(subset=["Date"])
    
    # Process Party
    if party_col:
        result["Party"] = clean_df[party_col].astype(str).str.strip()
    else:
        result["Party"] = "General Transaction"
        
    # Process Amount
    if amt_col:
        # Clean currency characters, commas, and strings
        amt_series = clean_df[amt_col].astype(str).str.replace("₹", "", regex=False)
        amt_series = amt_series.str.replace(",", "", regex=False).str.replace(" ", "", regex=False)
        result["Amount"] = pd.to_numeric(amt_series, errors="coerce").fillna(0.0).abs()
    else:
        result["Amount"] = 0.0
        
    # Process Type (Money In vs Money Out)
    if type_col:
        def parse_type(val):
            v = str(val).strip().lower()
            if any(k in v for k in ["in", "credit", "cr", "income", "receipt", "jama", "inflow", "+"]):
                return "Money In"
            return "Money Out"
        result["Type"] = clean_df[type_col].apply(parse_type)
    else:
        # If amount in original df had positive/negative signs
        if amt_col:
            raw_nums = pd.to_numeric(clean_df[amt_col].astype(str).str.replace("[₹, ]", "", regex=True), errors="coerce").fillna(0)
            result["Type"] = raw_nums.apply(lambda x: "Money In" if x >= 0 else "Money Out")
        else:
            result["Type"] = "Money In"
            
    # Process Notes / Category
    if notes_col:
        result["Notes"] = clean_df[notes_col].astype(str).str.strip()
        result["Category"] = clean_df[notes_col].astype(str).str.strip()
    else:
        result["Notes"] = "-"
        result["Category"] = "General"
        
    return result.sort_values(by="Date").reset_index(drop=True)

def project_cash_runway(opening_cash, transactions_df, target_days=30, horizon_days=90):
    """
    Projects daily cash balance from today through 90 days.
    Calculates runway (Safe Days Left), danger date, lowest balance point,
    and returns a clean day-by-day dataframe for Plotly charting.
    """
    today = date.today()
    end_date = today + timedelta(days=horizon_days)
    
    # Generate continuous daily timeline
    all_dates = [today + timedelta(days=i) for i in range(horizon_days + 1)]
    daily_df = pd.DataFrame({"Date": all_dates})
    daily_df["Day_Index"] = range(horizon_days + 1)
    
    # Filter transactions within horizon
    if not transactions_df.empty:
        valid_tx = transactions_df.copy()
        valid_tx["Date"] = pd.to_datetime(valid_tx["Date"]).dt.date
        valid_tx = valid_tx[(valid_tx["Date"] >= today) & (valid_tx["Date"] <= end_date)]
        
        # Group by Date and Type
        inflows = valid_tx[valid_tx["Type"] == "Money In"].groupby("Date")["Amount"].sum().reset_index()
        inflows.columns = ["Date", "Inflow"]
        
        outflows = valid_tx[valid_tx["Type"] == "Money Out"].groupby("Date")["Amount"].sum().reset_index()
        outflows.columns = ["Date", "Outflow"]
        
        daily_df = daily_df.merge(inflows, on="Date", how="left").fillna({"Inflow": 0})
        daily_df = daily_df.merge(outflows, on="Date", how="left").fillna({"Outflow": 0})
    else:
        daily_df["Inflow"] = 0.0
        daily_df["Outflow"] = 0.0
        
    daily_df["Net"] = daily_df["Inflow"] - daily_df["Outflow"]
    
    # Compute cumulative balance
    # Day 0 starts with opening_cash + day 0 net
    balances = []
    current = float(opening_cash)
    for idx, row in daily_df.iterrows():
        current += float(row["Net"])
        balances.append(current)
        
    daily_df["Cash_Balance"] = balances
    daily_df["Is_Danger"] = daily_df["Cash_Balance"] < 0
    
    # Compute Safe Days Left:
    # Safe days = number of days until the balance first drops below 0
    negative_days = daily_df[daily_df["Cash_Balance"] < 0]
    if not negative_days.empty:
        first_danger_day = int(negative_days.iloc[0]["Day_Index"])
        danger_date = negative_days.iloc[0]["Date"]
        safe_days = max(0, first_danger_day)
    else:
        first_danger_day = None
        danger_date = None
        safe_days = horizon_days  # Safe for entire 90 days
        
    lowest_cash = float(daily_df["Cash_Balance"].min())
    lowest_idx = daily_df["Cash_Balance"].idxmin()
    lowest_date = daily_df.loc[lowest_idx, "Date"]
    
    final_cash = float(daily_df.iloc[-1]["Cash_Balance"])
    total_inflow = float(daily_df["Inflow"].sum())
    total_outflow = float(daily_df["Outflow"].sum())
    net_change = total_inflow - total_outflow
    
    # Status calculation
    if safe_days < 10:
        status = "CRITICAL_DANGER"
        status_label = "🔴 Critical Cash Alert! Immediate action needed."
    elif safe_days < target_days:
        status = "WARNING"
        status_label = f"⚠️ Low Runway! Cash runs out in {safe_days} days (Target is {target_days} days)."
    else:
        status = "HEALTHY"
        status_label = f"🟢 Safe & Healthy! You have {safe_days}+ days of safe runway."
        
    summary = {
        "opening_cash": float(opening_cash),
        "safe_days": safe_days,
        "target_days": target_days,
        "is_safe": safe_days >= target_days,
        "status": status,
        "status_label": status_label,
        "danger_date": danger_date,
        "lowest_cash": lowest_cash,
        "lowest_cash_date": lowest_date,
        "final_cash": final_cash,
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "net_change": net_change,
        "deficit": abs(lowest_cash) if lowest_cash < 0 else 0
    }
    
    return daily_df, summary
