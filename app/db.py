import mysql.connector
import os

def get_connection():
    connection = mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME', 'defaultdb'),
        port=int(os.environ.get('DB_PORT', 19704)),
        ssl_ca=os.environ.get('DB_SSL_CA')
    )
    return connection