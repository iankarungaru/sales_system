import psycopg2

# Function to establish a database connection
def connect_to_database():
    return psycopg2.connect(
        user="postgres",
        dbname="sales_management_system",
        password="mamayogho",
        port=5432,
        host='localhost'
    )

# Function to check if an email exists in the users table
def emailExists(email_to_check):
    conn = connect_to_database()
    curr = conn.cursor()
    select_query = "SELECT COUNT(*) FROM users WHERE email = %s;"
    curr.execute(select_query, (email_to_check,))
    email_count = curr.fetchone()[0]
    curr.close()
    conn.close()
    return email_count > 0

# Function to authenticate a user based on email and password
def authenticate_user(email, password):
    conn = connect_to_database()
    curr = conn.cursor()
    select_query = "SELECT COUNT(*) FROM users WHERE email = %s AND password = %s;"
    curr.execute(select_query, (email, password))
    user_count = curr.fetchone()[0]
    curr.close()
    conn.close()
    return user_count > 0

# Function to insert product data into the database
def insert_products(values):
    conn = connect_to_database()
    curr = conn.cursor()
    insert_query = "INSERT INTO products (name, buying_price, selling_price, quantity_stock) VALUES (%s, %s, %s, %s);"
    curr.execute(insert_query, values)
    conn.commit()
    print("Product inserted successfully.")
    curr.close()
    conn.close()

# Function to insert sales data into the database
def insert_sales(values):
    conn = connect_to_database()
    curr = conn.cursor()
    insert_query = "INSERT INTO sales (product_id, quantity) VALUES (%s, %s);"
    curr.execute(insert_query, values)
    conn.commit()
    print("Sales data inserted successfully.")
    curr.close()
    conn.close()

# Function to fetch data from a specified table
def get_data(table_name):
    conn = connect_to_database()
    curr = conn.cursor()
    select_query = f"SELECT * FROM {table_name};"
    curr.execute(select_query)
    data = curr.fetchall()
    curr.close()
    conn.close()
    return data

# Function to retrieve sales data per product
def sales_product():
    conn = connect_to_database()
    curr = conn.cursor()
    select_query = "SELECT product_id, SUM(quantity) FROM sales GROUP BY product_id;"
    curr.execute(select_query)
    data = curr.fetchall()
    curr.close()
    conn.close()
    return data
def delete_product(product_id):
    conn = connect_to_database()
    curr = conn.cursor()
    delete_query = "DELETE FROM products WHERE id = %s;"
    curr.execute(delete_query, (product_id,))
    conn.commit()
    print("Product deleted successfully.")
    curr.close()
    conn.close()


# Function to retrieve profit data per product
def profit_product():
    conn = connect_to_database()
    curr = conn.cursor()
    select_query = "SELECT product_id, SUM(selling_price - buying_price) FROM sales JOIN products ON sales.product_id = products.id GROUP BY product_id;"
    curr.execute(select_query)
    data = curr.fetchall()
    curr.close()
    conn.close()
    return data

# Function to retrieve daily sales data
def daily_sales():
    conn = connect_to_database()
    curr = conn.cursor()
    select_query = "SELECT DATE_TRUNC('day', created_at), SUM(quantity) FROM sales GROUP BY DATE_TRUNC('day', created_at);"
    curr.execute(select_query)
    data = curr.fetchall()
    curr.close()
    conn.close()
    return data

# Function to retrieve daily profit data
def daily_profit():
    conn = connect_to_database()
    curr = conn.cursor()
    select_query = "SELECT DATE_TRUNC('day', created_at), SUM(selling_price - buying_price) FROM sales JOIN products ON sales.product_id = products.id GROUP BY DATE_TRUNC('day', created_at);"
    curr.execute(select_query)
    data = curr.fetchall()
    curr.close()
    conn.close()
    return data

# Function to register a new user
def register_user(values):
    conn = connect_to_database()
    curr = conn.cursor()
    # Check if the email already exists
    if emailExists(values[1]):
        print("Email already exists.")
        curr.close()
        conn.close()
        return False

    try:
        # Insert the user data into the database
        insert_query = "INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s);"
        curr.execute(insert_query, values)
        conn.commit()
        print("User registered successfully.")
        return True
    except Exception as e:
        print("Error registering user:", e)
        conn.rollback()
        return False
    finally:
        curr.close()
        conn.close()
