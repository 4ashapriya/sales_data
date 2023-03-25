import csv
import os
from sqlalchemy import text
from app import app, db


def read_data():
    folder_path = 'dataset'
    with app.app_context():

        session = db.session()
        queries = ['''CREATE TABLE IF NOT EXISTS commissions (
                        date TEXT NOT NULL,
                        vendor_id INTEGER NOT NULL,
                        rate NUMERIC(5,2) NOT NULL
                    );''',

                    '''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER,
                        created_at TIMESTAMP,
                        vendor_id INT,
                        customer_id INT
                    );''',

                    '''CREATE TABLE IF NOT EXISTS products (
                    id TEXT,
                    description VARCHAR(255)
                    );''',

                    '''CREATE TABLE IF NOT EXISTS promotions (
                    id INT,
                    description VARCHAR(255)
                    );''',

                    '''CREATE TABLE IF NOT EXISTS order_lines (
                    id INT,
                    order_id INT,
                    product_id TEXT NOT NULL,
                    product_description VARCHAR(255),
                    product_price DECIMAL(10, 2),
                    product_vat_rate DECIMAL(5, 2),
                    discount_rate DECIMAL(5, 2),
                    quantity INT,
                    full_price_amount DECIMAL(15, 2),
                    discounted_amount DECIMAL(15, 2),
                    vat_amount DECIMAL(15, 2),
                    total_amount DECIMAL(15, 2)
                    );''',

                    '''CREATE TABLE IF NOT EXISTS product_promotions (
                    date DATE,
                    product_id TEXT NOT NULL,
                    promotion_id INT
                    );'''
                  ]
        table_name = ['commissions', 'orders', 'products', 'promotions', 'order_lines', 'product_promotions']
        for table in table_name:
            with open(os.path.join(folder_path, table + '.csv'), encoding='utf', newline='') as csvfile:
                reader = csv.reader(csvfile)
                cols = next(reader)
                for query in queries:
                    session.execute(text(query))
                for row in reader:
                    values = ', '.join([f"'{value}'" for value in row])
                    session.execute(text(f"INSERT INTO {table} VALUES ({values})"))
        session.commit()

        session.close()
    return {"message": "Success",
            "status_code": 200}
