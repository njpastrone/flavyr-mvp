# FLAVYR MVP - Phase 1 Implementation Plan

## Data Structure Analysis

### 1. Sample Restaurant POS Data
**File**: [data/sample_restaurant_pos_data.csv](../data/sample_restaurant_pos_data.csv)

Daily operational data for one restaurant (September 2025):
- **Identifiers**: `date`, `cuisine_type`, `dining_model`
- **Performance Metrics**:
  - `avg_ticket` (average check size)
  - `covers` (customers served)
  - `labor_cost_pct`, `food_cost_pct`
  - `table_turnover`
  - `sales_per_sqft`
  - `expected_customer_repeat_rate`
- **Format**: 30 days of daily records for an American Full Service restaurant

### 2. Industry Benchmark Data
**File**: [data/sample_industry_benchmark_data.csv](../data/sample_industry_benchmark_data.csv)

Average metrics by restaurant type:
- **10 restaurant types** (cuisine + dining model combinations)
- **Same metrics** as POS data for direct comparison
- Examples: American Full Service, Mexican Fast Casual, Japanese Full Service, etc.

### 3. Deal Bank Strategy Matrix
**File**: [data/deal_bank_strategy_matrix.csv](../data/deal_bank_strategy_matrix.csv)

Maps business problems to deal types:
- **8 business problems**: Increase sales quantity, attract new customers, enhance margins, boost AOV, foster loyalty, improve slow days, inventory management
- **Deal types**: Holiday Deals, Loyalty Offerings, Bundles, Traffic Driver Discounts, Event Leveraging
- **Rationale**: Explains mechanism of impact for each recommendation

## Key Implementation Insights

1. **Direct mapping possible**: Restaurant data columns match benchmark columns exactly
2. **Aggregation needed**: POS data is daily; need to calculate monthly/overall averages
3. **Gap identification logic**: Simple percentage comparison (e.g., restaurant avg vs benchmark avg)
4. **Deal matching**: Map performance gaps to business problems, then to deal types

---

## Comprehensive MVP Development Plan

### **Phase 1: Project Setup & Structure** (Day 1-2)

**Create directory structure:**
```
flavyr-mvp/
├── app.py                    # Main Streamlit app
├── data/                     # Data files (already exists)
│   └── CLAUDE.md            # Data directory context
├── src/                      # Core application logic
│   ├── __init__.py
│   ├── data_loader.py       # Load CSVs and validate
│   ├── analyzer.py          # Gap analysis logic
│   ├── recommender.py       # Deal recommendation engine
│   ├── report_generator.py  # Generate reports
│   └── CLAUDE.md            # Source code context
├── database/                # SQLite database storage
│   └── CLAUDE.md            # Database context
├── utils/                   # Helper functions
│   ├── __init__.py
│   ├── validators.py        # Data validation
│   └── CLAUDE.md            # Utils context
├── requirements.txt         # Dependencies
└── README.md               # User-facing documentation
```

**Dependencies (requirements.txt):**
- streamlit
- pandas
- matplotlib / plotly (for visualizations)
- fpdf or reportlab (for PDF generation)

---

### **Phase 2: Data Layer** (Day 3-5)

#### Build `src/data_loader.py`
- Load benchmark data into SQLite on startup
- Validate uploaded restaurant CSV (check columns, data types)
- Calculate aggregated metrics from daily POS data
- Store restaurant data in SQLite

**Key Functions:**
```python
def load_benchmark_data()
def validate_restaurant_csv(file)
def aggregate_daily_to_monthly(dataframe)
def store_restaurant_data(dataframe, db_connection)
```

#### Build `utils/validators.py`
- Check required columns exist
- Validate data ranges (e.g., percentages 0-100)
- Handle missing values
- Return validation errors with helpful messages

**Key Functions:**
```python
def validate_columns(df, required_columns)
def validate_data_types(df)
def validate_ranges(df)
```

---

### **Phase 3: Analysis Engine** (Day 6-10)

#### Build `src/analyzer.py`

**Core Logic:**
1. Match restaurant to correct benchmark (by `cuisine_type` + `dining_model`)
2. Calculate performance gaps for each KPI:
   ```python
   gap_pct = ((restaurant_metric - benchmark_metric) / benchmark_metric) * 100
   ```
3. Identify underperforming areas (negative gaps)
4. Rank issues by severity

**Key Functions:**
```python
def get_matching_benchmark(cuisine_type, dining_model)
def calculate_gaps(restaurant_metrics, benchmark_metrics)
def identify_underperforming_kpis(gaps, threshold=-5.0)
def rank_issues_by_severity(gaps)
```

**Example Logic:**
- Restaurant avg_ticket: $33.50
- Benchmark avg_ticket: $35.00
- Gap: -4.3% (underperforming)

---

### **Phase 4: Recommendation Engine** (Day 11-15)

#### Build `src/recommender.py`

**Core Logic:**
1. Map performance gaps to business problems
2. Query Deal Bank for relevant deal types
3. Return ranked recommendations with rationale

**Gap-to-Problem Mapping:**
```python
if covers_gap < -10%:
    problems.append("Increase Quantity of Sales")
if avg_ticket_gap < -10%:
    problems.append("Boost Average Order Value")
if repeat_rate_gap < -10%:
    problems.append("Foster Customer Loyalty")
if sales_per_sqft_gap < -10%:
    problems.append("Improve Slow Days")
# etc.
```

**Key Functions:**
```python
def map_gaps_to_problems(gaps, thresholds)
def get_deal_recommendations(problems, deal_bank)
def rank_recommendations(recommendations, gap_severity)
```

---

### **Phase 5: Streamlit Dashboard** (Day 16-22)

#### Build `app.py` with Multiple Pages

**Page 1: Upload**
- File uploader for CSV
- Display preview of uploaded data
- Validate and confirm
- Store in session state

**Page 2: Dashboard**
- Show restaurant info (cuisine, model)
- KPI cards comparing restaurant vs benchmark
- Visual indicators (green/red) for performance
- Bar charts showing gaps

**Page 3: Recommendations**
- List identified problems
- Show recommended deal types
- Display rationale from Deal Bank
- Allow filtering/sorting

**Page 4: Report**
- Generate downloadable PDF/HTML summary
- Include all KPIs, gaps, and recommendations
- Professional formatting

**Key UI Components:**
- Metric cards with delta indicators
- Interactive charts (Plotly bar charts)
- Data tables with formatting
- Download buttons

---

### **Phase 6: Report Generation** (Day 23-25)

#### Build `src/report_generator.py`

**Report Structure:**
1. **Executive Summary**
   - Restaurant overview
   - Overall performance grade
   - Top 3 issues

2. **KPI Comparison Table**
   - All metrics side-by-side
   - Restaurant vs Benchmark
   - Gap percentages

3. **Gap Analysis**
   - Detailed breakdown of underperforming areas
   - Severity rankings

4. **Deal Recommendations**
   - Top 3-5 recommended deals
   - Business problem addressed
   - Expected impact rationale

**Key Functions:**
```python
def generate_executive_summary(gaps, recommendations)
def create_kpi_table(restaurant_data, benchmark_data, gaps)
def format_recommendations(recommendations)
def export_to_pdf(report_content)
def export_to_html(report_content)
```

---

### **Phase 7: Testing & Refinement** (Day 26-30)

**Testing Tasks:**
- Test with sample data provided
- Create 2-3 additional synthetic restaurant datasets
- Validate gap calculations are mathematically correct
- Test edge cases (missing data, extreme values)
- Refine UI/UX based on usability testing
- Prepare documentation for pilot testing

**Validation Checks:**
- Gap calculation accuracy
- Benchmark matching logic
- Deal recommendation relevance
- Report generation completeness

---

## Technical Decisions & Implementation Details

### Database Schema

**Tables:**
1. `restaurants`
   - id, cuisine_type, dining_model, upload_date
   - avg_ticket, covers, labor_cost_pct, food_cost_pct, etc.

2. `benchmarks`
   - cuisine_type, dining_model
   - avg_ticket, covers, labor_cost_pct, food_cost_pct, etc.

3. `deal_bank`
   - business_problem, deal_type, rationale

### Key Algorithms

**Aggregation Logic:**
```python
# Calculate mean of daily metrics for restaurant comparison
restaurant_avg_ticket = daily_data['avg_ticket'].mean()
restaurant_covers = daily_data['covers'].sum()
restaurant_labor_pct = daily_data['labor_cost_pct'].mean()
```

**Gap Threshold:**
- Start with **-5%** or **-10%** gap as "underperforming"
- Configurable via settings

**Deal Ranking:**
- Prioritize by gap severity (larger negative gaps = higher priority)
- Secondary: deal type frequency (avoid over-recommending same deal type)

---

## Success Metrics for Phase 1

1. **Functional completeness**: All 4 dashboard pages working
2. **Data accuracy**: Gap calculations validated
3. **Usability**: Non-technical user can upload data and understand results
4. **Report quality**: Professional, actionable recommendations
5. **Pilot readiness**: 3-5 restaurants can test and provide feedback

---

## Next Steps After Phase 1

1. Conduct pilot with 3-5 NYC restaurants
2. Gather feedback on:
   - Dashboard clarity
   - KPI relevance
   - Recommendation usefulness
   - Report actionability
3. Iterate based on feedback
4. Prepare for Phase 2 (Smart Clustering)

---

## Risk Mitigation

**Potential Issues:**
- Benchmark data may not cover all restaurant types → Start with limited cuisine/model options
- Gap thresholds may need tuning → Make configurable
- Deal recommendations may not align with real needs → Validate in pilot
- CSV format inconsistencies → Provide clear template and validation

**Contingencies:**
- Keep UI simple and intuitive
- Provide sample data and templates
- Include help text throughout app
- Prepare troubleshooting guide for pilot users
