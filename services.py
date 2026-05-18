import httpx
from datetime import datetime, timedelta

# --- Constants ---
COINGECKO_API_BASE_URL = "https://api.coingecko.com/api/v3"


# --- Main Service Function for Dashboard ---
async def get_live_bitcoin_data_with_candlesticks():
    """
    Fetches the current Bitcoin price, 24h change, and OHLCV data for a candlestick chart
    from the CoinGecko API in INR.
    """
    price_url = f"{COINGECKO_API_BASE_URL}/simple/price?ids=bitcoin&vs_currencies=inr&include_24hr_change=true"
    chart_url = f"{COINGECKO_API_BASE_URL}/coins/bitcoin/ohlc?vs_currency=inr&days=1"

    async with httpx.AsyncClient() as client:
        try:
            # Make API calls concurrently
            price_response_task = client.get(price_url)
            chart_response_task = client.get(chart_url)

            price_response = await price_response_task
            chart_response = await chart_response_task

            price_response.raise_for_status()
            chart_response.raise_for_status()

            price_data = price_response.json().get("bitcoin", {})
            chart_data_raw = chart_response.json()

            if not price_data or not chart_data_raw:
                raise ValueError("Incomplete data received from API.")

            # --- Process Chart Data ---
            chart_data_formatted = [
                {
                    "x": item[0],
                    "o": item[1],
                    "h": item[2],
                    "l": item[3],
                    "c": item[4]
                }
                for item in chart_data_raw
            ]

            # --- Calculate 24h absolute change ---
            current_price = price_data.get('inr', 0)
            change_percent = price_data.get('inr_24h_change', 0)
            # Formula: previous_price = current_price / (1 + (change_percent / 100))
            # change_abs = current_price - previous_price
            previous_price = current_price / (1 + (change_percent / 100))
            change_abs = current_price - previous_price

            return {
                "price": current_price,
                "change_24h": change_abs,
                "change_24h_percent": change_percent,
                "chart_data": chart_data_formatted
            }

        except httpx.HTTPStatusError as e:
            # Provide a more user-friendly error message
            if e.response.status_code == 429:
                raise Exception("API rate limit exceeded. Please wait a moment before refreshing.")
            raise Exception(f"API returned an error: {e.response.status_code}")
        except Exception as e:
            # Catch other errors like timeouts or JSON decoding errors
            raise Exception(f"An error occurred while fetching market data: {e}")

