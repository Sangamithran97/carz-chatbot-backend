from flask import Flask, request, jsonify

app= Flask(__name__)

@app.route('/')
def home():
    return "Carz Chatbot Backend is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    req= request.get_json(force=True)

    intent= req.get('queryResult',{}).get('intent',{}).get('displayName')

    if intent == 'car-info':
        car_name= req.get('queryResult').get('parameters').get('carname')
        
        response_text= f"{car_name} is a sedan with petrol engine, manual transmission, and comes in red, blue, or black. The on-road price of {car_name} is Rs. 10 Lakhs, with Rs. 1.5 Lakhs tax, total Rs. 11.5 Lakhs."
    
    else:
        response_text="Sorry, I didn't understand that."
    
    return jsonify({"fulfillmentText":response_text})