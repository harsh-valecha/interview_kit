# End-to-End Guide: Working with MySQL Databases in Python

This guide covers the complete workflow: installing MySQL, connecting from Python, creating tables, performing CRUD operations, using transactions, working with relationships, and building a clean database layer.

## 1. What You Need

You need:

- A running MySQL server
- A MySQL database and user
- Python 3
- A Python MySQL driver

Install the official MySQL Connector:

```bash
pip install mysql-connector-python
```

For larger applications, also consider SQLAlchemy:

```bash
pip install sqlalchemy
```

## 2. Basic Database Concepts

A MySQL database contains:

- **Databases**: Containers for tables
- **Tables**: Store structured data
- **Rows**: Individual records
- **Columns**: Fields in a record
- **Primary keys**: Uniquely identify rows
- **Foreign keys**: Link tables together
- **Indexes**: Improve search performance
- **Transactions**: Group multiple operations into one unit

Example table:

| id | name | email |
|---:|---|---|
| 1 | Alice | alice@example.com |
| 2 | Bob | bob@example.com |

## 3. Start MySQL

After installing MySQL, connect using the MySQL command-line client:

```bash
mysql -u root -p
```

Create a database:

```sql
CREATE DATABASE shop;
```

Select it:

```sql
USE shop;
```

Create a separate application user:

```sql
CREATE USER 'shop_user'@'localhost'
IDENTIFIED BY 'strong_password';

GRANT ALL PRIVILEGES ON shop.* TO 'shop_user'@'localhost';
```

Avoid using the `root` account in applications.

## 4. Connect Python to MySQL

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="shop_user",
    password="strong_password",
    database="shop",
    port=3306
)

print(connection.is_connected())
```

Close the connection when finished:

```python
connection.close()
```

A connection represents communication between your Python program and MySQL.

## 5. Use Configuration Variables

Do not hard-code passwords in your source code.

Create a `.env` file:

```text
DB_HOST=localhost
DB_USER=shop_user
DB_PASSWORD=strong_password
DB_NAME=shop
```

Install `python-dotenv`:

```bash
pip install python-dotenv
```

Load the values:

```python
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
```

Add `.env` to `.gitignore`:

```text
.env
```

## 6. Create Tables

Create a cursor to execute SQL:

```python
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

connection.commit()
cursor.close()
connection.close()
```

### Common MySQL Data Types

- `INT`: Whole numbers
- `DECIMAL(10, 2)`: Accurate monetary values
- `VARCHAR(255)`: Short text
- `TEXT`: Long text
- `BOOLEAN`: True or false
- `DATE`: Calendar date
- `DATETIME`: Date and time
- `TIMESTAMP`: Date and time, commonly used for record timestamps

## 7. Insert Data

Always use parameterized queries:

```python
cursor = connection.cursor()

sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
values = ("Alice", "alice@example.com")

cursor.execute(sql, values)
connection.commit()

print(cursor.lastrowid)
```

Do not build SQL using string concatenation:

```python
# Avoid this
name = "Alice"
cursor.execute(f"INSERT INTO users (name) VALUES ('{name}')")
```

Parameterized queries help prevent SQL injection and correctly handle special characters.

### Insert Multiple Rows

```python
users = [
    ("Alice", "alice@example.com"),
    ("Bob", "bob@example.com")
]

cursor.executemany(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    users
)

connection.commit()
```

## 8. Read Data

### Fetch One Row

```python
cursor.execute(
    "SELECT id, name, email FROM users WHERE id = %s",
    (1,)
)

user = cursor.fetchone()
print(user)
```

The comma in `(1,)` makes it a Python tuple.

### Fetch All Rows

```python
cursor.execute("SELECT id, name, email FROM users")

users = cursor.fetchall()

for user in users:
    print(user)
```

### Fetch Rows as Dictionaries

```python
cursor = connection.cursor(dictionary=True)

cursor.execute("SELECT * FROM users")

for user in cursor.fetchall():
    print(user["name"], user["email"])
```

Example result:

```python
{
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}
```

### Filter and Sort Results

```python
cursor.execute("""
    SELECT id, name, email
    FROM users
    WHERE name LIKE %s
    ORDER BY name
""", ("%Ali%",))
```

### Limit Results

```python
cursor.execute("""
    SELECT *
    FROM users
    ORDER BY id DESC
    LIMIT %s OFFSET %s
""", (10, 0))
```

## 9. Update Data

```python
cursor.execute(
    "UPDATE users SET name = %s WHERE id = %s",
    ("Alice Smith", 1)
)

connection.commit()

print(cursor.rowcount)
```

Always include a `WHERE` clause unless you intentionally want to update every row.

## 10. Delete Data

```python
cursor.execute(
    "DELETE FROM users WHERE id = %s",
    (1,)
)

connection.commit()
```

Check how many rows were deleted:

```python
print(cursor.rowcount)
```

Be especially careful with:

```sql
DELETE FROM users;
```

This deletes every row in the table.

## 11. Handle Errors

Use `try`, `except`, and `finally`:

```python
import mysql.connector

connection = None
cursor = None

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="shop_user",
        password="strong_password",
        database="shop"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    print(cursor.fetchone())

except mysql.connector.Error as error:
    print("Database error:", error)

finally:
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
```

## 12. Transactions

A transaction groups multiple operations together.

For example, transferring money should update two accounts as one operation:

```python
try:
    cursor.execute(
        "UPDATE accounts SET balance = balance - %s WHERE id = %s",
        (100, 1)
    )

    cursor.execute(
        "UPDATE accounts SET balance = balance + %s WHERE id = %s",
        (100, 2)
    )

    connection.commit()

except Exception:
    connection.rollback()
    raise
```

Important methods:

```python
connection.commit()    # Save changes
connection.rollback()  # Undo uncommitted changes
```

`SELECT` queries generally do not require `commit()`, but `INSERT`, `UPDATE`, and `DELETE` do.

## 13. Build Reusable Database Functions

Instead of repeating connection code, create a database module.

```python
# database.py
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
```

Use it elsewhere:

```python
from database import get_connection

def get_user(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()
```

## 14. Create a Simple Repository Layer

A repository keeps SQL code organized.

```python
class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    def create(self, name, email):
        cursor = self.connection.cursor()

        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email)
        )

        self.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()

        return user_id

    def find_by_id(self, user_id):
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )

        result = cursor.fetchone()
        cursor.close()

        return result
```

Usage:

```python
connection = get_connection()
users = UserRepository(connection)

user_id = users.create("Alice", "alice@example.com")
print(users.find_by_id(user_id))

connection.close()
```

## 15. Relationships Between Tables

Create a products table:

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

Create an orders table:

```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
);
```

The `user_id` column connects each order to a user.

### One-to-Many Relationship

One user can have many orders:

```sql
SELECT
    users.name,
    orders.id,
    orders.order_date
FROM users
JOIN orders ON orders.user_id = users.id
WHERE users.id = %s;
```

Run it from Python:

```python
cursor.execute(sql, (user_id,))
orders = cursor.fetchall()
```

### Many-to-Many Relationship

Orders can contain many products, and products can appear in many orders. Use a linking table:

```sql
CREATE TABLE order_items (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,

    PRIMARY KEY (order_id, product_id),

    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## 16. Useful SQL Queries

### Count Rows

```sql
SELECT COUNT(*) FROM users;
```

### Aggregate Values

```sql
SELECT SUM(price), AVG(price), MAX(price)
FROM products;
```

### Group Results

```sql
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id;
```

### Search Text

```sql
SELECT *
FROM products
WHERE name LIKE %s;
```

Python parameter:

```python
("%phone%",)
```

### Check for Existing Data

```sql
SELECT EXISTS(
    SELECT 1 FROM users WHERE email = %s
);
```

## 17. Indexes

Indexes make searches faster.

```sql
CREATE INDEX idx_users_email
ON users(email);
```

You may want indexes on:

- Foreign key columns
- Columns frequently used in `WHERE`
- Columns frequently used in `JOIN`
- Columns frequently used in `ORDER BY`

Avoid adding indexes to every column. Indexes use storage and can slow down inserts and updates.

Inspect a query:

```sql
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';
```

## 18. Prevent SQL Injection

Use placeholders for values:

```python
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)
)
```

Do not insert user input directly into SQL:

```python
# Unsafe
query = "SELECT * FROM users WHERE email = '" + email + "'"
```

Column names cannot normally be passed as parameters. If you need dynamic sorting, use an allowlist:

```python
allowed_columns = {"name", "created_at"}
sort_column = "name"

if sort_column not in allowed_columns:
    raise ValueError("Invalid sort column")

cursor.execute(f"SELECT * FROM users ORDER BY {sort_column}")
```

## 19. Connection Pooling

Creating a new connection for every request can be inefficient. A connection pool reuses connections.

```python
from mysql.connector import pooling

pool = pooling.MySQLConnectionPool(
    pool_name="shop_pool",
    pool_size=5,
    host="localhost",
    user="shop_user",
    password="strong_password",
    database="shop"
)

connection = pool.get_connection()

try:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
finally:
    cursor.close()
    connection.close()
```

Returning the connection with `close()` makes it available to the pool again.

## 20. Using SQLAlchemy

SQLAlchemy provides a higher-level database interface and optional ORM support.

Install it:

```bash
pip install sqlalchemy pymysql
```

Create an engine:

```python
from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://shop_user:strong_password@localhost/shop"
)
```

Run a query:

```python
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM users"))

    for row in result:
        print(row.name, row.email)
```

Insert data:

```python
with engine.begin() as connection:
    connection.execute(
        text("INSERT INTO users (name, email) VALUES (:name, :email)"),
        {"name": "Alice", "email": "alice@example.com"}
    )
```

SQLAlchemy uses named parameters such as `:name`.

## 21. SQLAlchemy ORM Basics

Define a model:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

Create tables:

```python
Base.metadata.create_all(engine)
```

Add and query objects:

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = User(name="Alice", email="alice@example.com")
    session.add(user)
    session.commit()
```

Query:

```python
from sqlalchemy import select

with Session(engine) as session:
    users = session.scalars(select(User)).all()

    for user in users:
        print(user.name)
```

Use raw SQL when you need precise SQL control. Use the ORM when your application has many related models and objects.

## 22. Database Migrations

Avoid manually changing production tables with ad hoc SQL. Use migrations to track schema changes.

A common tool is Alembic:

```bash
pip install alembic
alembic init migrations
```

Typical migration workflow:

```bash
alembic revision --autogenerate -m "add users table"
alembic upgrade head
```

Migrations allow you to:

- Reproduce the database schema
- Safely deploy schema changes
- Roll changes forward or backward
- Keep development and production databases consistent

## 23. Testing Database Code

Tests should use a separate test database.

Basic test idea:

```python
def test_create_user(repository):
    user_id = repository.create(
        "Test User",
        "test@example.com"
    )

    user = repository.find_by_id(user_id)

    assert user["name"] == "Test User"
```

Good testing practices:

- Never run tests against production
- Use temporary test data
- Clean up after each test
- Test invalid input
- Test duplicate emails
- Test transaction failures
- Test missing records

## 24. Performance Tips

- Select only the columns you need:

```sql
SELECT id, name FROM users;
```

- Use `LIMIT` for large result sets.
- Add indexes based on actual query patterns.
- Avoid queries inside loops when one `JOIN` can do the work.
- Use bulk inserts with `executemany()`.
- Use connection pooling in web applications.
- Use pagination for large lists.
- Use `EXPLAIN` to inspect slow queries.
- Keep transactions short.
- Avoid loading millions of rows into memory at once.

## 25. Common Errors

### Access Denied

```text
Access denied for user
```

Check:

- Username
- Password
- Host
- Database permissions
- Whether MySQL is running

### Unknown Database

```text
Unknown database
```

Create the database or correct the database name:

```sql
CREATE DATABASE shop;
```

### Duplicate Entry

This usually means a `UNIQUE` or primary key constraint was violated.

```sql
SELECT * FROM users WHERE email = %s;
```

Check for existing data before inserting, or handle the exception.

### Table Does Not Exist

Check the selected database:

```sql
SELECT DATABASE();
SHOW TABLES;
```

### Forgotten Commit

If inserted or updated data disappears, call:

```python
connection.commit()
```

## 26. Recommended Project Structure

```text
my_project/
├── app.py
├── database.py
├── models/
│   └── user.py
├── repositories/
│   └── user_repository.py
├── services/
│   └── user_service.py
├── migrations/
├── tests/
├── .env
├── .gitignore
└── requirements.txt
```

Save dependencies:

```bash
pip freeze > requirements.txt
```

Install them later:

```bash
pip install -r requirements.txt
```

## 27. A Small Complete Example

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="shop_user",
    password="strong_password",
    database="shop"
)

cursor = connection.cursor(dictionary=True)

try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            body TEXT NOT NULL
        )
    """)

    cursor.execute(
        "INSERT INTO notes (body) VALUES (%s)",
        ("Learn MySQL with Python",)
    )

    connection.commit()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    for note in notes:
        print(note)

finally:
    cursor.close()
    connection.close()
```

## 28. Learning Path

Follow this order:

1. Learn basic SQL: `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
2. Install MySQL and create a database.
3. Connect Python using `mysql-connector-python`.
4. Practice parameterized queries.
5. Learn transactions and error handling.
6. Create related tables with foreign keys.
7. Learn joins, grouping, indexes, and pagination.
8. Organize SQL into repository functions.
9. Add connection pooling.
10. Learn SQLAlchemy for larger applications.
11. Use Alembic for database migrations.
12. Add automated tests.
13. Practice optimizing queries with `EXPLAIN`.

The key workflow is:

```text
Connect
→ Create a cursor
→ Execute parameterized SQL
→ Fetch results or check affected rows
→ Commit or roll back
→ Close the cursor and connection
```

Keep SQL explicit, never concatenate untrusted input into queries, and separate database code from the rest of your application as your project grows.