"""
Deal recommendation engine for FLAVYR MVP.
Maps performance gaps to business problems and suggests deals.
"""

import pandas as pd
from typing import List, Dict, Tuple


# Mapping from KPIs to business problems
KPI_TO_PROBLEM = {
    'covers': 'Increase Quantity of Sales',
    'avg_ticket': 'Boost Average Order Value (AOV)',
    'expected_customer_repeat_rate': 'Foster Customer Loyalty',
    'sales_per_sqft': 'Improve Slow Days',
    'labor_cost_pct': 'Enhance Profit Margins',
    'food_cost_pct': 'Enhance Profit Margins',
    'table_turnover': 'Increase Quantity of Sales'
}


def map_gaps_to_problems(underperforming_kpis: List[Tuple[str, Dict]], gap_threshold: float = -10.0) -> List[str]:
    """
    Map underperforming KPIs to business problems.

    Args:
        underperforming_kpis: List of (kpi, gap_data) tuples
        gap_threshold: Minimum gap to trigger problem mapping

    Returns:
        List of unique business problems
    """
    problems = set()

    for kpi, data in underperforming_kpis:
        gap_pct = data['gap_pct']

        # Only map if gap is significant
        if gap_pct < gap_threshold:
            if kpi in KPI_TO_PROBLEM:
                problems.add(KPI_TO_PROBLEM[kpi])

    return list(problems)


def get_deal_recommendations(problems: List[str], deal_bank_df: pd.DataFrame) -> List[Dict]:
    """
    Get deal recommendations for identified business problems.

    Args:
        problems: List of business problems
        deal_bank_df: Dataframe with deal bank data

    Returns:
        List of recommendation dictionaries
    """
    recommendations = []

    for problem in problems:
        # Find matching deals in deal bank
        matching_deals = deal_bank_df[
            deal_bank_df['business_problem'] == problem
        ]

        if len(matching_deals) > 0:
            deal_row = matching_deals.iloc[0]

            recommendations.append({
                'business_problem': problem,
                'deal_types': deal_row['deal_types'],
                'rationale': deal_row['rationale']
            })

    return recommendations


def rank_recommendations(recommendations: List[Dict], ranked_issues: List[Tuple[str, Dict]]) -> List[Dict]:
    """
    Rank recommendations by gap severity.

    Args:
        recommendations: List of recommendation dictionaries
        ranked_issues: List of (kpi, gap_data) tuples sorted by severity

    Returns:
        Sorted list of recommendations with severity scores
    """
    # Map problems to severity based on gap
    problem_severity = {}

    for kpi, data in ranked_issues:
        if kpi in KPI_TO_PROBLEM:
            problem = KPI_TO_PROBLEM[kpi]
            gap_pct = data['gap_pct']

            # Take most severe gap for each problem
            if problem not in problem_severity or gap_pct < problem_severity[problem]:
                problem_severity[problem] = gap_pct

    # Add severity to recommendations and sort
    for rec in recommendations:
        problem = rec['business_problem']
        rec['severity'] = problem_severity.get(problem, 0)

    # Sort by severity (most negative first)
    recommendations.sort(key=lambda x: x['severity'])

    return recommendations


def format_deal_types(deal_types_str: str) -> List[str]:
    """
    Parse and format deal types from semicolon-separated string.

    Args:
        deal_types_str: String with deal types separated by semicolons

    Returns:
        List of individual deal types
    """
    if pd.isna(deal_types_str) or not deal_types_str:
        return []

    # Split by semicolon and clean up
    deals = [deal.strip() for deal in deal_types_str.split(';')]
    return [deal for deal in deals if deal]


def generate_recommendations(analysis_results: Dict, deal_bank_df: pd.DataFrame) -> Dict:
    """
    Generate complete recommendation report.

    Args:
        analysis_results: Results from analyzer.analyze_restaurant_performance
        deal_bank_df: Dataframe with deal bank data

    Returns:
        Dictionary with recommendations and supporting data
    """
    # Map gaps to problems
    underperforming = analysis_results['underperforming_kpis']
    problems = map_gaps_to_problems(underperforming, gap_threshold=-5.0)

    # Get deal recommendations
    recommendations = get_deal_recommendations(problems, deal_bank_df)

    # Rank by severity
    ranked_issues = analysis_results['ranked_issues']
    ranked_recommendations = rank_recommendations(recommendations, ranked_issues)

    # Format deal types for display
    for rec in ranked_recommendations:
        rec['deal_types_list'] = format_deal_types(rec['deal_types'])

    return {
        'business_problems': problems,
        'recommendations': ranked_recommendations,
        'top_recommendation': ranked_recommendations[0] if ranked_recommendations else None
    }


def create_recommendation_summary(recommendations: List[Dict]) -> str:
    """
    Create a text summary of top recommendations.

    Args:
        recommendations: List of recommendation dictionaries

    Returns:
        Formatted text summary
    """
    if not recommendations:
        return "No specific recommendations at this time. Your performance is strong across all metrics."

    summary_lines = []
    for i, rec in enumerate(recommendations[:3], 1):  # Top 3
        problem = rec['business_problem']
        deal_types = rec.get('deal_types_list', [])

        summary_lines.append(f"{i}. {problem}")
        if deal_types:
            summary_lines.append(f"   Recommended deals: {', '.join(deal_types[:2])}")

    return '\n'.join(summary_lines)
