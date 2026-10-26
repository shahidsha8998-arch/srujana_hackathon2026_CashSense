$env:PATH = "C:\Users\Lahari S\AppData\Local\Programs\Python\Python312;C:\Users\Lahari S\AppData\Local\Programs\Python\Python312\Scripts;" + $env:PATH
Write-Host "Starting CashSense Web Application..." -ForegroundColor Cyan
streamlit run app.py
