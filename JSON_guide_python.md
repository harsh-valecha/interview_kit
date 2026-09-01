# Working with JSON Files in Python

JSON (JavaScript Object Notation) is a lightweight format for storing and exchanging structured data. Python provides built-in support through the `json` module.

---

## 1. JSON Fundamentals

JSON supports:

| JSON type | Python type |
|---|---|
| Object `{}` | `dict` |
| Array `[]` | `list` |
| String | `str` |
| Number | `int` or `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Example JSON:

```json
{
  "name": "Alice",
  "age": 30,
  "skills": ["Python", "SQL"],
  "active": true
}
```

The equivalent Python object is:

```python
{
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "SQL"],
    "active": True
}
```

Important differences:

- JSON uses lowercase `true`, `false`, and `null`.
- JSON requires double quotes around strings and keys.
- JSON does not support comments.
- JSON keys must be strings.

---

## 2. Import the JSON Module

```python
import json
```

Python provides two main pairs of functions:

- `json.load()` and `json.dump()` work with files.
- `json.loads()` and `json.dumps()` work with strings.

---

## 3. Read a JSON File

Suppose `user.json` contains:

```json
{
  "name": "Alice",
  "age": 30
}
```

Read it with:

```python
import json

with open("user.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data)
print(data["name"])
```

Output:

```text
{'name': 'Alice', 'age': 30}
Alice
```

### Why use `with open()`?

It automatically closes the file, even if an error occurs.

---

## 4. Write Data to a JSON File

```python
import json

user = {
    "name": "Alice",
    "age": 30
}

with open("user.json", "w", encoding="utf-8") as file:
    json.dump(user, file)
```

The file will contain:

```json
{"name": "Alice", "age": 30}
```

### Write Readable, Pretty-Printed JSON

```python
with open("user.json", "w", encoding="utf-8") as file:
    json.dump(user, file, indent=4)
```

Output:

```json
{
    "name": "Alice",
    "age": 30
}
```

Useful options:

```python
json.dump(
    user,
    file,
    indent=4,
    sort_keys=True
)
```

- `indent=4`: formats the JSON neatly.
- `sort_keys=True`: sorts dictionary keys alphabetically.

---

## 5. Convert Between JSON and Python Strings

### Python Object to JSON String

```python
data = {"name": "Alice", "age": 30}

text = json.dumps(data)

print(text)
```

Output:

```text
{"name": "Alice", "age": 30}
```

### JSON String to Python Object

```python
text = '{"name": "Alice", "age": 30}'

data = json.loads(text)

print(data["name"])
```

Use:

- `dump` / `load` for files.
- `dumps` / `loads` for strings.

---

## 6. Access Nested Data

Example:

```json
{
  "user": {
    "name": "Alice",
    "contact": {
      "email": "alice@example.com"
    }
  }
}
```

Python:

```python
email = data["user"]["contact"]["email"]
print(email)
```

### Safer Access with `.get()`

```python
email = data.get("user", {}).get("contact", {}).get("email")
```

This returns `None` instead of raising an error when a key is missing.

You can provide a default value:

```python
name = data.get("name", "Unknown")
```

---

## 7. Work with JSON Arrays

Example:

```json
{
  "users": [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
  ]
}
```

Loop through the array:

```python
for user in data["users"]:
    print(user["name"])
```

Add an item:

```python
data["users"].append({
    "name": "Charlie",
    "age": 28
})
```

Remove an item:

```python
data["users"].pop(0)
```

Find a matching item:

```python
user = next(
    (user for user in data["users"] if user["name"] == "Bob"),
    None
)
```

---

## 8. Update JSON Data

Read, modify, and write the file:

```python
import json

with open("user.json", encoding="utf-8") as file:
    data = json.load(file)

data["age"] = 31
data["city"] = "London"

with open("user.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
```

JSON files do not update automatically when you modify the Python object. You must write the updated object back to the file.

---

## 9. Create a JSON File if It Does Not Exist

```python
from pathlib import Path
import json

path = Path("settings.json")

if not path.exists():
    path.write_text(
        json.dumps({"theme": "dark"}, indent=4),
        encoding="utf-8"
    )
```

For most applications, a normal `open()` call is simpler:

```python
try:
    with open("settings.json", encoding="utf-8") as file:
        settings = json.load(file)
except FileNotFoundError:
    settings = {"theme": "light"}
```

---

## 10. Handle Common Errors

### File Does Not Exist

```python
try:
    with open("data.json", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("The file was not found.")
```

### Invalid JSON

```python
try:
    with open("data.json", encoding="utf-8") as file:
        data = json.load(file)
except json.JSONDecodeError:
    print("The file contains invalid JSON.")
```

### Handle Both Errors

```python
try:
    with open("data.json", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("File not found.")
except json.JSONDecodeError:
    print("Invalid JSON.")
```

Other possible errors include:

- `PermissionError`: insufficient file permissions.
- `TypeError`: trying to serialize an unsupported Python object.
- `KeyError`: accessing a missing dictionary key.
- `IndexError`: accessing an invalid list position.

---

## 11. Check Whether JSON Data Is Valid

```python
import json

def is_valid_json(path):
    try:
        with open(path, encoding="utf-8") as file:
            json.load(file)
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False
```

Usage:

```python
print(is_valid_json("data.json"))
```

For a JSON string:

```python
def is_valid_json_text(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False
```

---

## 12. Validate Required Fields

The JSON syntax may be valid but the data may still be wrong.

```python
required = ["name", "email"]

for field in required:
    if field not in data:
        raise ValueError(f"Missing field: {field}")
```

Check value types:

```python
if not isinstance(data.get("age"), int):
    raise ValueError("Age must be an integer.")
```

For larger applications, consider a validation library such as Pydantic or `jsonschema`.

---

## 13. Handle Non-Serializable Python Objects

Some Python objects cannot be directly converted to JSON:

```python
from datetime import datetime
import json

data = {"created": datetime.now()}

json.dumps(data)  # TypeError
```

Convert the value first:

```python
data["created"] = data["created"].isoformat()

text = json.dumps(data)
```

Common conversions:

```python
from datetime import date

data = {
    "date": date.today().isoformat(),
    "tags": list({"python", "json"})
}
```

JSON can directly represent:

- Dictionaries
- Lists
- Strings
- Integers
- Floats
- Booleans
- `None`

It cannot directly represent:

- Sets
- Dates
- Datetimes
- Custom classes
- File objects
- Database connections

---

## 14. Store Unicode Correctly

Use UTF-8 when reading and writing:

```python
with open("names.json", "w", encoding="utf-8") as file:
    json.dump({"name": "José"}, file, ensure_ascii=False, indent=4)
```

Without `ensure_ascii=False`, non-ASCII characters may be written as escaped Unicode sequences.

---

## 15. Use `pathlib` for File Paths

`pathlib` makes file paths easier to manage:

```python
from pathlib import Path
import json

path = Path("data") / "users.json"

with path.open(encoding="utf-8") as file:
    users = json.load(file)
```

Write JSON:

```python
path.write_text(
    json.dumps(users, indent=4),
    encoding="utf-8"
)
```

Check for existence:

```python
if path.exists():
    print("File exists")
```

---

## 16. Build Reusable JSON Functions

```python
import json

def read_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
```

Usage:

```python
data = read_json("users.json")
data["count"] = len(data["users"])
write_json("users.json", data)
```

A version with error handling:

```python
def read_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default
```

---

## 17. Safely Update a JSON File

If a program stops while writing, the file could become incomplete. A safer approach is to write a temporary file first and then replace the original.

```python
import json
from pathlib import Path

def safe_write_json(path, data):
    path = Path(path)
    temp_path = path.with_suffix(".tmp")

    temp_path.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )

    temp_path.replace(path)
```

Usage:

```python
safe_write_json("settings.json", {"theme": "dark"})
```

This is useful for important configuration or data files.

---

## 18. JSON Lines / NDJSON Files

A regular JSON file usually contains one complete value. A JSON Lines file stores one JSON object per line:

```json
{"id": 1, "name": "Alice"}
{"id": 2, "name": "Bob"}
```

Read it line by line:

```python
import json

with open("users.jsonl", encoding="utf-8") as file:
    for line in file:
        user = json.loads(line)
        print(user["name"])
```

Write JSON Lines:

```python
with open("users.jsonl", "w", encoding="utf-8") as file:
    for user in users:
        file.write(json.dumps(user) + "\n")
```

JSON Lines is useful for:

- Large datasets
- Logs
- Streaming data
- Processing one record at a time

---

## 19. Large JSON Files

`json.load()` reads the entire file into memory:

```python
data = json.load(file)
```

For very large files:

- Prefer JSON Lines when possible.
- Process records incrementally.
- Use a streaming parser such as `ijson` for large standard JSON documents.
- Avoid repeatedly loading and rewriting a huge file.

A JSON array containing millions of objects is less convenient to stream than a JSON Lines file.

---

## 20. Preserve Key Order and Formatting

Python dictionaries preserve insertion order.

```python
data = {
    "zebra": 1,
    "apple": 2
}
```

To sort keys alphabetically when writing:

```python
json.dump(data, file, indent=4, sort_keys=True)
```

Compact output:

```python
json.dump(data, file, separators=(",", ":"))
```

---

## 21. Compare JSON Data

JSON formatting may differ even when the data is the same.

```python
import json

first = '{"name": "Alice", "age": 30}'
second = '{"age": 30, "name": "Alice"}'

same = json.loads(first) == json.loads(second)
print(same)
```

Output:

```text
True
```

Comparing parsed Python objects is better than comparing raw JSON strings.

---

## 22. Command-Line JSON Files

A simple script can accept a file path:

```python
import sys
import json

path = sys.argv[1]

with open(path, encoding="utf-8") as file:
    data = json.load(file)

print(data)
```

Run it:

```bash
python app.py users.json
```

For more advanced command-line tools, use `argparse`.

---

## 23. JSON Security Practices

When working with JSON:

- Use `json.load()` and `json.loads()` for untrusted JSON.
- Do not use `eval()` to parse JSON.
- Do not store passwords or secret keys in plain JSON files.
- Validate data before using it.
- Be cautious when JSON controls file paths, commands, database queries, or permissions.
- Limit the size of JSON received from external sources.

Avoid this:

```python
data = eval(user_input)
```

Use this instead:

```python
data = json.loads(user_input)
```

---

## 24. Common Mistakes

### Using Python syntax instead of JSON

Invalid JSON:

```json
{'name': 'Alice', 'active': True}
```

Valid JSON:

```json
{"name": "Alice", "active": true}
```

### Forgetting to write changes

```python
data["age"] = 31
```

This changes only the in-memory object. Save it:

```python
with open("user.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
```

### Accessing missing keys

Risky:

```python
email = data["email"]
```

Safer:

```python
email = data.get("email")
```

### Opening without an encoding

Prefer:

```python
open("data.json", encoding="utf-8")
```

### Appending multiple complete JSON objects to one file

This is invalid as a normal JSON document:

```text
{"id": 1}{"id": 2}
```

Use a JSON array:

```json
[
  {"id": 1},
  {"id": 2}
]
```

Or use JSON Lines:

```json
{"id": 1}
{"id": 2}
```

---

## 25. Complete Small Example

`tasks.json`:

```json
{
  "tasks": [
    {"title": "Learn JSON", "done": false}
  ]
}
```

Python program:

```python
import json

path = "tasks.json"

with open(path, encoding="utf-8") as file:
    data = json.load(file)

data["tasks"].append({
    "title": "Practice Python",
    "done": False
})

for task in data["tasks"]:
    print(task["title"])

with open(path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
```

This program:

1. Opens a JSON file.
2. Converts it to Python data.
3. Adds a task.
4. Reads values from the data.
5. Saves the modified data.

---

## 26. Recommended Workflow

When working with a JSON file:

1. Decide what structure the JSON should have.
2. Read the file with `json.load()`.
3. Handle missing files and invalid JSON.
4. Validate required fields and value types.
5. Access data using dictionaries and lists.
6. Modify the Python object.
7. Write it back with `json.dump()`.
8. Use `indent=4` for human-readable files.
9. Use UTF-8 encoding.
10. Use JSON Lines or a streaming parser for large datasets.
11. Avoid `eval()` and validate untrusted data.
12. Use temporary-file replacement when safe updates matter.

The core pattern is:

```python
import json

with open("data.json", encoding="utf-8") as file:
    data = json.load(file)

# Read or modify data here

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
```