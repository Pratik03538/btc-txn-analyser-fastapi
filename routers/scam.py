from fastapi import APIRouter, HTTPException, Query
from scam_detection_services import analyse_blocks_for_scams, get_block_info, get_single_tx_analysis
from blockchain_services import get_transaction_details_from_api

router = APIRouter(
    prefix="/scam",
    tags=["Scam Detection"]
)

@router.get("/block-info")
async def get_initial_block_info(
    block_identifier: str = Query("latest"),
    num_blocks: int = Query(1, ge=1, le=5)
):
    """Provides basic information about a block(s) before a deep scan."""
    try:
        return await get_block_info(block_identifier, num_blocks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/deep-scan")
async def get_block_analysis(
    start_block: int = Query(..., gt=0),
    num_blocks: int = Query(1, ge=1, le=5)
):
    """Provides a detailed scam analysis of a given block or number of blocks."""
    try:
        return await analyse_blocks_for_scams(start_block, num_blocks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyse-tx/{tx_hash}")
async def analyse_single_transaction(tx_hash: str):
    """Performs a quick scam analysis on a single transaction."""
    try:
        # First, get the full details of the transaction
        tx_details = await get_transaction_details_from_api(tx_hash)
        # Then, run the analysis on those details
        analysis = get_single_tx_analysis(tx_details)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

