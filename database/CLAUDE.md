# database/ - Data Storage

## Purpose
SQLite database storage for FLAVYR MVP.

## Database File
`flavyr.db` - Local SQLite database (created on first run)

## Schema

### restaurants table
Stores uploaded restaurant POS data after aggregation:
- id (PRIMARY KEY)
- upload_date (TIMESTAMP)
- cuisine_type (TEXT)
- dining_model (TEXT)
- avg_ticket (REAL)
- covers (INTEGER)
- labor_cost_pct (REAL)
- food_cost_pct (REAL)
- table_turnover (REAL)
- sales_per_sqft (REAL)
- expected_customer_repeat_rate (REAL)

### benchmarks table
Industry benchmark data loaded from CSV:
- cuisine_type (TEXT)
- dining_model (TEXT)
- avg_ticket (REAL)
- covers (INTEGER)
- labor_cost_pct (REAL)
- food_cost_pct (REAL)
- table_turnover (REAL)
- sales_per_sqft (REAL)
- expected_customer_repeat_rate (REAL)
- PRIMARY KEY (cuisine_type, dining_model)

### deal_bank table
Deal recommendations mapped to business problems:
- id (PRIMARY KEY)
- business_problem (TEXT)
- deal_types (TEXT)
- rationale (TEXT)

### transactions table
Transaction-level data for granular analytics:
- id (PRIMARY KEY)
- restaurant_id (INTEGER, FOREIGN KEY)
- date (TEXT)
- total (REAL)
- customer_id (TEXT)
- item_name (TEXT)
- day_of_week (TEXT)

## Usage
- Database is automatically initialized on first app run
- Benchmark data is loaded from data/sample_industry_benchmark_data.csv
- Deal bank data is loaded from data/deal_bank_strategy_matrix.csv
- Transaction data is uploaded via Transaction Insights tab
- Restaurant aggregated metrics are derived from transaction data

## Notes
- SQLite chosen for simplicity (no server required)
- Local file storage for MVP phase
- Will migrate to cloud database in later phases
