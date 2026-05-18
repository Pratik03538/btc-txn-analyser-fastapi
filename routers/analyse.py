from fastapi import APIRouter, HTTPException, Query
from analyse_services import analyse_transaction_by_hash

router = APIRouter(
    prefix="/analyse",
    tags=["Analysis"]
)

@router.get("/transaction")
async def get_transaction_analysis(tx_hash: str = Query(..., min_length=64, max_length=64)):
    """
    Provides a detailed analysis of a given transaction hash.
    """
    try:
        analysis_result = await analyse_transaction_by_hash(tx_hash)
        return analysis_result
    except Exception as e:
        # Catch exceptions from the service and return a proper HTTP error
        raise HTTPException(status_code=500, detail=str(e))

