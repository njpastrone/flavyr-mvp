# data/ - Sample Data and Benchmarks

## Purpose
Contains sample data files used for testing and initial database setup.

## Files

### sample_restaurant_pos_data.csv
Sample daily POS data for an American Full Service restaurant (30 days).

**Columns:**
- date - Daily dates (YYYY-MM-DD format)
- cuisine_type - "American"
- dining_model - "Full Service"
- avg_ticket - Average check size ($)
- covers - Daily customer count
- labor_cost_pct - Labor cost percentage
- food_cost_pct - Food cost percentage
- table_turnover - Tables per service period
- sales_per_sqft - Revenue per square foot
- expected_customer_repeat_rate - Repeat customer rate (0-1)

### sample_industry_benchmark_data.csv
Industry benchmark averages for 10 different restaurant types.

**Restaurant Types Included:**
- American - Full Service
- Italian - Casual Dining
- Mexican - Fast Casual
- Japanese - Full Service
- Vegetarian - Fast Casual
- American - Quick Service
- Indian - Full Service
- Seafood - Casual Dining
- Mediterranean - Fast Casual
- Asian Fusion - Quick Service

**Columns:** Same as restaurant POS data (except no date column)

### sample_transaction_data.csv
Sample transaction-level data for granular analytics (210 transactions over 30 days).

**Columns:**
- date - Transaction date (YYYY-MM-DD format)
- total - Transaction amount ($)
- customer_id - Unique customer identifier
- item_name - Item or product name
- day_of_week - Full day name (Monday, Tuesday, etc.)

**Data Characteristics:**
- 100 unique customers with 82% repeat rate
- 7 menu items with realistic pricing
- 30-day period (September 2025)
- Intentional day-of-week patterns for testing

### deal_bank_strategy_matrix.csv
Deal recommendations mapped to business problems.

**Columns:**
- Business Problem - The operational issue to solve
- Best Deal Types - Recommended promotion types (semicolon-separated)
- Rationale / Mechanism of Impact - Why these deals work

**Business Problems Covered:**
- Increase Quantity of Sales
- Attract New Customers
- Enhance Profit Margins
- Boost Average Order Value (AOV)
- Foster Customer Loyalty
- Improve Slow Days
- Inventory Management

## Usage

### Database Loading (Automatic on Startup)
- Benchmark data → `benchmarks` table
- Deal bank data → `deal_bank` table

### Testing and Templates
- `sample_restaurant_pos_data.csv` - Template for aggregated POS uploads
- `sample_transaction_data.csv` - Template for transaction-level uploads

## Notes

- All CSV files use standard comma separation
- Headers are required and case-sensitive
- Percentage values are stored as 0-100 (not 0-1)
- Files should not be deleted (required for app initialization)
