from fastapi import FastAPI
from fastapi.responses import FileResponse
from app_setup import configure_app
from routers import dashboard, transactions, analyse, scam

# Initialize and configure the app using the setup function
app = configure_app()

# --- Include API Routers ---
app.include_router(dashboard.router)
app.include_router(transactions.router)
app.include_router(analyse.router)
app.include_router(scam.router)

# --- Serve HTML Files ---
# Each HTML file gets its own explicit route for reliability.
@app.get("/", response_class=FileResponse, include_in_schema=False)
async def read_index():
    return "index.html"

@app.get("/fetch_transactions_page.html", response_class=FileResponse, include_in_schema=False)
async def get_fetch_transactions_page():
    return "fetch_transactions_page.html"

@app.get("/analyse_transaction_page.html", response_class=FileResponse, include_in_schema=False)
async def get_analyse_transaction_page():
    return "analyse_transaction_page.html"

@app.get("/transaction_popup.html", response_class=FileResponse, include_in_schema=False)
async def get_transaction_popup():
    return "transaction_popup.html"

@app.get("/scam_detection_page.html", response_class=FileResponse, include_in_schema=False)
async def get_scam_detection_page():
    return "scam_detection_page.html"

