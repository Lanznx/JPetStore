import mysql.connector
from mysql.connector import Error
import time
import sys
import time
import json
import os
import dotenv
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

dotenv.load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

print(f"MYSQL_URL: {MYSQL_URL}")
print(f"MYSQL_USERNAME: {MYSQL_USERNAME}")
print(f"MYSQL_PASSWORD: {MYSQL_PASSWORD}")

def connect_to_database():
    try:
        jdbc_url = MYSQL_URL
        url_to_parse = jdbc_url[5:]
        parsed_url = urlparse(url_to_parse)
        mydb = mysql.connector.connect(
            host=parsed_url.hostname,
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            database="jpetstore",
        )

        mycursor = mydb.cursor()

        mycursor.execute("SHOW TABLES LIKE 'batch'")
        result = mycursor.fetchone()

        if not result:
            create_table_query = """
            CREATE TABLE jpetstore.batch (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content TEXT
            );
            """
            mycursor.execute(create_table_query)
            mydb.commit()
            print("Table 'batch' created successfully.")

        mycursor.close()
        return mydb

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        sys.exit(1)

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def batch_insert_data(data, batch_size=1000):
    conn = connect_to_database()
    cursor = conn.cursor()
    start_time = time.time()
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        cursor.executemany("INSERT INTO batch (content) VALUES (%s)", [(line,) for line in batch])
        conn.commit()
    end_time = time.time()
    cursor.close()
    conn.close()
    return end_time - start_time

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, world!")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        data = json.loads(post_data)
        file_path = data['file_path']
        txt_data = read_text_file(file_path)
        response_time = batch_insert_data(txt_data)
        print(f"Data inserted successfully in {response_time} seconds")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps({'response_time': response_time}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server starting on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()