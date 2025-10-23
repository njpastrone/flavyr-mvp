# src/ - Core Application Logic

## Purpose
Contains the main business logic for FLAVYR MVP Phase 1.

## Files

### data_loader.py
Handles all data loading and storage operations:
- Load benchmark data from CSV into SQLite
- Validate uploaded restaurant POS CSV files
- Aggregate daily POS data to monthly/overall averages
- Store restaurant data in SQLite database

### analyzer.py
Performance gap analysis engine:
- Match restaurant to correct benchmark by cuisine_type + dining_model
- Calculate performance gaps for all KPIs
- Identify underperforming metrics (threshold: -5% to -10%)
- Rank issues by severity (largest negative gaps first)

### recommender.py
Deal recommendation system:
- Map performance gaps to business problems
- Query Deal Bank for relevant deal types
- Return ranked recommendations with rationale
- Prioritize by gap severity and deal diversity

### report_generator.py
Report creation and export:
- Generate executive summary
- Create KPI comparison tables
- Format gap analysis breakdown
- Export to PDF and HTML formats

## Data Flow
1. User uploads CSV via Streamlit
2. data_loader validates and stores data
3. analyzer compares against benchmarks
4. recommender suggests deals
5. report_generator creates downloadable summary

## Design Principles
- Simple, beginner-friendly code
- Clear function names and docstrings
- Minimal dependencies
- Pure Python logic (no framework coupling)
