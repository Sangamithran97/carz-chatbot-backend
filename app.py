from flask import Flask, request, jsonify
import psycopg2

app= Flask(__name__)

conn= psycopg2.connect(
	host="localhost:,
	database="carzchatbot",
	user="postgres",
	password="postgres97",
	port="5432"
)
cursor=conn.cursor()	

@app.route('/')
def home():
    return "Carz Chatbot Backend is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    req= request.get_json(force=True)

    intent= req.get('queryResult',{}).get('intent',{}).get('displayName')

    if intent == 'car-info':
        car_name= req.get('queryResult').get('parameters').get('carname')
	cursor.execute("SELECT * FROM car_info WHERE car_name ILIKE %s", (f"%{car_name}%",))
	result= cursor.fetchone()

	if result:
		brand, name, type, fuel_type, transmission, variants, price, color = result
		reply= (
			f"**{car_name}** by **{brand}** is a {type} car.\n"
			f"- Fuel Types: {fuel_type}
			f"- Transmission: {transmission}\n"
			f"- Variants: {variants}\n"
			f"- On-road price: {onroad_price}\n"
			f"- Available Colors: {color}"
		)
       
    	else:
        	reply="Sorry, I couldn't find that car in my database."
  
	return jsonify({"fulfillmentText":reply})
  
    return jsonify({"fulfillmentText":"Sorry, I didn't understand that})

if __name__ == '__main__':
    app.run()