"""
Data validation functions for FLAVYR MVP.
Validates uploaded restaurant POS CSV files.
"""

import pandas as pd
from typing import Tuple, List


# Required columns for restaurant POS data
REQUIRED_COLUMNS = [
    'date',
    'cuisine_type',
    'dining_model',
    'avg_ticket',
    'covers',
    'labor_cost_pct',
    'food_cost_pct',
    'table_turnover',
    'sales_per_sqft',
    'expected_customer_repeat_rate'
]


def validate_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Check if all required columns exist in the dataframe.

    Args:
        df: Uploaded dataframe to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, errors

    return True, errors


def validate_data_types(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that columns have appropriate data types.

    Args:
        df: Dataframe to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check date column can be parsed
    try:
        pd.to_datetime(df['date'])
    except Exception:
        errors.append("'date' column contains invalid dates. Use format: YYYY-MM-DD")

    # Check numeric columns
    numeric_columns = [
        'avg_ticket', 'covers', 'labor_cost_pct', 'food_cost_pct',
        'table_turnover', 'sales_per_sqft', 'expected_customer_repeat_rate'
    ]

    for col in numeric_columns:
        if col in df.columns:
            try:
                pd.to_numeric(df[col])
            except Exception:
                errors.append(f"'{col}' column contains non-numeric values")

    # Check text columns
    text_columns = ['cuisine_type', 'dining_model']
    for col in text_columns:
        if col in df.columns:
            if not df[col].dtype == 'object':
                errors.append(f"'{col}' should contain text values")

    return len(errors) == 0, errors


def validate_ranges(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that numeric values are within reasonable ranges.

    Args:
        df: Dataframe to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Percentage columns should be between 0 and 100
    percentage_columns = [
        'labor_cost_pct',
        'food_cost_pct',
        'expected_customer_repeat_rate'
    ]

    for col in percentage_columns:
        if col in df.columns:
            # Convert to numeric for validation
            try:
                values = pd.to_numeric(df[col], errors='coerce')
                if values.min() < 0 or values.max() > 100:
                    errors.append(f"'{col}' should be between 0 and 100")
            except Exception:
                pass  # Will be caught by data type validation

    # Positive value columns
    positive_columns = [
        'avg_ticket', 'covers', 'table_turnover', 'sales_per_sqft'
    ]

    for col in positive_columns:
        if col in df.columns:
            try:
                values = pd.to_numeric(df[col], errors='coerce')
                if values.min() < 0:
                    errors.append(f"'{col}' should contain only positive values")
            except Exception:
                pass  # Will be caught by data type validation

    return len(errors) == 0, errors


def validate_missing_values(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Check for missing values in required columns.

    Args:
        df: Dataframe to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                errors.append(f"'{col}' has {missing_count} missing values")

    return len(errors) == 0, errors


def validate_restaurant_csv(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Run all validation checks on uploaded restaurant CSV.

    Args:
        df: Uploaded dataframe to validate

    Returns:
        Tuple of (is_valid, list_of_all_errors)
    """
    all_errors = []

    # Run all validation checks
    checks = [
        validate_columns(df),
        validate_data_types(df),
        validate_ranges(df),
        validate_missing_values(df)
    ]

    # Collect all errors
    for is_valid, errors in checks:
        all_errors.extend(errors)

    is_valid = len(all_errors) == 0

    return is_valid, all_errors
