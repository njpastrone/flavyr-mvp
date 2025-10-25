# FLAVYR MVP - Code Simplification Action Plan

## Executive Summary

The FLAVYR MVP codebase is well-engineered at 2,774 lines across 11 Python files. However, comprehensive analysis reveals opportunities to reduce complexity by 100-150 lines (5-10%) and significantly improve maintainability through strategic consolidation.

**Current State:**
- Total Python LOC: 2,774
- Total Functions: ~68
- Code Quality: GOOD
- Architecture: Clean separation of concerns

**Simplification Potential:**
- Remove duplicate validation: ~36 lines
- Consolidate constants: ~50 lines
- Extract formatters: ~40 lines
- Refactor UI patterns: ~50 lines
- Total Reduction: ~176 lines (6.3%)

---

## Critical Issues Found

### 1. Duplicate Validation Functions (MUST FIX)

**Problem:** `validate_transaction_data()` exists in TWO locations:
- [src/transaction_analyzer.py:258](src/transaction_analyzer.py#L258) - NEVER called
- [utils/transaction_validator.py:12](utils/transaction_validator.py#L12) - Actually used

**Impact:**
- 36 lines of dead code
- Maintenance burden
- Risk of inconsistencies

**Action:** Delete unused function from transaction_analyzer.py

**Effort:** 30 minutes

---

### 2. Constants Scattered Across 5+ Files (HIGH IMPACT)

**Problem:** Same KPI definitions appear in multiple files with inconsistent names:

| Constant | Files | Example |
|----------|-------|---------|
| KPI columns | analyzer.py, validators.py, app.py | `KPI_COLUMNS`, `REQUIRED_COLUMNS` |
| KPI names | analyzer.py, app.py | `KPI_NAMES`, `kpi_help` |
| Cost/revenue metrics | analyzer.py, app.py | `LOWER_IS_BETTER`, `cost_metrics` |
| Problem mappings | recommender.py | `KPI_TO_PROBLEM` |
| Required columns | 3 files | Different definitions |

**Impact:**
- ~50 lines of duplication
- Hard to update consistently
- Error-prone maintenance

**Action:** Create centralized `src/config.py`

**Effort:** 2-3 hours

---

## Simplification Strategy

### Phase 1: Remove Dead Code (1-2 hours)

**Priority: CRITICAL**

#### Task 1.1: Delete Unused Validation Function
- File: [src/transaction_analyzer.py](src/transaction_analyzer.py)
- Lines: 258-293 (36 lines)
- Function: `validate_transaction_data()`
- Verification: No imports or calls to this function anywhere

#### Task 1.2: Check for Unused Imports
Run automated check:
```bash
pip install autoflake
autoflake --remove-all-unused-imports --check app.py src/*.py utils/*.py
```

**Expected Impact:** -36 lines minimum

---

### Phase 2: Centralize Configuration (2-3 hours)

**Priority: HIGH**

#### Task 2.1: Create src/config.py

New file structure:
```python
# src/config.py
from typing import Dict, List, Set

class KPIConfig:
    """Central configuration for all KPI-related constants."""

    # Core KPI definitions
    COLUMNS: List[str] = [
        'avg_ticket', 'covers', 'labor_cost_pct',
        'food_cost_pct', 'table_turnover',
        'sales_per_sqft', 'expected_customer_repeat_rate'
    ]

    # Friendly names
    NAMES: Dict[str, str] = {
        'avg_ticket': 'Average Ticket',
        'covers': 'Covers',
        # ... etc
    }

    # Cost metrics (lower is better)
    LOWER_IS_BETTER: List[str] = ['labor_cost_pct', 'food_cost_pct']
    COST_METRICS: Set[str] = {'labor_cost_pct', 'food_cost_pct'}
    REVENUE_METRICS: Set[str] = {
        'avg_ticket', 'covers', 'table_turnover',
        'sales_per_sqft', 'expected_customer_repeat_rate'
    }

    # KPI to business problem mapping
    TO_PROBLEM: Dict[str, str] = {
        'covers': 'Increase Quantity of Sales',
        'avg_ticket': 'Boost Average Order Value (AOV)',
        # ... etc
    }

    # Help text for UI
    HELP_TEXT: Dict[str, str] = {
        'avg_ticket': 'IMPACT: Directly increases revenue...',
        # ... etc
    }

    # Layout groupings for UI
    ROW1_KPIS: List[str] = ['avg_ticket', 'covers', 'table_turnover', 'sales_per_sqft']
    ROW2_KPIS: List[str] = ['labor_cost_pct', 'food_cost_pct', 'expected_customer_repeat_rate']


class ValidationConfig:
    """Central configuration for data validation."""

    # Restaurant POS CSV required columns
    RESTAURANT_REQUIRED_COLUMNS: List[str] = [
        'date', 'cuisine_type', 'dining_model',
        'avg_ticket', 'covers', 'labor_cost_pct',
        'food_cost_pct', 'table_turnover', 'sales_per_sqft',
        'expected_customer_repeat_rate'
    ]

    # Transaction CSV required columns
    TRANSACTION_REQUIRED_COLUMNS: List[str] = [
        'date', 'total', 'customer_id', 'item_name', 'day_of_week'
    ]


class ColorScheme:
    """UI color scheme."""

    GOOD = '#00ff00'
    BAD = '#ff0000'
    CRITICAL = '#ffcccc'
    WARNING = '#fff4cc'
    EXCELLENT = '#ccffcc'
```

#### Task 2.2: Update Files to Use config.py

Files to update:
1. [src/analyzer.py](src/analyzer.py) - Remove KPI_COLUMNS, KPI_NAMES, LOWER_IS_BETTER
2. [src/recommender.py](src/recommender.py) - Remove KPI_TO_PROBLEM
3. [app.py](app.py) - Remove cost_metrics, revenue_metrics, kpi_help, row groupings
4. [utils/validators.py](utils/validators.py) - Remove REQUIRED_COLUMNS
5. [utils/transaction_validator.py](utils/transaction_validator.py) - Remove required_columns

Example update for analyzer.py:
```python
# OLD
KPI_COLUMNS = ['avg_ticket', 'covers', ...]
KPI_NAMES = {...}

# NEW
from src.config import KPIConfig

# Use KPIConfig.COLUMNS instead of KPI_COLUMNS
# Use KPIConfig.NAMES instead of KPI_NAMES
```

**Expected Impact:** -50 lines, single source of truth

---

### Phase 3: Extract Formatting Utilities (2-3 hours)

**Priority: MEDIUM**

#### Task 3.1: Create src/formatters.py

Consolidate all result formatting logic:

```python
# src/formatters.py
from typing import Dict, List, Any
import pandas as pd

def format_gaps_for_display(gaps: Dict[str, Dict]) -> str:
    """Format gap analysis results for display."""
    # Moved from analyzer.py
    pass

def format_recommendations_for_display(recommendations: List[Dict]) -> str:
    """Format recommendations for display."""
    # Moved from recommender.py
    pass

def format_transaction_results_for_ui(results: Dict) -> Dict:
    """Format transaction analysis for UI display."""
    # Moved from transaction_analyzer.py
    pass

def create_kpi_comparison_table(gaps: Dict) -> List[List[Any]]:
    """Create table data for reports."""
    # Moved from report_generator.py
    pass

def format_currency(value: float) -> str:
    """Standardize currency formatting."""
    return f"${value:,.2f}"

def format_percentage(value: float) -> str:
    """Standardize percentage formatting."""
    return f"{value:.1f}%"

def get_status_color(gap_pct: float, is_cost_metric: bool) -> str:
    """Get color based on gap and metric type."""
    from src.config import ColorScheme

    if is_cost_metric:
        return ColorScheme.GOOD if gap_pct < 0 else ColorScheme.BAD
    else:
        return ColorScheme.GOOD if gap_pct > 0 else ColorScheme.BAD
```

#### Task 3.2: Update Files to Use Formatters

Files to update:
1. [src/analyzer.py](src/analyzer.py) - Move format_gap_summary()
2. [src/recommender.py](src/recommender.py) - Move create_recommendation_summary(), format_deal_types()
3. [src/report_generator.py](src/report_generator.py) - Move create_kpi_comparison_table()
4. [src/transaction_analyzer.py](src/transaction_analyzer.py) - Move format_results_for_display()
5. [app.py](app.py) - Use formatters instead of inline logic

**Expected Impact:** -40 lines, better organization

---

### Phase 4: Refactor UI Repetition (3-4 hours)

**Priority: MEDIUM**

#### Task 4.1: Extract Metric Display Helper

Current issue: Lines 297-347 in [app.py](app.py) contain 51 lines of nearly identical metric display code.

Create helper function:
```python
# In app.py or utils/ui_helpers.py
def display_metric_grid(
    gaps: Dict[str, Dict],
    kpi_list: List[str],
    kpi_help: Dict[str, str]
) -> None:
    """Display a grid of KPI metrics with deltas."""
    from src.config import KPIConfig

    cols = st.columns(len(kpi_list))
    for i, kpi in enumerate(kpi_list):
        data = gaps[kpi]
        with cols[i]:
            gap_pct = data['gap_pct']

            # Determine delta color based on metric type
            if kpi in KPIConfig.COST_METRICS:
                delta_color = "inverse" if gap_pct >= 0 else "normal"
            else:
                delta_color = "normal" if gap_pct >= 0 else "inverse"

            # Format labels
            value_label = f"Your: {data['restaurant_value']:.2f}"
            delta_label = f"Benchmark: {data['benchmark_value']:.2f} ({gap_pct:+.1f}%)"

            # Display metric
            st.metric(
                label=KPIConfig.NAMES[kpi],
                value=value_label,
                delta=delta_label,
                delta_color=delta_color,
                help=kpi_help.get(kpi, '')
            )
```

Then in dashboard_page():
```python
# OLD (51 lines)
cols = st.columns(4)
for i, kpi in enumerate(row1_kpis):
    # ... 25 lines
cols = st.columns(4)
for i, kpi in enumerate(row2_kpis):
    # ... 25 lines

# NEW (6 lines)
display_metric_grid(gaps, KPIConfig.ROW1_KPIS, kpi_help)
display_metric_grid(gaps, KPIConfig.ROW2_KPIS, kpi_help)
```

**Expected Impact:** -45 lines in dashboard_page()

#### Task 4.2: Break Up Large Page Functions

Target: [transaction_insights_page()](app.py) - 251 lines

Extract sections:
```python
def _render_transaction_upload_section() -> Optional[pd.DataFrame]:
    """Handle file upload and validation. Returns validated dataframe or None."""
    st.header("Upload Transaction Data")
    # Lines 650-720 from original function
    pass

def _render_transaction_metrics_section(results: Dict) -> None:
    """Display summary metrics."""
    st.subheader("Transaction Insights")
    # Lines 721-760
    pass

def _render_slowest_days_section(results: Dict) -> None:
    """Display slowest day analysis with charts."""
    st.subheader("Slowest Days Analysis")
    # Lines 761-810
    pass

def _render_item_rankings_section(results: Dict) -> None:
    """Display top/bottom selling items."""
    st.subheader("Item Performance")
    # Lines 811-850
    pass

def _render_tactical_recommendations_section(results: Dict) -> None:
    """Display day-specific recommendations."""
    st.subheader("Tactical Recommendations")
    # Lines 851-900
    pass

def transaction_insights_page() -> None:
    """Transaction insights page - orchestrator."""
    st.title("Transaction-Level Insights")

    # Upload section
    df = _render_transaction_upload_section()
    if df is None:
        return

    # Process and analyze
    results = analyze_transactions(df)
    st.session_state.transaction_results = results

    # Render sections
    _render_transaction_metrics_section(results)
    _render_slowest_days_section(results)
    _render_item_rankings_section(results)
    _render_tactical_recommendations_section(results)
```

**Expected Impact:** Better readability, easier testing, ~10 lines saved

---

### Phase 5: Performance Optimizations (1 hour)

**Priority: LOW**

#### Task 5.1: Add Caching for Static Data

Update [src/data_loader.py](src/data_loader.py):

```python
import streamlit as st

@st.cache_data
def get_benchmark_data(cuisine_type: str, dining_model: str) -> Optional[pd.DataFrame]:
    """Get benchmark data (cached)."""
    # Existing implementation
    pass

@st.cache_data
def get_all_deal_bank_data() -> Optional[pd.DataFrame]:
    """Get all deal bank data (cached)."""
    # Existing implementation
    pass
```

**Expected Impact:** Improved UI responsiveness, no line reduction

#### Task 5.2: Fix Misleading Function Name

In [src/data_loader.py:151](src/data_loader.py#L151):

```python
# OLD
def aggregate_daily_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates daily POS data into monthly averages."""
    # Actually computes overall averages, not monthly

# NEW
def compute_aggregate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Computes overall aggregate metrics from daily POS data."""
    # More accurate name
```

---

## Implementation Timeline

| Phase | Tasks | Effort | Lines Saved | Priority |
|-------|-------|--------|-------------|----------|
| **Phase 1** | Remove dead code, unused imports | 1-2 hrs | -36 | CRITICAL |
| **Phase 2** | Create config.py, consolidate constants | 2-3 hrs | -50 | HIGH |
| **Phase 3** | Extract formatters.py | 2-3 hrs | -40 | MEDIUM |
| **Phase 4** | Refactor UI patterns, break up functions | 3-4 hrs | -50 | MEDIUM |
| **Phase 5** | Add caching, rename functions | 1 hr | 0 | LOW |
| **TOTAL** | **All phases** | **9-13 hrs** | **-176 lines** | |

---

## Risk Assessment

### Low Risk Changes (Do First)
- Phase 1: Remove dead code
- Phase 5: Add caching decorators
- Rename functions for clarity

**Risk:** Minimal - these are isolated changes

### Medium Risk Changes (Test Thoroughly)
- Phase 2: Create config.py
- Phase 3: Extract formatters.py

**Risk:** Moderate - affects multiple files, but imports are straightforward

**Mitigation:**
- Update one file at a time
- Run tests after each file
- Keep git commits small

### Higher Risk Changes (Plan Carefully)
- Phase 4: Refactor large UI functions

**Risk:** Higher - UI behavior could change

**Mitigation:**
- Test each extracted section independently
- Compare UI before/after visually
- Keep original functions until verified

---

## Testing Strategy

### After Each Phase:

1. **Unit Tests**
```bash
python test_app.py
python test_ux_improvements.py
```

2. **Manual UI Testing**
- Upload sample POS data
- Upload transaction data
- Generate reports (PDF and HTML)
- Check all tabs render correctly
- Verify metrics display properly

3. **Integration Testing**
- End-to-end flow: upload → analyze → recommend → report
- Check session state persistence
- Test error handling

4. **Regression Checks**
- Compare gap calculations before/after
- Compare recommendation outputs
- Compare report contents

---

## File Change Checklist

### Files to Modify (by phase)

**Phase 1:**
- [ ] [src/transaction_analyzer.py](src/transaction_analyzer.py) - Delete lines 258-293

**Phase 2:**
- [ ] Create [src/config.py](src/config.py) - New file
- [ ] [src/analyzer.py](src/analyzer.py) - Replace constants with imports
- [ ] [src/recommender.py](src/recommender.py) - Replace constants with imports
- [ ] [app.py](app.py) - Replace constants with imports
- [ ] [utils/validators.py](utils/validators.py) - Replace constants with imports
- [ ] [utils/transaction_validator.py](utils/transaction_validator.py) - Replace constants with imports

**Phase 3:**
- [ ] Create [src/formatters.py](src/formatters.py) - New file
- [ ] [src/analyzer.py](src/analyzer.py) - Move format_gap_summary()
- [ ] [src/recommender.py](src/recommender.py) - Move formatting functions
- [ ] [src/report_generator.py](src/report_generator.py) - Move table creation
- [ ] [src/transaction_analyzer.py](src/transaction_analyzer.py) - Move format_results_for_display()
- [ ] [app.py](app.py) - Use formatters

**Phase 4:**
- [ ] [app.py](app.py) - Extract display_metric_grid()
- [ ] [app.py](app.py) - Extract transaction page helpers

**Phase 5:**
- [ ] [src/data_loader.py](src/data_loader.py) - Add caching decorators
- [ ] [src/data_loader.py](src/data_loader.py) - Rename aggregate_daily_to_monthly()

---

## Expected Outcomes

### Quantitative Benefits
- **Code reduction:** 176 lines (6.3%)
- **Files reduced:** From 11 to 13 (adding config.py, formatters.py)
- **Lines per file:** Average drops from 252 to 232
- **Longest function:** Reduced from 251 to ~50 lines
- **Constants consolidated:** 8-10 definitions → 2 config classes

### Qualitative Benefits
- **Single source of truth** for all KPI metadata
- **Easier maintenance** - update constants in one place
- **Better testability** - smaller, focused functions
- **Improved readability** - less repetition
- **Clearer architecture** - config, formatters, logic separated
- **Faster onboarding** - new developers find things easily

### No Breaking Changes
- All refactoring preserves existing functionality
- No changes to:
  - Database schema
  - CSV formats
  - API contracts
  - User-facing behavior

---

## Success Metrics

After completing all phases, verify:

- [ ] All tests pass
- [ ] No regressions in UI behavior
- [ ] Gap calculations remain identical
- [ ] Recommendations unchanged
- [ ] Reports generate correctly
- [ ] Performance improved or unchanged
- [ ] Code is more maintainable
- [ ] Constants centralized
- [ ] No duplicate validation code
- [ ] Largest function < 100 lines

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Create feature branch** for refactoring
3. **Execute Phase 1** (critical fixes first)
4. **Test and verify** after each phase
5. **Update documentation** as changes are made
6. **Merge to main** when all phases complete and tested

---

## Related Documents

- [CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md) - Full detailed analysis
- [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md) - Executive summary
- [planning_docs/principles.md](planning_docs/principles.md) - Project principles
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Current implementation status

---

**Estimated Total Effort:** 9-13 hours across 5 phases
**Expected Benefit:** 6-10% code reduction, significant maintainability improvement
**Risk Level:** LOW to MEDIUM with proper testing
**Recommended Timeline:** 2-3 focused work sessions
