from flask import Flask, request, jsonify

app= Flask(__name__)

@app.route('/')
def home():
    return "Carz Chatbot Backend is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    req= request.get_json(force=True)

    intent= req.get('queryResult',{}).get('intent',{}).get('displayName')

    if intent == 'car-details':
        return jsonify({
            "fulfillmentText": "Car Details: Brand - Toyota, Model - Innova, Type - SUV, Fuel - Diesel"
        })
    
    elif intent == 'price-details':
        return jsonify({
            "fulfillmentText": "Price Breakdown: On-Road - Rs.15 Lakhs, Tax - Rs.2 Lakhs, Total - Rs.17 Lakhs"
        })
    
    else:
        return jsonify({
            "fulfillmentText": "Sorry, I didn't understand that."
        })
    
if __name__ == '__main__':
    app.run(debug=True)