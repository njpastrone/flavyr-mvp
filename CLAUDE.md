# FLAVYR MVP - Project Overview

## What This Project Is

FLAVYR is a data-driven restaurant performance diagnostic platform that helps restaurants identify operational issues and receive targeted deal recommendations based on industry benchmarks.

## Current Status

**Phase 1 MVP COMPLETE** - Fully functional application ready for pilot testing.

## Project Structure

```
flavyr-mvp/
├── CLAUDE.md                    # This file - project overview
├── README.md                    # User guide and quick start
├── IMPLEMENTATION_SUMMARY.md    # Complete implementation details
├── app.py                       # Main Streamlit application
├── requirements.txt             # Python dependencies
├── test_app.py                  # Test script
├── .gitignore                   # Git exclusions
├── planning_docs/               # All planning and architecture documents
│   └── CLAUDE.md               # Planning docs context
├── data/                        # Sample data and benchmarks
│   ├── sample_restaurant_pos_data.csv
│   ├── sample_industry_benchmark_data.csv
│   └── deal_bank_strategy_matrix.csv
├── database/                    # SQLite database (auto-created)
│   ├── CLAUDE.md               # Database schema documentation
│   └── flavyr.db               # Local SQLite database
├── src/                         # Core application logic
│   ├── CLAUDE.md               # Source code documentation
│   ├── data_loader.py          # Data loading and validation
│   ├── analyzer.py             # Performance gap analysis
│   ├── recommender.py          # Deal recommendations
│   └── report_generator.py     # PDF/HTML reports
└── utils/                       # Helper functions
    ├── CLAUDE.md               # Utils documentation
    └── validators.py           # Data validation
```

## Core Functionality (Phase 1)

1. **Data Upload** - Restaurants upload POS data via CSV
2. **Benchmark Comparison** - Compare restaurant KPIs against industry averages
3. **Gap Analysis** - Identify underperforming metrics
4. **Deal Recommendations** - Suggest promotions from Deal Bank to address issues
5. **Dashboard & Reports** - Streamlit interface with downloadable reports

## Tech Stack

- **Language**: Python 3.10+
- **Frontend**: Streamlit
- **Database**: SQLite (local file)
- **Data Processing**: Pandas
- **Hosting**: Local (MVP), Cloud later

## Key Principles

**ALWAYS read [planning_docs/principles.md](planning_docs/principles.md) before making any decisions.**

Critical rules:
- Python only for MVP
- Beginner-friendly, simple code
- Streamlit for frontend
- No emojis anywhere
- Minimize codebase size
- Make autonomous decisions
- Every folder has its own CLAUDE.md

## Data Schema (Phase 1)

Core metrics tracked:
- `avg_ticket` - Average check size
- `covers` - Number of customers served
- `labor_cost_pct` - Labor cost as % of revenue
- `food_cost_pct` - Food cost as % of revenue
- `table_turnover` - Tables turned per service period
- `sales_per_sqft` - Revenue per square foot
- Plus: promo data, customer metrics, etc.

## Development Timeline

**Phase 1 Target**: 4-6 weeks (part-time development)

Week 1-2: Data upload & validation, benchmark loading
Week 3: Gap analysis implementation
Week 4: Deal recommendations & report generation
Week 5: Testing & pilot with 3-5 restaurants

## Important Files to Reference

- [planning_docs/principles.md](planning_docs/principles.md) - NON-NEGOTIABLE rules
- [planning_docs/FLAVYR_Technical_Roadmap_Final.md](planning_docs/FLAVYR_Technical_Roadmap_Final.md) - Full product roadmap
- [planning_docs/FLAVYR_MVP_System_Architecture_Phase1.md](planning_docs/FLAVYR_MVP_System_Architecture_Phase1.md) - Phase 1 architecture
- [planning_docs/FLAVYR_Phase1_Technical_Plan_Natural_Language.md](planning_docs/FLAVYR_Phase1_Technical_Plan_Natural_Language.md) - Phase 1 implementation guide

## Future Phases

- **Phase 2**: Smart clustering (personalized peer groupings)
- **Phase 3**: Causal impact measurement (deal effectiveness)
- **Phase 4**: POS integration & automation

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

# Run tests
python test_app.py
```

## Implementation Complete

All Phase 1 features have been implemented:
- [x] CSV upload with validation
- [x] Industry benchmark comparison (10 restaurant types)
- [x] Performance gap analysis (7 KPIs)
- [x] Deal recommendation engine
- [x] Interactive Streamlit dashboard (4 pages)
- [x] PDF and HTML report generation
- [x] SQLite database with automated setup
- [x] Comprehensive testing and validation

See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for complete details.

## Next Steps

1. **Pilot Testing** - Deploy to 3-5 NYC restaurants
2. **Feedback Collection** - Gather insights on usability and accuracy
3. **Iteration** - Refine based on pilot feedback
4. **Phase 2 Planning** - Prepare for Smart Clustering implementation
