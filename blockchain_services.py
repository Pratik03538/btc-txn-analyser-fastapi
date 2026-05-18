import httpx
from datetime import datetime
import json
import asyncio

# --- Constants ---
BLOCKCHAIN_INFO_BASE_URL = "https://blockchain.info"
TRANSACTIONS_DB_FILE = "blockchain_data.json"
MAX_RETRIES = 3

# --- Helper Functions ---
satoshi_to_btc = lambda satoshi: satoshi / 100_000_000 if satoshi is not None else 0


# --- New function to get the latest block height ---
async def get_latest_block_height():
    """Fetches the height of the most recent block from the API."""
    url = f"{BLOCKCHAIN_INFO_BASE_URL}/latestblock"
    print("[INFO] Fetching latest block height...")
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            height = data.get("height")
            if height:
                print(f"[SUCCESS] Latest block height is {height}")
                return height
            else:
                raise ValueError("Block height not found in API response.")
    except Exception as e:
        print(f"[ERROR] Could not fetch latest block height: {e}")
        raise Exception("Could not fetch latest block height from the API.") from e


async def fetch_block_data(block_height: int):
    """Fetches raw block data for a given block height."""
    url = f"{BLOCKCHAIN_INFO_BASE_URL}/block-height/{block_height}?format=json"
    print(f"[INFO] Fetching block data for height: {block_height}")
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                if data and "blocks" in data and len(data["blocks"]) > 0:
                    print(f"[SUCCESS] Successfully fetched block data.")
                    return data["blocks"][0]
                else:
                    raise ValueError("Empty or invalid block data received.")
        except Exception as e:
            print(f"[WARNING] Attempt {attempt + 1} to fetch block {block_height} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(2)
            else:
                raise Exception(f"Failed to fetch block {block_height} after multiple attempts.")
    return None


# --- Transaction Functions ---
async def fetch_and_save_transactions_from_blocks(num_blocks: int):
    print(f"\n[INFO] Starting fetch for {num_blocks} block(s)...")
    summarized_txs = []
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            latest_block_url = f"{BLOCKCHAIN_INFO_BASE_URL}/latestblock"
            response = await client.get(latest_block_url)
            response.raise_for_status()
            current_block_hash = response.json()["hash"]
        except Exception as e:
            raise Exception("Could not connect to Blockchain API to get the latest block.") from e

        for i in range(num_blocks):
            if not current_block_hash: break

            block_data = None
            for attempt in range(MAX_RETRIES):
                try:
                    block_data_url = f"{BLOCKCHAIN_INFO_BASE_URL}/rawblock/{current_block_hash}"
                    response = await client.get(block_data_url)
                    response.raise_for_status()
                    block_data = response.json()
                    break
                except Exception as e:
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(2)
                    else:
                        raise Exception(f"Failed to fetch block data after {MAX_RETRIES} attempts.") from e

            if not block_data: break

            for tx in block_data.get("tx", []):
                output_value = sum(out.get("value", 0) for out in tx.get("out", []))
                summary = {"hash": tx.get("hash"),
                           "time": datetime.fromtimestamp(tx.get("time", 0)).strftime('%Y-%m-%d %H:%M:%S'),
                           "block": block_data.get("height"), "output_value_satoshi": output_value,
                           "output_value_btc": satoshi_to_btc(output_value), "input_count": len(tx.get("inputs", [])),
                           "output_count": len(tx.get("out", []))}
                summarized_txs.append(summary)

            current_block_hash = block_data.get("prev_block")
            if i < num_blocks - 1: await asyncio.sleep(0.5)

    with open(TRANSACTIONS_DB_FILE, 'w') as f:
        json.dump(summarized_txs, f, indent=4)

    return summarized_txs


async def get_transaction_details_from_api(tx_hash: str):
    url = f"{BLOCKCHAIN_INFO_BASE_URL}/rawtx/{tx_hash}"
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                tx_data = response.json()

                total_output_value = sum(out.get("value", 0) for out in tx_data.get("out", []))
                total_input_value = sum(
                    inp.get("prev_out", {}).get("value", 0) for inp in tx_data.get("inputs", []) if inp.get("prev_out"))
                fee = total_input_value - total_output_value if total_input_value > 0 else 0
                size = tx_data.get("size", 1)
                weight = tx_data.get("weight", 1)

                details = {
                    "hash": tx_data.get("hash"), "block_id": tx_data.get("block_height"),
                    "time_raw": tx_data.get("time", 0),
                    "time_formatted": datetime.fromtimestamp(tx_data.get("time", 0)).strftime(
                        '%d %b %Y %H:%M:%S GMT%z'),
                    "amount_btc": satoshi_to_btc(total_output_value), "fee_sats": fee, "fee_btc": satoshi_to_btc(fee),
                    "input_value_btc": satoshi_to_btc(total_input_value),
                    "output_value_btc": satoshi_to_btc(total_output_value),
                    "inputs_count": len(tx_data.get("inputs", [])), "outputs_count": len(tx_data.get("out", [])),
                    "fee_per_byte": fee / size, "fee_per_vb": fee / (weight / 4),
                    "size": size, "weight": weight, "weight_unit": "WU", "version": tx_data.get("ver"),
                    "locktime": tx_data.get("lock_time"),
                    "rbf": any(inp.get("sequence", 0) < 0xffffffff - 1 for inp in tx_data.get("inputs", [])),
                    "is_coinbase": total_input_value == 0,
                    "inputs": [{"address": inp.get("prev_out", {}).get("addr", "N/A"),
                                "value_btc": satoshi_to_btc(inp.get("prev_out", {}).get("value", 0))} for inp in
                               tx_data.get("inputs", []) if inp.get("prev_out")],
                    "outputs": [{"address": out.get("addr", "N/A"), "value_btc": satoshi_to_btc(out.get("value", 0))}
                                for out in tx_data.get("out", [])]
                }
                return details
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(2)
            else:
                raise Exception(f"Failed to fetch details for transaction {tx_hash[:15]}...") from e
    raise Exception("Failed to fetch transaction details due to an unknown error.")

