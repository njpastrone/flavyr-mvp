"""
Transaction-Level Analytics Module

Provides granular sales analytics from transaction-level data.
Addresses Founders' original challenge requirements:
- Slowest day analysis (by transactions and revenue)
- Customer loyalty rate calculation
- Average Order Value (AOV) analysis
- Best/worst selling items identification
- Day-specific actionable recommendations
- Derives aggregated metrics for strategic analysis
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime


def analyze_transactions(df: pd.DataFrame) -> Dict:
    """
    Complete transaction analysis matching Founders' requirements.

    Args:
        df: DataFrame with columns: date, total, customer_id, item_name, day_of_week

    Returns:
        Dictionary containing:
        - slowest_day_transactions: Day with fewest transactions
        - slowest_day_revenue: Day with lowest revenue
        - loyalty_rate: Percentage of repeat customers
        - aov_overall: Overall average order value
        - aov_by_day: AOV breakdown by day of week
        - top_items_revenue: Top 3 items by revenue
        - top_items_quantity: Top 3 items by quantity sold
        - bottom_items: Bottom 3 items by revenue
        - recommendations: Day-specific tactical recommendations
    """

    results = {
        'slowest_days': find_slowest_days(df),
        'loyalty': calculate_loyalty(df),
        'aov': calculate_aov(df),
        'items': rank_items(df),
        'recommendations': generate_day_recommendations(df)
    }

    return results


def find_slowest_days(df: pd.DataFrame) -> Dict:
    """
    Identify slowest days by transaction count and revenue.

    Args:
        df: Transaction DataFrame

    Returns:
        Dict with slowest_day_transactions and slowest_day_revenue
    """
    # Group by day of week
    by_day = df.groupby('day_of_week').agg({
        'total': ['sum', 'count']
    })

    by_day.columns = ['revenue', 'transaction_count']

    # Find slowest days
    slowest_by_transactions = by_day['transaction_count'].idxmin()
    slowest_by_revenue = by_day['revenue'].idxmin()

    return {
        'slowest_day_transactions': {
            'day': slowest_by_transactions,
            'count': int(by_day.loc[slowest_by_transactions, 'transaction_count']),
            'all_days': by_day['transaction_count'].to_dict()
        },
        'slowest_day_revenue': {
            'day': slowest_by_revenue,
            'revenue': float(by_day.loc[slowest_by_revenue, 'revenue']),
            'all_days': by_day['revenue'].to_dict()
        }
    }


def calculate_loyalty(df: pd.DataFrame) -> Dict:
    """
    Calculate percentage of repeat customers.

    Args:
        df: Transaction DataFrame with customer_id column

    Returns:
        Dict with loyalty_rate and customer counts
    """
    # Count purchases per customer
    customer_purchases = df.groupby('customer_id').size()

    total_customers = len(customer_purchases)
    repeat_customers = (customer_purchases > 1).sum()

    loyalty_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0

    return {
        'loyalty_rate': round(loyalty_rate, 2),
        'total_customers': total_customers,
        'repeat_customers': int(repeat_customers),
        'new_customers': int(total_customers - repeat_customers)
    }


def calculate_aov(df: pd.DataFrame) -> Dict:
    """
    Calculate Average Order Value overall and by day of week.

    Args:
        df: Transaction DataFrame

    Returns:
        Dict with aov_overall and aov_by_day
    """
    # Overall AOV
    aov_overall = df['total'].mean()

    # AOV by day of week
    aov_by_day = df.groupby('day_of_week')['total'].mean().to_dict()

    return {
        'aov_overall': round(aov_overall, 2),
        'aov_by_day': {day: round(aov, 2) for day, aov in aov_by_day.items()}
    }


def rank_items(df: pd.DataFrame) -> Dict:
    """
    Identify top and bottom selling items by revenue and quantity.

    Args:
        df: Transaction DataFrame with item_name column

    Returns:
        Dict with top/bottom items by revenue and quantity
    """
    # Aggregate by item
    items = df.groupby('item_name').agg({
        'total': ['sum', 'count']
    })

    items.columns = ['revenue', 'quantity']
    items = items.sort_values('revenue', ascending=False)

    # Top 3 by revenue
    top_revenue = items.head(3)
    top_items_revenue = [
        {
            'item': item,
            'revenue': round(row['revenue'], 2),
            'quantity': int(row['quantity'])
        }
        for item, row in top_revenue.iterrows()
    ]

    # Top 3 by quantity
    top_quantity = items.sort_values('quantity', ascending=False).head(3)
    top_items_quantity = [
        {
            'item': item,
            'quantity': int(row['quantity']),
            'revenue': round(row['revenue'], 2)
        }
        for item, row in top_quantity.iterrows()
    ]

    # Bottom 3 by revenue
    bottom_revenue = items.tail(3)
    bottom_items = [
        {
            'item': item,
            'revenue': round(row['revenue'], 2),
            'quantity': int(row['quantity'])
        }
        for item, row in bottom_revenue.iterrows()
    ]

    return {
        'top_items_revenue': top_items_revenue,
        'top_items_quantity': top_items_quantity,
        'bottom_items': bottom_items
    }


def generate_day_recommendations(df: pd.DataFrame) -> List[str]:
    """
    Generate day-specific tactical recommendations based on transaction patterns.

    Args:
        df: Transaction DataFrame

    Returns:
        List of actionable recommendations
    """
    recommendations = []

    # Analyze day patterns
    slowest = find_slowest_days(df)
    aov_data = calculate_aov(df)

    # Slowest day recommendation
    slowest_day = slowest['slowest_day_transactions']['day']
    recommendations.append(
        f"Run midweek promotion on {slowest_day} to boost traffic "
        f"(currently lowest at {slowest['slowest_day_transactions']['count']} transactions)"
    )

    # Revenue gap recommendation
    if slowest['slowest_day_revenue']['day'] != slowest_day:
        revenue_day = slowest['slowest_day_revenue']['day']
        recommendations.append(
            f"Focus on upselling on {revenue_day} - has transactions but low revenue "
            f"(${slowest['slowest_day_revenue']['revenue']:.2f})"
        )

    # AOV recommendations
    aov_by_day = aov_data['aov_by_day']
    if aov_by_day:
        lowest_aov_day = min(aov_by_day, key=aov_by_day.get)
        highest_aov_day = max(aov_by_day, key=aov_by_day.get)

        recommendations.append(
            f"Implement bundling strategy on {lowest_aov_day} to increase AOV "
            f"(currently ${aov_by_day[lowest_aov_day]:.2f} vs ${aov_by_day[highest_aov_day]:.2f} on {highest_aov_day})"
        )

    # Item-based recommendations
    items = rank_items(df)
    if items['bottom_items']:
        bottom_item = items['bottom_items'][0]['item']
        recommendations.append(
            f"Consider removing or reformulating '{bottom_item}' from menu "
            f"(lowest revenue item at ${items['bottom_items'][0]['revenue']:.2f})"
        )

    if items['top_items_revenue']:
        top_item = items['top_items_revenue'][0]['item']
        recommendations.append(
            f"Feature '{top_item}' prominently - top revenue driver at ${items['top_items_revenue'][0]['revenue']:.2f}"
        )

    # Customer loyalty recommendation
    loyalty = calculate_loyalty(df)
    if loyalty['loyalty_rate'] < 30:
        recommendations.append(
            f"Launch loyalty program - only {loyalty['loyalty_rate']:.1f}% of customers return "
            f"({loyalty['repeat_customers']} of {loyalty['total_customers']} customers)"
        )

    return recommendations


def format_results_for_display(results: Dict) -> Dict:
    """
    Format analysis results for clean display in UI.

    Args:
        results: Raw analysis results

    Returns:
        Formatted results dictionary
    """
    formatted = {
        'Slowest Day (Transactions)': {
            'Day': results['slowest_days']['slowest_day_transactions']['day'],
            'Transaction Count': results['slowest_days']['slowest_day_transactions']['count'],
            'All Days': results['slowest_days']['slowest_day_transactions']['all_days']
        },
        'Slowest Day (Revenue)': {
            'Day': results['slowest_days']['slowest_day_revenue']['day'],
            'Revenue': f"${results['slowest_days']['slowest_day_revenue']['revenue']:,.2f}",
            'All Days': {
                day: f"${rev:,.2f}"
                for day, rev in results['slowest_days']['slowest_day_revenue']['all_days'].items()
            }
        },
        'Customer Loyalty': {
            'Loyalty Rate': f"{results['loyalty']['loyalty_rate']}%",
            'Total Customers': results['loyalty']['total_customers'],
            'Repeat Customers': results['loyalty']['repeat_customers'],
            'New Customers': results['loyalty']['new_customers']
        },
        'Average Order Value': {
            'Overall AOV': f"${results['aov']['aov_overall']:.2f}",
            'By Day of Week': {
                day: f"${aov:.2f}"
                for day, aov in results['aov']['aov_by_day'].items()
            }
        },
        'Top Items (Revenue)': results['items']['top_items_revenue'],
        'Top Items (Quantity)': results['items']['top_items_quantity'],
        'Bottom Items': results['items']['bottom_items'],
        'Recommendations': results['recommendations']
    }

    return formatted


def derive_aggregated_metrics(df: pd.DataFrame, cuisine_type: str, dining_model: str) -> pd.DataFrame:
    """
    Derive aggregated performance metrics from transaction-level data.

    This function bridges transaction-level data with strategic analysis by calculating
    the 7 core KPIs used in the Dashboard and Recommendations modules.

    Args:
        df: Transaction DataFrame with columns: date, total, customer_id, item_name, day_of_week
        cuisine_type: Restaurant cuisine type (e.g., "Italian", "American")
        dining_model: Restaurant dining model (e.g., "Fine Dining", "Casual")

    Returns:
        Single-row DataFrame with aggregated metrics matching the restaurants table schema:
        - cuisine_type, dining_model
        - avg_ticket, covers, labor_cost_pct, food_cost_pct
        - table_turnover, sales_per_sqft, expected_customer_repeat_rate

    Notes:
        - Some metrics (labor_cost_pct, food_cost_pct, table_turnover, sales_per_sqft)
          cannot be derived from transaction data alone and are set to reasonable defaults
        - These defaults allow the pipeline to function but should be manually updated if available
    """

    # Calculate derivable metrics
    avg_ticket = df['total'].mean()

    # Covers = unique transactions (assuming 1 transaction = 1 customer visit)
    # Group by date and customer to count unique visits
    daily_visits = df.groupby('date')['customer_id'].nunique()
    avg_daily_covers = daily_visits.mean()

    # Customer loyalty rate (can be derived from transaction data)
    customer_purchases = df.groupby('customer_id').size()
    total_customers = len(customer_purchases)
    repeat_customers = (customer_purchases > 1).sum()
    loyalty_rate = (repeat_customers / total_customers) if total_customers > 0 else 0.0

    # Metrics that CANNOT be derived from transaction data alone
    # Set to industry-neutral defaults (will appear as "at benchmark" in comparisons)
    # These should be updated with actual data if available
    labor_cost_pct = 0.30  # 30% - typical restaurant average
    food_cost_pct = 0.30   # 30% - typical restaurant average
    table_turnover = 2.0   # 2x per service period - typical average

    # Sales per sqft: Cannot be calculated without square footage data
    # Use a neutral default that won't skew analysis
    sales_per_sqft = 100.0  # Placeholder - should be updated with actual data

    # Create aggregated dataframe
    aggregated = pd.DataFrame([{
        'cuisine_type': cuisine_type,
        'dining_model': dining_model,
        'avg_ticket': round(avg_ticket, 2),
        'covers': int(round(avg_daily_covers)),
        'labor_cost_pct': labor_cost_pct,
        'food_cost_pct': food_cost_pct,
        'table_turnover': table_turnover,
        'sales_per_sqft': sales_per_sqft,
        'expected_customer_repeat_rate': round(loyalty_rate, 4)
    }])

    return aggregated


def get_derivation_metadata(df: pd.DataFrame) -> Dict:
    """
    Provide metadata about which metrics were derived vs. defaulted.

    Args:
        df: Transaction DataFrame

    Returns:
        Dictionary with derivation status for each metric
    """
    return {
        'avg_ticket': {
            'derived': True,
            'source': 'Mean of transaction totals',
            'confidence': 'high'
        },
        'covers': {
            'derived': True,
            'source': 'Average daily unique customer visits',
            'confidence': 'high'
        },
        'expected_customer_repeat_rate': {
            'derived': True,
            'source': 'Percentage of customers with multiple transactions',
            'confidence': 'high'
        },
        'labor_cost_pct': {
            'derived': False,
            'source': 'Default value (30%) - update with actual data for accurate analysis',
            'confidence': 'low'
        },
        'food_cost_pct': {
            'derived': False,
            'source': 'Default value (30%) - update with actual data for accurate analysis',
            'confidence': 'low'
        },
        'table_turnover': {
            'derived': False,
            'source': 'Default value (2.0x) - update with actual data for accurate analysis',
            'confidence': 'low'
        },
        'sales_per_sqft': {
            'derived': False,
            'source': 'Default value (100) - update with actual data for accurate analysis',
            'confidence': 'low'
        }
    }
