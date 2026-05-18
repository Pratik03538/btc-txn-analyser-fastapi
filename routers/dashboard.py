from fastapi import APIRouter, HTTPException
from services import get_live_bitcoin_data_with_candlesticks

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/data")
async def get_dashboard_data():
    """
    Endpoint to get all the necessary data for the main dashboard,
    including live price and candlestick chart data.
    """
    try:
        data = await get_live_bitcoin_data_with_candlesticks()
        return data
    except Exception as e:
        # Pass the specific error message from the service to the frontend
        raise HTTPException(status_code=500, detail=str(e))

