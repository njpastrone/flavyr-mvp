# FLAVYR MVP - Restaurant Performance Diagnostic Platform

Phase 1 MVP: Benchmark comparison, gap analysis, and deal recommendations.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Upload Page
1. Click "Upload" in the sidebar
2. Upload your restaurant's POS data CSV file
3. Review the data preview
4. Click "Process Data"

### Dashboard Page
- View your performance grade
- See KPI comparisons vs industry benchmarks
- Analyze performance gaps with visual charts

### Recommendations Page
- Review identified business problems
- See recommended deal types
- Understand the rationale behind each recommendation

### Report Page
- Generate downloadable PDF or HTML reports
- Share performance insights with your team

## CSV Format

Your POS data CSV must include these columns:

- `date` - Date in YYYY-MM-DD format
- `cuisine_type` - Restaurant cuisine (e.g., "American", "Italian")
- `dining_model` - Service model (e.g., "Full Service", "Fast Casual")
- `avg_ticket` - Average check size ($)
- `covers` - Number of customers served
- `labor_cost_pct` - Labor cost as % of revenue (0-100)
- `food_cost_pct` - Food cost as % of revenue (0-100)
- `table_turnover` - Tables turned per service period
- `sales_per_sqft` - Revenue per square foot ($)
- `expected_customer_repeat_rate` - Repeat customer rate (0-1)

See `data/sample_restaurant_pos_data.csv` for an example.

## Testing

Run the test script to validate functionality:

```bash
python test_app.py
```

## Project Structure

```
flavyr-mvp/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── data/                     # Sample data and benchmarks
│   ├── sample_restaurant_pos_data.csv
│   ├── sample_industry_benchmark_data.csv
│   └── deal_bank_strategy_matrix.csv
├── database/                 # SQLite database (auto-created)
│   └── flavyr.db
├── src/                      # Core application logic
│   ├── data_loader.py        # Data loading and validation
│   ├── analyzer.py           # Performance gap analysis
│   ├── recommender.py        # Deal recommendations
│   └── report_generator.py   # PDF/HTML reports
└── utils/                    # Helper functions
    └── validators.py         # Data validation
```

## Key Features

- CSV upload with validation
- Industry benchmark comparison
- Performance gap analysis (7 KPIs)
- Deal recommendations mapped to business problems
- Interactive dashboard with charts
- Downloadable PDF and HTML reports

## Next Steps

After testing the MVP:
1. Pilot with 3-5 restaurants
2. Gather feedback on insights and recommendations
3. Iterate based on pilot results
4. Prepare for Phase 2 (Smart Clustering)

## Support

For issues or questions, refer to the planning documentation in `planning_docs/`.
