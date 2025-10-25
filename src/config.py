"""
Central configuration for FLAVYR MVP.
All KPI definitions, validation rules, and UI constants in one place.
"""

from typing import Dict, List, Set


class KPIConfig:
    """Central configuration for all KPI-related constants."""

    # Core KPI definitions - focusing on 3 key metrics
    COLUMNS: List[str] = [
        'avg_ticket',
        'covers',
        'expected_customer_repeat_rate'
    ]

    # Friendly names for UI display
    NAMES: Dict[str, str] = {
        'avg_ticket': 'Average Ticket Size (AOV)',
        'covers': 'Total Covers',
        'expected_customer_repeat_rate': 'Customer Repeat Rate'
    }

    # Cost metrics (lower is better) - none in current focus
    LOWER_IS_BETTER: List[str] = []
    COST_METRICS: Set[str] = set()
    REVENUE_METRICS: Set[str] = {
        'avg_ticket', 'covers', 'expected_customer_repeat_rate'
    }

    # KPI to business problem mapping
    TO_PROBLEM: Dict[str, str] = {
        'covers': 'Increase Quantity of Sales',
        'avg_ticket': 'Boost Average Order Value (AOV)',
        'expected_customer_repeat_rate': 'Foster Customer Loyalty'
    }

    # Help text for UI tooltips
    HELP_TEXT: Dict[str, str] = {
        'avg_ticket': 'Average dollar amount spent per customer visit (also known as Average Order Value or AOV). Higher values indicate customers are ordering more. IMPACT: Increasing avg ticket by 10% can boost monthly revenue by $10,000+ for typical restaurants.',
        'covers': 'Number of customers served during the period. Higher values indicate more traffic. IMPACT: More covers = higher revenue potential and business growth.',
        'expected_customer_repeat_rate': 'Percentage of customers expected to return. Higher values indicate stronger customer loyalty. IMPACT: Increasing repeat rate by 10% can double lifetime customer value.'
    }

    # Layout groupings for dashboard UI
    ROW1_KPIS: List[str] = ['avg_ticket', 'covers', 'expected_customer_repeat_rate']
    ROW2_KPIS: List[str] = []


class ValidationConfig:
    """Central configuration for data validation."""

    # Restaurant POS CSV required columns
    RESTAURANT_REQUIRED_COLUMNS: List[str] = [
        'date',
        'cuisine_type',
        'dining_model',
        'avg_ticket',
        'covers',
        'expected_customer_repeat_rate'
    ]

    # Transaction CSV required columns
    TRANSACTION_REQUIRED_COLUMNS: List[str] = [
        'date',
        'total',
        'customer_id',
        'item_name',
        'day_of_week'
    ]


class ColorScheme:
    """UI color scheme for reports and visualizations."""

    GOOD = '#00ff00'
    BAD = '#ff0000'
    CRITICAL = '#ffcccc'
    WARNING = '#fff4cc'
    EXCELLENT = '#ccffcc'
