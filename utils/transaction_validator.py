"""
Transaction Data Validator

Validates transaction-level CSV data for the Transaction Insights module.
Ensures data meets requirements for granular sales analytics.
"""

import pandas as pd
from typing import Tuple, List
from src.config import ValidationConfig


def validate_transaction_csv(df: pd.DataFrame) -> Tuple[bool, str, List[str]]:
    """
    Comprehensive validation of transaction-level CSV data.

    Required columns:
    - date: Transaction date (YYYY-MM-DD format)
    - total: Transaction amount (numeric, positive)
    - customer_id: Customer identifier (string)
    - item_name: Item/product name (string)
    - day_of_week: Day name (Monday, Tuesday, etc.)

    Args:
        df: DataFrame loaded from CSV

    Returns:
        Tuple of (is_valid, error_message, warnings)
    """
    errors = []
    warnings = []

    # Check required columns
    required_columns = ValidationConfig.TRANSACTION_REQUIRED_COLUMNS
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, "; ".join(errors), warnings

    # Check for empty DataFrame
    if df.empty:
        errors.append("CSV file is empty")
        return False, "; ".join(errors), warnings

    # Validate date column
    try:
        dates = pd.to_datetime(df['date'], errors='coerce')
        null_dates = dates.isna().sum()
        if null_dates > 0:
            errors.append(f"{null_dates} invalid date(s) found - use YYYY-MM-DD format")
    except Exception as e:
        errors.append(f"Date column validation failed: {str(e)}")

    # Validate total column
    if not pd.api.types.is_numeric_dtype(df['total']):
        try:
            df['total'] = pd.to_numeric(df['total'], errors='coerce')
            null_totals = df['total'].isna().sum()
            if null_totals > 0:
                errors.append(f"{null_totals} non-numeric transaction total(s) found")
        except Exception:
            errors.append("'total' column must contain numeric values")

    # Check for negative or zero totals
    if (df['total'] <= 0).any():
        negative_count = (df['total'] <= 0).sum()
        warnings.append(f"{negative_count} transaction(s) with zero or negative totals")

    # Validate day_of_week values
    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    invalid_days = df[~df['day_of_week'].isin(valid_days)]
    if not invalid_days.empty:
        errors.append(f"{len(invalid_days)} invalid day_of_week values - must be full day names (Monday, Tuesday, etc.)")

    # Check for null values in required columns
    for col in required_columns:
        null_count = df[col].isna().sum()
        if null_count > 0:
            errors.append(f"{null_count} missing value(s) in '{col}' column")

    # Data quality warnings
    if len(df) < 30:
        warnings.append(f"Only {len(df)} transactions - recommend at least 30 for meaningful analysis")

    unique_customers = df['customer_id'].nunique()
    if unique_customers < 10:
        warnings.append(f"Only {unique_customers} unique customers - results may not be representative")

    unique_items = df['item_name'].nunique()
    if unique_items < 5:
        warnings.append(f"Only {unique_items} unique items - limited menu analysis possible")

    # Date range check
    try:
        date_range = (pd.to_datetime(df['date']).max() - pd.to_datetime(df['date']).min()).days
        if date_range < 7:
            warnings.append(f"Data spans only {date_range} days - recommend at least 7 days for day-of-week analysis")
    except Exception:
        pass

    # Return results
    if errors:
        return False, "; ".join(errors), warnings
    else:
        return True, "Validation successful", warnings


def get_transaction_data_summary(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics for transaction data.

    Args:
        df: Validated transaction DataFrame

    Returns:
        Dictionary with data summary
    """
    try:
        dates = pd.to_datetime(df['date'])
        return {
            'total_transactions': len(df),
            'unique_customers': df['customer_id'].nunique(),
            'unique_items': df['item_name'].nunique(),
            'date_range': {
                'start': dates.min().strftime('%Y-%m-%d'),
                'end': dates.max().strftime('%Y-%m-%d'),
                'days': (dates.max() - dates.min()).days + 1
            },
            'revenue': {
                'total': df['total'].sum(),
                'average': df['total'].mean(),
                'min': df['total'].min(),
                'max': df['total'].max()
            },
            'transactions_per_day': df.groupby('day_of_week').size().to_dict()
        }
    except Exception as e:
        return {'error': f"Could not generate summary: {str(e)}"}


def prepare_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare transaction data for analysis.

    Args:
        df: Raw transaction DataFrame

    Returns:
        Cleaned DataFrame ready for analysis
    """
    # Create a copy
    cleaned = df.copy()

    # Convert date to datetime
    cleaned['date'] = pd.to_datetime(cleaned['date'], errors='coerce')

    # Convert total to numeric
    cleaned['total'] = pd.to_numeric(cleaned['total'], errors='coerce')

    # Strip whitespace from string columns
    for col in ['customer_id', 'item_name', 'day_of_week']:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).str.strip()

    # Remove rows with null values in critical columns
    cleaned = cleaned.dropna(subset=['date', 'total', 'customer_id', 'item_name', 'day_of_week'])

    # Remove transactions with zero or negative totals
    cleaned = cleaned[cleaned['total'] > 0]

    # Sort by date
    cleaned = cleaned.sort_values('date')

    return cleaned


def generate_sample_transaction_format() -> pd.DataFrame:
    """
    Generate a sample DataFrame showing the expected transaction format.

    Returns:
        Sample DataFrame with correct structure
    """
    sample_data = {
        'date': ['2025-10-01', '2025-10-01', '2025-10-01', '2025-10-02', '2025-10-02'],
        'total': [45.50, 32.00, 67.25, 28.75, 52.00],
        'customer_id': ['C001', 'C002', 'C001', 'C003', 'C002'],
        'item_name': ['Burger', 'Salad', 'Steak', 'Pasta', 'Pizza'],
        'day_of_week': ['Monday', 'Monday', 'Monday', 'Tuesday', 'Tuesday']
    }

    return pd.DataFrame(sample_data)
