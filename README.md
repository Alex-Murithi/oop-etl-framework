# Object-Oriented ETL Framework

A reusable Object-Oriented ETL (Extract, Transform, Load) framework built in Python. The project demonstrates abstraction, inheritance, polymorphism, method overriding, exception handling, and clean software design by processing data from multiple sources through a common pipeline architecture.

## Project Overview

Jumla Logistics previously maintained several copy-pasted ETL scripts for different data sources. This project replaces those scripts with a small reusable framework that allows any compatible data source to be processed through the same extraction, transformation, and loading workflow.

The framework supports:

- CSV data sources
- REST API data sources
- Data validation and cleaning
- Rejected record tracking
- Multiple output formats
- Custom exception handling
- Execution reporting and summaries

## Learning Objectives

This project demonstrates:

- Object-Oriented Programming (OOP)
- Abstract Base Classes (ABC)
- Inheritance
- Polymorphism
- Method Overriding
- Exception Handling
- File Handling
- API Integration
- Data Validation
- ETL Pipeline Design

---

# Project Structure

```text
day4-oop-etl/
│
├── etl/
│   ├── __init__.py
│   ├── errors.py
│   ├── extractors.py
│   ├── transformer.py
│   ├── loader.py
│   └── pipeline.py
│
├── data/
│   └── orders.csv
│
├── output/
│   ├── orders_clean.csv
│   ├── orders_rejected.csv
│   └── users.json
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Framework Design

The application follows the ETL pattern:

```text
Extractor
    ↓
Transformer
    ↓
Loader
    ↓
Output
```

The Pipeline class orchestrates the process without needing to know which specific extractor is being used.

---

# Class Design

## DataExtractor (Abstract Base Class)

Provides a common contract for all extractors.

### Responsibilities

- Store source information
- Define the extract() interface
- Provide common behavior
- Prevent direct instantiation

### Methods

```python
extract()
__repr__()
```

---

## CSVExtractor

Inherits from DataExtractor.

### Responsibilities

- Read records from CSV files
- Convert rows to dictionaries
- Handle file-related extraction failures

### Example

```python
CSVExtractor("data/orders.csv")
```

---

## APIExtractor

Inherits from DataExtractor.

### Responsibilities

- Retrieve JSON data from REST APIs
- Validate API responses
- Handle network and HTTP failures

### Example

```python
APIExtractor(
    "https://jsonplaceholder.typicode.com/users"
)
```

### Method Overriding

This class overrides the base implementation of:

```python
__repr__()
```

to provide API-specific output.

---

## DataTransformer

Validates and cleans extracted records.

### Responsibilities

- Validate records
- Clean valid data
- Track rejected records
- Store rejection reasons

### Methods

```python
validate()
clean()
transform()
```

---

## DataLoader

Writes transformed records to storage.

### Supported Formats

```text
.csv
.json
```

### Responsibilities

- Create missing folders
- Write files
- Return number of rows written

---

## Pipeline

Coordinates the ETL workflow.

### Responsibilities

1. Extract data
2. Transform data
3. Load data
4. Return execution statistics

The Pipeline uses polymorphism and works with any extractor implementing the DataExtractor interface.

---

## RunSummary

Stores execution metrics and generates reports.

### Tracks

- Extracted records
- Valid records
- Rejected records
- Loaded records
- Execution duration
- Pipeline status
- Rejection reasons

---

# OOP Concepts Demonstrated

## Abstraction

Implemented using the abstract DataExtractor base class.

```python
class DataExtractor(ABC):
```

Direct instantiation is not allowed.

---

## Inheritance

Concrete extractors inherit common functionality.

```python
class CSVExtractor(DataExtractor)

class APIExtractor(DataExtractor)
```

---

## Polymorphism

The Pipeline operates on DataExtractor objects without knowing the concrete source type.

```python
records = extractor.extract()
```

The same code works for both API and CSV extractors.

---

## Method Overriding

APIExtractor overrides:

```python
__repr__()
```

to provide specialized behavior.

---

# Validation Rules

The transformer applies the following validation rules.

## Required Fields

Records must contain all required fields.

Examples:

```text
order_id
customer_email
product_sku
quantity
unit_price_kes
```

Missing fields cause rejection.

---

## Email Validation

Emails must match a valid email pattern.

Valid:

```text
user@example.com
```

Invalid:

```text
not-an-email
```

---

## Positive Quantity

Quantity must be greater than zero.

Valid:

```text
1
5
20
```

Invalid:

```text
0
-1
abc
```

---

## Positive Unit Price

Unit price must be greater than zero.

Valid:

```text
185
1150
```

Invalid:

```text
0
-330
```

---

## Duplicate Orders

Duplicate order IDs are rejected.

Example:

```text
ORD-7004
```

appearing more than once.

---

# Data Cleaning Rules

Valid records are normalized before loading.

## Date Standardization

Before:

```text
10/14/2026
```

After:

```text
2026-10-14
```

---

## City Names

Before:

```text
NAIROBI
kisumu
 Mombasa
```

After:

```text
Nairobi
Kisumu
Mombasa
```

---

## Status Values

Before:

```text
delivered
Delivered
DELIVERED
```

After:

```text
DELIVERED
```

---

## Derived Column

The transformer calculates:

```text
line_total_kes
```

Formula:

```python
quantity * unit_price_kes
```

Example:

```text
4 × 185 = 740
```

---

# Exception Handling

A custom exception hierarchy is used.

```text
ETLError
├── ExtractionError
└── ValidationError
```

## ExtractionError

Raised when:

- CSV file does not exist
- API request fails
- Invalid source is provided

---

## ValidationError

Used when records fail validation rules.

These errors are collected rather than stopping execution.

---

# Failure Testing

The framework demonstrates graceful failure handling.

## Missing CSV File

```python
CSVExtractor(
    "data/missing.csv"
)
```

Result:

```text
Pipeline status = FAILED
```

Other pipelines continue running.

---

## Invalid API URL

```python
APIExtractor(
    "https://wrong-url.com"
)
```

Result:

```text
Pipeline status = FAILED
```

Other pipelines continue running.

---

# Execution Summary

Each pipeline produces a summary.

Example:

```text
=== ETL Execution Summary ===

Pipeline: Orders CSV (CSVExtractor -> output/orders_clean.csv)
  Extracted : 25
  Valid     : 20
  Rejected  : 5
    - Invalid email: 1
    - Duplicate order_id: 1
    - Non-positive price: 1
    - Invalid quantity: 1
    - Missing product_sku: 1
  Loaded    : 20
  Duration  : 0.04s
  Status    : PARTIAL

Pipeline: Users API (APIExtractor -> output/users.json)
  Extracted : 10
  Valid     : 10
  Rejected  : 0
  Loaded    : 10
  Duration  : 0.23s
  Status    : SUCCESS

Total pipelines: 2 | Succeeded: 2 | Failed: 0
```

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
```

## Navigate Into Project

```bash
cd day4-oop-etl
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Git Bash

```bash
source venv/Scripts/activate
```

### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

Execute the application:

```bash
python main.py
```

---

# Generated Outputs

Successful execution creates:

```text
output/
├── orders_clean.csv
├── orders_rejected.csv
└── users.json
```

## orders_clean.csv

Contains validated and cleaned order records.

## orders_rejected.csv

Contains rejected records and the reasons for rejection.

## users.json

Contains transformed API records.

---

# Assumptions

- Order dates follow MM/DD/YYYY format.
- API returns JSON arrays.
- Email validation uses a regular expression pattern.
- Cities are normalized to Title Case.
- Status values are normalized to uppercase.
- Duplicate order IDs are not allowed.
- Invalid records are excluded from final output but retained in rejection logs.

---

# Conclusion

This project demonstrates how Object-Oriented Programming can be used to build a reusable ETL framework instead of maintaining multiple independent scripts. By combining abstraction, inheritance, polymorphism, exception handling, and clean separation of responsibilities, the framework can easily support new data sources while remaining maintainable, scalable, and easy to extend.