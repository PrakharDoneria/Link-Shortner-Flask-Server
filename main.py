from flask import Flask, request, redirect, jsonify
import hashlib
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
mysql_config = {
    'host': '',
    'user': '',
    'password': '',  
    'database': '',
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

@app.route('/short', methods=['POST'])
def short():
    long_url = request.json.get('long')

    if not long_url:
        return jsonify({'error': 'Missing long URL parameter'}), 400

    try:
        connection = connect_to_mysql()
        if not connection:
            return jsonify({'error': 'Failed to connect to the database.'}), 500

        create_url_table(connection)

        shortcode = shorten_url(long_url)

        cursor = connection.cursor()
        cursor.execute("INSERT INTO urls (original_url, shortcode) VALUES (%s, %s)", (long_url, shortcode))
        connection.commit()

        return jsonify({'shortened_url': f'{request.host_url}{shortcode}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()


@app.route('/')
def hello_world():
    return 'Hello Mate!'


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
    app.run(port=5001)