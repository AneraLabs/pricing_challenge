from flask import Flask, request, jsonify
import requests

available_liquidity = {
    "ETH" : 1000,
    "KON" : 500,
    "VIS" : 500
}

app = Flask(__name__)

def get_price_quote(instrument, quantity):
    # Binance API endpoint for price ticker
    if instrument == "KON":
        instrument = "BTC"
    elif instrument == "VIS":
        instrument = "SOL"

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={instrument}USDT"
    
    try:
        # Fetch the price from Binance API
        response = requests.get(url)
        data = response.json()
        
        # Check if the response contains a valid price
        if 'price' in data:
            price = float(data['price'])
            total_price = price * quantity
            return total_price
        else:
            raise Exception(f"Price for {instrument} not found.")
    
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def calculate_pricing(instrument, borrow_time_seconds, quantity):
    if instrument not in available_liquidity:
        return None, None

    # Placeholder logic for pricing - replace with actual pricing logic as needed
    # For demonstration, let's just return dummy bid and ask prices

    external_price = get_price_quote(instrument, quantity)
    bid = external_price
    ask = external_price + 0.1
    
    # You can use the parameters here to adjust the pricing logic if needed
    return bid, ask

@app.route('/getPricingUSD', methods=['GET'])
def get_pricing_api():
    instrument = request.args.get('instrument')
    borrow_time_seconds = request.args.get('borrow_time_seconds', type=int)
    quantity = request.args.get('quantity', type=int)
    
    return jsonify(get_pricing(instrument, borrow_time_seconds, quantity))

def get_pricing(instrument, borrow_time_seconds, quantity):
    # Validate parameters
    if not instrument or borrow_time_seconds is None or quantity is None:
        return {"error": "Missing required parameters"}

    # Perform pricing logic
    bid, ask = calculate_pricing(instrument, borrow_time_seconds, quantity)

    pricing_data = {
        "instrument": instrument,
        "borrow_time_seconds": borrow_time_seconds,
        "quantity": quantity,
        "bid": bid,
        "ask": ask
    }

    # Return pricing response
    return pricing_data

if __name__ == '__main__':
    #app.run(debug=True)

    # examples
    print(get_price_quote("VIS", 10))
    print(get_pricing("ETH", 120, 20))