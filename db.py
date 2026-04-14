
import mysql.connector
import json

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "actowiz",
}

DATABASE = "NYKAA"
LINK_LIMIT = 10
PRODUCT_LINK_LIMIT = 50
BATCH_SIZE = 1000 

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_db_connection():
    config = DB_CONFIG.copy()
    config["database"] = DATABASE
    return mysql.connector.connect(**config)


def create_database():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")


def create_tables():
    category_table_sql = """
        CREATE TABLE IF NOT EXISTS category_nodes (
            sub_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(255) NOT NULL,
            category_path VARCHAR(1024) NOT NULL,
            category_url VARCHAR(1024) NULL,
            product_api_url VARCHAR(2048) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) 
    """

    product_link_table_sql = """
        CREATE TABLE IF NOT EXISTS product_links (
            id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            category_source_id BIGINT UNSIGNED NOT NULL,
            product_url VARCHAR(1024) NOT NULL,
            page_number INT NOT NULL,
            status ENUM('pending', 'processing', 'done', 'failed') NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_product_category
                FOREIGN KEY (category_source_id) REFERENCES category_nodes (sub_id)
                ON DELETE CASCADE
        )
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(category_table_sql)
            cursor.execute(product_link_table_sql)

            cursor.execute(
                "ALTER TABLE category_nodes MODIFY COLUMN status ENUM('pending', 'processing', 'done', 'failed') NOT NULL DEFAULT 'pending'"
            )
            cursor.execute(
                "ALTER TABLE product_links MODIFY COLUMN status ENUM('pending', 'processing', 'done', 'failed') NOT NULL DEFAULT 'pending'"
            )
        conn.commit()

def insert_category_link(json_data: dict) -> int:
    categories = json_data['categories']
    count = 0
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            for category in categories:
                cursor.execute(
                    "INSERT INTO category_nodes (category_name, category_path, category_url, product_api_url) VALUES (%s, %s, %s, %s)",
                    (
                        category["category_name"],
                        category["category_path"],
                        category["category_url"],
                        category["product_api_url"]
                    )
                )
                count += 1
            conn.commit()
            return count
def get_pending_category_links():
    con= get_db_connection()
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT sub_id, product_api_url FROM category_nodes WHERE status='pending' LIMIT %s", (LINK_LIMIT,))
    rows=cursor.fetchall()
    cursor.execute("UPDATE category_nodes SET status='processing' WHERE sub_id IN (%s)" % ",".join(str(row['sub_id']) for row in rows))
    con.commit()
    cursor.close()
    return rows

def insert_product_links(category_id, product_links):
    print('*' * 50)
    print(f"Inserting product links for category {category_id}: {len(product_links)} links")
    if has_products_for_category(category_id):
        print(f"Products already exist for category {category_id}. Skipping.")
        return
    with get_db_connection() as conn:
        with conn.cursor() as cursor:

            data_batch = []

            for idx, link in enumerate(product_links):
                data_batch.append((category_id, link, idx + 1))

                if len(data_batch) == BATCH_SIZE:
                    cursor.executemany(
                        "INSERT INTO product_links (category_source_id, product_url, page_number) VALUES (%s, %s, %s)",
                        data_batch
                    )
                    data_batch.clear()  

            
            if data_batch:
                cursor.executemany(
                    "INSERT INTO product_links (category_source_id, product_url, page_number) VALUES (%s, %s, %s)",
                    data_batch
                )

        conn.commit()

def create_schema():
    create_database()
    create_tables()


def has_categories():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM category_nodes")
            count = cursor.fetchone()[0]
            return count > 0


def has_products_for_category(category_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM product_links WHERE category_source_id = %s", (category_id,))
            count = cursor.fetchone()[0]
            return count > 0


def update_category_status(sub_id, status):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE category_nodes SET status = %s WHERE sub_id = %s", (status, sub_id))
        conn.commit()


