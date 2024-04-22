from flask import Flask, request, redirect, jsonify
import hashlib
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
mysql_config = {
    'host': 'prakhardoneria.mysql.pythonanywhere-services.com',
    'user': 'prakhardoneria',
    'password': 'Yash@2021',  # Replace with your MySQL password
    'database': 'prakhardoneria$TGDB',
}

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(**mysql_config)
        print("Connected to MySQL successfully!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_url_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                original_url VARCHAR(200) UNIQUE NOT NULL,
                shortcode VARCHAR(10) UNIQUE NOT NULL
            )
        """)
        connection.commit()
        print("URL table created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def shorten_url(original_url):
    shortcode = hashlib.sha1(original_url.encode()).hexdigest()[:6]
    return shortcode

def get_short_url_from_db(original_url):
    try:
        connection = connect_to_mysql()
        if not connection:
            return None

        cursor = connection.cursor()
        cursor.execute("SELECT shortcode FROM urls WHERE original_url = %s", (original_url,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching short URL from database: {e}")
        return None
    finally:
        if connection:
            connection.close()

def insert_url_into_db(original_url, shortcode):
    try:
        connection = connect_to_mysql()
        if not connection:
            return False

        cursor = connection.cursor()
        cursor.execute("INSERT INTO urls (original_url, shortcode) VALUES (%s, %s)", (original_url, shortcode))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting URL into database: {e}")
        return False
    finally:
        if connection:
            connection.close()

@app.route('/short', methods=['GET'])
def short():
    long_url = request.args.get('long')

    if not long_url:
        return jsonify({'error': 'Missing long URL parameter'}), 400

    if "pythonanywhere" in long_url:
        return jsonify({'error': 'Invalid URL'}), 400

    try:
        short_url = get_short_url_from_db(long_url)
        if short_url:
            return jsonify({'shortened_url': f'{request.host_url}{short_url}'}), 200

        shortcode = shorten_url(long_url)

        if insert_url_into_db(long_url, shortcode):
            return jsonify({'shortened_url': f'{request.host_url}{shortcode}'}), 200
        else:
            return jsonify({'error': 'Failed to create short URL'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def hello_world():
    return 'YAY ITS WORKING'

@app.route('/<shortcode>')
def redirect_to_original(shortcode):
    try:
        connection = connect_to_mysql()
        if not connection:
            return jsonify({'error': 'Failed to connect to the database.'}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE shortcode = %s", (shortcode,))
        result = cursor.fetchone()

        if result:
            original_url = result[0]
            return redirect(original_url)
        else:
            return jsonify({'error': 'Shortcode not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(port=5003)
