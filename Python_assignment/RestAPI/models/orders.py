from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# Database connection configuration
DB_HOST = 'localhost'
DB_NAME = 'RestApi'
DB_USER = 'postgres'
DB_PASSWORD = 'ra11'

# Connect to PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Route to insert a new order
@app.route('/orders', methods=['POST'])
def add_order():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            data = request.get_json()
            customer_id = data['customer_id']
            product_name = data['product_name']
            quantity = data['quantity']
            # Inserting into orders table with columns: customer_id, product_name, and quantity
            cur.execute("INSERT INTO orders (customer_id, product_name, quantity) VALUES (%s, %s, %s)", (customer_id, product_name, quantity))
            conn.commit()
            return jsonify({"message": "Order added successfully"}), 201
        except Error as e:
            conn.rollback()
            return jsonify({"error": f"Failed to add order: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to update an order
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            data = request.get_json()
            customer_id = data['customer_id']
            product_name = data['product_name']
            quantity = data['quantity']
            cur.execute("UPDATE orders SET customer_id = %s, product_name = %s, quantity = %s WHERE id = %s", (customer_id, product_name, quantity, order_id))
            conn.commit()
            return jsonify({"message": "Order updated successfully"}), 200
        except Error as e:
            conn.rollback()
            return jsonify({"error": f"Failed to update order: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to select all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders")
            orders = cur.fetchall()
            return jsonify(orders), 200
        except Error as e:
            return jsonify({"error": f"Failed to fetch orders: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

if __name__ == '__main__':
    app.run(debug=True)
