# Working with CSV Files in Python: End-to-End Guide

CSV files are plain-text files used to store tabular data. Each line usually represents a row, and commas separate values.

Example:

```csv
name,age,city
Alice,25,London
Bob,30,Paris
```

This guide covers working with CSV files using Python’s built-in `csv` module and the popular `pandas` library.

---

## 1. CSV Basics

A CSV file commonly contains:

- A header row
- Rows of data
- Values separated by commas
- Optional quoted values
- Missing or empty values

Example:

```csv
id,name,score
1,Alice,88
2,Bob,92
3,Charlie,75
```

CSV files can also use other separators, such as:

```csv
name;age;city
Alice;25;London
```

The separator is called the **delimiter**.

---

# Part 1: Using Python’s `csv` Module

The `csv` module is built into Python and works well when you need simple, lightweight CSV processing.

## 2. Import the Module

```python
import csv
```

---

## 3. Reading a CSV File

Suppose `students.csv` contains:

```csv
name,age,grade
Alice,20,A
Bob,21,B
```

Read the file row by row:

```python
import csv

with open("students.csv", "r", newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

Output:

```python
['name', 'age', 'grade']
['Alice', '20', 'A']
['Bob', '21', 'B']
```

Values are returned as strings.

---

## 4. Reading CSV Headers Separately

```python
with open("students.csv", newline="") as file:
    reader = csv.reader(file)

    header = next(reader)
    print(header)

    for row in reader:
        print(row)
```

`next(reader)` reads the first row.

---

## 5. Reading Rows as Dictionaries

`csv.DictReader` maps column names to values.

```python
with open("students.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row["name"], row["grade"])
```

Each row behaves like a dictionary:

```python
{
    "name": "Alice",
    "age": "20",
    "grade": "A"
}
```

This is often easier to read than using indexes.

---

## 6. Converting Values to Numbers

CSV values are read as strings, so convert them when needed.

```python
with open("students.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        age = int(row["age"])
        print(age + 1)
```

Common conversions:

```python
age = int(row["age"])
price = float(row["price"])
active = row["active"].lower() == "true"
```

---

## 7. Handling Missing Values

Example:

```csv
name,age,city
Alice,20,London
Bob,,Paris
```

Check for empty values:

```python
with open("students.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        age = row["age"]

        if age:
            print(int(age))
        else:
            print("Age missing")
```

Using a default value:

```python
age = int(row["age"] or 0)
```

---

## 8. Writing a CSV File

Use `csv.writer`.

```python
import csv

rows = [
    ["name", "age"],
    ["Alice", 25],
    ["Bob", 30],
]

with open("people.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
```

---

## 9. Writing One Row at a Time

```python
with open("people.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["name", "age"])
    writer.writerow(["Alice", 25])
    writer.writerow(["Bob", 30])
```

---

## 10. Writing Dictionaries

Use `csv.DictWriter`.

```python
import csv

fields = ["name", "age"]

with open("people.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fields)

    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 25})
```

Writing multiple dictionaries:

```python
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
]

with open("people.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(people)
```

---

## 11. Appending to a CSV File

Use append mode, `"a"`.

```python
with open("people.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Charlie", 35])
```

Do not write the header again when appending.

---

## 12. Custom Delimiters

For semicolon-separated files:

```python
with open("data.csv", newline="") as file:
    reader = csv.reader(file, delimiter=";")

    for row in reader:
        print(row)
```

Writing with a semicolon:

```python
with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["name", "age"])
```

---

## 13. Quoted Values

CSV files can contain commas inside quoted text:

```csv
name,address
Alice,"10 Main Street, London"
```

The `csv` module handles this automatically:

```python
with open("people.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row["address"])
```

---

## 14. File Encoding

For most modern files, use UTF-8:

```python
with open("people.csv", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
```

When exporting files for some spreadsheet applications, this may help:

```python
with open("people.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
```

---

## 15. Basic CSV Validation

You can check whether required columns exist:

```python
required = {"name", "age"}

with open("people.csv", newline="") as file:
    reader = csv.DictReader(file)

    if not required.issubset(reader.fieldnames):
        raise ValueError("Missing required columns")
```

Validate individual rows:

```python
for row in reader:
    if not row["name"]:
        print("Name is missing")

    if row["age"] and not row["age"].isdigit():
        print("Invalid age")
```

---

# Part 2: Using pandas

`pandas` is better for data analysis, filtering, cleaning, grouping, and transforming larger datasets.

## 16. Installing pandas

```bash
pip install pandas
```

Import it:

```python
import pandas as pd
```

---

## 17. Reading a CSV File

```python
import pandas as pd

df = pd.read_csv("students.csv")
print(df)
```

`df` is a pandas **DataFrame**.

Example:

```text
      name  age grade
0    Alice   20     A
1      Bob   21     B
```

---

## 18. Viewing the Data

View the first rows:

```python
df.head()
```

View the last rows:

```python
df.tail()
```

View a specific number of rows:

```python
df.head(10)
```

Get the number of rows and columns:

```python
df.shape
```

Get column names:

```python
df.columns
```

Get general information:

```python
df.info()
```

Get numeric summaries:

```python
df.describe()
```

---

## 19. Selecting Columns

Select one column:

```python
df["name"]
```

Select multiple columns:

```python
df[["name", "grade"]]
```

Using dot notation is sometimes possible:

```python
df.name
```

Bracket notation is safer, especially when column names contain spaces.

---

## 20. Selecting Rows

Select the first row by position:

```python
df.iloc[0]
```

Select the first five rows:

```python
df.iloc[:5]
```

Select a row by label:

```python
df.loc[0]
```

Select specific rows and columns:

```python
df.loc[0:2, ["name", "grade"]]
```

---

## 21. Filtering Rows

Filter students older than 20:

```python
df[df["age"] > 20]
```

Filter by text:

```python
df[df["grade"] == "A"]
```

Multiple conditions:

```python
df[(df["age"] > 20) & (df["grade"] == "A")]
```

Use `|` for OR:

```python
df[(df["grade"] == "A") | (df["grade"] == "B")]
```

Use `~` for NOT:

```python
df[~(df["grade"] == "A")]
```

---

## 22. Filtering with `isin`

```python
df[df["city"].isin(["London", "Paris"])]
```

---

## 23. Filtering Text

Find names containing `"al"`:

```python
df[df["name"].str.contains("al", case=False, na=False)]
```

Starts with a value:

```python
df[df["name"].str.startswith("A", na=False)]
```

---

## 24. Sorting Data

Sort by age:

```python
df.sort_values("age")
```

Sort descending:

```python
df.sort_values("age", ascending=False)
```

Sort by multiple columns:

```python
df.sort_values(["city", "age"])
```

Modify the original DataFrame:

```python
df.sort_values("age", inplace=True)
```

---

## 25. Adding Columns

Create a new column:

```python
df["passed"] = df["score"] >= 50
```

Calculate a value:

```python
df["score_percent"] = df["score"] / 100
```

Create a column from text:

```python
df["full_name"] = df["first"] + " " + df["last"]
```

---

## 26. Renaming Columns

```python
df = df.rename(columns={"old_name": "new_name"})
```

Rename all columns:

```python
df.columns = ["name", "age", "city"]
```

Clean column names:

```python
df.columns = df.columns.str.strip().str.lower()
```

Replace spaces:

```python
df.columns = df.columns.str.replace(" ", "_")
```

---

## 27. Changing Data Types

Check data types:

```python
df.dtypes
```

Convert a column to integers:

```python
df["age"] = df["age"].astype(int)
```

Convert safely:

```python
df["age"] = pd.to_numeric(df["age"], errors="coerce")
```

Convert dates:

```python
df["date"] = pd.to_datetime(df["date"])
```

Convert to text:

```python
df["name"] = df["name"].astype("string")
```

---

## 28. Handling Missing Data

Check missing values:

```python
df.isna().sum()
```

Remove rows containing missing values:

```python
df.dropna()
```

Remove rows missing a specific column:

```python
df.dropna(subset=["email"])
```

Fill missing values:

```python
df["age"] = df["age"].fillna(0)
```

Fill text values:

```python
df["city"] = df["city"].fillna("Unknown")
```

Fill with the average:

```python
df["score"] = df["score"].fillna(df["score"].mean())
```

---

## 29. Removing Duplicate Rows

Find duplicates:

```python
df.duplicated()
```

Remove duplicates:

```python
df = df.drop_duplicates()
```

Remove duplicates based on selected columns:

```python
df = df.drop_duplicates(subset=["email"])
```

Keep the last duplicate:

```python
df = df.drop_duplicates(subset=["email"], keep="last")
```

---

## 30. Replacing Values

Replace one value:

```python
df["city"] = df["city"].replace("NYC", "New York")
```

Replace multiple values:

```python
df["grade"] = df["grade"].replace({
    "A+": "A",
    "A-": "A"
})
```

---

## 31. String Cleaning

Remove extra spaces:

```python
df["name"] = df["name"].str.strip()
```

Convert to lowercase:

```python
df["email"] = df["email"].str.lower()
```

Replace text:

```python
df["phone"] = df["phone"].str.replace("-", "", regex=False)
```

Extract part of a string:

```python
df["domain"] = df["email"].str.split("@").str[-1]
```

---

## 32. Date Handling

Read dates while loading:

```python
df = pd.read_csv("sales.csv", parse_dates=["date"])
```

Convert after loading:

```python
df["date"] = pd.to_datetime(df["date"])
```

Extract date components:

```python
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["weekday"] = df["date"].dt.day_name()
```

Filter by date:

```python
df[df["date"] >= "2026-01-01"]
```

---

## 33. Grouping and Aggregation

Average score by class:

```python
df.groupby("class")["score"].mean()
```

Total sales by product:

```python
df.groupby("product")["sales"].sum()
```

Multiple calculations:

```python
df.groupby("city")["sales"].agg(["sum", "mean", "count"])
```

Group by multiple columns:

```python
df.groupby(["city", "year"])["sales"].sum()
```

---

## 34. Counting Values

Count each category:

```python
df["city"].value_counts()
```

Include missing values:

```python
df["city"].value_counts(dropna=False)
```

Count unique values:

```python
df["city"].nunique()
```

Get unique values:

```python
df["city"].unique()
```

---

## 35. Combining DataFrames

### Concatenating Rows

```python
combined = pd.concat([df1, df2], ignore_index=True)
```

### Concatenating Columns

```python
combined = pd.concat([df1, df2], axis=1)
```

### Merging DataFrames

```python
merged = pd.merge(users, orders, on="user_id")
```

Left join:

```python
merged = pd.merge(users, orders, on="user_id", how="left")
```

Common join types:

- `inner`: Keep matching rows
- `left`: Keep all rows from the left DataFrame
- `right`: Keep all rows from the right DataFrame
- `outer`: Keep all rows from both DataFrames

---

## 36. Reading CSV Options

Read a file with a custom delimiter:

```python
df = pd.read_csv("data.csv", sep=";")
```

Use a specific encoding:

```python
df = pd.read_csv("data.csv", encoding="utf-8")
```

Treat certain values as missing:

```python
df = pd.read_csv("data.csv", na_values=["N/A", "unknown", "-"])
```

Read only selected columns:

```python
df = pd.read_csv("data.csv", usecols=["name", "age"])
```

Read a limited number of rows:

```python
df = pd.read_csv("data.csv", nrows=100)
```

Skip rows:

```python
df = pd.read_csv("data.csv", skiprows=2)
```

Use a column as the index:

```python
df = pd.read_csv("data.csv", index_col="id")
```

---

## 37. Reading Large CSV Files in Chunks

For very large files, process smaller portions:

```python
for chunk in pd.read_csv("large.csv", chunksize=10000):
    print(chunk.shape)
```

Calculate a result across chunks:

```python
total = 0

for chunk in pd.read_csv("sales.csv", chunksize=10000):
    total += chunk["amount"].sum()

print(total)
```

---

## 38. Writing a DataFrame to CSV

```python
df.to_csv("output.csv", index=False)
```

`index=False` prevents pandas from writing the DataFrame index as an extra column.

Write only selected columns:

```python
df[["name", "score"]].to_csv("scores.csv", index=False)
```

Write with a custom separator:

```python
df.to_csv("output.csv", sep=";", index=False)
```

Write without headers:

```python
df.to_csv("output.csv", header=False, index=False)
```

Append to an existing file:

```python
df.to_csv("output.csv", mode="a", header=False, index=False)
```

---

## 39. A Complete pandas Workflow

```python
import pandas as pd

df = pd.read_csv("sales.csv")

df.columns = df.columns.str.strip().str.lower()
df["date"] = pd.to_datetime(df["date"])
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

df = df.dropna(subset=["product", "amount"])
df = df.drop_duplicates()

large_sales = df[df["amount"] > 100]

summary = (
    df.groupby("product")["amount"]
      .sum()
      .reset_index()
)

summary.to_csv("sales_summary.csv", index=False)
```

This workflow:

1. Loads the CSV
2. Cleans column names
3. Converts data types
4. Removes invalid rows
5. Removes duplicates
6. Filters data
7. Groups and summarizes data
8. Exports the result

---

# Part 3: Choosing Between `csv` and pandas

Use the built-in `csv` module when:

- The file is small
- You only need to read or write rows
- You want no external dependencies
- You are building a simple script
- You need precise control over individual rows

Use pandas when:

- You need filtering and sorting
- You need data cleaning
- You need grouping and aggregation
- You need date processing
- You need to combine multiple datasets
- You are doing analysis
- The dataset is moderately large

A simple rule:

```text
Simple row processing → csv
Data analysis and transformation → pandas
```

---

# Part 4: Common Problems and Solutions

## Extra Index Column

Problem:

```text
Unnamed: 0
```

Solution when writing:

```python
df.to_csv("output.csv", index=False)
```

Or remove it after reading:

```python
df = df.drop(columns=["Unnamed: 0"])
```

---

## Incorrect Data Types

Check the types:

```python
print(df.dtypes)
```

Convert numeric data:

```python
df["price"] = pd.to_numeric(df["price"], errors="coerce")
```

---

## Encoding Errors

Try another encoding:

```python
df = pd.read_csv("data.csv", encoding="latin1")
```

---

## Wrong Delimiter

If the entire row appears in one column, check the separator:

```python
df = pd.read_csv("data.csv", sep=";")
```

---

## Column Names with Spaces

Clean them:

```python
df.columns = df.columns.str.strip()
```

Convert to snake case:

```python
df.columns = (
    df.columns.str.strip()
             .str.lower()
             .str.replace(" ", "_")
)
```

---

## Commas Inside Values

Use proper quoting with the `csv` module:

```python
import csv

with open("data.csv", newline="") as file:
    reader = csv.reader(file)
```

For pandas, quoting is usually handled automatically:

```python
df = pd.read_csv("data.csv")
```

---

## Dates Not Parsing Correctly

```python
df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)
```

Invalid dates become missing values.

---

# Part 5: Best Practices

## Always Use `with open`

This automatically closes the file:

```python
with open("data.csv", newline="") as file:
    reader = csv.reader(file)
```

## Use `newline=""` with the `csv` Module

This prevents unwanted blank lines, especially on Windows:

```python
open("data.csv", newline="")
```

## Use `index=False` with pandas

```python
df.to_csv("output.csv", index=False)
```

## Inspect Data Before Processing

```python
print(df.head())
print(df.shape)
print(df.dtypes)
print(df.isna().sum())
```

## Avoid Modifying Data Accidentally

Use a copy when needed:

```python
filtered = df[df["score"] > 50].copy()
```

## Convert Types Explicitly

Do not assume numbers and dates were loaded correctly:

```python
df["amount"] = pd.to_numeric(df["amount"])
df["date"] = pd.to_datetime(df["date"])
```

## Keep Raw and Cleaned Data Separate

For example:

```text
data/raw/input.csv
data/processed/cleaned.csv
```

## Validate Important Data

Check required columns:

```python
required = {"id", "name", "email"}

if not required.issubset(df.columns):
    raise ValueError("Required columns are missing")
```

---

# Part 6: Mini Practice Project

Assume `orders.csv` contains:

```csv
order_id,product,quantity,price
1,Keyboard,2,25.50
2,Mouse,3,10.00
3,Keyboard,1,25.50
```

Calculate total order value:

```python
import pandas as pd

df = pd.read_csv("orders.csv")
df["total"] = df["quantity"] * df["price"]

print(df)
```

Calculate product totals:

```python
summary = (
    df.groupby("product")["total"]
      .sum()
      .reset_index()
)

print(summary)
```

Export the summary:

```python
summary.to_csv("product_totals.csv", index=False)
```

Expected result:

```text
    product  total
0  Keyboard  76.50
1  Mouse     30.00
```

---

# Quick Reference

## `csv` Module

```python
import csv

# Read
with open("data.csv", newline="") as file:
    rows = list(csv.reader(file))

# Read dictionaries
with open("data.csv", newline="") as file:
    rows = list(csv.DictReader(file))

# Write
with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "age"])
    writer.writerow(["Alice", 25])
```

## pandas

```python
import pandas as pd

# Read
df = pd.read_csv("data.csv")

# Inspect
df.head()
df.info()
df.describe()

# Select
df["name"]
df[["name", "age"]]

# Filter
df[df["age"] > 18]

# Sort
df.sort_values("age")

# Group
df.groupby("city")["sales"].sum()

# Write
df.to_csv("output.csv", index=False)
```

## Recommended Learning Order

1. Understand CSV structure
2. Read files with `csv.reader`
3. Read rows with `csv.DictReader`
4. Write and append CSV files
5. Learn pandas DataFrames
6. Select columns and rows
7. Filter and sort data
8. Handle missing values
9. Convert data types
10. Group and summarize data
11. Merge multiple files
12. Process large CSV files in chunks
13. Build complete cleaning and export workflows