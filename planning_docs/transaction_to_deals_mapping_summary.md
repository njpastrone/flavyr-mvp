# Transaction Metrics → Deal Recommendations Mapping

## Quick Reference Guide

This document shows how transaction-level insights from the Dashboard connect to actionable Deal Recommendations.

---

## Metric-to-Problem-to-Deal Flow

### 1. Customer Loyalty Rate

**What We Measure:**
- Percentage of customers who return for multiple visits
- Calculated from transaction data: `repeat_customers / total_customers * 100`

**Industry Benchmarks:**
- Full Service: 38-45%
- Casual Dining: 40-50%
- Fast Casual: 30-38%
- Quick Service: 25-33%

**Business Problem Mapping:**

| Your Loyalty Rate | Problem Identified | Severity | Recommended Deals |
|-------------------|-------------------|----------|-------------------|
| <25% | Foster Customer Loyalty + Attract New Customers | **Critical** | Loyalty Offerings, Holiday Deals, First-visit incentives |
| 25-30% | Foster Customer Loyalty | **High** | Loyalty Offerings, Bundling with member perks |
| 30-35% | Foster Customer Loyalty | **Medium** | Loyalty Offerings, Seasonal re-engagement |
| >Benchmark | No issue | ✓ Good | Maintain current strategy |

**Example Recommendation:**
```
Problem: Foster Customer Loyalty
Your Rate: 24.5%
Benchmark: 40.0%
Gap: -15.5 percentage points
Severity: CRITICAL

Recommended Deals:
1. Launch points-based loyalty program with sign-up bonus
2. Holiday comeback offers to re-engage past customers
3. Member-exclusive bundles (20% higher perceived value)

Expected Impact: Increase repeat rate by 10-15 percentage points over 6 months
```

---

### 2. Average Order Value (AOV)

**What We Measure:**
- Overall AOV: Mean transaction value
- AOV by Day: Breakdown by Monday-Sunday
- AOV Variation: Weekend vs. Weekday uplift

**Industry Benchmarks:**
| Restaurant Type | Weekday AOV | Weekend AOV | Variation % |
|----------------|-------------|-------------|-------------|
| Full Service | $32-45 | $42-60 | 25-35% |
| Casual Dining | $38-48 | $48-60 | 20-30% |
| Fast Casual | $18-25 | $24-32 | 25-35% |
| Quick Service | $13-18 | $16-22 | 20-28% |

**Business Problem Mapping:**

| Condition | Problem | Severity | Recommended Deals |
|-----------|---------|----------|-------------------|
| Overall AOV <90% of benchmark | Boost Average Order Value | **High** | Bundling & Fixed-Price Offerings, Event-based upsells |
| Weekend uplift <15% | Boost Average Order Value | **Medium** | Weekend-specific bundles, Premium menu highlights |
| Weekday AOV very low | Boost Average Order Value | **Medium** | Weekday lunch bundles, Value meal combos |

**Example Recommendation:**
```
Problem: Boost Average Order Value
Your Overall AOV: $28.50
Benchmark AOV: $35.00
Gap: -18.6%
Severity: HIGH

Additional Issue: Weekend uplift only 12% (benchmark: 25-35%)

Recommended Deals:
1. Weekend Premium Bundles: 3-course meal at $45 (vs. à la carte $52)
2. Weekday Value Bundles: Lunch combo $18 (drives volume + spend)
3. Event-based upsells: Prix fixe menu for date nights

Expected Impact:
- Increase overall AOV to $32-34 (+12-19%)
- Improve weekend uplift to 22-28%
```

---

### 3. Slowest Day Performance

**What We Measure:**
- Day with fewest transactions
- Day with lowest revenue
- Percentage drop from average day

**Industry Benchmarks:**

| Restaurant Type | Expected Slowest Day | Normal Drop from Average |
|----------------|---------------------|--------------------------|
| Full Service | Monday/Tuesday | 30-35% |
| Casual Dining | Monday/Tuesday | 28-32% |
| Fast Casual | Sunday | 25-30% |
| Quick Service | Tuesday/Wednesday | 23-28% |

**Business Problem Mapping:**

| Condition | Problem | Severity | Recommended Deals |
|-----------|---------|----------|-------------------|
| Drop >40% below average | Improve Slow Days | **Critical** | Discount Traffic Driver Items, Aggressive weekday promos |
| Drop 35-40% below average | Improve Slow Days | **High** | Weekday bundles, Loyalty bonus points on slow days |
| Drop at benchmark level | Normal | ✓ Good | Optional: Mild incentives to smooth traffic |

**Example Recommendation:**
```
Problem: Improve Slow Days
Your Slowest Day: Monday (45 transactions, $1,280 revenue)
Average Day: 87 transactions, $2,615 revenue
Your Drop: 48% below average
Benchmark Drop: 35% below average
Severity: CRITICAL

Recommended Deals:
1. "Monday Madness" - 20% off top 5 menu items
2. Monday Loyalty Bonus - 2x points for loyalty members
3. Happy Hour Extension - 3pm-7pm (vs. normal 5pm-7pm)
4. Family Bundle Monday - $60 for 4-person meal (normally $78)

Expected Impact: Increase Monday transactions by 15-25 (33-55% improvement)
```

---

### 4. Item Performance

**What We Measure:**
- Top 3 items by revenue
- Top 3 items by quantity
- Bottom 3 items by revenue
- Bottom 3 items by quantity
- Revenue concentration of top item

**Industry Benchmarks:**

| Metric | Healthy Range | Warning Level | Action Needed |
|--------|---------------|---------------|---------------|
| Top Item Revenue Share | 15-25% | 25-30% | >30% |
| Bottom Item Revenue Share | >2.5% | 2.0-2.5% | <2.0% |
| Number of items <2% share | 0-3 items | 3-5 items | >5 items |

**Business Problem Mapping:**

| Condition | Problem | Severity | Recommended Deals |
|-----------|---------|----------|-------------------|
| Top item >30% revenue | Increase Quantity of Sales | **Medium** | Promote variety, Create bundles featuring other items |
| >5 items <2% revenue | Inventory Management | **Medium** | Bundle slow movers, LTO to test interest, Consider removal |
| Top & bottom same by rev/qty | Menu imbalance | **Low** | Diversify offerings, Test new items |

**Example Recommendations:**

**Scenario A: Over-reliance on Star Item**
```
Problem: Increase Quantity of Sales (Menu Diversification)
Top Item: "Signature Burger" - 34% of total revenue
Benchmark: <25% healthy
Severity: MEDIUM

Recommended Deals:
1. "Chef's Favorites Bundle" - Highlights 3 other high-margin items at 15% discount
2. "Mix & Match Monday" - Try any 3 items at $35 (encourages exploration)
3. LTO featuring seasonal ingredient across 4 menu items

Expected Impact: Reduce top item concentration to 26-28%, increase variety of purchases
```

**Scenario B: Too Many Underperformers**
```
Problem: Inventory Management
Bottom Items: 7 items generating <2% revenue each (14% total)
Benchmark: <3 items ideal
Severity: MEDIUM

Recommended Deals:
1. "Hidden Gems Bundle" - Feature 3 slow movers in value combo
2. "Limited Time Special" - Reposition bottom item as LTO with story
3. Gradual menu reduction - Remove 2 worst performers after 30-day test

Expected Impact:
- Move 3-4 items above 2.5% threshold via bundling
- Remove 2-3 items confirmed as non-viable
- Simplify menu for better operational efficiency
```

---

## Combined Recommendation Strategy

### When Multiple Issues Exist

**Priority Ranking:**
1. **Critical Loyalty Issues** (<25% repeat rate) - Immediate revenue risk
2. **Critical Slow Day Issues** (>40% drop) - Lost revenue opportunity
3. **High AOV Gaps** (<90% benchmark) - Systemic underperformance
4. **Medium Issues** (Menu mix, moderate gaps) - Optimization opportunities

**Example Combined Strategy:**
```
Restaurant: "Mario's Italian Bistro" (Casual Dining)

Top 3 Issues Identified:
1. Loyalty Rate: 22% (benchmark 43%) - CRITICAL
2. Monday Drop: 51% below average (benchmark 30%) - CRITICAL
3. AOV: $34 (benchmark $42) - HIGH

Integrated Deal Recommendation:
┌─────────────────────────────────────────────────────────────┐
│ Phase 1 (Weeks 1-4): Loyalty Foundation + Monday Fix       │
├─────────────────────────────────────────────────────────────┤
│ 1. Launch "Mario's Rewards" loyalty program                │
│    - Sign-up bonus: Free appetizer                         │
│    - 2x points on Mondays                                  │
│    - Birthday month: 25% off visit                         │
│                                                             │
│ 2. "Monday Italian Night" Bundle                           │
│    - Pasta + Wine + Dessert = $35 (normally $42)           │
│    - Available Monday only                                 │
│    - Members get garlic bread add-on free                  │
│                                                             │
│ Expected Impact:                                            │
│ - Increase loyalty enrollment to 40% of customers          │
│ - Boost Monday traffic 25-35%                              │
│ - Immediate AOV improvement via bundles                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 2 (Weeks 5-8): AOV Optimization                      │
├─────────────────────────────────────────────────────────────┤
│ 1. "Date Night Duo" (Fri-Sat)                              │
│    - 2 entrées + wine bottle + shared dessert = $68       │
│    - Targets weekend AOV increase                          │
│                                                             │
│ 2. Loyalty Member Upsell                                   │
│    - "Complete your meal" suggestions at checkout          │
│    - Members-only premium add-ons                          │
│                                                             │
│ Expected Impact:                                            │
│ - Weekend AOV: $34 → $40 (+18%)                            │
│ - Overall AOV: $34 → $37 (+9%)                             │
│ - Loyalty members spend 20-25% more per visit             │
└─────────────────────────────────────────────────────────────┘

6-Month Projection:
- Loyalty Rate: 22% → 35-38% (+13-16 pp)
- Monday Transactions: +30-40%
- Overall AOV: $34 → $38-39 (+12-15%)
- Estimated Revenue Impact: +18-24%
```

---

## Implementation Checklist

### For Each Identified Issue:

- [ ] Confirm metric calculation is accurate
- [ ] Verify benchmark comparison is appropriate for restaurant type
- [ ] Determine severity level (Critical/High/Medium/Low)
- [ ] Map to primary business problem
- [ ] Select 2-3 most relevant deal types
- [ ] Draft specific, actionable recommendation
- [ ] Estimate expected impact
- [ ] Prioritize against other issues
- [ ] Present in logical sequence to user

---

## Next Steps in Development

1. **Build Transaction Performance Analyzer** - Automate benchmark comparisons
2. **Expand Deal Bank** - Add transaction-specific deal examples
3. **Create Unified Recommender** - Merge strategic + tactical recommendations
4. **Enhance Dashboard** - Show benchmark indicators and severity flags
5. **Build Recommendation Page** - Display integrated strategic + tactical actions

---

## Success Criteria

✓ Every transaction metric has a clear benchmark
✓ Every gap triggers specific business problem identification
✓ Every problem maps to actionable deal recommendations
✓ Severity levels guide prioritization
✓ Combined recommendations create coherent strategy
✓ Restaurant owners can take immediate action
