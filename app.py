from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def home():
    return "Carz Chatbot Backend is running"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)

    intent = req.get('queryResult', {}).get('intent', {}).get('displayName')

    if intent == 'car-info':
        car_name = req.get('queryResult', {}).get('parameters', {}).get('car-names')

        if not car_name:
            return jsonify({"fulfillmentText": "Please provide a car name."})

        # If Dialogflow returns list, take first item
        if isinstance(car_name, list):
            car_name = car_name[0]

        keywords = car_name.split()

        query = "SELECT * FROM car_info WHERE " + \
                " OR ".join(["car_name ILIKE %s" for _ in keywords])

        values = [f"%{word}%" for word in keywords]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(query, values)
            result = cursor.fetchone()

            cursor.close()
            conn.close()

        except Exception as e:
            print("Database error:", e)
            return jsonify({"fulfillmentText": "Internal server error while fetching car details."})

        if result:
            id, brand, name, type_, fuel_type, transmission, variants, onroad_price, color = result

            reply = (
                f"{name} by {brand} is a {type_} car.\n"
                f"Fuel Types: {fuel_type}\n"
                f"Transmission: {transmission}\n"
                f"Variants: {variants}\n"
                f"On-road price: {onroad_price}\n"
                f"Available Colors: {color}"
            )
        else:
            reply = "Sorry, I couldn't find that car in my database."

        return jsonify({"fulfillmentText": reply})

    return jsonify({"fulfillmentText": "Sorry, I didn't understand that."})


if __name__ == '__main__':
    app.run()
