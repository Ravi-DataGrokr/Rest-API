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

# Route to insert a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            data = request.get_json()
            name = data['name']
            email = data['email']
            address = data['address']
            phone = data['phone']
            # Inserting into customers table with additional columns: address and phone
            cur.execute("INSERT INTO customers (name, email, address, phone) VALUES (%s, %s, %s, %s)", (name, email, address, phone))
            conn.commit()
            return jsonify({"message": "Customer added successfully"}), 201
        except Error as e:
            conn.rollback()
            return jsonify({"error": f"Failed to add customer: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to update a customer
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            data = request.get_json()
            name = data['name']
            email = data['email']
            address = data['address']
            phone = data['phone']
            cur.execute("UPDATE customers SET name = %s, email = %s, address = %s, phone = %s WHERE id = %s", (name, email, address, phone, customer_id))
            conn.commit()
            return jsonify({"message": "Customer updated successfully"}), 200
        except Error as e:
            conn.rollback()
            return jsonify({"error": f"Failed to update customer: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to select all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM customers")
            customers = cur.fetchall()
            return jsonify(customers), 200
        except Error as e:
            return jsonify({"error": f"Failed to fetch customers: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

if __name__ == '__main__':
    app.run(debug=True)
