"""
Central configuration for FLAVYR MVP.
All KPI definitions, validation rules, and UI constants in one place.
"""

from typing import Dict, List, Set


class KPIConfig:
    """Central configuration for all KPI-related constants."""

    # Core KPI definitions
    COLUMNS: List[str] = [
        'avg_ticket',
        'covers',
        'labor_cost_pct',
        'food_cost_pct',
        'table_turnover',
        'sales_per_sqft',
        'expected_customer_repeat_rate'
    ]

    # Friendly names for UI display
    NAMES: Dict[str, str] = {
        'avg_ticket': 'Average Ticket Size',
        'covers': 'Total Covers',
        'labor_cost_pct': 'Labor Cost %',
        'food_cost_pct': 'Food Cost %',
        'table_turnover': 'Table Turnover',
        'sales_per_sqft': 'Sales per Sq Ft',
        'expected_customer_repeat_rate': 'Customer Repeat Rate'
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
        'expected_customer_repeat_rate': 'Foster Customer Loyalty',
        'sales_per_sqft': 'Improve Slow Days',
        'labor_cost_pct': 'Enhance Profit Margins',
        'food_cost_pct': 'Enhance Profit Margins',
        'table_turnover': 'Increase Quantity of Sales'
    }

    # Help text for UI tooltips
    HELP_TEXT: Dict[str, str] = {
        'avg_ticket': 'Average dollar amount spent per customer visit. Higher values indicate customers are ordering more. IMPACT: Increasing avg ticket by 10% can boost monthly revenue by $10,000+ for typical restaurants.',
        'covers': 'Number of customers served during the period. Higher values indicate more traffic. IMPACT: More covers = higher revenue potential, but watch labor costs.',
        'table_turnover': 'Number of times a table is used during a service period. Higher values indicate efficient table management. IMPACT: Improving turnover by 0.5x can add 15-20% capacity.',
        'sales_per_sqft': 'Revenue generated per square foot of restaurant space. Higher values indicate better space utilization. IMPACT: Industry leaders achieve 2-3x the average through optimized layouts.',
        'labor_cost_pct': 'Labor costs as a percentage of total revenue. LOWER is better. IMPACT: Reducing labor costs by 5% can add $15,000+ to annual profit.',
        'food_cost_pct': 'Food and beverage costs as a percentage of total revenue. LOWER is better. IMPACT: Every 1% reduction in food cost = ~1% increase in profit margin.',
        'expected_customer_repeat_rate': 'Percentage of customers expected to return. Higher values indicate stronger customer loyalty. IMPACT: Increasing repeat rate by 10% can double lifetime customer value.'
    }

    # Layout groupings for dashboard UI
    ROW1_KPIS: List[str] = ['avg_ticket', 'covers', 'table_turnover', 'sales_per_sqft']
    ROW2_KPIS: List[str] = ['labor_cost_pct', 'food_cost_pct', 'expected_customer_repeat_rate']


class ValidationConfig:
    """Central configuration for data validation."""

    # Restaurant POS CSV required columns
    RESTAURANT_REQUIRED_COLUMNS: List[str] = [
        'date',
        'cuisine_type',
        'dining_model',
        'avg_ticket',
        'covers',
        'labor_cost_pct',
        'food_cost_pct',
        'table_turnover',
        'sales_per_sqft',
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
