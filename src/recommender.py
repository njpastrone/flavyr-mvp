"""
Deal recommendation engine for FLAVYR MVP.
Maps performance gaps to business problems and suggests deals.
"""

import pandas as pd
from typing import List, Dict, Tuple
from src.config import KPIConfig


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
            if kpi in KPIConfig.TO_PROBLEM:
                problems.add(KPIConfig.TO_PROBLEM[kpi])

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
        if kpi in KPIConfig.TO_PROBLEM:
            problem = KPIConfig.TO_PROBLEM[kpi]
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


def map_transaction_issues_to_problems(transaction_performance: Dict, deal_mapping_df: pd.DataFrame) -> List[Dict]:
    """
    Map transaction-level performance issues to business problems.

    Args:
        transaction_performance: Results from transaction_performance_analyzer
        deal_mapping_df: Transaction deal mapping dataframe

    Returns:
        List of mapped issues with business problems and deal recommendations
    """
    mapped_issues = []

    all_issues = transaction_performance.get('all_issues', [])

    for issue in all_issues:
        issue_category = issue.get('category')
        severity = issue.get('severity')
        issue_type = issue.get('issue_type')
        analysis = issue.get('analysis', {})

        # Find matching mapping in deal_mapping
        # Match by metric or issue type
        metric_name = analysis.get('metric', '')

        matching_mappings = deal_mapping_df[
            (deal_mapping_df['Transaction_Metric'] == metric_name) |
            (deal_mapping_df['Issue_Type'] == issue_type)
        ]

        business_problem = None
        priority = 'Medium'

        if len(matching_mappings) > 0:
            mapping = matching_mappings.iloc[0]
            business_problem = mapping['Business_Problem']
            priority = mapping['Priority']

        # Fallback business problem mapping
        if not business_problem:
            if 'loyalty' in issue_type.lower():
                business_problem = 'Foster Customer Loyalty'
            elif 'aov' in issue_type.lower() or 'order value' in issue_type.lower():
                business_problem = 'Boost Average Order Value'
            elif 'slow day' in issue_type.lower():
                business_problem = 'Improve Slow Days'
            elif 'item' in issue_type.lower() or 'menu' in issue_type.lower():
                business_problem = 'Inventory Management'
            else:
                business_problem = 'Increase Quantity of Sales'

        mapped_issues.append({
            'source': 'transaction',
            'category': issue_category,
            'issue_type': issue_type,
            'severity': severity,
            'severity_label': issue.get('severity_label', severity.capitalize()),
            'business_problem': business_problem,
            'priority': priority,
            'analysis': analysis
        })

    return mapped_issues


def generate_transaction_recommendations(
    transaction_performance: Dict,
    deal_bank_df: pd.DataFrame,
    deal_mapping_df: pd.DataFrame
) -> List[Dict]:
    """
    Generate deal recommendations based on transaction-level insights.

    Args:
        transaction_performance: Results from transaction_performance_analyzer
        deal_bank_df: Deal bank dataframe
        deal_mapping_df: Transaction deal mapping dataframe

    Returns:
        List of transaction-based recommendations
    """
    # Map issues to business problems
    mapped_issues = map_transaction_issues_to_problems(transaction_performance, deal_mapping_df)

    recommendations = []

    for issue in mapped_issues:
        business_problem = issue['business_problem']

        # Find matching deals in deal bank
        matching_deals = deal_bank_df[
            deal_bank_df['business_problem'] == business_problem
        ]

        if len(matching_deals) > 0:
            deal_row = matching_deals.iloc[0]

            # Build detailed recommendation
            analysis = issue['analysis']

            # Create actionable insight based on issue type
            actionable_insight = create_actionable_insight(issue)

            recommendations.append({
                'source': 'transaction',
                'business_problem': business_problem,
                'severity': issue['severity'],
                'severity_label': issue['severity_label'],
                'metric': analysis.get('metric', issue['category']),
                'actual_value': format_metric_value(analysis),
                'benchmark_value': format_benchmark_value(analysis),
                'gap': format_gap_value(analysis),
                'deal_types': deal_row['deal_types'],
                'deal_types_list': format_deal_types(deal_row['deal_types']),
                'rationale': deal_row['rationale'],
                'actionable_insight': actionable_insight,
                'priority': issue['priority']
            })

    # Sort by severity
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    recommendations.sort(key=lambda x: severity_order.get(x['severity'], 3))

    return recommendations


def create_actionable_insight(issue: Dict) -> str:
    """
    Create specific actionable insight based on issue type.

    Args:
        issue: Issue dictionary with category and analysis

    Returns:
        Actionable recommendation text
    """
    category = issue.get('category', '')
    analysis = issue.get('analysis', {})
    issue_type = issue.get('issue_type', '')

    if 'Loyalty' in category:
        actual = analysis.get('actual_value', 0)
        benchmark = analysis.get('benchmark_value', 0)
        return f"Launch a points-based loyalty program with sign-up incentive. Target: Increase repeat rate from {actual:.1f}% to {benchmark:.1f}%"

    elif 'Order Value' in category:
        if 'weekend' in issue_type.lower():
            return "Introduce weekend premium bundles (e.g., 3-course meal) to capture higher weekend spending"
        else:
            return "Implement bundling strategy: combo meals at 15-20% discount vs. à la carte to increase spend per visit"

    elif 'Slow Day' in category:
        day = analysis.get('actual_day', 'Monday')
        return f"Run '{day} Madness' promotion featuring top-selling items at 15-20% off to boost traffic"

    elif 'Menu' in category:
        if 'over-reliance' in issue_type.lower():
            return "Create 'Chef's Favorites' bundle highlighting 3-4 other high-margin items to diversify revenue"
        else:
            return "Bundle slow-moving items in value combos or consider menu reduction for operational efficiency"

    return "Review operational processes and implement targeted promotional strategy"


def format_metric_value(analysis: Dict) -> str:
    """Format actual metric value for display."""
    metric = analysis.get('metric', '')

    if 'loyalty' in metric:
        return f"{analysis.get('actual_value', 0):.1f}%"
    elif 'aov' in metric:
        return f"${analysis.get('actual_value', 0):.2f}"
    elif 'slowest_day' in metric:
        day = analysis.get('actual_day', 'Unknown')
        count = analysis.get('transaction_count', 0)
        return f"{day} ({count} transactions)"
    else:
        return str(analysis.get('actual_value', 'N/A'))


def format_benchmark_value(analysis: Dict) -> str:
    """Format benchmark value for display."""
    metric = analysis.get('metric', '')

    if 'loyalty' in metric:
        return f"{analysis.get('benchmark_value', 0):.1f}%"
    elif 'aov' in metric:
        return f"${analysis.get('benchmark_value', 0):.2f}"
    elif 'slowest_day' in metric:
        drop = analysis.get('benchmark_drop_pct', 0)
        return f"Typically {drop:.0f}% below average"
    else:
        return str(analysis.get('benchmark_value', 'N/A'))


def format_gap_value(analysis: Dict) -> str:
    """Format gap value for display."""
    metric = analysis.get('metric', '')

    if 'loyalty' in metric:
        gap = analysis.get('gap', 0)
        return f"{gap:+.1f} percentage points"
    elif 'aov' in metric:
        gap_pct = analysis.get('gap_pct', 0)
        return f"{gap_pct:+.1f}%"
    elif 'slowest_day' in metric:
        actual_drop = analysis.get('actual_drop_pct', 0)
        benchmark_drop = analysis.get('benchmark_drop_pct', 0)
        return f"Actual drop: {actual_drop:.0f}% (vs. {benchmark_drop:.0f}% expected)"
    else:
        return str(analysis.get('gap', 'N/A'))


def generate_combined_recommendations(
    analysis_results: Dict,
    transaction_performance: Dict,
    deal_bank_df: pd.DataFrame,
    deal_mapping_df: pd.DataFrame
) -> Dict:
    """
    Generate combined strategic and transaction-based recommendations.

    Args:
        analysis_results: Strategic analysis results
        transaction_performance: Transaction performance analysis
        deal_bank_df: Deal bank dataframe
        deal_mapping_df: Transaction deal mapping dataframe

    Returns:
        Dictionary with both strategic and tactical recommendations
    """
    # Generate strategic recommendations (existing)
    strategic_recs = generate_recommendations(analysis_results, deal_bank_df)

    # Generate transaction recommendations (new)
    tactical_recs = generate_transaction_recommendations(
        transaction_performance,
        deal_bank_df,
        deal_mapping_df
    )

    # Create priority action list
    all_recs = []

    # Add strategic recommendations
    for rec in strategic_recs['recommendations']:
        all_recs.append({
            'type': 'strategic',
            'severity': rec.get('severity', 0),
            'problem': rec['business_problem'],
            'recommendation': rec
        })

    # Add tactical recommendations
    for rec in tactical_recs:
        all_recs.append({
            'type': 'tactical',
            'severity': rec.get('severity', 'medium'),
            'problem': rec['business_problem'],
            'recommendation': rec
        })

    # Sort all by severity
    severity_value = {
        'critical': 0,
        'high': 1,
        'medium': 2,
        'low': 3
    }

    def get_severity_value(rec):
        sev = rec['severity']
        if isinstance(sev, (int, float)):
            # Strategic severity is a negative number (gap_pct)
            return abs(sev)
        else:
            # Tactical severity is a string
            return severity_value.get(sev, 3)

    all_recs.sort(key=get_severity_value, reverse=True)

    # Create priority action list
    priority_actions = []
    for i, rec in enumerate(all_recs[:5], 1):  # Top 5 overall
        rec_data = rec['recommendation']
        severity_label = rec_data.get('severity_label', 'Medium')
        problem = rec['problem']

        if rec['type'] == 'tactical':
            insight = rec_data.get('actionable_insight', problem)
            priority_actions.append(f"{severity_label}: {insight}")
        else:
            priority_actions.append(f"{severity_label}: Address {problem}")

    return {
        'strategic_recommendations': strategic_recs['recommendations'],
        'tactical_recommendations': tactical_recs,
        'combined_count': len(strategic_recs['recommendations']) + len(tactical_recs),
        'priority_actions': priority_actions,
        'has_critical_issues': any(
            rec.get('severity') == 'critical' or rec.get('severity', 0) < -20
            for rec in all_recs
        )
    }
