# 📰 Articles Code Challenge

## Overview

This project is a command-line and module-based Python application that manages a system of **Authors**, **Magazines**, and **Articles**. It uses SQLite for persistent data storage and is structured using Object-Oriented Programming principles.

The application supports:

- Creating and managing authors, magazines, and articles
- Establishing relationships between models (e.g., authors write articles, magazines publish them)
- Running tests with `pytest` to validate functionality
- Seeding and resetting the database using a simple script

---

## 🗂️ Project Structure

articles-code-challenge/
│
├── lib/
│ ├── db/
│ │ ├── connection.py # Handles SQLite DB connection
│ │ ├── schema.sql # SQL schema for initializing tables
│ │ └── seed.py # Seeds the database with initial data
│ ├── models/
│ │ ├── author.py # Author model
│ │ ├── magazine.py # Magazine model
│ │ └── article.py # Article model
│ └── init.py
│
├── tests/
│ ├── test_author.py # Tests for Author model
│ ├── test_magazine.py # Tests for Magazine model
│ └── test_article.py # Tests for Article model
│
├── scripts/
│ ├── run_queries.py # Optional script to run custom DB queries
│ └── setup_db.py # Reinitializes the database schema
│
├── .gitignore
├── README.md
├── Pipfile / requirements.txt 

---

## 📦 Requirements

- Python 3.9+
- `pipenv` or `virtualenv` (recommended)

Install dependencies:

```bash
pip install -r requirements.txt
# or if using pipenv:
pipenv install
```

---

## Usage

### Setting up the database

To initialize or reset the database schema and seed it with initial data, run:

```bash

python3 -m lib.db.seed
```

### Running the application

This project is primarily a module-based system. You can interact with the models via Python scripts or an interactive shell:

```bash
python
>>> from lib.models.author import Author
>>> author = Author("lenny kimanthi")
>>> author.save()
```

### Running tests

Run the test suite using `pytest`:

```bash
pytest
```
HAPPY CODING LADS.....