from blockchain_services import get_transaction_details_from_api


async def analyse_transaction_by_hash(tx_hash: str):
    """
    Fetches transaction details and adds analytical insights.
    """
    try:
        # 1. Get the base transaction details
        details = await get_transaction_details_from_api(tx_hash)

        # 2. Add analytical fields to the details dictionary
        analysis = {}

        # --- Fee Analysis ---
        fee_rate = details.get("fee_per_vb", 0)
        if fee_rate > 100:
            analysis["fee_level"] = "High"
            analysis["fee_comment"] = "This transaction paid a high fee for faster confirmation."
        elif fee_rate > 20:
            analysis["fee_level"] = "Normal"
            analysis["fee_comment"] = "The fee is in a typical range for standard confirmation times."
        else:
            analysis["fee_level"] = "Low"
            analysis["fee_comment"] = "This transaction paid a low fee, which might lead to slower confirmation."

        # --- Spending Pattern Analysis ---
        inputs_count = details.get("inputs_count", 0)
        outputs_count = details.get("outputs_count", 0)

        if inputs_count == 1 and outputs_count == 1:
            analysis["pattern"] = "Direct Transfer"
            analysis["pattern_comment"] = "A simple transfer from one address to another."
        elif inputs_count == 1 and outputs_count == 2:
            analysis["pattern"] = "Common Payment"
            analysis[
                "pattern_comment"] = "Likely a payment to one address, with the remainder sent to a change address."
        elif inputs_count > 1 and outputs_count == 1:
            analysis["pattern"] = "Consolidation"
            analysis[
                "pattern_comment"] = "Multiple inputs are being combined into a single output, possibly to consolidate funds."
        elif inputs_count > 5 or outputs_count > 5:
            analysis["pattern"] = "Complex (Batch)"
            analysis["pattern_comment"] = "This is a complex transaction, possibly a batch payment from an exchange."
        else:
            analysis["pattern"] = "Standard"
            analysis["pattern_comment"] = "A standard multi-input or multi-output transaction."

        # --- Other Flags ---
        analysis["is_high_value"] = details.get("amount_btc", 0) > 10  # Flag if > 10 BTC
        analysis["is_confirmed"] = bool(details.get("block_id"))

        # 3. Combine base details with the new analysis
        details["analysis"] = analysis

        return details

    except Exception as e:
        # Re-raise the exception to be handled by the router
        raise e

