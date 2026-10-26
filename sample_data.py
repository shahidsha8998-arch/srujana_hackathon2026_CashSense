"""
sample_data.py - Realistic Indian SME sample datasets and template generators for CashSense.
Designed to be immediately understandable by Indian shop owners, traders, and small manufacturers.
"""

from datetime import date, timedelta
import pandas as pd
import io

def get_today():
    return date.today()

def get_sharma_kirana_data():
    """
    Sample 1: Sharma Kirana & General Store
    Retail & wholesale grocery store in Jaipur / Delhi.
    Opening Cash: ₹75,000
    Crisis Context: A large FMCG distributor bill of ₹1,35,000 arrives on Day 16,
    causing cash to dip negative (-₹59,500) if no action is taken.
    """
    today = get_today()
    
    entries = [
        {"Date": today + timedelta(days=2), "Party": "Daily Counter Sales (Week 1)", "Type": "Money In", "Amount": 28000, "Category": "Customer Sales", "Notes": "Retail cash & counter UPI collections"},
        {"Date": today + timedelta(days=4), "Party": "Shop Staff Wages (2 helpers)", "Type": "Money Out", "Amount": 24000, "Category": "Staff Wages", "Notes": "Monthly helper salary"},
        {"Date": today + timedelta(days=6), "Party": "Electricity & Commercial Power", "Type": "Money Out", "Amount": 8500, "Category": "Bills & Utilities", "Notes": "Shop electricity & godown power"},
        {"Date": today + timedelta(days=8), "Party": "Daily Counter Sales (Week 2)", "Type": "Money In", "Amount": 32000, "Category": "Customer Sales", "Notes": "Retail cash & counter UPI collections"},
        {"Date": today + timedelta(days=10), "Party": "Shop Rent (Babu Lal Ji)", "Type": "Money Out", "Amount": 35000, "Category": "Rent", "Notes": "Main market shop monthly rent"},
        {"Date": today + timedelta(days=12), "Party": "Hotel Rajdhani Catering", "Type": "Money In", "Amount": 30000, "Category": "Customer Payment", "Notes": "Bulk grocery delivery balance"},
        {"Date": today + timedelta(days=14), "Party": "New Display Shelf Rack", "Type": "Money Out", "Amount": 22000, "Category": "Equipment/Upgrades", "Notes": "Planned new front shelf racks"},
        # Heavy supplier payment creates danger on Day 16
        {"Date": today + timedelta(days=16), "Party": "Hindustan FMCG Distributors", "Type": "Money Out", "Amount": 135000, "Category": "Supplier Bill", "Notes": "Monthly inventory payment for soaps, oils, atta"},
        {"Date": today + timedelta(days=19), "Party": "Daily Counter Sales (Week 3)", "Type": "Money In", "Amount": 35000, "Category": "Customer Sales", "Notes": "Retail cash & counter UPI collections"},
        {"Date": today + timedelta(days=22), "Party": "Verma Sweets & Bakers", "Type": "Money In", "Amount": 45000, "Category": "Customer Payment", "Notes": "Payment for bulk flour & dry fruits"},
        {"Date": today + timedelta(days=25), "Party": "GST Tax Payment", "Type": "Money Out", "Amount": 22000, "Category": "Taxes & Govt", "Notes": "Monthly GSTR-3B tax payment"},
        {"Date": today + timedelta(days=35), "Party": "Daily Counter Sales (Month 2)", "Type": "Money In", "Amount": 140000, "Category": "Customer Sales", "Notes": "Estimated 4 weeks counter sales"},
        {"Date": today + timedelta(days=45), "Party": "Amul Dairy & Stock Bill", "Type": "Money Out", "Amount": 50000, "Category": "Supplier Bill", "Notes": "Milk, butter and cold drink stock"},
        {"Date": today + timedelta(days=55), "Party": "Staff Wages (Month 2)", "Type": "Money Out", "Amount": 24000, "Category": "Staff Wages", "Notes": "Monthly helper salary"},
        {"Date": today + timedelta(days=65), "Party": "Daily Counter Sales (Month 3)", "Type": "Money In", "Amount": 150000, "Category": "Customer Sales", "Notes": "Estimated 4 weeks counter sales"},
        {"Date": today + timedelta(days=70), "Party": "Hindustan FMCG Distributors (Cycle 2)", "Type": "Money Out", "Amount": 95000, "Category": "Supplier Bill", "Notes": "Restock cycle 2"},
    ]
    
    df = pd.DataFrame(entries)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df, 75000  # Default opening cash balance

def get_patel_auto_data():
    """
    Sample 2: Patel Auto Spares & Engineering
    Small manufacturing and spare parts trading workshop in Pune / Ahmedabad.
    Opening Cash: ₹1,10,000
    Crisis Context: Tata Steel invoice of ₹1,65,000 hits on Day 18, and workshop rent on Day 21,
    while major client collections are delayed to Day 26+. Cash runs out on Day 18.
    """
    today = get_today()
    
    entries = [
        {"Date": today + timedelta(days=3), "Party": "Bajaj Auto Service Centre", "Type": "Money In", "Amount": 45000, "Category": "Customer Payment", "Notes": "Brake shoe batch delivery payment"},
        {"Date": today + timedelta(days=5), "Party": "Machinist & Labor Weekly Pay", "Type": "Money Out", "Amount": 38000, "Category": "Staff Wages", "Notes": "4 lathe operators & helpers"},
        {"Date": today + timedelta(days=8), "Party": "Industrial Power & Utilities", "Type": "Money Out", "Amount": 16000, "Category": "Bills & Utilities", "Notes": "High tension power bill"},
        {"Date": today + timedelta(days=11), "Party": "Apex Motors Pune", "Type": "Money In", "Amount": 52000, "Category": "Customer Payment", "Notes": "Gear shaft consignment payment"},
        {"Date": today + timedelta(days=14), "Party": "Precision CNC Tooling Purchase", "Type": "Money Out", "Amount": 35000, "Category": "Equipment/Upgrades", "Notes": "New cutter drill sets"},
        # Big steel crunch on Day 18
        {"Date": today + timedelta(days=18), "Party": "Tata Steel & Alloy Traders", "Type": "Money Out", "Amount": 165000, "Category": "Supplier Bill", "Notes": "Raw alloy rod consignment invoice #902"},
        {"Date": today + timedelta(days=21), "Party": "Workshop Shed Rent", "Type": "Money Out", "Amount": 42000, "Category": "Rent", "Notes": "GIDC industrial shed monthly rent"},
        {"Date": today + timedelta(days=24), "Party": "Mehta Freight & Transport", "Type": "Money Out", "Amount": 14000, "Category": "Logistics", "Notes": "Truck freight charges"},
        {"Date": today + timedelta(days=27), "Party": "Shree Ram Tractors (Rajkot)", "Type": "Money In", "Amount": 85000, "Category": "Customer Payment", "Notes": "Tractor spare pins batch order"},
        {"Date": today + timedelta(days=30), "Party": "GST & Factory Advance Tax", "Type": "Money Out", "Amount": 36000, "Category": "Taxes & Govt", "Notes": "Quarterly tax advance"},
        {"Date": today + timedelta(days=38), "Party": "Kalyani Forgings Ltd", "Type": "Money In", "Amount": 125000, "Category": "Customer Payment", "Notes": "Custom flange order balance"},
        {"Date": today + timedelta(days=45), "Party": "Tata Steel & Alloy Traders", "Type": "Money Out", "Amount": 95000, "Category": "Supplier Bill", "Notes": "Batch 2 steel order"},
        {"Date": today + timedelta(days=55), "Party": "National Highway Fleet Spares", "Type": "Money In", "Amount": 140000, "Category": "Customer Payment", "Notes": "Fleet replacement parts order"},
        {"Date": today + timedelta(days=68), "Party": "Workshop Shed Rent (Month 3)", "Type": "Money Out", "Amount": 42000, "Category": "Rent", "Notes": "GIDC shed rent"},
    ]
    
    df = pd.DataFrame(entries)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df, 110000  # Default opening cash balance

def generate_template_csv():
    """Generates a clean CSV template in simple English with example rows for the user."""
    today = get_today()
    sample_rows = [
        {"Date": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "Party": "Ramesh Customer", "Type": "Money In", "Amount": 25000, "Notes": "Payment for bill #101"},
        {"Date": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "Party": "Shop Helper Salary", "Type": "Money Out", "Amount": 15000, "Notes": "Monthly helper pay"},
        {"Date": (today + timedelta(days=10)).strftime("%Y-%m-%d"), "Party": "Market Supplier Co.", "Type": "Money Out", "Amount": 60000, "Notes": "Stock purchase bill"},
        {"Date": (today + timedelta(days=15)).strftime("%Y-%m-%d"), "Party": "City Wholesale Buyer", "Type": "Money In", "Amount": 45000, "Notes": "Pending order payment"},
        {"Date": (today + timedelta(days=20)).strftime("%Y-%m-%d"), "Party": "Shop Rent", "Type": "Money Out", "Amount": 20000, "Notes": "Owner rent payment"}
    ]
    df = pd.DataFrame(sample_rows)
    return df.to_csv(index=False).encode('utf-8')

def generate_template_excel():
    """Generates an Excel template (.xlsx) for direct download."""
    today = get_today()
    sample_rows = [
        {"Date": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "Party": "Ramesh Customer", "Type": "Money In", "Amount": 25000, "Notes": "Payment for bill #101"},
        {"Date": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "Party": "Shop Helper Salary", "Type": "Money Out", "Amount": 15000, "Notes": "Monthly helper pay"},
        {"Date": (today + timedelta(days=10)).strftime("%Y-%m-%d"), "Party": "Market Supplier Co.", "Type": "Money Out", "Amount": 60000, "Notes": "Stock purchase bill"},
        {"Date": (today + timedelta(days=15)).strftime("%Y-%m-%d"), "Party": "City Wholesale Buyer", "Type": "Money In", "Amount": 45000, "Notes": "Pending order payment"},
        {"Date": (today + timedelta(days=20)).strftime("%Y-%m-%d"), "Party": "Shop Rent", "Type": "Money Out", "Amount": 20000, "Notes": "Owner rent payment"}
    ]
    df = pd.DataFrame(sample_rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Cash_Flow')
    return output.getvalue()
