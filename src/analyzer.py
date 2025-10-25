"""
Performance gap analysis engine for FLAVYR MVP.
Compares restaurant metrics against industry benchmarks.
"""

import pandas as pd
from typing import Dict, List, Tuple
from src.config import KPIConfig


def calculate_gap_percentage(restaurant_value: float, benchmark_value: float, lower_is_better: bool = False) -> float:
    """
    Calculate percentage gap between restaurant and benchmark.

    Args:
        restaurant_value: Restaurant's metric value
        benchmark_value: Benchmark metric value
        lower_is_better: If True, negative gap means overperforming (for costs)

    Returns:
        Gap percentage (positive = above benchmark, negative = below benchmark)
    """
    if benchmark_value == 0:
        return 0.0

    gap = ((restaurant_value - benchmark_value) / benchmark_value) * 100

    # For cost metrics, invert the gap interpretation
    if lower_is_better:
        gap = -gap

    return gap


def calculate_all_gaps(restaurant_data: pd.Series, benchmark_data: pd.Series) -> Dict[str, Dict]:
    """
    Calculate gaps for all KPIs.

    Args:
        restaurant_data: Restaurant metrics (single row as Series)
        benchmark_data: Benchmark metrics (single row as Series)

    Returns:
        Dictionary with gap analysis for each KPI
    """
    gaps = {}

    for kpi in KPIConfig.COLUMNS:
        restaurant_value = restaurant_data[kpi]
        benchmark_value = benchmark_data[kpi]
        lower_is_better = kpi in KPIConfig.LOWER_IS_BETTER

        gap_pct = calculate_gap_percentage(restaurant_value, benchmark_value, lower_is_better)

        gaps[kpi] = {
            'kpi_name': KPIConfig.NAMES[kpi],
            'restaurant_value': restaurant_value,
            'benchmark_value': benchmark_value,
            'gap_pct': gap_pct,
            'lower_is_better': lower_is_better
        }

    return gaps


def identify_underperforming_kpis(gaps: Dict[str, Dict], threshold: float = -5.0) -> List[Tuple[str, Dict]]:
    """
    Identify KPIs where restaurant is underperforming.

    Args:
        gaps: Gap analysis dictionary from calculate_all_gaps
        threshold: Gap percentage threshold (default: -5%)

    Returns:
        List of (kpi_key, gap_data) tuples for underperforming KPIs
    """
    underperforming = []

    for kpi, data in gaps.items():
        if data['gap_pct'] < threshold:
            underperforming.append((kpi, data))

    return underperforming


def rank_issues_by_severity(gaps: Dict[str, Dict]) -> List[Tuple[str, Dict]]:
    """
    Rank all gaps by severity (most negative first).

    Args:
        gaps: Gap analysis dictionary from calculate_all_gaps

    Returns:
        List of (kpi_key, gap_data) tuples sorted by gap percentage (ascending)
    """
    # Convert to list of tuples
    gap_list = [(kpi, data) for kpi, data in gaps.items()]

    # Sort by gap percentage (most negative first)
    gap_list.sort(key=lambda x: x[1]['gap_pct'])

    return gap_list


def get_performance_grade(gaps: Dict[str, Dict]) -> str:
    """
    Calculate overall performance grade based on gaps.

    Args:
        gaps: Gap analysis dictionary

    Returns:
        Performance grade (A, B, C, D, F)
    """
    # Calculate average gap across all KPIs
    total_gap = sum(data['gap_pct'] for data in gaps.values())
    avg_gap = total_gap / len(gaps)

    # Assign grade based on average gap
    if avg_gap >= 10:
        return 'A'
    elif avg_gap >= 0:
        return 'B'
    elif avg_gap >= -10:
        return 'C'
    elif avg_gap >= -20:
        return 'D'
    else:
        return 'F'


def format_gap_summary(gaps: Dict[str, Dict]) -> str:
    """
    Create a human-readable summary of gaps.

    Args:
        gaps: Gap analysis dictionary

    Returns:
        Formatted string summary
    """
    ranked_gaps = rank_issues_by_severity(gaps)

    summary_lines = []
    for kpi, data in ranked_gaps[:3]:  # Top 3 issues
        kpi_name = data['kpi_name']
        gap_pct = data['gap_pct']

        if gap_pct < 0:
            summary_lines.append(f"- {kpi_name}: {abs(gap_pct):.1f}% below benchmark")
        else:
            summary_lines.append(f"- {kpi_name}: {gap_pct:.1f}% above benchmark")

    return '\n'.join(summary_lines)


def analyze_restaurant_performance(restaurant_data: pd.DataFrame, benchmark_data: pd.DataFrame) -> Dict:
    """
    Complete performance analysis of a restaurant.

    Args:
        restaurant_data: Restaurant metrics (single row dataframe)
        benchmark_data: Benchmark metrics (single row dataframe)

    Returns:
        Dictionary with complete analysis results
    """
    # Convert to Series for easier access
    restaurant_series = restaurant_data.iloc[0]
    benchmark_series = benchmark_data.iloc[0]

    # Calculate all gaps
    gaps = calculate_all_gaps(restaurant_series, benchmark_series)

    # Identify issues
    underperforming = identify_underperforming_kpis(gaps, threshold=-5.0)
    ranked_issues = rank_issues_by_severity(gaps)

    # Get overall grade
    grade = get_performance_grade(gaps)

    # Create summary
    summary = format_gap_summary(gaps)

    return {
        'cuisine_type': restaurant_series['cuisine_type'],
        'dining_model': restaurant_series['dining_model'],
        'gaps': gaps,
        'underperforming_kpis': underperforming,
        'ranked_issues': ranked_issues,
        'performance_grade': grade,
        'summary': summary
    }
