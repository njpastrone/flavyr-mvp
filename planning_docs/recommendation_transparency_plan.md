# Deal Recommendations Transparency Plan

## Executive Summary

**Goal:** Make the recommendation calculation process fully transparent to restaurant owners so they understand exactly why each recommendation was made and how the system arrived at its conclusions.

**Current Problem:** Users see recommendations but don't understand:
- How their metrics were calculated
- Why specific thresholds trigger recommendations
- How severity is determined
- How recommendations are prioritized
- What data sources feed into each recommendation

---

## Current State Analysis

### What Users Currently See:

```
Critical Issues

1. Foster Customer Loyalty [Transaction Insight]
   Severity: Critical
   Suggested Deal Types: Loyalty Offerings, Holiday Deals
   Rationale: Loyalty programs create repeat behavior...
```

### What's Missing:

❌ **No visibility into:**
1. How the loyalty rate was calculated from transaction data
2. Why 24.5% is classified as "Critical"
3. What the specific threshold is (e.g., <25% = Critical)
4. How the benchmark of 40.0% was determined
5. Why this specific recommendation was chosen over others
6. What happens if they implement the recommendation
7. How the system prioritized this over other issues

---

## Transparency Framework

### 5 Pillars of Transparent Recommendations

1. **Data Lineage** - Show what data contributed to this metric
2. **Calculation Method** - Explain how the metric was computed
3. **Threshold Logic** - Show why this severity level was assigned
4. **Benchmark Source** - Explain where industry standards come from
5. **Impact Projection** - Estimate what improvement looks like

---

## Proposed Transparency Features

### Feature 1: "How Was This Calculated?" Expandable

**Location:** Under each recommendation
**Visual:** Expandable accordion with step-by-step breakdown

**Example for Loyalty Rate:**

```
📊 How Was This Calculated?
└─ Your Data
   ├─ Total Customers: 500 (from transaction uploads)
   ├─ Customers with Multiple Visits: 122
   └─ Calculation: 122 / 500 × 100 = 24.5%

└─ Industry Benchmark
   ├─ Restaurant Type: American - Full Service
   ├─ Benchmark Loyalty Rate: 40.0%
   └─ Source: Industry average for Full Service restaurants

└─ Gap Analysis
   ├─ Your Rate: 24.5%
   ├─ Benchmark: 40.0%
   ├─ Gap: -15.5 percentage points
   └─ Classification: Critical (threshold: <25%)

└─ Severity Logic
   ├─ <25% loyalty rate → Critical
   ├─ 25-30% → High
   ├─ 30-35% → Medium
   └─ >Benchmark → Good
```

### Feature 2: Data Source Badges

**Visual:** Small badges showing data origin

```
[From Your Transactions: Oct 1-31, 2024]
[Benchmark: American Full Service Industry Average]
[Calculated: Real-time from 1,247 transactions]
```

### Feature 3: Interactive Calculation Explorer

**Location:** Dashboard page - new section
**Purpose:** Let users see live calculations

```
🔍 Calculation Explorer

Select a Metric: [Dropdown: Loyalty Rate ▼]

Your Data Input:
├─ Total Unique Customers: 500
├─ Customers with 2+ Visits: 122
└─ Customers with 1 Visit: 378

Calculation Steps:
Step 1: Count unique customer_id values → 500
Step 2: Count customers with count > 1 → 122
Step 3: Calculate percentage: 122 ÷ 500 = 0.245
Step 4: Convert to percentage: 0.245 × 100 = 24.5%

Result: 24.5% Loyalty Rate
```

### Feature 4: Recommendation Decision Tree

**Visual:** Flow chart showing decision logic

```
Loyalty Rate: 24.5%
    ↓
Is it < 25%? → YES
    ↓
Severity: CRITICAL
    ↓
Gap from benchmark: -15.5 pp
    ↓
Maps to Problem: "Foster Customer Loyalty"
    ↓
Lookup in Deal Bank:
  ├─ Loyalty Offerings (Primary)
  ├─ Holiday Deals (Secondary)
  └─ Bundling & Fixed-Price (Tertiary)
    ↓
Selected Deals: Loyalty Offerings + Holiday Deals
    ↓
Priority: #1 (Most Critical Issue)
```

### Feature 5: "What If?" Scenario Planner

**Interactive Tool:** Let users see impact of improvements

```
📈 Impact Simulator

Current State:
Loyalty Rate: 24.5%
Severity: Critical

What if you improved to:
[Slider: 24.5% ————●———— 50%] → 35%

New Assessment:
├─ Severity: Medium → Low
├─ Gap: -5 pp (vs. -15.5 pp now)
├─ Priority: Moves from #1 to #3
└─ Status: No longer critical ✓

Estimated Actions Needed:
└─ Implement loyalty program with ~10-15% enrollment rate
```

### Feature 6: Confidence Indicators

**Visual:** Confidence level for each recommendation

```
Confidence: ████████░░ 80%

Based on:
✓ 1,247 transactions (High confidence - large sample)
✓ 30 days of data (Medium confidence - decent time range)
✓ Benchmark from 500+ restaurants (High confidence)
⚠ Limited to one location (May not reflect full brand)
```

### Feature 7: Explanation Tooltips

**Interactive:** Hover over any metric for instant explanation

```
[Hover over "Loyalty Rate"]
↓
Tooltip appears:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Loyalty Rate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What it measures: Percentage of customers who
return for multiple visits

How it's calculated:
(Customers with 2+ visits) ÷ (Total customers) × 100

Data source: Your transaction uploads
Timeframe: Last 30 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Feature 8: Recommendation Audit Trail

**Location:** Bottom of recommendations page
**Purpose:** Show complete decision path

```
🔍 Recommendation Audit Trail

Analysis Run: October 25, 2024 at 2:45 PM

Data Inputs:
├─ Transaction data: 1,247 records (Oct 1-31, 2024)
├─ Restaurant type: American - Full Service
├─ Benchmarks loaded: transaction_benchmark_data.csv
└─ Deal mapping: transaction_deal_mapping.csv

Analysis Steps:
1. ✓ Calculated loyalty rate from transactions (24.5%)
2. ✓ Loaded benchmark for American Full Service (40.0%)
3. ✓ Compared actual vs benchmark (-15.5 pp gap)
4. ✓ Applied severity threshold (<25% = Critical)
5. ✓ Mapped to business problem (Foster Customer Loyalty)
6. ✓ Retrieved deal recommendations from Deal Bank
7. ✓ Combined with strategic recommendations
8. ✓ Prioritized by severity (Critical → High → Medium)

Issues Identified: 3 Critical, 2 High, 1 Medium
Recommendations Generated: 6 total (3 strategic + 3 tactical)
```

---

## Implementation Plan

### Phase 1: Basic Transparency (Week 1)

**Priority:** High
**Effort:** Medium

**Deliverables:**
1. Add "How Was This Calculated?" expandable to each recommendation
2. Show calculation steps for all metrics
3. Display severity thresholds explicitly
4. Add data source badges

**Files to Modify:**
- `app.py` - Update recommendations_page() display
- Create new helper functions for explanation text

**Example Code Structure:**
```python
def generate_calculation_explanation(rec: Dict) -> str:
    """Generate step-by-step calculation explanation."""
    metric = rec['metric']

    if metric == 'loyalty_rate':
        return f"""
        **Your Data:**
        - Total Customers: {rec['total_customers']}
        - Repeat Customers: {rec['repeat_customers']}

        **Calculation:**
        {rec['repeat_customers']} ÷ {rec['total_customers']} × 100 = {rec['actual_value']}

        **Benchmark Comparison:**
        - Industry Standard: {rec['benchmark_value']}
        - Your Performance: {rec['actual_value']}
        - Gap: {rec['gap']}

        **Severity Classification:**
        - <25% = Critical (You: {rec['actual_value']})
        - 25-30% = High
        - 30-35% = Medium
        """
```

### Phase 2: Interactive Explorers (Week 2)

**Priority:** Medium
**Effort:** High

**Deliverables:**
1. Build Calculation Explorer component
2. Add Recommendation Decision Tree visualization
3. Implement tooltips for all metrics

**New Components:**
- `components/calculation_explorer.py`
- `components/decision_tree_viz.py`
- Enhanced tooltip system

### Phase 3: Advanced Features (Week 3)

**Priority:** Low
**Effort:** High

**Deliverables:**
1. "What If?" Scenario Planner
2. Confidence indicators
3. Complete audit trail

**New Modules:**
- `src/scenario_planner.py`
- `src/confidence_calculator.py`
- Enhanced logging for audit trail

---

## UI/UX Design Mockups

### Mockup 1: Enhanced Recommendation Card

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Foster Customer Loyalty [Transaction Insight]           │
│                                                             │
│ Severity: Critical    Confidence: ████████░░ 80%           │
│                                                             │
│ 📊 Your Performance                                         │
│ ├─ Loyalty Rate: 24.5%                                     │
│ ├─ Industry Benchmark: 40.0%                               │
│ └─ Gap: -15.5 percentage points                            │
│                                                             │
│ [Data Source: 1,247 transactions, Oct 1-31, 2024]         │
│                                                             │
│ ▼ How Was This Calculated?                                 │
│   └─ [Click to expand step-by-step breakdown]              │
│                                                             │
│ ▼ Why This Severity?                                       │
│   └─ [Click to see threshold logic]                        │
│                                                             │
│ Immediate Action:                                          │
│ Launch a points-based loyalty program with sign-up         │
│ incentive. Target: Increase repeat rate from 24.5% to 40%  │
│                                                             │
│ Suggested Deal Types:                                      │
│ • Loyalty Offerings                                        │
│ • Holiday Deals                                            │
│                                                             │
│ 📈 Estimated Impact: +10-15 pp loyalty rate over 6 months  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Mockup 2: Calculation Explanation (Expanded)

```
┌─────────────────────────────────────────────────────────────┐
│ 📊 How Was This Calculated?                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Step 1: Load Your Transaction Data                         │
│ ├─ Source: CSV upload (Oct 1-31, 2024)                    │
│ ├─ Total Transactions: 1,247                               │
│ └─ Unique Customers: 500                                   │
│                                                             │
│ Step 2: Calculate Loyalty Rate                             │
│ ├─ Count customers with 1 visit: 378                       │
│ ├─ Count customers with 2+ visits: 122                     │
│ ├─ Formula: repeat_customers ÷ total_customers × 100       │
│ └─ Result: 122 ÷ 500 × 100 = 24.5%                        │
│                                                             │
│ Step 3: Load Industry Benchmark                            │
│ ├─ Restaurant Type: American - Full Service                │
│ ├─ Benchmark Source: transaction_benchmark_data.csv        │
│ ├─ Industry Average: 40.0%                                 │
│ └─ Based on: 500+ similar restaurants                      │
│                                                             │
│ Step 4: Compare & Classify                                 │
│ ├─ Your Rate: 24.5%                                        │
│ ├─ Benchmark: 40.0%                                        │
│ ├─ Gap: -15.5 percentage points                            │
│ └─ Severity: Critical (<25% threshold)                     │
│                                                             │
│ Step 5: Map to Recommendation                              │
│ ├─ Problem Identified: Foster Customer Loyalty             │
│ ├─ Deal Mapping: transaction_deal_mapping.csv              │
│ ├─ Matching Deals: Loyalty Offerings, Holiday Deals        │
│ └─ Priority: #1 (most severe issue)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Mockup 3: Severity Threshold Explanation

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️ Why This Severity Level?                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Severity Thresholds for Loyalty Rate:                      │
│                                                             │
│ 🔴 CRITICAL (<25%)          ← You are here (24.5%)        │
│    Immediate action required                               │
│    Customer retention is dangerously low                   │
│                                                             │
│ 🟠 HIGH (25-30%)                                           │
│    Significant underperformance                            │
│    Should be prioritized                                   │
│                                                             │
│ 🟡 MEDIUM (30-35%)                                         │
│    Below industry standard                                 │
│    Opportunity for improvement                             │
│                                                             │
│ 🟢 GOOD (>Benchmark)                                       │
│    Meeting or exceeding expectations                       │
│    Maintain current practices                              │
│                                                             │
│ Your Position:                                             │
│ [▓▓▓▓░░░░░░░░░░░░░░░░] 24.5% / 40.0% benchmark            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Implementation Details

### 1. Data Structure Enhancements

Add transparency metadata to recommendation objects:

```python
{
    'business_problem': 'Foster Customer Loyalty',
    'severity': 'critical',

    # NEW: Transparency fields
    'transparency': {
        'calculation_steps': [
            {
                'step': 1,
                'description': 'Load transaction data',
                'input': '1,247 transactions',
                'output': '500 unique customers'
            },
            {
                'step': 2,
                'description': 'Calculate loyalty rate',
                'formula': 'repeat_customers ÷ total_customers × 100',
                'calculation': '122 ÷ 500 × 100',
                'result': '24.5%'
            }
        ],
        'data_sources': {
            'transaction_data': {
                'type': 'csv_upload',
                'date_range': '2024-10-01 to 2024-10-31',
                'record_count': 1247
            },
            'benchmark': {
                'type': 'industry_standard',
                'source_file': 'transaction_benchmark_data.csv',
                'restaurant_type': 'American - Full Service',
                'value': 40.0
            }
        },
        'severity_thresholds': {
            'critical': '<25%',
            'high': '25-30%',
            'medium': '30-35%',
            'good': '>benchmark'
        },
        'confidence_factors': {
            'sample_size': 'high (1,247 transactions)',
            'time_range': 'medium (30 days)',
            'benchmark_quality': 'high (500+ restaurants)',
            'overall_confidence': 0.80
        }
    }
}
```

### 2. Helper Functions to Create

```python
# In src/transparency_helpers.py

def generate_calculation_explanation(metric_type: str, data: Dict) -> List[Dict]:
    """Generate step-by-step calculation explanation."""

def create_severity_explanation(metric: str, value: float, thresholds: Dict) -> str:
    """Explain why this severity level was assigned."""

def get_data_lineage(metric: str, session_state: Dict) -> Dict:
    """Show complete data lineage for a metric."""

def calculate_confidence_score(data: Dict) -> float:
    """Calculate confidence score based on data quality."""

def generate_audit_trail(analysis_run: Dict) -> str:
    """Generate complete audit trail of recommendation process."""
```

### 3. UI Component Structure

```
app.py
├─ recommendations_page()
   ├─ display_priority_actions()
   ├─ display_recommendation_card()
   │  ├─ show_basic_info()
   │  ├─ show_calculation_expander()  ← NEW
   │  ├─ show_severity_expander()     ← NEW
   │  ├─ show_data_sources()          ← NEW
   │  └─ show_confidence_indicator()  ← NEW
   └─ display_audit_trail()           ← NEW
```

---

## User Benefits

### 1. Trust Building
- Users see exactly how numbers are calculated
- No "black box" mystery algorithms
- Clear methodology builds confidence

### 2. Learning & Education
- Users learn what metrics matter
- Understand industry standards
- Can spot data quality issues

### 3. Actionable Insights
- Know exactly what to improve
- See clear targets (e.g., 24.5% → 40%)
- Understand impact of actions

### 4. Data Quality Validation
- Spot errors in uploaded data
- Verify calculations make sense
- Ensure benchmarks are appropriate

---

## Success Metrics

**How we'll measure transparency improvements:**

1. **User Engagement**
   - % of users clicking "How Was This Calculated?"
   - Time spent on recommendation explanations
   - Target: >60% engagement with transparency features

2. **User Feedback**
   - Survey: "Do you understand why this recommendation was made?"
   - Target: >85% answer "Yes"

3. **Implementation Rate**
   - % of users who implement recommended deals
   - Hypothesis: Transparency → Higher implementation
   - Target: +20% implementation rate

4. **Support Tickets**
   - Reduction in "How did you calculate this?" questions
   - Target: -50% calculation-related support requests

---

## Rollout Plan

### Week 1: Foundation
- [ ] Add calculation explanations to transaction_performance_analyzer.py
- [ ] Update recommender.py to include transparency metadata
- [ ] Add "How Was This Calculated?" expandables to UI

### Week 2: Enhancement
- [ ] Add severity threshold explanations
- [ ] Implement data source badges
- [ ] Create confidence indicators

### Week 3: Advanced Features
- [ ] Build Calculation Explorer
- [ ] Add audit trail
- [ ] Implement tooltips

### Week 4: Testing & Refinement
- [ ] User testing with 3-5 restaurant owners
- [ ] Gather feedback on clarity
- [ ] Refine explanations based on feedback

---

## Example Implementation Snippets

### Snippet 1: Calculation Explanation Generator

```python
def explain_loyalty_calculation(data: Dict) -> str:
    """Generate human-readable explanation of loyalty calculation."""

    total_customers = data['total_customers']
    repeat_customers = data['repeat_customers']
    loyalty_rate = data['loyalty_rate']

    return f"""
    ### How Your Loyalty Rate Was Calculated

    **Step 1: Count Your Customers**
    - We analyzed your transaction data from {data['date_range']}
    - Found {total_customers} unique customers (based on customer_id)

    **Step 2: Identify Repeat Customers**
    - Counted customers who made 2 or more visits
    - Result: {repeat_customers} repeat customers

    **Step 3: Calculate Percentage**
    - Formula: (Repeat Customers ÷ Total Customers) × 100
    - Calculation: ({repeat_customers} ÷ {total_customers}) × 100
    - Your Loyalty Rate: {loyalty_rate}%

    **Step 4: Compare to Industry**
    - Industry benchmark for {data['restaurant_type']}: {data['benchmark']}%
    - Your gap: {loyalty_rate - data['benchmark']:+.1f} percentage points
    """
```

### Snippet 2: Severity Explanation

```python
def explain_severity(metric: str, value: float, severity: str) -> str:
    """Explain why this severity level was assigned."""

    thresholds = {
        'loyalty_rate': {
            'critical': 25,
            'high': 30,
            'medium': 35
        }
    }

    t = thresholds.get(metric, {})

    explanation = f"**Why is this {severity.upper()}?**\n\n"

    if severity == 'critical':
        explanation += f"Your {metric} of {value}% is below {t['critical']}%, "
        explanation += "indicating immediate action is required. "
        explanation += "This level of performance poses significant business risk."

    return explanation
```

---

## Next Steps

1. **Review & Approve** this plan
2. **Prioritize** which transparency features to implement first
3. **Prototype** the "How Was This Calculated?" expandable
4. **Test** with real users to validate clarity
5. **Iterate** based on feedback

---

## Appendix: Transparency Best Practices

### What Makes Good Transparency?

✅ **Do:**
- Use plain language, not technical jargon
- Show actual numbers, not just percentages
- Explain "why" not just "what"
- Provide context (e.g., "for restaurants like yours...")
- Make it optional (expandables, not overwhelming)

❌ **Don't:**
- Dump raw data without explanation
- Use complex formulas without breaking them down
- Assume users know industry terminology
- Hide behind "proprietary algorithms"
- Make explanations mandatory reading

### Examples of Good vs. Bad Transparency

**Bad:**
> "Your loyalty coefficient diverges from the normalized industry quintile by -1.5 standard deviations."

**Good:**
> "Your loyalty rate (24.5%) is 15.5 percentage points below the industry average (40%). This means fewer customers are returning for second visits compared to similar restaurants."

---

**End of Plan**
