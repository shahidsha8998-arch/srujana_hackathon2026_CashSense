"""
action_engine.py - Dynamic, Relationship-Safe Actions Engine for CashSense
==========================================================================
Generates tailored, high-impact, zero-damage actions to protect cash runway
based on whatever invoices and transactions are currently in the active ledger.
Works dynamically for any uploaded invoice, custom ledger, or demo dataset.
"""

from datetime import date, timedelta
import pandas as pd
from financial_engine import format_inr

def generate_recommendations(transactions_df, opening_cash, summary):
    """
    Dynamically finds the 3 clearest, highest-impact, and safest actions
    to protect cash runway based on the active transactions in the ledger.
    If no transactions exist, returns an empty list.
    """
    if transactions_df is None or transactions_df.empty:
        return []
        
    today = date.today()
    actions = []
    horizon_window = today + timedelta(days=90)
    
    # Filter upcoming valid transactions
    tx = transactions_df.copy()
    tx["Date"] = pd.to_datetime(tx["Date"]).dt.date
    
    upcoming_inflows = tx[
        (tx["Type"] == "Money In") & 
        (tx["Date"] >= today) & 
        (tx["Date"] <= horizon_window)
    ].sort_values(by="Amount", ascending=False)
    
    upcoming_outflows = tx[
        (tx["Type"] == "Money Out") & 
        (tx["Date"] >= today) & 
        (tx["Date"] <= horizon_window)
    ].sort_values(by="Amount", ascending=False)
    
    # -----------------------------------------------------------------
    # ACTION 1: Split Largest Upcoming Outflow (50% Now, 50% Later)
    # -----------------------------------------------------------------
    if not upcoming_outflows.empty:
        target_supplier = upcoming_outflows.iloc[0]
        supp_name = str(target_supplier["Party"])
        supp_amount = float(target_supplier["Amount"])
        supp_date = target_supplier["Date"]
        half_amount = round(supp_amount / 2)
        
        actions.append({
            "id": "act_split_supplier",
            "title": f"Ask {supp_name} to split bill into 2 payments",
            "what_to_do": f"Pay 50% ({format_inr(half_amount)}) on due date, and 50% after 25 days.",
            "why_it_works": "Suppliers agree happily when you proactively inform them 1 week early rather than delaying at the last moment.",
            "money_protected": half_amount,
            "money_label": f"+{format_inr(half_amount)} Protected",
            "risk_level": "Low",
            "risk_label": "Low Risk (Safe)",
            "risk_color": "#10B981",
            "action_type": "split_outflow",
            "target_party": supp_name,
            "target_amount": supp_amount,
            "target_date": supp_date,
            "split_delay_days": 25
        })

    # -----------------------------------------------------------------
    # ACTION 2: Fast-Track Customer Collection with a 2% Cash Discount
    # -----------------------------------------------------------------
    if not upcoming_inflows.empty:
        target_cust = upcoming_inflows.iloc[0]
        cust_name = str(target_cust["Party"])
        cust_amount = float(target_cust["Amount"])
        cust_date = target_cust["Date"]
        discount_rate = 0.02
        collected_amount = round(cust_amount * (1 - discount_rate))
        
        actions.append({
            "id": "act_early_discount",
            "title": f"Offer 2% quick discount to {cust_name} to pay this week",
            "what_to_do": f"Collect {format_inr(collected_amount)} right away instead of waiting until {cust_date.strftime('%d %b')}.",
            "why_it_works": "Customers love saving 2% cash; you get liquidity in bank immediately with zero relationship friction.",
            "money_protected": collected_amount,
            "money_label": f"+{format_inr(collected_amount)} Cash Early",
            "risk_level": "Low",
            "risk_label": "Low Risk (Safe)",
            "risk_color": "#10B981",
            "action_type": "accelerate_inflow",
            "target_party": cust_name,
            "target_amount": cust_amount,
            "new_amount": collected_amount,
            "target_date": cust_date,
            "accelerate_to_days": 2
        })
    elif len(upcoming_outflows) > 1:
        # If no inflows exist, provide a 2nd payment rescheduling option
        target_sec = upcoming_outflows.iloc[1]
        sec_name = str(target_sec["Party"])
        sec_amount = float(target_sec["Amount"])
        sec_date = target_sec["Date"]
        actions.append({
            "id": "act_reschedule_outflow",
            "title": f"Request 21-day grace period for {sec_name}",
            "what_to_do": f"Reschedule this {format_inr(sec_amount)} bill forward by 3 weeks.",
            "why_it_works": "Vendor relationships are protected by providing scheduled installment predictability.",
            "money_protected": sec_amount,
            "money_label": f"+{format_inr(sec_amount)} Deferred",
            "risk_level": "Low",
            "risk_label": "Low Risk (Safe)",
            "risk_color": "#10B981",
            "action_type": "defer_outflow",
            "target_party": sec_name,
            "target_amount": sec_amount,
            "target_date": sec_date,
            "defer_days": 21
        })

    # -----------------------------------------------------------------
    # ACTION 3: Pause Discretionary / Non-Urgent Upgrades or Purchases
    # -----------------------------------------------------------------
    # Look for equipment / capex / upgrades first
    non_urgent = upcoming_outflows[
        upcoming_outflows["Category"].str.contains("Equipment|Upgrade|Furniture|Tooling|Expense", case=False, na=False) |
        upcoming_outflows["Party"].str.contains("Rack|Tool|Display|New|Renovation|Machine|Equipment", case=False, na=False)
    ]
    
    if not non_urgent.empty:
        target_exp = non_urgent.iloc[0]
        exp_name = str(target_exp["Party"])
        exp_amount = float(target_exp["Amount"])
        exp_date = target_exp["Date"]
        
        actions.append({
            "id": "act_pause_capex",
            "title": f"Hold '{exp_name}' purchase for 3 weeks",
            "what_to_do": f"Delay this non-urgent outlay ({format_inr(exp_amount)}) until cash recovers.",
            "why_it_works": "This is completely internal. Zero impact on any customer or supplier.",
            "money_protected": exp_amount,
            "money_label": f"+{format_inr(exp_amount)} Saved Now",
            "risk_level": "Low",
            "risk_label": "Low Risk (Zero Risk)",
            "risk_color": "#10B981",
            "action_type": "defer_outflow",
            "target_party": exp_name,
            "target_amount": exp_amount,
            "target_date": exp_date,
            "defer_days": 21
        })
    elif len(upcoming_outflows) > 2:
        # Fallback to 3rd outflow
        target_3rd = upcoming_outflows.iloc[2]
        t3_name = str(target_3rd["Party"])
        t3_amount = float(target_3rd["Amount"])
        t3_date = target_3rd["Date"]
        actions.append({
            "id": "act_defer_secondary",
            "title": f"Reschedule payment for {t3_name}",
            "what_to_do": f"Push this {format_inr(t3_amount)} bill forward by 14 days.",
            "why_it_works": "Gives you breathing room during the tight week without defaulting.",
            "money_protected": t3_amount,
            "money_label": f"+{format_inr(t3_amount)} Protected",
            "risk_level": "Medium",
            "risk_label": "Medium Risk",
            "risk_color": "#F59E0B",
            "action_type": "defer_outflow",
            "target_party": t3_name,
            "target_amount": t3_amount,
            "target_date": t3_date,
            "defer_days": 14
        })
    elif not upcoming_outflows.empty:
        # If only 1 outflow exists in the entire ledger
        sole_outflow = upcoming_outflows.iloc[0]
        s_name = str(sole_outflow["Party"])
        s_amt = float(sole_outflow["Amount"])
        actions.append({
            "id": "act_credit_extension",
            "title": f"Request Net-45 credit terms with {s_name}",
            "what_to_do": f"Negotiate a 15-day grace extension on the {format_inr(s_amt)} invoice balance.",
            "why_it_works": "Standard B2B trade credit terms allow temporary liquidity buffer during inventory turnover.",
            "money_protected": round(s_amt * 0.5),
            "money_label": f"+{format_inr(round(s_amt * 0.5))} Buffer",
            "risk_level": "Low",
            "risk_label": "Low Risk (Safe)",
            "risk_color": "#10B981",
            "action_type": "defer_outflow",
            "target_party": s_name,
            "target_amount": s_amt,
            "target_date": sole_outflow["Date"],
            "defer_days": 15
        })

    # Return whatever actions were discovered (up to 3)
    return actions[:3]

def apply_actions_to_data(original_df, selected_action_ids, all_actions):
    """
    Applies the selected actions to the transactions dataframe and returns
    the simulated new dataframe.
    """
    if not selected_action_ids or original_df is None or original_df.empty:
        return original_df.copy() if original_df is not None else pd.DataFrame()
    
    sim_df = original_df.copy()
    today = date.today()
    
    for action in all_actions:
        if action["id"] not in selected_action_ids:
            continue
            
        act_type = action.get("action_type")
        party = action.get("target_party")
        
        # 1. SPLIT OUTFLOW
        if act_type == "split_outflow":
            mask = (sim_df["Party"] == party) & (sim_df["Type"] == "Money Out")
            if mask.any():
                match_idx = sim_df[mask].index[0]
                orig_amt = sim_df.loc[match_idx, "Amount"]
                orig_date = sim_df.loc[match_idx, "Date"]
                half1 = round(orig_amt / 2)
                half2 = orig_amt - half1
                
                sim_df.loc[match_idx, "Amount"] = half1
                sim_df.loc[match_idx, "Notes"] = f"{sim_df.loc[match_idx, 'Notes']} (Part 1/2 - Split)"
                
                new_date = orig_date + timedelta(days=action.get("split_delay_days", 25))
                new_row = {
                    "Date": new_date,
                    "Party": f"{party} (Part 2/2)",
                    "Type": "Money Out",
                    "Amount": half2,
                    "Category": sim_df.loc[match_idx, "Category"] if "Category" in sim_df else "Supplier Bill",
                    "Notes": "Agreed 2nd payment installment"
                }
                sim_df = pd.concat([sim_df, pd.DataFrame([new_row])], ignore_index=True)

        # 2. ACCELERATE INFLOW
        elif act_type == "accelerate_inflow":
            mask = (sim_df["Party"] == party) & (sim_df["Type"] == "Money In")
            if mask.any():
                match_idx = sim_df[mask].index[0]
                target_days = action.get("accelerate_to_days", 2)
                sim_df.loc[match_idx, "Date"] = today + timedelta(days=target_days)
                if "new_amount" in action:
                    sim_df.loc[match_idx, "Amount"] = action["new_amount"]
                sim_df.loc[match_idx, "Notes"] = f"{sim_df.loc[match_idx, 'Notes']} (Early 2% cash discount)"

        # 3. DEFER OUTFLOW
        elif act_type == "defer_outflow":
            mask = (sim_df["Party"] == party) & (sim_df["Type"] == "Money Out")
            if mask.any():
                match_idx = sim_df[mask].index[0]
                defer_days = action.get("defer_days", 21)
                sim_df.loc[match_idx, "Date"] = sim_df.loc[match_idx, "Date"] + timedelta(days=defer_days)
                sim_df.loc[match_idx, "Notes"] = f"{sim_df.loc[match_idx, 'Notes']} (Deferred +{defer_days}d)"

    sim_df["Date"] = pd.to_datetime(sim_df["Date"]).dt.date
    return sim_df.sort_values(by="Date").reset_index(drop=True)
