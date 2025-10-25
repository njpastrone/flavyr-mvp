# Transaction Metrics Benchmark & Deal Recommendation Integration Plan

## Overview

This document outlines the plan to:
1. Generate industry benchmark data for transaction-level metrics
2. Map transaction metrics to business problems
3. Connect Transaction Analytics Dashboard insights to Deal Recommendations

---

## Part 1: Industry Benchmark Data for Transaction Metrics

### Current State
- Existing benchmarks: `avg_ticket`, `covers`, `expected_customer_repeat_rate`
- Transaction metrics analyzed but NOT benchmarked: Loyalty Rate, AOV by day, slowest days, item rankings

### Proposed New Benchmark Fields

#### A. Customer Loyalty Benchmarks
```csv
cuisine_type,dining_model,benchmark_loyalty_rate,benchmark_repeat_customers_pct
American,Full Service,40.0,0.40
Italian,Casual Dining,43.0,0.43
Mexican,Fast Casual,32.0,0.32
```

**Rationale:** Different restaurant types have different loyalty expectations:
- Full Service: 38-45% (higher due to experience-focused dining)
- Casual Dining: 40-50% (balance of value and experience)
- Fast Casual: 30-38% (convenience-driven, lower loyalty)
- Quick Service: 25-33% (transactional, lowest loyalty)

#### B. AOV Distribution Benchmarks
```csv
cuisine_type,dining_model,benchmark_aov_weekday,benchmark_aov_weekend,benchmark_aov_variation_pct
American,Full Service,32.00,42.00,31.25
Italian,Casual Dining,38.00,48.00,26.32
```

**Rationale:**
- Weekend AOV typically 20-40% higher than weekday
- Variation percentage = (weekend - weekday) / weekday * 100
- Used to identify if restaurant has healthy day-of-week performance spread

#### C. Day Performance Benchmarks
```csv
cuisine_type,dining_model,expected_slowest_day,benchmark_slow_day_transaction_drop_pct
American,Full Service,Monday,35.0
Italian,Casual Dining,Tuesday,30.0
Fast Casual,All,Sunday,25.0
```

**Rationale:**
- Every restaurant type has naturally slow days
- Drop percentage = how much below average the slowest day should be
- Used to identify if slowest day is "normal slow" vs. "problem slow"

#### D. Item Performance Benchmarks
```csv
cuisine_type,dining_model,benchmark_top_item_revenue_share_pct,benchmark_bottom_item_removal_threshold
American,Full Service,18.0,2.0
Italian,Casual Dining,22.0,3.0
```

**Rationale:**
- Top item should drive 15-25% of total revenue (healthy concentration)
- Bottom items <2-3% revenue share should be considered for removal

---

## Part 2: Transaction Metrics → Business Problems Mapping

### Mapping Table

| Transaction Metric | Threshold/Condition | Business Problem | Deal Type Recommendation |
|-------------------|---------------------|------------------|--------------------------|
| **Loyalty Rate < Benchmark** | <30% (critical), <benchmark (warning) | Foster Customer Loyalty | Loyalty Offerings, Holiday Deals |
| **AOV below benchmark** | Overall AOV <90% of benchmark | Boost Average Order Value | Bundling & Fixed-Price Offerings, Leveraging Big Events |
| **AOV variation low** | Weekend/weekday spread <15% | Boost Average Order Value | Weekday-specific bundles, Event-based upsells |
| **Slowest day transactions** | >40% below average | Improve Slow Days | Discount 'Traffic Driver' Items, Weekday bundles |
| **Slowest day revenue** | Different from transaction slowest | Boost Average Order Value | Upsell tactics on that specific day |
| **Bottom items >5 items** | Many low performers | Inventory Management | Bundling to move slow inventory |
| **Top item concentration >30%** | Over-reliance on one item | Increase Quantity of Sales | Promote other items, create variety bundles |
| **Repeat customers <25%** | Very low loyalty | Attract New Customers + Foster Loyalty | Loyalty programs, first-time visitor deals |

### New Business Problems to Add to Deal Bank

Based on transaction insights, we should add these new problem categories:

1. **"Improve Weekday Performance"** - Specific to slow weekdays
2. **"Optimize Menu Mix"** - When item performance is unbalanced
3. **"Increase Weekend AOV"** - When weekend spending is below potential
4. **"Reduce Customer Churn"** - When repeat rate is critically low

---

## Part 3: Implementation Architecture

### File Structure Changes

```
data/
├── sample_industry_benchmark_data.csv (existing - strategic KPIs)
├── transaction_benchmark_data.csv (NEW - tactical KPIs)
├── deal_bank_strategy_matrix.csv (existing - to be expanded)
└── transaction_deal_mapping.csv (NEW - maps transaction issues to deals)
```

### New Data Files to Create

#### 1. `transaction_benchmark_data.csv`
```csv
cuisine_type,dining_model,benchmark_loyalty_rate,benchmark_aov_weekday,benchmark_aov_weekend,benchmark_slowest_day_drop_pct,benchmark_top_item_share_pct
American,Full Service,40.0,32.00,42.00,35.0,20.0
Italian,Casual Dining,43.0,38.00,48.00,30.0,22.0
Mexican,Fast Casual,32.0,18.00,24.00,28.0,18.0
Japanese,Full Service,45.0,45.00,60.00,32.0,25.0
...
```

#### 2. `transaction_deal_mapping.csv`
```csv
Transaction_Issue,Severity_Threshold,Business_Problem,Priority
Low Loyalty Rate,<30%,Foster Customer Loyalty,High
Low AOV,<benchmark_aov * 0.9,Boost Average Order Value,High
High Slow Day Drop,>40%,Improve Slow Days,Medium
Menu Imbalance,Top item >30% OR >5 bottom items <2%,Inventory Management,Medium
Low Weekend Uplift,Weekend/Weekday ratio <1.15,Boost Average Order Value,Low
```

---

## Part 4: Code Integration Plan

### Step 1: Create Transaction Benchmark Loader
**File:** `src/data_loader.py`

Add function:
```python
def get_transaction_benchmarks(cuisine_type: str, dining_model: str) -> pd.DataFrame:
    """Load transaction-level benchmarks for restaurant type."""
    # Load transaction_benchmark_data.csv
    # Filter by cuisine_type and dining_model
    # Return benchmark values
```

### Step 2: Create Transaction Performance Analyzer
**File:** `src/transaction_performance_analyzer.py` (NEW)

Functions:
```python
def analyze_loyalty_performance(actual_loyalty: float, benchmark: float) -> dict
def analyze_aov_performance(aov_by_day: dict, benchmarks: dict) -> dict
def analyze_day_performance(slowest_day_data: dict, benchmarks: dict) -> dict
def analyze_item_performance(items_data: dict, benchmarks: dict) -> dict
def generate_transaction_performance_report(transaction_results, benchmarks) -> dict
```

### Step 3: Update Recommender
**File:** `src/recommender.py`

Add:
```python
def generate_transaction_recommendations(
    transaction_performance: dict,
    deal_bank_df: pd.DataFrame
) -> dict:
    """
    Generate deal recommendations based on transaction-level insights.

    Maps transaction issues to business problems and suggests deals.
    """
    # Map transaction issues to business problems
    # Rank by severity
    # Return structured recommendations
```

### Step 4: Update Dashboard Display
**File:** `app.py` - `transaction_dashboard_page()`

Add benchmark comparison indicators:
- Show loyalty rate with benchmark comparison (green/yellow/red)
- Show AOV with benchmark ranges
- Highlight slowest day severity (is this normal or problem?)
- Item performance flags (concentration risk, removal candidates)

---

## Part 5: Integration Workflow

### Current Flow
```
Transaction Upload
    ↓
Transaction Analysis (tactical insights only)
    ↓
Derive Aggregated Metrics (avg_ticket, covers, repeat_rate)
    ↓
Strategic Analysis (benchmark comparison on aggregated metrics)
    ↓
Deal Recommendations (based on strategic gaps)
```

### Proposed Enhanced Flow
```
Transaction Upload
    ↓
Transaction Analysis (tactical insights)
    ↓
[NEW] Transaction Benchmark Comparison
    ↓
    ├─→ Derive Aggregated Metrics
    │       ↓
    │   Strategic Analysis (existing)
    │       ↓
    │   Strategic Recommendations
    │
    └─→ [NEW] Transaction Performance Analysis
            ↓
        [NEW] Transaction-Level Recommendations
            ↓
        [NEW] Combined Recommendation Report
            (Strategic + Tactical)
```

---

## Part 6: Recommendation Output Format

### Enhanced Recommendations Structure

```python
{
    "strategic_recommendations": [
        {
            "source": "strategic_kpi",
            "business_problem": "Boost Average Order Value",
            "severity": -15.2,
            "metric": "avg_ticket",
            "your_value": 29.50,
            "benchmark": 35.00,
            "deal_types": ["Bundling & Fixed-Price Offerings", "Leveraging Big Events"],
            "rationale": "..."
        }
    ],
    "tactical_recommendations": [
        {
            "source": "transaction_insight",
            "business_problem": "Improve Slow Days",
            "severity": "high",
            "metric": "slowest_day_transactions",
            "your_value": "Monday (45 transactions)",
            "benchmark": "Monday typically 35% below average",
            "actual_drop": "52% below average",
            "deal_types": ["Discount 'Traffic Driver' Items", "Weekday bundles"],
            "rationale": "Your Monday traffic is significantly below industry norms...",
            "actionable_insight": "Run a 'Monday Madness' promotion featuring your top-selling items at 15% off"
        },
        {
            "source": "transaction_insight",
            "business_problem": "Foster Customer Loyalty",
            "severity": "critical",
            "metric": "loyalty_rate",
            "your_value": "24.5%",
            "benchmark": "40.0%",
            "gap": "-15.5 percentage points",
            "deal_types": ["Loyalty Offerings", "Holiday Deals"],
            "rationale": "Only 24.5% of customers return - well below 40% industry standard...",
            "actionable_insight": "Launch a points-based loyalty program with sign-up incentive"
        }
    ],
    "priority_actions": [
        "Critical: Launch loyalty program to address 24.5% repeat rate",
        "High: Implement Monday traffic driver promotion",
        "Medium: Introduce weekend upsell bundles to increase AOV"
    ]
}
```

---

## Part 7: Dashboard Display Enhancements

### Visual Indicators to Add

1. **Loyalty Rate Card**
   ```
   Loyalty Rate: 24.5% [RED]
   Benchmark: 40.0%
   Gap: -15.5 pp (Below Industry Standard)
   ```

2. **AOV Chart Enhancement**
   - Add benchmark line overlay
   - Shade "healthy range" zone
   - Flag days outside acceptable variance

3. **Slowest Day Analysis**
   ```
   Your Slowest Day: Monday (45 transactions)
   Expected Slowest Day: Monday ✓
   Severity: 52% below average [CRITICAL]
   Industry Norm: 35% below average
   Status: Needs Attention [RED]
   ```

4. **Item Performance Flags**
   ```
   Top Item Concentration: 32% [WARNING]
   (Benchmark: <25% healthy)

   Removal Candidates: 7 items <2% revenue share
   (Benchmark: Consider removing items <2%)
   ```

---

## Part 8: Implementation Phases

### Phase 1: Generate Benchmark Data (Week 1)
- [ ] Create transaction_benchmark_data.csv with 10 restaurant types
- [ ] Create transaction_deal_mapping.csv
- [ ] Add new business problems to deal_bank_strategy_matrix.csv

### Phase 2: Build Analysis Engine (Week 1-2)
- [ ] Create transaction_performance_analyzer.py
- [ ] Add get_transaction_benchmarks() to data_loader.py
- [ ] Write unit tests for benchmark comparison logic

### Phase 3: Integrate with Recommendations (Week 2)
- [ ] Update recommender.py to handle transaction insights
- [ ] Merge strategic + tactical recommendations
- [ ] Create priority ranking algorithm

### Phase 4: Update Dashboard UI (Week 2-3)
- [ ] Add benchmark indicators to Dashboard
- [ ] Add color-coded performance flags
- [ ] Update Recommendations page to show both strategic and tactical

### Phase 5: Testing & Validation (Week 3)
- [ ] Test with sample transaction data
- [ ] Validate recommendation accuracy
- [ ] Refine thresholds based on test results

---

## Success Metrics

1. **Completeness**: All transaction metrics have corresponding benchmarks
2. **Actionability**: Each identified gap maps to specific deal recommendation
3. **Clarity**: Dashboard clearly shows "what's wrong" and "what to do"
4. **Integration**: Strategic + Tactical recommendations work together seamlessly
5. **User Value**: Restaurant owners can take immediate action from insights

---

## Next Steps

1. Review and approve this plan
2. Generate the benchmark data files
3. Implement transaction_performance_analyzer.py
4. Update recommender to integrate both strategic and tactical insights
5. Enhance Dashboard with benchmark comparisons
