# utils/ - Helper Functions

## Purpose
Utility functions and validators for FLAVYR MVP.

## Files

### validators.py
Data validation functions for aggregated POS CSV files:
- Column validation (check required columns exist)
- Data type validation (ensure correct types)
- Range validation (percentages 0-100, positive numbers)
- Missing value handling
- User-friendly error message generation

### transaction_validator.py
Transaction-level data validation functions:
- Transaction CSV format validation
- Required columns: date, total, customer_id, item_name, day_of_week
- Data quality checks (minimum transactions, date range)
- Data cleaning and preparation
- Warning system for data quality issues

## Usage
- Import `validators.py` in data_loader.py for aggregated POS data validation
- Import `transaction_validator.py` in app.py for transaction-level data validation

## Design Principles
- Pure functions (no side effects)
- Clear error messages for users
- Reusable across different data sources
- Simple validation logic
