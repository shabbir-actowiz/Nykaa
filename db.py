
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


def create_table():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
    CREATE TABLE IF NOT EXISTS category_links (
        sub_id INT AUTO_INCREMENT PRIMARY KEY,
        category_name VARCHAR(255),
        main_url TEXT,
        status VARCHAR(50) DEFAULT 'pending'
    )
    """)

            cursor.execute("""
    CREATE TABLE IF NOT EXISTS sub_category_links (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sub_id INT,
        product_url TEXT,
        status VARCHAR(50) DEFAULT 'pending',
        FOREIGN KEY (sub_id) REFERENCES category_links(sub_id)
    )
    """)

            cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_links (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sub_id INT,
        product_url TEXT,
        status VARCHAR(50) DEFAULT 'pending',
        FOREIGN KEY (sub_id) REFERENCES category_links(sub_id)
    )
    """)

            cursor.execute("""
    CREATE TABLE IF NOT EXISTS products_details (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_url TEXT,
        data JSON,
        status VARCHAR(50) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

            conn.commit()

def fetch_category_count():
    query = "SELECT COUNT(*) FROM category_links"
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            count = result[0] if result else 0
    return count

def fetch_sub_category_count():
    query = "SELECT COUNT(*) FROM sub_category_links"
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            count = result[0] if result else 0
    return count

def insert_multiple_category(data_list):
    query = """
    INSERT INTO category_links (category_name, main_url)
    VALUES (%s, %s)
    """

    # Convert list of dicts to list of tuples
    data_tuples = [(item['category_name'], item['main_url']) for item in data_list]

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(query, data_tuples)
            conn.commit()

def get_pending_links():
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"""
                SELECT sub_id, category_name, main_url
                FROM category_links
                WHERE status = 'pending'
                LIMIT {LINK_LIMIT}
                """)

            rows = cursor.fetchall()
            if rows:
                sub_ids = [row['sub_id'] for row in rows]
                placeholders = ','.join(['%s'] * len(sub_ids))
                cursor.execute(f"""
                    UPDATE category_links
                    SET status = 'processing'
                    WHERE sub_id IN ({placeholders})
                """, sub_ids)
                conn.commit()

    return rows

def get_sub_category_links():
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"""
                SELECT scl.id, scl.sub_id, scl.product_url as main_url, cl.category_name 
                FROM sub_category_links scl
                JOIN category_links cl ON scl.sub_id = cl.sub_id
                WHERE scl.status = 'pending'
                LIMIT {LINK_LIMIT}
                """)

            rows = cursor.fetchall()
            if rows:
                ids = [row['id'] for row in rows]
                placeholders = ','.join(['%s'] * len(ids))
                cursor.execute(f"""
                    UPDATE sub_category_links
                    SET status = 'processing'
                    WHERE id IN ({placeholders})
                """, ids)
                conn.commit()
    print(f"Fetched {len(rows)} pending sub-category links.")
    return rows

def update_status_done(sub_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
    UPDATE category_links
    SET status = 'done'
    WHERE sub_id = %s
    """, (sub_id,))

            conn.commit()

def update_status_fail(sub_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
    UPDATE category_links
    SET status = 'fail'
    WHERE sub_id = %s
    """, (sub_id,))

            conn.commit()

def update_sub_category_status_done(sub_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
    UPDATE sub_category_links
    SET status = 'done'
    WHERE sub_id = %s
    """, (sub_id,))

            conn.commit()

def update_sub_category_status_fail(sub_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
    UPDATE sub_category_links
    SET status = 'fail'
    WHERE sub_id = %s
    """, (sub_id,))

            conn.commit()

def insert_sub_category_links(sub_id, product_urls):
    if not product_urls:
        raise Exception("No product URLs found")

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = """
        INSERT INTO sub_category_links (sub_id, product_url)
        VALUES (%s, %s)
        """

            data_list = [(sub_id, url) for url in product_urls]

            cursor.executemany(query, data_list)

            if cursor.rowcount != len(data_list):
                raise Exception("Some rows were not inserted properly")

            conn.commit()



def insert_products_links(sub_id, product_urls):
    if not product_urls:
        raise Exception("No product URLs found")

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = """
        INSERT INTO products_links (sub_id, product_url)
        VALUES (%s, %s)
        """

            data_list = [(sub_id, url) for url in product_urls]

            cursor.executemany(query, data_list)

            if cursor.rowcount != len(data_list):
                raise Exception("Some rows were not inserted properly")

            conn.commit()


def fetch_product_links():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("""
            SELECT id, product_url FROM products_links
            WHERE status = 'pending'
            ORDER BY id ASC
            LIMIT %s
        """, (PRODUCT_LINK_LIMIT,))

                rows = cursor.fetchall()
                if not rows:
                    print("No pending product links found.")
                    return []

                link_ids = [row[0] for row in rows]
                placeholders = ','.join(['%s'] * len(link_ids))
                cursor.execute(f"""
            UPDATE products_links
            SET status = 'processing'
            WHERE id IN ({placeholders})
        """, link_ids)

                conn.commit()
                return rows

            except Exception as e:
                conn.rollback()
                print(f"Database error in fetch_product_links: {e}")
                return []

def insert_product(product_url, data):
    create_table()
    payload = data.model_dump() if hasattr(data, "model_dump") else data

    query = """
    INSERT INTO products_details (product_url, data, status)
    VALUES (%s, %s, 'done')
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (product_url, json.dumps(payload if data else None)))
            conn.commit()

def insert_products_batch(records):
    if not records:
        return
    create_table()
    query = """
    INSERT INTO products_details (product_url, data, status)
    VALUES (%s, %s, 'done')
    """
    data_list = [
        (
            record["product_url"],
            json.dumps(record["data"].model_dump() if hasattr(record["data"], "model_dump") else record["data"] if record["data"] else None),
        )
        for record in records
    ]

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.executemany(query, data_list)
                conn.commit()
            except Exception:
                conn.rollback()
                raise

def update_product_link_status(link_id, status="done"):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
    UPDATE products_links
    SET status = %s
    WHERE id = %s
    """, (status, link_id))

            conn.commit()

def update_product_link_status_batch(link_ids, status="done"):
    if not link_ids:
        return

    query = """
    UPDATE products_links
    SET status = %s
    WHERE id = %s
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.executemany(query, [(status, link_id) for link_id in link_ids])
                conn.commit()
            except Exception:
                conn.rollback()
                raise

