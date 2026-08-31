# Python CSV Files

## 1. Using Python’s Built-in `csv` Module

### Read rows

```python
import csv

with open("data.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

Values are returned as strings.

### Read rows as dictionaries

```python
import csv

with open("data.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row["name"])
```

Example row:

```python
{
    "id": "1",
    "name": "Alice",
    "age": "30"
}
```

Convert values when needed:

```python
employee_id = int(row["id"])
age = int(row["age"])
```

### Write a CSV file

```python
import csv

rows = [
    ["name", "age"],
    ["Alice", 30],
    ["Bob", 25],
]

with open("output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
```

### Write dictionaries

```python
import csv

rows = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
]

with open("output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)
```

---

## 2. Using pandas

Install it:

```bash
python -m pip install pandas
```

### Read a CSV

```python
import pandas as pd

df = pd.read_csv("data.csv")
print(df.head())
```

### Inspect data

```python
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())
```

### Select columns

```python
names = df["name"]
small_df = df[["name", "age"]]
```

### Filter rows

```python
adults = df[df["age"] >= 18]
```

Multiple conditions:

```python
result = df[
    (df["age"] >= 18)
    & (df["city"] == "Boston")
]
```

### Sort rows

```python
df = df.sort_values("age", ascending=False)
```

### Create a column

```python
df["monthly_salary"] = df["salary"] / 12
```

### Handle missing values

```python
print(df.isna().sum())

df = df.dropna(subset=["name"])
df["city"] = df["city"].fillna("Unknown")
```

### Convert data types

```python
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
```

### Remove duplicates

```python
df = df.drop_duplicates()
```

### Group and summarize

```python
summary = df.groupby("department")["salary"].mean()
print(summary)
```

### Save a CSV

```python
df.to_csv("cleaned_data.csv", index=False)
```

`index=False` prevents pandas from adding an unwanted index column.

---

## 3. Important CSV Options

### Different delimiter

```python
df = pd.read_csv("data.csv", sep=";")
```

### Preserve IDs with leading zeroes

```python
df = pd.read_csv(
    "customers.csv",
    dtype={"zip_code": "string"}
)
```

### Handle custom missing values

```python
df = pd.read_csv(
    "data.csv",
    na_values=["N/A", "null", "-", ""]
)
```

### Read large files in chunks

```python
for chunk in pd.read_csv("large.csv", chunksize=10_000):
    process_chunk(chunk)
```

---

## 4. Basic Validation

```python
required = {"id", "name", "age"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing columns: {missing}")

if df["id"].duplicated().any():
    raise ValueError("IDs must be unique")
```

---

## 5. Best Practices

- Use `newline=""` and `encoding="utf-8"` with the built-in `csv` module.
- Do not parse CSV files with `line.split(",")`; quoted fields can contain commas.
- Treat CSV values as strings until you convert them.
- Preserve the original file and save cleaned data separately.
- Use `csv` for simple row-by-row processing.
- Use pandas for cleaning, filtering, grouping, and analysis.
- Read large files in chunks instead of loading everything into memory.