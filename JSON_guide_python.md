# Working with JSON Files in Python

JSON (JavaScript Object Notation) is a text format commonly used for configuration files, APIs, data exchange, and storage of structured data.

Python includes the built-in `json` module, so no installation is required.

## 1. JSON Fundamentals

JSON supports these data types:

| JSON | Python |
|---|---|
| Object | `dict` |
| Array | `list` |
| String | `str` |
| Number | `int` or `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Example JSON:

```json
{
  "name": "Ada",
  "age": 36,
  "is_active": true,
  "skills": ["Python", "Math"],
  "address": null
}
```

JSON objects use:

- Double quotes around keys and strings
- Commas between items
- Curly braces for objects
- Square brackets for arrays
- No trailing commas

Invalid JSON:

```json
{
  "name": "Ada",
}
```

The trailing comma makes it invalid.

---

## 2. Import the JSON Module

```python
import json
```

The two most important pairs of functions are:

```python
json.load()   # Read JSON from a file
json.dump()   # Write JSON to a file

json.loads()  # Read JSON from a string
json.dumps()  # Convert Python data to a JSON string
```

The `s` means “string.”

---

## 3. Reading a JSON File

Suppose `user.json` contains:

```json
{
  "name": "Ada",
  "age": 36,
  "skills": ["Python", "Mathematics"]
}
```

Read it with `json.load()`:

```python
import json

with open("user.json", "r", encoding="utf-8") as file:
    user = json.load(file)

print(user)
print(user["name"])
print(user["skills"])
```

Output:

```text
{'name': 'Ada', 'age': 36, 'skills': ['Python', 'Mathematics']}
Ada
['Python', 'Mathematics']
```

### Why use `with open()`?

The `with` statement automatically closes the file, even if an error occurs.

The following is generally preferred:

```python
with open("data.json", encoding="utf-8") as file:
    data = json.load(file)
```

Rather than:

```python
file = open("data.json")
data = json.load(file)
file.close()
```

---

## 4. Accessing JSON Data

After loading JSON, you work with normal Python dictionaries and lists.

```python
data = {
    "user": {
        "name": "Ada",
        "roles": ["admin", "editor"]
    }
}

print(data["user"]["name"])
print(data["user"]["roles"][0])
```

Output:

```text
Ada
admin
```

### Avoiding missing-key errors

Using square brackets raises `KeyError` if the key does not exist:

```python
name = data["username"]  # KeyError
```

Use `.get()` when a key may be missing:

```python
name = data.get("username")
print(name)  # None
```

You can provide a default:

```python
name = data.get("username", "Unknown")
```

For nested data:

```python
user = data.get("user", {})
name = user.get("name", "Unknown")
```

---

## 5. Reading Arrays of Objects

A common JSON structure is a list of records:

```json
[
  {
    "id": 1,
    "name": "Ada",
    "active": true
  },
  {
    "id": 2,
    "name": "Grace",
    "active": false
  }
]
```

Python:

```python
import json

with open("users.json", encoding="utf-8") as file:
    users = json.load(file)

for user in users:
    print(user["id"], user["name"])
```

Filter records:

```python
active_users = [
    user for user in users
    if user.get("active") is True
]

print(active_users)
```

Find one record:

```python
user = next(
    (user for user in users if user.get("id") == 2),
    None
)

print(user)
```

---

## 6. Writing JSON to a File

Use `json.dump()` to write Python data to a file:

```python
import json

user = {
    "name": "Ada",
    "age": 36,
    "skills": ["Python", "Mathematics"]
}

with open("user.json", "w", encoding="utf-8") as file:
    json.dump(user, file)
```

This produces compact JSON:

```json
{"name": "Ada", "age": 36, "skills": ["Python", "Mathematics"]}
```

### Pretty-printing JSON

Use `indent` to make the file easier to read:

```python
with open("user.json", "w", encoding="utf-8") as file:
    json.dump(user, file, indent=2)
```

Output:

```json
{
  "name": "Ada",
  "age": 36,
  "skills": [
    "Python",
    "Mathematics"
  ]
}
```

### Sorting keys

```python
with open("user.json", "w", encoding="utf-8") as file:
    json.dump(user, file, indent=2, sort_keys=True)
```

This is useful when comparing files in version control.

### Adding a final newline

```python
with open("user.json", "w", encoding="utf-8") as file:
    json.dump(user, file, indent=2)
    file.write("\n")
```

---

## 7. Converting Between JSON and Strings

Use `json.dumps()` to convert Python data into a JSON string:

```python
import json

data = {
    "name": "Ada",
    "age": 36
}

json_text = json.dumps(data, indent=2)
print(json_text)
```

Use `json.loads()` to parse a JSON string:

```python
json_text = '{"name": "Ada", "age": 36}'

data = json.loads(json_text)

print(data["name"])
```

The difference is:

```python
json.load(file)       # File → Python object
json.loads(string)    # String → Python object

json.dump(data, file) # Python object → File
json.dumps(data)      # Python object → String
```

---

## 8. Handling JSON Errors

Malformed JSON raises `json.JSONDecodeError`:

```python
import json

try:
    with open("data.json", encoding="utf-8") as file:
        data = json.load(file)

except FileNotFoundError:
    print("The file does not exist.")

except json.JSONDecodeError as error:
    print(f"Invalid JSON: {error}")

except OSError as error:
    print(f"File error: {error}")
```

A reusable function:

```python
import json
from pathlib import Path
from typing import Any

def read_json(path: str | Path) -> Any:
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise RuntimeError(f"JSON file not found: {path}")
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Invalid JSON in {path}, line {error.lineno}, "
            f"column {error.colno}"
        ) from error
```

---

## 9. Using `pathlib` for File Paths

`pathlib` is often clearer than manually building paths.

```python
import json
from pathlib import Path

path = Path("data") / "users.json"

with path.open(encoding="utf-8") as file:
    users = json.load(file)
```

Writing:

```python
output_path = Path("output") / "result.json"
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as file:
    json.dump(users, file, indent=2)
```

This creates the parent directory if it does not already exist.

---

## 10. Updating JSON Data

Loading, modifying, and saving is the usual workflow:

```python
import json

with open("settings.json", encoding="utf-8") as file:
    settings = json.load(file)

settings["theme"] = "dark"
settings["notifications"] = True

with open("settings.json", "w", encoding="utf-8") as file:
    json.dump(settings, file, indent=2)
```

### Updating a nested value

```python
settings.setdefault("display", {})
settings["display"]["font_size"] = 14
```

`setdefault()` creates the nested dictionary if it does not exist.

### Adding to a list

```python
settings.setdefault("recent_files", [])
settings["recent_files"].append("report.txt")
```

### Removing a key

```python
settings.pop("temporary_value", None)
```

The `None` prevents an error if the key is missing.

---

## 11. Creating a Reusable JSON Repository

For repeated file operations, wrap them in functions:

```python
import json
from pathlib import Path
from typing import Any

def load_json(path: str | Path, default: Any = None) -> Any:
    path = Path(path)

    if not path.exists():
        return default

    with path.open(encoding="utf-8") as file:
        return json.load(file)


def save_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


data = load_json("data.json", default={})
data["updated"] = True
save_json("data.json", data)
```

---

## 12. Unicode and Non-ASCII Text

By default, `json.dump()` may escape non-ASCII characters:

```python
data = {"city": "München", "greeting": "こんにちは"}

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)
```

To preserve readable Unicode characters:

```python
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
```

Use UTF-8 consistently when opening files:

```python
open("data.json", encoding="utf-8")
```

---

## 13. JSON Type Limitations

JSON does not directly support every Python type.

### Supported naturally

```python
data = {
    "text": "hello",
    "number": 42,
    "decimal": 3.14,
    "enabled": True,
    "missing": None,
    "items": [1, 2, 3],
    "nested": {"key": "value"}
}
```

### Unsupported by default

These cannot be serialized directly:

- `datetime`
- `date`
- `set`
- `bytes`
- Custom classes
- `Decimal`

Example problem:

```python
import json
from datetime import datetime

data = {"created_at": datetime.now()}

json.dumps(data)  # TypeError
```

### Converting a datetime

```python
from datetime import datetime
import json

data = {
    "created_at": datetime.now().isoformat()
}

print(json.dumps(data))
```

### Converting a set

```python
data = {
    "tags": list({"python", "json", "files"})
}

print(json.dumps(data))
```

### Custom serialization with `default`

```python
import json
from datetime import datetime

def serialize(value):
    if isinstance(value, datetime):
        return value.isoformat()

    raise TypeError(f"Unsupported type: {type(value).__name__}")

data = {"created_at": datetime.now()}

text = json.dumps(data, default=serialize)
print(text)
```

---

## 14. Preserving Large or Precise Numbers

JSON numbers are normally converted to Python `int` or `float`.

For precise decimal values, use `Decimal`:

```python
import json
from decimal import Decimal

json_text = '{"price": 19.99}'

data = json.loads(
    json_text,
    parse_float=Decimal
)

print(data["price"])
print(type(data["price"]))
```

For unusual or invalid numeric constants, you can reject them:

```python
def reject_invalid_number(value):
    raise ValueError(f"Invalid number: {value}")

data = json.loads(
    json_text,
    parse_constant=reject_invalid_number
)
```

---

## 15. Validating JSON Structure

Parsing confirms that JSON is syntactically valid. It does not confirm that it has the expected structure.

For example, this is valid JSON:

```json
{
  "name": 123
}
```

But your application may require `name` to be a string.

Basic manual validation:

```python
def validate_user(user: dict) -> None:
    if not isinstance(user, dict):
        raise ValueError("User must be an object.")

    if not isinstance(user.get("name"), str):
        raise ValueError("User name must be a string.")

    if not isinstance(user.get("age"), int):
        raise ValueError("User age must be an integer.")
```

For larger applications, use a JSON Schema validator such as `jsonschema`:

```bash
python -m pip install jsonschema
```

Example schema:

```python
schema = {
    "type": "object",
    "required": ["name", "age"],
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "additionalProperties": False
}
```

Validation:

```python
from jsonschema import validate

validate(instance=user, schema=schema)
```

---

## 16. Working with JSON Lines

A regular JSON file contains one complete JSON document.

A JSON Lines file, often ending in `.jsonl`, contains one JSON value per line:

```json
{"id": 1, "name": "Ada"}
{"id": 2, "name": "Grace"}
{"id": 3, "name": "Linus"}
```

Read it line by line:

```python
import json

with open("users.jsonl", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        if not line.strip():
            continue

        try:
            user = json.loads(line)
            print(user["name"])
        except json.JSONDecodeError as error:
            print(f"Invalid JSON on line {line_number}: {error}")
```

Write JSON Lines:

```python
import json

users = [
    {"id": 1, "name": "Ada"},
    {"id": 2, "name": "Grace"}
]

with open("users.jsonl", "w", encoding="utf-8") as file:
    for user in users:
        file.write(json.dumps(user) + "\n")
```

JSON Lines is useful for large datasets because you can process one record at a time.

---

## 17. Handling Large JSON Files

`json.load()` reads the complete document into memory:

```python
data = json.load(file)
```

This is convenient but may be unsuitable for very large files.

Prefer JSON Lines for streaming:

```python
with open("events.jsonl", encoding="utf-8") as file:
    for line in file:
        event = json.loads(line)
        process(event)
```

For a large regular JSON array, consider a streaming parser such as `ijson`:

```bash
python -m pip install ijson
```

```python
import ijson

with open("large-data.json", "rb") as file:
    for record in ijson.items(file, "item"):
        process(record)
```

Streaming avoids loading the complete array into memory.

---

## 18. Atomic File Writes

If a program is interrupted while writing, the JSON file could become incomplete. A safer approach is to write a temporary file and then replace the original:

```python
import json
import os
import tempfile
from pathlib import Path
from typing import Any

def atomic_save_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        delete=False
    ) as temporary_file:
        json.dump(data, temporary_file, indent=2)
        temporary_file.write("\n")
        temporary_path = temporary_file.name

    os.replace(temporary_path, path)
```

`os.replace()` replaces the destination in a single operation on supported operating systems.

---

## 19. Security Considerations

JSON itself does not execute code, so it is safer to parse than Python-specific formats such as `pickle`.

Still:

- Do not assume JSON data is trustworthy.
- Validate types and required fields.
- Do not use `eval()` to parse JSON.
- Avoid inserting unescaped JSON values into HTML or SQL.
- Treat values from users and external APIs as untrusted.
- Limit file size when processing uploaded files.
- Be careful when converting JSON fields into file paths or shell commands.

Use:

```python
data = json.loads(text)
```

Do not use:

```python
data = eval(text)
```

---

## 20. Common Mistakes

### Using single quotes

Invalid JSON:

```python
text = "{'name': 'Ada'}"
json.loads(text)
```

JSON requires double quotes:

```python
text = '{"name": "Ada"}'
data = json.loads(text)
```

### Confusing `dump` and `dumps`

```python
json.dump(data, file)   # Writes to a file
json.dumps(data)        # Returns a string
```

### Confusing `load` and `loads`

```python
json.load(file)         # Reads from a file
json.loads(text)        # Reads from a string
```

### Overwriting a file accidentally

Opening with `"w"` replaces existing contents:

```python
open("data.json", "w")
```

Load the existing data first if you need to update it.

### Expecting comments to work

This is not valid JSON:

```json
{
  "name": "Ada",
  // This is a comment
  "age": 36
}
```

Use a separate documentation file or a format designed to support comments.

### Assuming keys always exist

Prefer:

```python
email = user.get("email")
```

when the field is optional.

---

## 21. Complete Example: A JSON-Based Task Manager

`tasks.json`:

```json
[
  {
    "id": 1,
    "title": "Learn JSON",
    "completed": false
  }
]
```

Python program:

```python
import json
from pathlib import Path

TASKS_FILE = Path("tasks.json")


def load_tasks() -> list[dict]:
    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open(encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            raise ValueError("The JSON root must be a list.")

        return tasks

    except json.JSONDecodeError as error:
        raise RuntimeError(f"Invalid JSON: {error}") from error


def save_tasks(tasks: list[dict]) -> None:
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)
        file.write("\n")


def add_task(title: str) -> dict:
    tasks = load_tasks()

    next_id = max(
        (task.get("id", 0) for task in tasks),
        default=0
    ) + 1

    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)

    return task


def complete_task(task_id: int) -> bool:
    tasks = load_tasks()

    for task in tasks:
        if task.get("id") == task_id:
            task["completed"] = True
            save_tasks(tasks)
            return True

    return False


def list_tasks() -> None:
    for task in load_tasks():
        status = "done" if task["completed"] else "pending"
        print(f'{task["id"]}: {task["title"]} [{status}]')


add_task("Practice json.load and json.dump")
complete_task(1)
list_tasks()
```

This example demonstrates:

- Reading a JSON file
- Handling a missing file
- Validating the top-level type
- Adding records
- Updating records
- Saving changes
- Formatting output

---

## 22. Recommended Workflow

For most JSON file tasks:

1. Import `json`.
2. Use UTF-8 encoding.
3. Open files with `with`.
4. Read using `json.load()`.
5. Validate the loaded structure.
6. Access values using dictionaries and lists.
7. Modify the Python object.
8. Save using `json.dump()`.
9. Use `indent=2` for human-readable files.
10. Handle `FileNotFoundError`, `JSONDecodeError`, and other file errors.
11. Use JSON Lines or a streaming parser for large datasets.
12. Use atomic writes when data must not be corrupted.

A typical implementation looks like this:

```python
import json
from pathlib import Path

path = Path("data.json")

try:
    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    # Read or modify data here.
    data["updated"] = True

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")

except FileNotFoundError:
    print(f"File not found: {path}")

except json.JSONDecodeError as error:
    print(f"Invalid JSON: {error}")
```

## Quick Reference

```python
import json

# File → Python
with open("data.json", encoding="utf-8") as file:
    data = json.load(file)

# Python → File
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

# String → Python
data = json.loads('{"key": "value"}')

# Python → String
text = json.dumps(data, indent=2)

# Safe dictionary lookup
value = data.get("key", "default")

# JSON Lines
for line in open("data.jsonl", encoding="utf-8"):
    record = json.loads(line)
```