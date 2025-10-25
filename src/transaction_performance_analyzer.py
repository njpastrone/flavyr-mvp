"""
Transaction Performance Analyzer

Compares actual transaction metrics against industry benchmarks
and identifies performance gaps that map to business problems.

Includes transparency metadata to show how calculations were performed.
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime


def analyze_loyalty_performance(
    actual_loyalty_rate: float,
    benchmark_loyalty_rate: float,
    total_customers: int = 0,
    repeat_customers: int = 0
) -> Dict:
    """
    Analyze customer loyalty performance vs. benchmark.

    Args:
        actual_loyalty_rate: Restaurant's actual loyalty rate (percentage)
        benchmark_loyalty_rate: Industry benchmark (percentage)
        total_customers: Total number of unique customers
        repeat_customers: Number of customers with 2+ visits

    Returns:
        Dict with gap analysis, severity classification, and transparency data
    """
    gap = actual_loyalty_rate - benchmark_loyalty_rate
    gap_pct = (gap / benchmark_loyalty_rate * 100) if benchmark_loyalty_rate > 0 else 0

    # Determine severity
    if actual_loyalty_rate < 25:
        severity = "critical"
        severity_label = "Critical"
    elif actual_loyalty_rate < 30:
        severity = "high"
        severity_label = "High"
    elif gap < -5:  # More than 5 percentage points below benchmark
        severity = "medium"
        severity_label = "Medium"
    else:
        severity = "good"
        severity_label = "Good"

    # Transparency metadata
    transparency = {
        'thresholds': {
            'critical': '<25%',
            'high': '25-30%',
            'medium': '30-35% or <5pp below benchmark',
            'good': '>Benchmark'
        },
        'calculation_inputs': {
            'total_customers': total_customers,
            'repeat_customers': repeat_customers,
            'new_customers': total_customers - repeat_customers
        },
        'calculation_formula': '(Repeat Customers ÷ Total Customers) × 100',
        'data_source': 'transaction_uploads'
    }

    return {
        'metric': 'loyalty_rate',
        'actual_value': actual_loyalty_rate,
        'benchmark_value': benchmark_loyalty_rate,
        'gap': gap,
        'gap_pct': gap_pct,
        'severity': severity,
        'severity_label': severity_label,
        'has_issue': severity != 'good',
        'issue_type': 'Low Customer Loyalty' if severity != 'good' else None,
        'transparency': transparency
    }


def analyze_aov_performance(
    actual_aov: float,
    aov_by_day: Dict[str, float],
    benchmark_aov_weekday: float,
    benchmark_aov_weekend: float,
    benchmark_variation_pct: float
) -> Dict:
    """
    Analyze Average Order Value performance vs. benchmarks.

    Args:
        actual_aov: Overall average order value
        aov_by_day: Dict of day_name -> aov_value
        benchmark_aov_weekday: Expected weekday AOV
        benchmark_aov_weekend: Expected weekend AOV
        benchmark_variation_pct: Expected weekend uplift percentage

    Returns:
        Dict with AOV gap analysis
    """
    # Calculate overall benchmark (weighted average assuming 5 weekdays, 2 weekend days)
    benchmark_aov_overall = (benchmark_aov_weekday * 5 + benchmark_aov_weekend * 2) / 7

    # Overall AOV gap
    gap = actual_aov - benchmark_aov_overall
    gap_pct = (gap / benchmark_aov_overall * 100) if benchmark_aov_overall > 0 else 0

    # Determine severity
    if actual_aov < benchmark_aov_overall * 0.90:  # <90% of benchmark
        severity = "high"
        severity_label = "High"
    elif actual_aov < benchmark_aov_overall * 0.95:  # 90-95% of benchmark
        severity = "medium"
        severity_label = "Medium"
    else:
        severity = "good"
        severity_label = "Good"

    # Calculate actual weekend uplift
    weekend_days = ['Saturday', 'Sunday']
    weekday_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    weekend_aovs = [aov_by_day.get(day, 0) for day in weekend_days if day in aov_by_day]
    weekday_aovs = [aov_by_day.get(day, 0) for day in weekday_days if day in aov_by_day]

    actual_weekend_avg = sum(weekend_aovs) / len(weekend_aovs) if weekend_aovs else 0
    actual_weekday_avg = sum(weekday_aovs) / len(weekday_aovs) if weekday_aovs else 0

    actual_variation_pct = 0
    if actual_weekday_avg > 0:
        actual_variation_pct = ((actual_weekend_avg - actual_weekday_avg) / actual_weekday_avg * 100)

    # Check weekend uplift issue
    weekend_uplift_issue = actual_variation_pct < 15  # Less than 15% uplift

    return {
        'metric': 'aov',
        'actual_value': actual_aov,
        'benchmark_value': benchmark_aov_overall,
        'gap': gap,
        'gap_pct': gap_pct,
        'severity': severity,
        'severity_label': severity_label,
        'has_issue': severity != 'good',
        'issue_type': 'Low Average Order Value' if severity != 'good' else None,
        'weekend_uplift': {
            'actual_pct': actual_variation_pct,
            'benchmark_pct': benchmark_variation_pct,
            'has_issue': weekend_uplift_issue,
            'actual_weekend_avg': actual_weekend_avg,
            'actual_weekday_avg': actual_weekday_avg
        }
    }


def analyze_slowest_day_performance(
    slowest_day_name: str,
    slowest_day_count: int,
    average_daily_count: float,
    expected_slowest_day: str,
    benchmark_drop_pct: float
) -> Dict:
    """
    Analyze slowest day performance vs. benchmark.

    Args:
        slowest_day_name: Name of the slowest day
        slowest_day_count: Transaction count on slowest day
        average_daily_count: Average transactions per day
        expected_slowest_day: Industry benchmark slowest day
        benchmark_drop_pct: Expected percentage drop from average

    Returns:
        Dict with slowest day gap analysis
    """
    # Calculate actual drop percentage
    actual_drop_pct = 0
    if average_daily_count > 0:
        actual_drop_pct = ((average_daily_count - slowest_day_count) / average_daily_count * 100)

    # Check if slowest day matches expectation
    day_matches_expectation = slowest_day_name == expected_slowest_day

    # Determine severity
    if actual_drop_pct > 40:  # >40% drop
        severity = "critical"
        severity_label = "Critical"
    elif actual_drop_pct > 35:  # 35-40% drop
        severity = "high"
        severity_label = "High"
    elif actual_drop_pct > benchmark_drop_pct + 5:  # More than 5pp above benchmark
        severity = "medium"
        severity_label = "Medium"
    else:
        severity = "good"
        severity_label = "Good"

    return {
        'metric': 'slowest_day',
        'actual_day': slowest_day_name,
        'expected_day': expected_slowest_day,
        'day_matches': day_matches_expectation,
        'actual_drop_pct': actual_drop_pct,
        'benchmark_drop_pct': benchmark_drop_pct,
        'drop_gap': actual_drop_pct - benchmark_drop_pct,
        'severity': severity,
        'severity_label': severity_label,
        'has_issue': severity != 'good',
        'issue_type': 'Excessive Slow Day Drop' if severity != 'good' else None,
        'transaction_count': slowest_day_count,
        'average_count': average_daily_count
    }


def analyze_item_performance(
    top_items: List[Dict],
    bottom_items: List[Dict],
    total_revenue: float,
    benchmark_top_item_share_pct: float,
    benchmark_bottom_threshold_pct: float
) -> Dict:
    """
    Analyze item performance and menu balance.

    Args:
        top_items: List of top items with 'item', 'revenue', 'quantity'
        bottom_items: List of bottom items with 'item', 'revenue', 'quantity'
        total_revenue: Total revenue across all items
        benchmark_top_item_share_pct: Healthy max percentage for top item
        benchmark_bottom_threshold_pct: Minimum revenue share for items

    Returns:
        Dict with item performance analysis
    """
    issues = []

    # Analyze top item concentration
    top_item_revenue_share = 0
    if top_items and total_revenue > 0:
        top_item_revenue = top_items[0]['revenue']
        top_item_revenue_share = (top_item_revenue / total_revenue * 100)

    top_item_issue = top_item_revenue_share > 30  # Critical threshold
    top_item_warning = top_item_revenue_share > benchmark_top_item_share_pct

    if top_item_issue:
        issues.append({
            'type': 'Over-reliance on Single Item',
            'severity': 'medium',
            'severity_label': 'Medium',
            'metric': 'top_item_concentration',
            'actual_value': top_item_revenue_share,
            'benchmark_value': benchmark_top_item_share_pct,
            'item_name': top_items[0]['item'] if top_items else None
        })

    # Analyze bottom items - count how many are below threshold
    poor_performers = []
    if bottom_items and total_revenue > 0:
        for item in bottom_items:
            item_share = (item['revenue'] / total_revenue * 100)
            if item_share < benchmark_bottom_threshold_pct:
                poor_performers.append({
                    'item': item['item'],
                    'revenue_share': item_share,
                    'revenue': item['revenue']
                })

    poor_performers_issue = len(poor_performers) > 5

    if poor_performers_issue:
        issues.append({
            'type': 'Too Many Low Performers',
            'severity': 'medium',
            'severity_label': 'Medium',
            'metric': 'bottom_items_count',
            'actual_value': len(poor_performers),
            'benchmark_value': 3,
            'items': poor_performers
        })

    return {
        'metric': 'item_performance',
        'top_item_concentration': {
            'percentage': top_item_revenue_share,
            'benchmark': benchmark_top_item_share_pct,
            'has_issue': top_item_warning,
            'is_critical': top_item_issue,
            'item_name': top_items[0]['item'] if top_items else None
        },
        'poor_performers': {
            'count': len(poor_performers),
            'benchmark_max': 3,
            'has_issue': poor_performers_issue,
            'items': poor_performers
        },
        'has_issue': len(issues) > 0,
        'issues': issues
    }


def generate_transaction_performance_report(
    transaction_results: Dict,
    transaction_benchmarks: pd.Series,
    total_revenue: float = None
) -> Dict:
    """
    Generate complete transaction performance report with benchmark comparisons.

    Args:
        transaction_results: Results from analyze_transactions() (formatted)
        transaction_benchmarks: Benchmark data for restaurant type
        total_revenue: Total revenue (optional, calculated from data if not provided)

    Returns:
        Dict with complete performance analysis including all gaps and issues
    """
    # Extract actual values from transaction results
    loyalty_data = transaction_results.get('Customer Loyalty', {})
    aov_data = transaction_results.get('Average Order Value', {})
    slowest_tx = transaction_results.get('Slowest Day (Transactions)', {})
    top_items = transaction_results.get('Top Items (Revenue)', [])
    bottom_items = transaction_results.get('Bottom Items (Revenue)', [])

    # Parse actual loyalty rate (remove % sign)
    actual_loyalty_rate = float(loyalty_data.get('Loyalty Rate', '0%').replace('%', ''))
    total_customers = loyalty_data.get('Total Customers', 0)
    repeat_customers = loyalty_data.get('Repeat Customers', 0)

    # Parse actual AOV (remove $ and commas)
    actual_aov_str = aov_data.get('Overall AOV', '$0')
    actual_aov = float(actual_aov_str.replace('$', '').replace(',', ''))

    # Parse AOV by day
    aov_by_day_str = aov_data.get('By Day of Week', {})
    aov_by_day = {}
    for day, value in aov_by_day_str.items():
        aov_by_day[day] = float(value.replace('$', '').replace(',', ''))

    # Calculate average daily transactions
    all_days_counts = slowest_tx.get('All Days', {})
    average_daily_count = sum(all_days_counts.values()) / len(all_days_counts) if all_days_counts else 0

    # Calculate total revenue if not provided
    if total_revenue is None:
        total_revenue = sum(item['revenue'] for item in top_items)

    # Run all analyses with transparency data
    loyalty_analysis = analyze_loyalty_performance(
        actual_loyalty_rate,
        transaction_benchmarks.get('benchmark_loyalty_rate', 35.0),
        total_customers,
        repeat_customers
    )

    aov_analysis = analyze_aov_performance(
        actual_aov,
        aov_by_day,
        transaction_benchmarks.get('benchmark_aov_weekday', 25.0),
        transaction_benchmarks.get('benchmark_aov_weekend', 32.0),
        transaction_benchmarks.get('benchmark_aov_variation_pct', 28.0)
    )

    slowest_day_analysis = analyze_slowest_day_performance(
        slowest_tx.get('Day', 'Monday'),
        slowest_tx.get('Transaction Count', 0),
        average_daily_count,
        transaction_benchmarks.get('expected_slowest_day', 'Monday'),
        transaction_benchmarks.get('benchmark_slow_day_drop_pct', 30.0)
    )

    item_analysis = analyze_item_performance(
        top_items,
        bottom_items,
        total_revenue,
        transaction_benchmarks.get('benchmark_top_item_share_pct', 20.0),
        transaction_benchmarks.get('benchmark_bottom_item_threshold_pct', 2.5)
    )

    # Collect all issues
    all_issues = []

    if loyalty_analysis['has_issue']:
        all_issues.append({
            'category': 'Customer Loyalty',
            'severity': loyalty_analysis['severity'],
            'severity_label': loyalty_analysis['severity_label'],
            'issue_type': loyalty_analysis['issue_type'],
            'analysis': loyalty_analysis
        })

    if aov_analysis['has_issue']:
        all_issues.append({
            'category': 'Average Order Value',
            'severity': aov_analysis['severity'],
            'severity_label': aov_analysis['severity_label'],
            'issue_type': aov_analysis['issue_type'],
            'analysis': aov_analysis
        })

    if aov_analysis['weekend_uplift']['has_issue']:
        all_issues.append({
            'category': 'Weekend Performance',
            'severity': 'medium',
            'severity_label': 'Medium',
            'issue_type': 'Low Weekend Uplift',
            'analysis': aov_analysis['weekend_uplift']
        })

    if slowest_day_analysis['has_issue']:
        all_issues.append({
            'category': 'Slow Day Performance',
            'severity': slowest_day_analysis['severity'],
            'severity_label': slowest_day_analysis['severity_label'],
            'issue_type': slowest_day_analysis['issue_type'],
            'analysis': slowest_day_analysis
        })

    if item_analysis['has_issue']:
        for issue in item_analysis['issues']:
            all_issues.append({
                'category': 'Menu Performance',
                'severity': issue['severity'],
                'severity_label': issue['severity_label'],
                'issue_type': issue['type'],
                'analysis': issue
            })

    # Sort issues by severity (critical > high > medium > low)
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'good': 4}
    all_issues.sort(key=lambda x: severity_order.get(x['severity'], 4))

    return {
        'loyalty_analysis': loyalty_analysis,
        'aov_analysis': aov_analysis,
        'slowest_day_analysis': slowest_day_analysis,
        'item_analysis': item_analysis,
        'all_issues': all_issues,
        'total_issues': len(all_issues),
        'has_critical_issues': any(issue['severity'] == 'critical' for issue in all_issues),
        'has_high_issues': any(issue['severity'] == 'high' for issue in all_issues)
    }
