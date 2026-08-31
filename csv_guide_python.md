# Working with CSV Files in Python — End-to-End Guide

## 1. What is a CSV file?
A CSV (Comma-Separated Values) file is a plain-text tabular format where rows are lines and columns are separated by a delimiter (usually a comma). Despite the name, delimiters can also be `;`, `\t` (TSV), or `|`.

Key quirks to know upfront:
- Fields containing the delimiter, quotes, or newlines must be quoted (`"like, this"`).
- Encoding matters — UTF-8 is standard, but you'll hit `latin-1`/`cp1252` files often.
- There's no strict "CSV standard," but [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180) is the closest thing.

Python has two main tools for CSV: the built-in `csv` module (lightweight, stdlib) and `pandas` (heavyweight, analysis-focused). Use `csv` for simple read/write/streaming; use `pandas` for analysis, transformation, and larger data.

---

## 2. Reading CSV — the built-in `csv` module

```python
import csv

with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)          # skip/capture header row
    for row in reader:
        print(row)                 # row is a list of strings
```

**Always open with `newline=""`** — this prevents the `csv` module from mangling embedded newlines on Windows.

### Reading as dictionaries
```python
with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])   # row is an OrderedDict/dict
```

### Custom delimiters and dialects
```python
reader = csv.reader(f, delimiter=";", quotechar='"')

csv.register_dialect("pipes", delimiter="|", quoting=csv.QUOTE_MINIMAL)
reader = csv.reader(f, dialect="pipes")
```

### Sniffing an unknown format
```python
sample = open("data.csv").read(2048)
dialect = csv.Sniffer().sniff(sample)
has_header = csv.Sniffer().has_header(sample)
```

---

## 3. Writing CSV — the built-in `csv` module

```python
import csv

rows = [["name", "age"], ["Alice", 30], ["Bob", 25]]
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
```

### Writing from dictionaries
```python
fieldnames = ["name", "age"]
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 30})
```

### Quoting control
```python
csv.writer(f, quoting=csv.QUOTE_ALL)       # quote everything
csv.writer(f, quoting=csv.QUOTE_NONNUMERIC) # quote non-numbers
csv.writer(f, quoting=csv.QUOTE_MINIMAL)    # default — only when needed
```

---

## 4. Reading/Writing with pandas

```python
import pandas as pd

df = pd.read_csv("data.csv")
df = pd.read_csv("data.csv", sep=";", encoding="latin-1")
df = pd.read_csv("data.csv", usecols=["name", "age"], dtype={"age": "int32"})
df = pd.read_csv("data.csv", parse_dates=["signup_date"])
df = pd.read_csv("data.csv", nrows=1000)          # limit rows
df = pd.read_csv("data.csv", skiprows=2)          # skip junk header rows
df = pd.read_csv("data.csv", na_values=["NA", "-", "?"])
```

Writing:
```python
df.to_csv("out.csv", index=False)
df.to_csv("out.csv", index=False, columns=["name", "age"])
df.to_csv("out.csv", index=False, sep="\t")       # TSV
```

**Rule of thumb**: `csv` module for streaming/line-by-line or huge files; `pandas` for anything you'll filter, group, join, or reshape.

---

## 5. Large files: don't load it all into memory

```python
# csv module — inherently streams row by row
with open("huge.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        process(row)

# pandas — chunked reading
for chunk in pd.read_csv("huge.csv", chunksize=100_000):
    process(chunk)

# pandas — pick only needed columns + efficient dtypes to cut memory
df = pd.read_csv("huge.csv", usecols=["id", "amount"], dtype={"id": "int32", "amount": "float32"})
```

For truly massive files, consider `polars` (`pl.read_csv`, `pl.scan_csv` for lazy/streaming) or `dask.dataframe` — both parallelize and handle out-of-core data far better than pandas.

---

## 6. Common data-cleaning tasks

```python
df.isna().sum()                          # find missing values
df = df.dropna(subset=["email"])         # drop rows missing key fields
df["age"] = df["age"].fillna(df["age"].median())

df = df.drop_duplicates()
df.columns = df.columns.str.strip().str.lower()   # normalize headers

df["price"] = pd.to_numeric(df["price"], errors="coerce")  # bad values -> NaN
df["date"] = pd.to_datetime(df["date"], errors="coerce", format="%Y-%m-%d")

df["name"] = df["name"].str.strip().str.title()
```

---

## 7. Handling messy real-world CSVs

| Problem | Fix |
|---|---|
| Wrong encoding (`UnicodeDecodeError`) | Try `encoding="latin-1"` or detect with `chardet`/`charset-normalizer` |
| Inconsistent delimiters | `csv.Sniffer()` or inspect manually, pass `sep=None, engine="python"` in pandas to auto-detect |
| Extra/missing columns per row | `csv.reader` won't error; pandas: `on_bad_lines="skip"` or `"warn"` |
| BOM at file start | `encoding="utf-8-sig"` |
| Embedded commas/newlines in fields | Ensure proper quoting on write; `newline=""` on read |
| Huge file, low RAM | Chunking, `usecols`, better dtypes, or polars/dask |

```python
# skip malformed rows instead of crashing
df = pd.read_csv("messy.csv", on_bad_lines="skip", engine="python")
```

---

## 8. Validation

For anything beyond ad-hoc scripts, validate schema/types instead of hoping the data is clean:

```python
import pandera as pa

schema = pa.DataFrameSchema({
    "age": pa.Column(int, pa.Check.ge(0)),
    "email": pa.Column(str, pa.Check.str_matches(r"^[^@]+@[^@]+\.[^@]+$")),
})
schema.validate(df)
```

Simpler manual checks work fine too — verify column names, dtypes, and value ranges before processing.

---

## 9. Performance tips

- Specify `dtype` explicitly in pandas — avoids slow type inference.
- Use `usecols` to skip columns you don't need.
- Prefer `polars` for large files — it's multi-threaded and much faster than pandas.
- Avoid `iterrows()` for transformations — use vectorized operations (`df["col"].apply()` or better, direct vector math) instead.
- Compress on write (`df.to_csv("out.csv.gz")`) — pandas handles `.gz`/`.zip`/`.bz2` transparently by extension.

---

## 10. Quick decision guide

- **Just need to read/write rows, no analysis** → `csv` module
- **Filtering, grouping, joining, reshaping** → `pandas`
- **File is huge (GBs) or you need speed** → `polars` or chunked pandas
- **Untrusted/messy external data** → sniff dialect, validate schema, handle encoding explicitly
- **Need strict data contracts** → `pandera` or manual schema checks

---

## 11. Minimal end-to-end example

```python
import pandas as pd

df = pd.read_csv("raw_sales.csv", encoding="utf-8-sig", on_bad_lines="skip")
df.columns = df.columns.str.strip().str.lower()
df = df.drop_duplicates()
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["amount", "date"])

summary = df.groupby(df["date"].dt.month)["amount"].sum()
df.to_csv("cleaned_sales.csv", index=False)
```

This pattern — load → normalize → clean → validate/transform → export — covers most real-world CSV work.
