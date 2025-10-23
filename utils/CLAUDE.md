# utils/ - Helper Functions

## Purpose
Utility functions and validators for FLAVYR MVP.

## Files

### validators.py
Data validation functions for uploaded CSV files:
- Column validation (check required columns exist)
- Data type validation (ensure correct types)
- Range validation (percentages 0-100, positive numbers)
- Missing value handling
- User-friendly error message generation

## Usage
Import validators in data_loader.py to validate uploaded restaurant data before processing.

## Design Principles
- Pure functions (no side effects)
- Clear error messages for users
- Reusable across different data sources
- Simple validation logic
