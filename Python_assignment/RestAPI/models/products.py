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

# Route to insert a new product
@app.route('/products', methods=['POST'])
def add_product():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            data = request.get_json()
            name = data['name']
            price = data['price']
            # Assuming products table has 'name' and 'price' columns
            cur.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
            conn.commit()
            return jsonify({"message": "Product added successfully"}), 201
        except Error as e:
            conn.rollback()
            return jsonify({"error": f"Failed to add product: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to update a product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            data = request.get_json()
            name = data['name']
            price = data['price']
            cur.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (name, price, product_id))
            conn.commit()
            return jsonify({"message": "Product updated successfully"}), 200
        except Error as e:
            conn.rollback()
            return jsonify({"error": f"Failed to update product: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route to select all products
@app.route('/products', methods=['GET'])
def get_products():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()
            return jsonify(products), 200
        except Error as e:
            return jsonify({"error": f"Failed to fetch products: {e}"}), 400
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

if __name__ == '__main__':
    app.run(debug=True)
