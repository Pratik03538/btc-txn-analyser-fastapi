import random
from datetime import datetime
from blockchain_services import fetch_block_data, get_latest_block_height, get_transaction_details_from_api


# --- ALGORITHM SIMULATIONS with more realistic scoring and flagged TXs ---

def simulate_high_fanout(transactions):
    """Simulates detection of One-to-Many (splitting) patterns."""
    flagged_txs = [{'hash': tx['hash'], 'value_btc': sum(o.get("value", 0) for o in tx.get("out", [])) / 1e8} for tx in
                   transactions if len(tx.get("inputs", [])) < 3 and len(tx.get("out", [])) > 20]
    score = min(int((len(flagged_txs) / len(transactions) * 100) * 1.5) if transactions else 0, 100)
    return {
        "name": "High Fan-out (Splitting)",
        "description": "Detects single sources sending funds to many outputs, a pattern in airdrop scams or fund distribution.",
        "risk_score": score,
        "flagged_txs": flagged_txs,
        "how_it_works": "Our algorithm counts inputs and outputs. If a transaction has very few inputs (e.g., <3) and many outputs (e.g., >20), we flag it. This ratio can indicate distribution patterns."
    }


def simulate_high_fanin(transactions):
    """Simulates detection of Many-to-One (collection) patterns."""
    high_fanin_txs = [{'hash': tx['hash'], 'value_btc': sum(o.get("value", 0) for o in tx.get("out", [])) / 1e8} for tx
                      in transactions if len(tx.get("inputs", [])) > 20 and len(tx.get("out", [])) < 3]
    score = min(int((len(high_fanin_txs) / len(transactions) * 100) * 4) if transactions else 0, 100)  # Higher weight
    return {
        "name": "High Fan-in (Collection)",
        "description": "Identifies transactions consolidating funds from many inputs, often used to collect scammed funds.",
        "risk_score": score,
        "flagged_txs": high_fanin_txs,
        "how_it_works": "If a transaction has many inputs (e.g., >20) and few outputs (e.g., <3), it's flagged. This is a strong indicator of funds being collected into one place."
    }


def simulate_dusting_attack(transactions):
    """Simulates detection of dusting attack patterns."""
    flagged_txs = [{'hash': tx['hash'], 'value_btc': sum(o.get("value", 0) for o in tx.get("out", [])) / 1e8} for tx in
                   transactions if any(out.get("value", 0) / 1e8 < 0.00000546 for out in tx.get("out", []))]
    score = min(int(len(flagged_txs) / (len(transactions) + 1) * 10), 100)  # Lower weight
    return {
        "name": "Dusting Activity",
        "description": "Flags transactions with tiny 'dust' outputs, which can indicate privacy attacks.",
        "risk_score": score,
        "flagged_txs": flagged_txs,
        "how_it_works": "The algorithm flags any transaction containing an output below the 'dust limit' (546 satoshis). A high count of such transactions can signal a privacy attack."
    }


def simulate_ponzi_flow(transactions):
    """A very simplified heuristic to simulate Ponzi-like flow."""
    flagged_txs = [{'hash': tx['hash'], 'value_btc': sum(o.get("value", 0) for o in tx.get("out", [])) / 1e8} for tx in
                   transactions if len(tx.get("inputs", [])) > 5 and len(tx.get("out", [])) > 5]
    score = min(int((len(flagged_txs) / len(transactions) * 100) * 2.5) if transactions else 0, 100)
    return {
        "name": "Ponzi Flow Heuristics",
        "description": "Simulates detection of multi-level payout structures where funds from many are redistributed.",
        "risk_score": score,
        "flagged_txs": flagged_txs,
        "how_it_works": "This simulation looks for complex transactions (many inputs and many outputs). This pattern is often seen in Ponzi schemes where money from new investors is used to pay earlier ones."
    }


# --- New function for single transaction analysis ---
def get_single_tx_analysis(tx_details: dict):
    """Runs a quick analysis on a single transaction's details."""
    score = 0
    reasons = []

    if len(tx_details.get("inputs", [])) > 20 and len(tx_details.get("out", [])) < 3:
        score += 45
        reasons.append("High Fan-in: Consolidating funds from many sources.")
    if len(tx_details.get("inputs", [])) < 3 and len(tx_details.get("out", [])) > 20:
        score += 25
        reasons.append("High Fan-out: Distributing funds to many destinations.")
    if any(out.get("value_btc", 0) < 0.00000546 for out in tx_details.get("outputs", [])):
        score += 5
        reasons.append("Dust Outputs: Contains very small, potentially privacy-compromising outputs.")
    if tx_details.get("amount_btc", 0) > 100:
        score += 15
        reasons.append("High Value: Transaction moves a very large amount of BTC (>100).")

    if not reasons:
        reasons.append("No obvious suspicious patterns found.")

    return {"risk_score": min(score, 100), "reasons": reasons}


# --- MAIN SERVICE FUNCTIONS ---
async def get_block_info(block_identifier: str, num_blocks: int = 1):
    try:
        if block_identifier == 'latest':
            start_block_height = await get_latest_block_height()
        else:
            start_block_height = int(block_identifier)
        total_transactions = 0
        for i in range(num_blocks):
            block_data = await fetch_block_data(start_block_height - i)
            if block_data: total_transactions += len(block_data.get("tx", []))
        return {"start_block": start_block_height - num_blocks + 1, "end_block": start_block_height,
                "num_blocks": num_blocks, "total_transactions": total_transactions}
    except Exception as e:
        raise e


async def analyse_blocks_for_scams(start_block: int, num_blocks: int = 1):
    try:
        all_transactions = []
        for i in range(num_blocks):
            block_data = await fetch_block_data(start_block + i)
            if block_data: all_transactions.extend(block_data.get("tx", []))
        if not all_transactions: raise ValueError("No transactions found in the specified block range.")

        algorithms = [simulate_high_fanout, simulate_high_fanin, simulate_dusting_attack, simulate_ponzi_flow]
        results = [algo(all_transactions) for algo in algorithms]

        # Stronger weight for high fan-in, lower for others
        weighted_score = (results[0]["risk_score"] * 0.15 + results[1]["risk_score"] * 0.50 + results[2][
            "risk_score"] * 0.05 + results[3]["risk_score"] * 0.30)
        overall_probability = min(weighted_score * 0.6, 95.0)  # Scaled down for realism

        if overall_probability < 2:
            risk_level = "Very Low"
        elif overall_probability < 10:
            risk_level = "Low"
        elif overall_probability < 30:
            risk_level = "Medium"
        elif overall_probability < 60:
            risk_level = "High"
        else:
            risk_level = "Critical"

        suspicious_tx_hashes = set()
        for res in results:
            for tx in res['flagged_txs']: suspicious_tx_hashes.add(tx['hash'])

        return {
            "start_block": start_block, "end_block": start_block + num_blocks - 1,
            "total_transactions": len(all_transactions), "suspicious_transactions": len(suspicious_tx_hashes),
            "algorithm_results": results, "overall_scam_probability": round(overall_probability, 2),
            "risk_level": risk_level, "graph_data": {"labels": ["Normal", "Suspicious"],
                                                     "data": [len(all_transactions) - len(suspicious_tx_hashes),
                                                              len(suspicious_tx_hashes)]}
        }
    except Exception as e:
        raise e

