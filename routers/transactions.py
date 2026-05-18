from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from blockchain_services import fetch_and_save_transactions_from_blocks, get_transaction_details_from_api
import websockets
import json

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("/fetch")
async def fetch_transactions(blocks: int = Query(1, ge=1, le=10)):
    try:
        transactions = await fetch_and_save_transactions_from_blocks(blocks)
        return transactions
    except Exception as e:
        # Catch exceptions from the service and return a proper HTTP error
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/details/{tx_hash}")
async def get_transaction_details(tx_hash: str):
    try:
        details = await get_transaction_details_from_api(tx_hash)
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- New WebSocket Endpoint for Live Transactions ---
@router.websocket("/ws/live-transactions")
async def websocket_endpoint(websocket: WebSocket):
    """
    Connects to blockchain.info's WebSocket and streams unconfirmed transactions
    to the frontend client.
    """
    await websocket.accept()
    uri = "wss://ws.blockchain.info/inv"
    try:
        # Connect to the external WebSocket provider
        async with websockets.connect(uri) as external_ws:
            # Subscribe to unconfirmed transactions feed
            await external_ws.send('{"op":"unconfirmed_sub"}')
            print("[INFO] Subscribed to live unconfirmed transactions feed.")

            while True:
                # Listen for messages from the external WebSocket
                data = await external_ws.recv()
                tx_data = json.loads(data)

                # We only care about actual transaction data (op is 'utx')
                if tx_data.get('op') == 'utx':
                    tx = tx_data.get('x', {})

                    # Simplify the data before sending it to our frontend
                    simplified_tx = {
                        "hash": tx.get("hash"),
                        "time": tx.get("time"),
                        "output_value_btc": sum(out.get("value", 0) for out in tx.get("out", [])) / 100_000_000,
                        "input_count": len(tx.get("inputs", [])),
                        "output_count": len(tx.get("out", []))
                    }

                    # Send the simplified data to our connected frontend client
                    await websocket.send_json(simplified_tx)

    except WebSocketDisconnect:
        print("[INFO] Frontend client disconnected from the live feed.")
    except Exception as e:
        print(f"[ERROR] An error occurred with the WebSocket connection: {e}")
    finally:
        print("[INFO] Closing live transaction WebSocket connection.")

