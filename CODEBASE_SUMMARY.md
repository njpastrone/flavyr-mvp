# FLAVYR MVP - Codebase Analysis Summary

## Quick Stats

| Metric | Value |
|--------|-------|
| Total Python Files | 11 |
| Total Lines of Code | 2,774 |
| Largest File | app.py (924 lines - 33% of codebase) |
| Median File Size | 192 lines |
| Total Functions | ~68 |
| Avg Lines per Function | ~20-30 |
| External Dependencies | 3 major (streamlit, pandas, plotly) |

## Code Quality Assessment: GOOD

The FLAVYR MVP demonstrates solid engineering practices with:
- Clear module separation (src/ for logic, utils/ for helpers)
- Consistent use of type hints
- Appropriate function decomposition
- Good validation framework
- Documented test coverage

**Overall Complexity:** MODERATE - manageable at current size

---

## Critical Issues Found (Must Fix)

### 1. Duplicate Validation Functions
- `validate_transaction_data()` exists in BOTH:
  - `src/transaction_analyzer.py` (line 258) - never called
  - `utils/transaction_validator.py` (line 12) - actually used
- Creates maintenance burden and inconsistency

**Fix:** Remove unused function from transaction_analyzer.py

### 2. Constants Scattered Across Files
- KPI definitions appear in: analyzer.py, recommender.py, app.py, validators.py, transaction_validator.py
- Same column lists defined in multiple places with slightly different names
- Makes it hard to update consistently

**Fix:** Create centralized `src/config.py` with all constants

---

## Key Areas of Duplication

### Validation (40-50% duplication)
- `utils/transaction_validator.py` vs `src/transaction_analyzer.py`
- Same required_columns list appears in 3 files
- Similar validation patterns with different implementations

### UI Layout (20% of app.py)
- Metric display pattern repeated in dashboard_page()
- Color logic for cost vs revenue metrics repeated multiple times
- Formatting logic (decimals, currency) scattered throughout

### Result Formatting (15% of codebase)
- Each module has own formatting function
- Similar patterns: gaps, recommendations, transactions all need display formatting
- No shared formatting utilities

### Constants (8-10 redundant definitions)
- Cost metrics: defined in analyzer.py and app.py
- Revenue metrics: defined in analyzer.py and app.py
- KPI names: defined in analyzer.py with different structure in app.py
- Column lists: defined in 3+ places

---

## Architectural Strengths

1. **Clean Module Boundaries** - src/, utils/, and app.py have clear responsibilities
2. **Type Safety** - Consistent use of type hints and Optional types
3. **Function Design** - Most functions are small (20-30 lines) and focused
4. **Data Validation** - Comprehensive CSV validation with user-friendly errors
5. **Configuration** - Uses external CSV files for data, not hardcoded values

---

## Top 5 Improvement Opportunities

### Priority 1: Remove Validation Duplication (1-2 hours)
- Delete `validate_transaction_data()` from transaction_analyzer.py
- Use `validate_transaction_csv()` from transaction_validator.py everywhere
- Single source of truth for transaction column requirements

**Impact:** Reduce redundancy, fewer bugs

### Priority 2: Create src/config.py (2-3 hours)
- Consolidate KPI_COLUMNS, KPI_NAMES, LOWER_IS_BETTER
- Consolidate KPI_TO_PROBLEM mapping
- Consolidate REQUIRED_COLUMNS and column lists
- Consolidate cost_metrics, revenue_metrics sets
- Consolidate KPI help text and descriptions

**Impact:** ~50 lines of duplication eliminated, easier to maintain

### Priority 3: Extract src/formatters.py (2-3 hours)
- Move format_gap_summary() from analyzer.py
- Move format_deal_types() and create_recommendation_summary() from recommender.py
- Move create_kpi_comparison_table() from report_generator.py
- Create format_results_for_display() wrapper

**Impact:** Single place for formatting logic, easier to adjust presentation

### Priority 4: Refactor app.py Page Functions (3-4 hours)
- Break transaction_insights_page() (251 lines) into 5-6 focused helpers
- Break dashboard_page() (193 lines) into metric display + chart sections
- Extract metric_display_grid() helper to eliminate repetition

**Impact:** ~100 lines of duplication removed, better readability

### Priority 5: Add Caching for Static Data (1 hour)
- Add `@st.cache_data` to get_benchmark_data()
- Add caching to get_all_deal_bank_data()
- Improves UI responsiveness

**Impact:** Better performance for interactive UI

---

## Files Analyzed

### Largest Files (Risk Areas)
1. **app.py (924 lines)** - Main UI orchestration
   - 6 page functions: home, upload, dashboard, recommendations, transaction_insights, report
   - Heavy session state management (8 variables)
   - Tight coupling with business logic

2. **src/transaction_analyzer.py (339 lines)** - Contains unused validation
   - Well-structured analytics
   - But: duplicate validation function (line 258-293)

3. **src/report_generator.py (313 lines)** - PDF/HTML generation
   - Largest single-responsibility function: export_to_pdf() (88 lines)
   - Repeated color-coding logic

4. **src/data_loader.py (307 lines)** - Database operations
   - 11 functions for DB access
   - No connection pooling (opens/closes each query)

### Smaller, Well-Designed Files
- **src/analyzer.py (218 lines)** - Performance analytics. Clean, reusable.
- **src/recommender.py (184 lines)** - Deal recommendations. Good abstraction.
- **utils/validators.py (179 lines)** - CSV validation. Well-structured checks.
- **utils/transaction_validator.py (192 lines)** - Transaction validation. Duplicate of analyzer.

---

## Code Metrics Summary

### Function Complexity Distribution
```
Size        Count   Examples
Small (<20) 47      Most utility/helper functions
Medium      18      Analytics, formatting functions
Large       8       Report generation, page handlers
XL (100+)   3       Main UI pages in app.py
```

### Cyclomatic Complexity (Estimated)
- transaction_insights_page(): 12+ (HIGH)
- dashboard_page(): 10+ (HIGH)
- export_to_pdf(): 8+ (MEDIUM-HIGH)
- Most analytics: 4-6 (MEDIUM)
- Utilities: 2-3 (LOW)

---

## Specific Examples of Issues

### Example 1: Hardcoded Colors in Multiple Places
```python
# app.py line 373
colors = ['green' if gap >= 0 else 'red' for gap in gap_values]

# report_generator.py lines 244-250
if status == 'Critical': row_color = '#ffcccc'
elif status == 'Needs Attention': row_color = '#fff4cc'
```

**Issue:** Update color scheme = change multiple files

### Example 2: Repeated Metric Display Pattern
```python
# Lines 297-322 (Row 1)
cols = st.columns(4)
for i, kpi in enumerate(row1_kpis):
    # ... metric display logic (25 lines)

# Lines 323-347 (Row 2)
cols = st.columns(4)
for i, kpi in enumerate(row2_kpis):
    # ... IDENTICAL metric display logic (25 lines)
```

**Issue:** 50 lines for nearly identical code

### Example 3: Constants Scattered
```python
# analyzer.py
KPI_COLUMNS = ['avg_ticket', 'covers', 'labor_cost_pct', ...]
KPI_NAMES = {same keys...}

# app.py
cost_metrics = {'labor_cost_pct', 'food_cost_pct'}
revenue_metrics = {'avg_ticket', 'covers', ...}

# validators.py
REQUIRED_COLUMNS = [different set of 10 columns]

# transaction_validator.py
required_columns = [different set of 5 columns]
```

**Issue:** 5+ different definitions, hard to keep in sync

---

## Recommendations Timeline

| Phase | Tasks | Effort | Benefit |
|-------|-------|--------|---------|
| **Phase 1** | Remove duplicate validation; Create config.py | 3-5 hrs | -50 lines, single source of truth |
| **Phase 2** | Extract formatters.py; Refactor app.py | 5-7 hrs | -100 lines, better readability |
| **Phase 3** | Add caching; Improve error handling | 2-3 hrs | +performance, better debugging |

---

## Conclusion

**FLAVYR MVP is WELL-ENGINEERED at its current size.** The architecture is sound, and the code is generally clean and maintainable.

However, there are clear opportunities to:
1. **Eliminate duplication** (validation, constants, formatting)
2. **Centralize configuration** (all KPI metadata in one place)
3. **Break up large functions** (especially app.py page handlers)

These improvements would:
- Reduce codebase by ~100-150 lines (5-10%)
- Improve maintainability significantly
- Make future changes easier
- Reduce bugs from inconsistencies

**Estimated effort:** 2-3 sprints of focused refactoring with zero breaking changes.

---

## Full Analysis Document

For detailed analysis including:
- Line-by-line breakdown of each module
- Complete dependency graph
- Cyclomatic complexity analysis
- Code examples for each issue
- Implementation recommendations

See: `CODEBASE_ANALYSIS.md` in this directory
