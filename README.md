# Inventory Management API

A RESTful Inventory Management System built with Flask. Supports full CRUD operations, external product lookups via the OpenFoodFacts API, and a CLI interface for interacting with the API.

## 📌 Overview

This project simulates a small retail company's backend system. Employees can add, view, update, and delete inventory items. They can also fetch real product data from OpenFoodFacts by barcode and import it into the inventory.

Built as a summative lab for Module 5: Python Flask.

## 🛠️ Tech Stack

- **Python 3**
- **Flask** — REST API framework
- **Requests** — external API integration
- **pytest** — testing suite
- **unittest.mock** — mocking external API calls

## 📁 Project Structure

```text
inventory-api/
│
├── app.py                # Flask routes
├── database.py           # In-memory inventory storage
├── external_api.py       # OpenFoodFacts integration
├── cli.py                # CLI interface
├── conftest.py           # pytest config
├── requirements.txt
├── .gitignore
│
├── tests/
│   ├── test_database.py
│   ├── test_external_api.py
│   └── test_app.py
│
└── README.md