"""
Data loading and storage functions for FLAVYR MVP.
Handles benchmark data, restaurant data, and SQLite operations.
"""

import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from utils.validators import validate_restaurant_csv


# Database path
DB_PATH = Path(__file__).parent.parent / 'database' / 'flavyr.db'

# Data file paths
BENCHMARK_DATA_PATH = Path(__file__).parent.parent / 'data' / 'sample_industry_benchmark_data.csv'
DEAL_BANK_PATH = Path(__file__).parent.parent / 'data' / 'deal_bank_strategy_matrix.csv'


def get_db_connection():
    """
    Create and return a connection to the SQLite database.

    Returns:
        sqlite3.Connection object
    """
    conn = sqlite3.connect(DB_PATH)
    return conn


def initialize_database():
    """
    Initialize the SQLite database with required tables.
    Creates tables for restaurants, benchmarks, and deal bank.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create restaurants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upload_date TEXT NOT NULL,
            cuisine_type TEXT NOT NULL,
            dining_model TEXT NOT NULL,
            avg_ticket REAL NOT NULL,
            covers INTEGER NOT NULL,
            labor_cost_pct REAL NOT NULL,
            food_cost_pct REAL NOT NULL,
            table_turnover REAL NOT NULL,
            sales_per_sqft REAL NOT NULL,
            expected_customer_repeat_rate REAL NOT NULL
        )
    ''')

    # Create benchmarks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS benchmarks (
            cuisine_type TEXT NOT NULL,
            dining_model TEXT NOT NULL,
            avg_ticket REAL NOT NULL,
            covers INTEGER NOT NULL,
            labor_cost_pct REAL NOT NULL,
            food_cost_pct REAL NOT NULL,
            table_turnover REAL NOT NULL,
            sales_per_sqft REAL NOT NULL,
            expected_customer_repeat_rate REAL NOT NULL,
            PRIMARY KEY (cuisine_type, dining_model)
        )
    ''')

    # Create deal_bank table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deal_bank (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_problem TEXT NOT NULL,
            deal_types TEXT NOT NULL,
            rationale TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def load_benchmark_data():
    """
    Load industry benchmark data from CSV into SQLite database.
    Only loads if the benchmarks table is empty.
    """
    conn = get_db_connection()

    # Check if benchmarks already loaded
    existing_count = pd.read_sql_query(
        "SELECT COUNT(*) as count FROM benchmarks",
        conn
    )['count'][0]

    if existing_count == 0:
        # Load benchmark data from CSV
        df = pd.read_csv(BENCHMARK_DATA_PATH)
        df.to_sql('benchmarks', conn, if_exists='replace', index=False)

    conn.close()


def load_deal_bank_data():
    """
    Load deal bank strategy matrix from CSV into SQLite database.
    Only loads if the deal_bank table is empty.
    """
    conn = get_db_connection()

    # Check if deal bank already loaded
    existing_count = pd.read_sql_query(
        "SELECT COUNT(*) as count FROM deal_bank",
        conn
    )['count'][0]

    if existing_count == 0:
        # Load deal bank data from CSV
        df = pd.read_csv(DEAL_BANK_PATH)
        # Rename columns to match database schema
        df = df.rename(columns={
            'Business Problem': 'business_problem',
            'Best Deal Types': 'deal_types',
            'Rationale / Mechanism of Impact': 'rationale'
        })
        df.to_sql('deal_bank', conn, if_exists='replace', index=False)

    conn.close()


def aggregate_daily_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate daily POS data to calculate overall averages.

    Args:
        df: Daily POS data

    Returns:
        Single-row dataframe with aggregated metrics
    """
    # Get cuisine type and dining model (should be same for all rows)
    cuisine_type = df['cuisine_type'].iloc[0]
    dining_model = df['dining_model'].iloc[0]

    # Calculate aggregated metrics
    aggregated = {
        'cuisine_type': cuisine_type,
        'dining_model': dining_model,
        'avg_ticket': df['avg_ticket'].mean(),
        'covers': int(df['covers'].sum()),  # Total covers
        'labor_cost_pct': df['labor_cost_pct'].mean(),
        'food_cost_pct': df['food_cost_pct'].mean(),
        'table_turnover': df['table_turnover'].mean(),
        'sales_per_sqft': df['sales_per_sqft'].mean(),
        'expected_customer_repeat_rate': df['expected_customer_repeat_rate'].mean()
    }

    return pd.DataFrame([aggregated])


def store_restaurant_data(df: pd.DataFrame) -> int:
    """
    Store restaurant data in SQLite database after aggregation.

    Args:
        df: Aggregated restaurant data (single row)

    Returns:
        ID of the inserted restaurant record
    """
    conn = get_db_connection()

    # Add upload date
    df_copy = df.copy()
    df_copy['upload_date'] = datetime.now().isoformat()

    # Reorder columns to match table schema
    column_order = [
        'upload_date', 'cuisine_type', 'dining_model', 'avg_ticket',
        'covers', 'labor_cost_pct', 'food_cost_pct', 'table_turnover',
        'sales_per_sqft', 'expected_customer_repeat_rate'
    ]
    df_copy = df_copy[column_order]

    # Insert into database
    df_copy.to_sql('restaurants', conn, if_exists='append', index=False)

    # Get the ID of the inserted record
    cursor = conn.cursor()
    cursor.execute("SELECT last_insert_rowid()")
    restaurant_id = cursor.fetchone()[0]

    conn.close()

    return restaurant_id


def validate_and_load_restaurant_csv(uploaded_file) -> Tuple[bool, Optional[pd.DataFrame], list]:
    """
    Validate and load uploaded restaurant CSV file.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Tuple of (success, dataframe, errors)
    """
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Validate
        is_valid, errors = validate_restaurant_csv(df)

        if not is_valid:
            return False, None, errors

        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])

        # Convert numeric columns
        numeric_columns = [
            'avg_ticket', 'covers', 'labor_cost_pct', 'food_cost_pct',
            'table_turnover', 'sales_per_sqft', 'expected_customer_repeat_rate'
        ]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col])

        return True, df, []

    except Exception as e:
        return False, None, [f"Error reading CSV file: {str(e)}"]


def get_restaurant_data(restaurant_id: int) -> Optional[pd.DataFrame]:
    """
    Retrieve restaurant data from database by ID.

    Args:
        restaurant_id: Restaurant record ID

    Returns:
        Dataframe with restaurant data or None if not found
    """
    conn = get_db_connection()
    query = "SELECT * FROM restaurants WHERE id = ?"
    df = pd.read_sql_query(query, conn, params=(restaurant_id,))
    conn.close()

    if len(df) == 0:
        return None

    return df


def get_benchmark_data(cuisine_type: str, dining_model: str) -> Optional[pd.DataFrame]:
    """
    Retrieve benchmark data for a specific restaurant type.

    Args:
        cuisine_type: Restaurant cuisine type
        dining_model: Restaurant dining model

    Returns:
        Dataframe with benchmark data or None if not found
    """
    conn = get_db_connection()
    query = """
        SELECT * FROM benchmarks
        WHERE cuisine_type = ? AND dining_model = ?
    """
    df = pd.read_sql_query(query, conn, params=(cuisine_type, dining_model))
    conn.close()

    if len(df) == 0:
        return None

    return df


def get_all_deal_bank_data() -> pd.DataFrame:
    """
    Retrieve all deal bank data.

    Returns:
        Dataframe with all deal bank records
    """
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM deal_bank", conn)
    conn.close()

    return df


def setup_database():
    """
    Complete database setup: initialize tables and load static data.
    Call this once when the app starts.
    """
    initialize_database()
    load_benchmark_data()
    load_deal_bank_data()
