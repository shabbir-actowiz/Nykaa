
import mysql.connector
import json

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "actowiz",
}

DATABASE = "NYKAA"
LINK_LIMIT = 10
PRODUCT_LINK_LIMIT = 200

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_db_connection():
    config = DB_CONFIG.copy()
    config["database"] = DATABASE
    return mysql.connector.connect(**config)


def create_database():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")


