# Performance Score Transparency Feature

**Date:** October 26, 2025
**Feature:** Expandable explanation of Performance Score calculation
**Status:** ✅ Implemented

## Overview

Added a "How is this score calculated?" expandable section below the Performance Gauge that provides complete transparency into how the 0-100 performance score is derived.

---

## What Was Added

### 1. Transparency Function

**File:** `src/visualization_helpers.py`

**New Function:** `generate_performance_score_explanation(gaps, score)`

Creates a comprehensive, step-by-step explanation showing:
1. Individual gap calculations for each metric
2. Average gap calculation with formula
3. Score conversion scale and logic
4. Interpretation guidelines

### 2. UI Integration

**File:** `app.py` - recommendations_page()

Added expandable section below the gauge chart:
```python
with st.expander("How is this score calculated?"):
    explanation = generate_performance_score_explanation(gaps, performance_score)
    st.markdown(explanation)
```

---

## Explanation Structure

### Step 1: Individual Gaps
Shows each metric's performance vs. benchmark:
```
- Average Ticket Size (AOV): $32.00 vs $35.00 benchmark = 8.6% below
- Total Covers: 180 vs 200 benchmark = 10.0% below
- Customer Repeat Rate: 35.0% vs 40.0% benchmark = 12.5% below
```

### Step 2: Average Gap Calculation
Shows the math clearly:
```
(-8.6% + -10.0% + -12.5%) ÷ 3 = -10.4%
```

### Step 3: Score Conversion
Displays the scoring scale in a table:

| Average Gap | Score Range | Performance Level |
|-------------|-------------|-------------------|
| +20% or better | 100 | Exceptional |
| 0% to +20% | 70-100 | Above Average |
| 0% (at benchmark) | 70 | Average |
| -20% to 0% | 40-70 | Below Average |
| -40% to -20% | 0-40 | Needs Improvement |
| -40% or worse | 0 | Critical |

Then shows which formula applies:
```
- Average gap of -10.4% is between -40% and 0%
- Score = 70 + (-10.4 ÷ 40) × 70 = 51.9
```

### Step 4: Interpretation
Explains what the score means in context:
- **85-100**: Outperforming most peers
- **70-84**: Meeting industry standards
- **50-69**: Room for improvement
- **Below 50**: Focus on critical issues

---

## Scoring Logic

### Formula

The score is calculated using a piecewise function:

```python
if avg_gap >= 20:
    score = 100
elif avg_gap >= 0:
    score = 70 + (avg_gap / 20) * 30
elif avg_gap >= -40:
    score = 70 + (avg_gap / 40) * 70
else:
    score = 0
```

### Rationale

- **Baseline (70 points)**: Matching industry benchmarks = average performance
- **Above benchmark**: Earn up to 30 bonus points (70 → 100)
- **Below benchmark**: Lose up to 70 points (70 → 0)
- **Critical threshold (-40%)**: Extreme underperformance = 0 points

This creates a scale where:
- Most restaurants cluster around 50-90 points
- Exceptional performers reach 100
- Critical issues push toward 0

---

## Testing Results

### Test Cases Verified

**1. Sample Restaurant (Below Average)**
- Gaps: -8.6%, -10.0%, -12.5%
- Average: -10.4%
- Score: **51.9/100** ✓
- Explanation generated successfully

**2. Excellent Performance**
- Gaps: +20%, +20%, +20%
- Average: +20%
- Score: **100.0/100** ✓

**3. Critical Performance**
- Gaps: -42.9%, -40%, -45%
- Average: -42.6%
- Score: **0.0/100** ✓

**4. At Benchmark**
- Gaps: 0%, 0%, 0%
- Average: 0%
- Score: **70.0/100** ✓

All edge cases handled correctly!

---

## User Experience

### Before
- Gauge chart shows score and grade
- No explanation of how score was calculated
- Users might wonder "Why 51.9?"

### After
- Gauge chart shows score and grade
- **Expandable link:** "How is this score calculated?"
- Click to see complete step-by-step breakdown
- Users understand exactly how their score was derived

### Progressive Disclosure
- High-level overview visible by default
- Details available on demand
- Doesn't clutter the main page
- Educational for users who want to learn

---

## Value Proposition

### Transparency Benefits

1. **Trust Building**
   - Users see the math behind the score
   - No "black box" algorithm
   - Clear, reproducible calculation

2. **Educational**
   - Users learn how metrics combine
   - Understand relative importance
   - See impact of improvements

3. **Actionable**
   - Identifies which metrics drag down score
   - Shows quantified impact of gaps
   - Motivates improvement efforts

4. **Credibility**
   - Professional presentation
   - Industry-standard approach
   - Comparable to other analytics platforms

---

## Implementation Details

### Files Modified

1. **src/visualization_helpers.py** (117 new lines)
   - Added `generate_performance_score_explanation()` function
   - Comprehensive docstring
   - Handles all edge cases
   - Formats values appropriately (%, $, numbers)

2. **app.py** (4 lines added)
   - Imported new function
   - Added expandable section below gauge
   - Passes gaps and score to explanation generator

### Code Quality

- ✅ Clear variable naming
- ✅ Comprehensive comments
- ✅ Type hints in docstring
- ✅ DRY principle (reuses existing score calculation)
- ✅ Handles multiple metric types (%, $, counts)
- ✅ Edge case handling (very high, very low scores)

---

## Example Output

For a restaurant with:
- AOV: $32 vs $35 benchmark (-8.6%)
- Covers: 180 vs 200 benchmark (-10%)
- Repeat Rate: 35% vs 40% benchmark (-12.5%)

The explanation shows:

```markdown
### How Your Performance Score Was Calculated

Your score of **51.9/100** is based on how your restaurant
performs across all key metrics compared to industry benchmarks.

#### Step 1: Calculate Individual Gaps
- Average Ticket Size (AOV): $32.00 vs $35.00 = 8.6% below
- Total Covers: 180 vs 200 = 10.0% below
- Customer Repeat Rate: 35.0% vs 40.0% = 12.5% below

#### Step 2: Calculate Average Gap
(-8.6% + -10.0% + -12.5%) ÷ 3 = -10.4%

#### Step 3: Convert to Score
Score = 70 + (-10.4 ÷ 40) × 70 = 51.9

#### What This Means
Your score of 50-69 indicates there's room for improvement...
```

---

## Future Enhancements (Optional)

### Potential Additions

1. **Visual Score Breakdown**
   - Stacked bar showing contribution of each metric
   - Color-coded by positive/negative impact

2. **Score History**
   - Track score over time
   - Show improvement trends

3. **Peer Comparison**
   - "You scored better than X% of similar restaurants"
   - Percentile ranking

4. **What-If Calculator**
   - "If you improved AOV by 5%, your score would be..."
   - Interactive sliders

5. **Weighted Metrics**
   - Allow different importance weights
   - Customize calculation for specific goals

---

## Consistency with Transparency System

This feature aligns with FLAVYR's existing transparency infrastructure:

**Similar Features:**
- "How Was This Calculated?" for transaction metrics
- "Why This Severity?" for recommendation prioritization
- "Confidence Details" for data quality factors

**Benefits:**
- Consistent user experience
- Builds trust through openness
- Educational value
- Professional presentation

---

## Summary

**Added:** Complete transparency for Performance Score calculation

**Implementation:**
- New explanation generator function (117 lines)
- Expandable section in UI (4 lines)
- Comprehensive testing (all edge cases verified)

**Result:**
- ✅ Users understand how their score is calculated
- ✅ Step-by-step math shown clearly
- ✅ Progressive disclosure (doesn't clutter page)
- ✅ Builds trust and credibility
- ✅ Educational value for restaurant operators

**Status:** Ready for production ✨
