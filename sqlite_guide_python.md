# End-to-End Guide: Working with SQLite Files in Python

SQLite is a lightweight, file-based relational database. A complete database is usually stored in a single file such as `app.db` or `data.sqlite`.

Python includes SQLite support through the built-in `sqlite3` module, so no installation is required.

## 1. When to Use SQLite

SQLite is a good choice when you need:

- A local database for a script or desktop application
- A prototype or small-to-medium application
- Structured data with SQL queries
- Transactions and constraints
- A database that is easy to copy and back up
- No separate database server

SQLite may not be ideal when you need:

- Many simultaneous writers
- Multiple servers accessing the same database
- Advanced user permissions
- Very high write throughput

---

## 2. Create or Open a SQLite File

```python
import sqlite3

connection = sqlite3.connect("app.db")
connection.close()
```

If `app.db` does not exist, SQLite creates it.

You can also use an in-memory database:

```python
connection = sqlite3.connect(":memory:")
```

An in-memory database disappears when the connection closes.

A context manager automatically commits successful work and rolls back if an exception occurs:

```python
import sqlite3

with sqlite3.connect("app.db") as connection:
    connection.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER)")
```

---

## 3. Create a Table

```python
import sqlite3

with sqlite3.connect("app.db") as connection:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
```

Common SQLite types:

- `INTEGER`
- `REAL`
- `TEXT`
- `BLOB`
- `NULL`

SQLite uses flexible typing, but declaring appropriate types improves readability and consistency.

### Common Constraints

```sql
PRIMARY KEY
NOT NULL
UNIQUE
DEFAULT
CHECK
FOREIGN KEY
```

Example:

```python
connection.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL CHECK(price >= 0),
        category TEXT DEFAULT 'General'
    )
""")
```

---

## 4. Understand Primary Keys

The usual SQLite primary key is:

```sql
id INTEGER PRIMARY KEY
```

SQLite automatically assigns an integer ID when you omit it:

```python
connection.execute(
    "INSERT INTO users (name, email) VALUES (?, ?)",
    ("Alice", "alice@example.com")
)
```

Retrieve the generated ID:

```python
user_id = connection.execute(
    "SELECT last_insert_rowid()"
).fetchone()[0]
```

You can also use:

```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
```

`AUTOINCREMENT` is usually unnecessary. Use `INTEGER PRIMARY KEY` unless you specifically need stricter ID behavior.

---

## 5. Insert Data

Always use parameters instead of building SQL strings manually.

```python
connection.execute(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    ("Alice", "alice@example.com", 30)
)
```

Never do this:

```python
# Unsafe
name = "Alice"
connection.execute(f"INSERT INTO users (name) VALUES ('{name}')")
```

Parameters protect against SQL injection and correctly handle special characters.

### Insert Multiple Rows

```python
users = [
    ("Alice", "alice@example.com", 30),
    ("Bob", "bob@example.com", 25),
]

connection.executemany(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    users
)
```

---

## 6. Commit Transactions

Changes are normally saved when you commit:

```python
connection.commit()
```

A transaction groups several operations together:

```python
with sqlite3.connect("app.db") as connection:
    connection.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Alice", "alice@example.com")
    )

    connection.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Bob", "bob@example.com")
    )
```

If an error occurs inside the `with` block, the transaction is rolled back.

Manual rollback:

```python
try:
    connection.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    connection.commit()
except sqlite3.Error:
    connection.rollback()
```

---

## 7. Query Data

### Fetch One Row

```python
cursor = connection.execute(
    "SELECT * FROM users WHERE id = ?",
    (1,)
)

user = cursor.fetchone()
print(user)
```

A normal row is returned as a tuple:

```python
(1, "Alice", "alice@example.com", 30, "2026-09-01 12:00:00")
```

### Fetch All Rows

```python
rows = connection.execute(
    "SELECT * FROM users ORDER BY name"
).fetchall()

for row in rows:
    print(row)
```

### Fetch a Limited Number of Rows

```python
rows = connection.execute(
    "SELECT * FROM users LIMIT ?",
    (10,)
).fetchall()
```

### Iterate Directly

```python
for row in connection.execute("SELECT name, email FROM users"):
    print(row)
```

---

## 8. Use Named Columns with `Row`

Tuples work, but named access is easier to read:

```python
import sqlite3

connection = sqlite3.connect("app.db")
connection.row_factory = sqlite3.Row

user = connection.execute(
    "SELECT * FROM users WHERE id = ?",
    (1,)
).fetchone()

print(user["name"])
print(user["email"])
```

You can also convert a row to a dictionary:

```python
user_data = dict(user)
```

Set `row_factory` immediately after creating the connection.

---

## 9. Select Specific Columns

Prefer selecting only the columns you need:

```python
rows = connection.execute("""
    SELECT id, name, email
    FROM users
    WHERE age >= ?
    ORDER BY name
""", (18,)).fetchall()
```

Avoid using `SELECT *` in application code when you know the required columns.

---

## 10. Filter and Search Data

```python
users = connection.execute(
    "SELECT * FROM users WHERE age BETWEEN ? AND ?",
    (18, 40)
).fetchall()
```

Search text:

```python
users = connection.execute(
    "SELECT * FROM users WHERE name LIKE ?",
    ("%ali%",)
).fetchall()
```

Case-insensitive search:

```python
users = connection.execute(
    "SELECT * FROM users WHERE LOWER(name) = LOWER(?)",
    ("alice",)
).fetchall()
```

Check for missing values:

```sql
WHERE age IS NULL
```

Do not use:

```sql
WHERE age = NULL
```

---

## 11. Update Data

```python
connection.execute(
    "UPDATE users SET age = ? WHERE id = ?",
    (31, 1)
)
connection.commit()
```

Check how many rows changed:

```python
cursor = connection.execute(
    "UPDATE users SET age = ? WHERE id = ?",
    (31, 1)
)

print(cursor.rowcount)
```

Update multiple columns:

```python
connection.execute("""
    UPDATE users
    SET name = ?, email = ?, age = ?
    WHERE id = ?
""", ("Alicia", "alicia@example.com", 31, 1))
```

Always include a `WHERE` clause unless you intentionally want to update every row.

---

## 12. Delete Data

```python
connection.execute(
    "DELETE FROM users WHERE id = ?",
    (1,)
)
connection.commit()
```

Delete all rows while keeping the table:

```python
connection.execute("DELETE FROM users")
connection.commit()
```

Delete the table itself:

```python
connection.execute("DROP TABLE IF EXISTS users")
connection.commit()
```

Be especially careful with `DELETE` and `DROP`.

---

## 13. Handle Errors

SQLite exceptions inherit from `sqlite3.Error`.

```python
import sqlite3

try:
    with sqlite3.connect("app.db") as connection:
        connection.execute(
            "INSERT INTO users (email) VALUES (?)",
            ("alice@example.com",)
        )
except sqlite3.IntegrityError:
    print("The email may already exist.")
except sqlite3.Error as error:
    print(f"Database error: {error}")
```

Useful exception types include:

- `sqlite3.IntegrityError` — constraint violation
- `sqlite3.OperationalError` — invalid SQL, missing table, locked database
- `sqlite3.ProgrammingError` — incorrect API usage
- `sqlite3.DatabaseError` — broader database-related error

---

## 14. Work with Foreign Keys

SQLite foreign-key enforcement should be enabled for each connection:

```python
connection.execute("PRAGMA foreign_keys = ON")
```

Create related tables:

```python
connection.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
```

Now an order must reference an existing user.

### Cascading Deletes

```sql
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE
```

If the user is deleted, related orders are deleted automatically.

---

## 15. Join Related Tables

```python
rows = connection.execute("""
    SELECT users.name, orders.total
    FROM users
    JOIN orders ON orders.user_id = users.id
    WHERE users.id = ?
""", (1,)).fetchall()
```

Common joins:

- `INNER JOIN` — only matching records
- `LEFT JOIN` — all records from the left table
- `CROSS JOIN` — every combination

---

## 16. Aggregate Data

Count rows:

```python
count = connection.execute(
    "SELECT COUNT(*) FROM users"
).fetchone()[0]
```

Calculate totals:

```python
summary = connection.execute("""
    SELECT
        COUNT(*) AS order_count,
        SUM(total) AS total_sales,
        AVG(total) AS average_order
    FROM orders
""").fetchone()
```

Group results:

```python
rows = connection.execute("""
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 1
""").fetchall()
```

---

## 17. Add Indexes

Indexes speed up searches on frequently queried columns:

```python
connection.execute("""
    CREATE INDEX IF NOT EXISTS idx_users_email
    ON users(email)
""")
```

Good candidates include:

- Columns used in `WHERE`
- Columns used in `JOIN`
- Columns used in `ORDER BY`
- Foreign-key columns

Indexes use disk space and slow down writes slightly, so do not index every column.

Inspect a query:

```python
plan = connection.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = ?",
    ("alice@example.com",)
).fetchall()

print(plan)
```

---

## 18. Use a Database Helper Function

A helper function keeps connection code consistent:

```python
import sqlite3

def get_connection():
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
```

Usage:

```python
with get_connection() as connection:
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (1,)
    ).fetchone()
```

For a larger project, keep database code in a separate module such as:

```text
project/
├── app.py
├── database.py
└── app.db
```

---

## 19. Build Small CRUD Functions

```python
def create_user(name, email, age):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (name, email, age)
        )
        return cursor.lastrowid
```

```python
def get_user(user_id):
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
```

```python
def update_user(user_id, name, age):
    with get_connection() as connection:
        connection.execute(
            "UPDATE users SET name = ?, age = ? WHERE id = ?",
            (name, age, user_id)
        )
```

```python
def delete_user(user_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
```

---

## 20. Store Python Values

SQLite directly supports common Python values:

| Python value | SQLite value |
|---|---|
| `None` | `NULL` |
| `int` | `INTEGER` |
| `float` | `REAL` |
| `str` | `TEXT` |
| `bytes` | `BLOB` |

### Store JSON

Convert dictionaries to JSON text:

```python
import json

settings = {"theme": "dark", "notifications": True}

connection.execute(
    "INSERT INTO profiles (settings) VALUES (?)",
    (json.dumps(settings),)
)
```

Read it back:

```python
settings = json.loads(row["settings"])
```

### Store Dates and Times

A simple option is ISO-formatted text:

```python
from datetime import datetime

created_at = datetime.now().isoformat()
```

Read it back:

```python
from datetime import datetime

created = datetime.fromisoformat(row["created_at"])
```

For many applications, storing UTC timestamps is preferable.

---

## 21. Store Files as BLOBs

A BLOB stores binary data such as an image or PDF.

```python
with open("photo.jpg", "rb") as file:
    image_data = file.read()

connection.execute(
    "INSERT INTO photos (name, data) VALUES (?, ?)",
    ("photo.jpg", image_data)
)
```

Write it back:

```python
with open("restored.jpg", "wb") as file:
    file.write(row["data"])
```

Store large files outside SQLite when they become numerous or large, and store only their file paths in the database.

---

## 22. Import CSV Data

```python
import csv

with get_connection() as connection:
    with open("users.csv", newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)

        connection.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            [(row["name"], row["email"], int(row["age"])) for row in rows]
        )
```

For large imports, use one transaction rather than committing each row individually.

---

## 23. Export Query Results to CSV

```python
import csv

with get_connection() as connection:
    rows = connection.execute(
        "SELECT id, name, email FROM users"
    ).fetchall()

with open("users-export.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "email"])
    writer.writerows(rows)
```

---

## 24. Use SQLite from the Command Line

If SQLite is installed, open a database file:

```bash
sqlite3 app.db
```

Useful commands:

```sql
.tables
.schema users
.headers on
.mode column
SELECT * FROM users;
.quit
```

These commands are SQLite shell commands, not Python commands.

---

## 25. Inspect Database Metadata

List tables:

```python
tables = connection.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""").fetchall()
```

Inspect table columns:

```python
columns = connection.execute(
    "PRAGMA table_info(users)"
).fetchall()
```

Check foreign keys:

```python
foreign_keys = connection.execute(
    "PRAGMA foreign_key_list(orders)"
).fetchall()
```

---

## 26. Back Up a SQLite Database

### Using Python

```python
import sqlite3

source = sqlite3.connect("app.db")
backup = sqlite3.connect("app-backup.db")

with backup:
    source.backup(backup)

source.close()
backup.close()
```

### Using SQL

```python
with get_connection() as connection:
    connection.execute("VACUUM INTO 'app-backup.db'")
```

Do not copy a database file while it is actively being written unless you use SQLite’s backup mechanisms or another safe backup strategy.

---

## 27. Improve Performance

Useful techniques:

### Use transactions

```python
with connection:
    connection.executemany(
        "INSERT INTO users (name) VALUES (?)",
        [("Alice",), ("Bob",)]
    )
```

### Avoid repeated connections in tight loops

Open one connection for a batch of work.

### Add appropriate indexes

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Select only required columns

```sql
SELECT name, email FROM users;
```

### Use query plans

```sql
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = ?;
```

### Consider WAL mode

Write-Ahead Logging can improve read/write concurrency:

```python
connection.execute("PRAGMA journal_mode = WAL")
```

WAL creates additional files beside the database, so include them in your operational and backup planning.

---

## 28. Handle Database Locking

SQLite allows many readers but has more limited write concurrency.

Set a timeout:

```python
connection = sqlite3.connect("app.db", timeout=10)
```

A busy timeout can also be configured:

```python
connection.execute("PRAGMA busy_timeout = 10000")
```

Good practices:

- Keep transactions short
- Do not leave connections open unnecessarily
- Avoid long-running write operations
- Use WAL mode for suitable applications
- Use a server database if many processes write heavily

---

## 29. Manage Schema Changes

SQLite does not have a built-in migration framework in Python. Use a version table:

```python
connection.execute("""
    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER NOT NULL
    )
""")
```

A simple migration:

```python
version = connection.execute(
    "SELECT version FROM schema_version"
).fetchone()

if version is None:
    connection.execute("INSERT INTO schema_version VALUES (1)")
```

For real applications, consider a migration tool such as Alembic or a small custom migration system.

Keep schema changes in numbered files:

```text
migrations/
├── 001_create_users.sql
├── 002_create_orders.sql
└── 003_add_user_status.sql
```

---

## 30. Test Database Code

Use an in-memory database for fast tests:

```python
import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
""")
```

Basic test:

```python
connection.execute(
    "INSERT INTO users (name) VALUES (?)",
    ("Alice",)
)

user = connection.execute(
    "SELECT name FROM users"
).fetchone()

assert user[0] == "Alice"
```

Test important cases:

- Valid inserts
- Duplicate unique values
- Missing required values
- Updates
- Deletes
- Foreign-key failures
- Empty query results
- Transaction rollback

---

## 31. Common Mistakes

### Forgetting to commit

```python
connection.commit()
```

Use a `with connection:` block where possible.

### Building SQL with f-strings

Use parameters:

```python
connection.execute(
    "SELECT * FROM users WHERE name = ?",
    (name,)
)
```

### Forgetting the comma for one parameter

Correct:

```python
(name,)
```

Incorrect:

```python
(name)
```

### Forgetting foreign-key enforcement

```python
connection.execute("PRAGMA foreign_keys = ON")
```

### Using `NULL` incorrectly

Correct:

```sql
WHERE age IS NULL
```

### Updating or deleting every row accidentally

Always check the `WHERE` clause.

### Opening too many connections

Use a helper and close connections promptly.

### Treating SQLite as a multi-server database

For large, highly concurrent systems, use PostgreSQL, MySQL, or another server-based database.

---

## 32. A Small Complete Example

```python
import sqlite3

DATABASE = "app.db"

def connect():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)

def add_task(title):
    with connect() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        return cursor.lastrowid

def list_tasks():
    with connect() as connection:
        return connection.execute("""
            SELECT id, title, completed
            FROM tasks
            ORDER BY id
        """).fetchall()

def complete_task(task_id):
    with connect() as connection:
        connection.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?",
            (task_id,)
        )

initialize()

task_id = add_task("Learn SQLite")
complete_task(task_id)

for task in list_tasks():
    print(dict(task))
```

---

## 33. Recommended Project Pattern

For a small application:

```text
project/
├── main.py
├── database.py
├── migrations/
│   └── 001_initial.sql
├── tests/
│   └── test_database.py
└── data/
    └── app.db
```

Practical guidelines:

Keep SQL near the database functions that use it
Use parameterized queries everywhere
Enable foreign keys on every connection
Use transactions for related changes
Add indexes based on real query patterns
Back up important database files
Test database operations independently
Store sensitive configuration outside the database when possible
Move to a server database when concurrency and scale require it
Quick Reference
```
python


import sqlite3

connection = sqlite3.connect("app.db")
connection.row_factory = sqlite3.Row

connection.execute("PRAGMA foreign_keys = ON")

connection.execute(
    "INSERT INTO users (name) VALUES (?)",
    ("Alice",)
)

rows = connection.execute(
    "SELECT * FROM users WHERE name = ?",
    ("Alice",)
).fetchall()

connection.execute(
    "UPDATE users SET name = ? WHERE id = ?",
    ("Alicia", 1)
)

connection.execute(
    "DELETE FROM users WHERE id = ?",
    (1,)
)

connection.commit()
connection.close()
```

The core workflow is:

1. Connect to the SQLite file.
2. Create or migrate the schema.
3. Use parameterized SQL.
4. Insert, query, update, and delete data.
5. Commit transactions 
6. Handle errors
7. Close connections 
8. Backup and test the database