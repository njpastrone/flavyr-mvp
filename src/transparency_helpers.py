"""
Transparency Helpers for FLAVYR MVP

Generates human-readable explanations of how recommendations were calculated,
showing data lineage, calculation steps, and severity logic.
"""

from typing import Dict, List
from datetime import datetime


def generate_loyalty_calculation_explanation(data: Dict) -> str:
    """
    Generate step-by-step explanation of loyalty rate calculation.

    Args:
        data: Dictionary with loyalty calculation details

    Returns:
        Formatted markdown explanation
    """
    total_customers = data.get('total_customers', 0)
    repeat_customers = data.get('repeat_customers', 0)
    new_customers = data.get('new_customers', 0)
    loyalty_rate = data.get('loyalty_rate', 0)
    benchmark = data.get('benchmark', 0)
    restaurant_type = data.get('restaurant_type', 'your restaurant type')

    explanation = f"""
**Step 1: Count Your Customers**
- Source: Your uploaded transaction data
- Analyzed unique customer_id values
- **Total Customers Found:** {total_customers}

**Step 2: Identify Repeat Customers**
- Counted customers who made 2 or more visits
- **Repeat Customers:** {repeat_customers}
- **New Customers (1 visit only):** {new_customers}

**Step 3: Calculate Loyalty Rate**
- Formula: `(Repeat Customers ÷ Total Customers) × 100`
- Calculation: `({repeat_customers} ÷ {total_customers}) × 100`
- **Your Loyalty Rate:** {loyalty_rate:.1f}%

**Step 4: Compare to Industry Benchmark**
- Restaurant Type: {restaurant_type}
- Industry Benchmark: {benchmark:.1f}%
- **Gap:** {loyalty_rate - benchmark:+.1f} percentage points
"""
    return explanation


def generate_aov_calculation_explanation(data: Dict) -> str:
    """
    Generate step-by-step explanation of AOV calculation.

    Args:
        data: Dictionary with AOV calculation details

    Returns:
        Formatted markdown explanation
    """
    total_transactions = data.get('total_transactions', 0)
    total_revenue = data.get('total_revenue', 0)
    actual_aov = data.get('actual_aov', 0)
    benchmark_aov = data.get('benchmark_aov', 0)
    weekday_aov = data.get('weekday_aov', 0)
    weekend_aov = data.get('weekend_aov', 0)
    restaurant_type = data.get('restaurant_type', 'your restaurant type')

    explanation = f"""
**Step 1: Calculate Total Revenue**
- Source: Sum of all transaction 'total' values
- **Total Revenue:** ${total_revenue:,.2f}

**Step 2: Count Transactions**
- Source: Number of transaction records
- **Total Transactions:** {total_transactions}

**Step 3: Calculate Average Order Value**
- Formula: `Total Revenue ÷ Total Transactions`
- Calculation: `${total_revenue:,.2f} ÷ {total_transactions}`
- **Your AOV:** ${actual_aov:.2f}

**Step 4: Analyze Day-of-Week Pattern**
- Weekday Average (Mon-Fri): ${weekday_aov:.2f}
- Weekend Average (Sat-Sun): ${weekend_aov:.2f}
- Weekend Uplift: {((weekend_aov - weekday_aov) / weekday_aov * 100):.1f}%

**Step 5: Compare to Industry Benchmark**
- Restaurant Type: {restaurant_type}
- Industry Benchmark: ${benchmark_aov:.2f}
- **Gap:** {((actual_aov - benchmark_aov) / benchmark_aov * 100):+.1f}%
"""
    return explanation


def generate_slowest_day_calculation_explanation(data: Dict) -> str:
    """
    Generate step-by-step explanation of slowest day analysis.

    Args:
        data: Dictionary with slowest day details

    Returns:
        Formatted markdown explanation
    """
    slowest_day = data.get('slowest_day', 'Monday')
    slowest_count = data.get('slowest_count', 0)
    average_count = data.get('average_count', 0)
    actual_drop = data.get('actual_drop_pct', 0)
    expected_drop = data.get('expected_drop_pct', 0)
    expected_slowest = data.get('expected_slowest', 'Monday')
    restaurant_type = data.get('restaurant_type', 'your restaurant type')

    explanation = f"""
**Step 1: Count Transactions by Day**
- Source: Grouped transaction data by day_of_week
- **Your Slowest Day:** {slowest_day}
- **Transactions on {slowest_day}:** {slowest_count}

**Step 2: Calculate Average Daily Transactions**
- Total transactions across all days
- **Average per Day:** {average_count:.0f} transactions

**Step 3: Calculate Performance Drop**
- Formula: `(Average - Slowest) ÷ Average × 100`
- Calculation: `({average_count:.0f} - {slowest_count}) ÷ {average_count:.0f} × 100`
- **Your Drop:** {actual_drop:.1f}% below average

**Step 4: Compare to Industry Pattern**
- Restaurant Type: {restaurant_type}
- Expected Slowest Day: {expected_slowest}
- Expected Drop: {expected_drop:.0f}% below average
- **Day Matches Expectation:** {"✓ Yes" if slowest_day == expected_slowest else "✗ No"}
- **Drop Severity:** {actual_drop - expected_drop:+.1f}pp vs expected
"""
    return explanation


def generate_item_performance_explanation(data: Dict) -> str:
    """
    Generate explanation of item performance analysis.

    Args:
        data: Dictionary with item performance details

    Returns:
        Formatted markdown explanation
    """
    top_item = data.get('top_item', 'Unknown')
    top_item_revenue = data.get('top_item_revenue', 0)
    top_item_share = data.get('top_item_share', 0)
    total_revenue = data.get('total_revenue', 0)
    poor_performers_count = data.get('poor_performers_count', 0)
    benchmark_top_share = data.get('benchmark_top_share', 20)

    explanation = f"""
**Step 1: Analyze Top Item Performance**
- Top Revenue Item: {top_item}
- Revenue from This Item: ${top_item_revenue:,.2f}
- Total Revenue: ${total_revenue:,.2f}
- **Top Item Share:** {top_item_share:.1f}%

**Step 2: Check Menu Concentration Risk**
- Healthy Range: <{benchmark_top_share:.0f}% from single item
- Your Concentration: {top_item_share:.1f}%
- **Status:** {"⚠ High concentration risk" if top_item_share > 30 else "✓ Healthy balance"}

**Step 3: Identify Poor Performers**
- Items generating <2-3% of revenue
- **Count of Low Performers:** {poor_performers_count}
- Healthy Benchmark: <3 items

**Step 4: Menu Balance Assessment**
- Over-reliance on {top_item}: {"Yes - consider diversifying" if top_item_share > 30 else "No"}
- Poor performers needing attention: {poor_performers_count}
"""
    return explanation


def generate_severity_explanation(metric: str, value: float, severity: str, thresholds: Dict) -> str:
    """
    Explain why a specific severity level was assigned.

    Args:
        metric: Name of the metric
        value: Actual value
        severity: Assigned severity level
        thresholds: Dictionary of severity thresholds

    Returns:
        Formatted markdown explanation
    """
    severity_upper = severity.upper()

    explanation = f"**Why is this {severity_upper}?**\n\n"

    # Get thresholds
    critical = thresholds.get('critical', 0)
    high = thresholds.get('high', 0)
    medium = thresholds.get('medium', 0)

    # Build threshold visualization
    explanation += "**Severity Scale:**\n\n"

    if 'loyalty' in metric.lower():
        explanation += f"🔴 **CRITICAL** (<{critical}%){'  ← You are here' if severity == 'critical' else ''}\n"
        explanation += f"   Immediate action required - customer retention is dangerously low\n\n"
        explanation += f"🟠 **HIGH** ({critical}-{high}%){'  ← You are here' if severity == 'high' else ''}\n"
        explanation += f"   Significant underperformance - should be prioritized\n\n"
        explanation += f"🟡 **MEDIUM** ({high}-{medium}%){'  ← You are here' if severity == 'medium' else ''}\n"
        explanation += f"   Below industry standard - opportunity for improvement\n\n"
        explanation += f"🟢 **GOOD** (>Benchmark){'  ← You are here' if severity == 'good' else ''}\n"
        explanation += f"   Meeting or exceeding expectations\n\n"

    elif 'aov' in metric.lower():
        explanation += f"🔴 **CRITICAL** (<90% of benchmark){'  ← You are here' if severity == 'critical' or severity == 'high' else ''}\n"
        explanation += f"   Customers spending significantly less than competitors\n\n"
        explanation += f"🟡 **MEDIUM** (90-95% of benchmark){'  ← You are here' if severity == 'medium' else ''}\n"
        explanation += f"   Room for improvement through upsells and bundles\n\n"
        explanation += f"🟢 **GOOD** (>95% of benchmark){'  ← You are here' if severity == 'good' else ''}\n"
        explanation += f"   Competitive or better than industry average\n\n"

    elif 'slow' in metric.lower():
        explanation += f"🔴 **CRITICAL** (>40% drop){'  ← You are here' if severity == 'critical' else ''}\n"
        explanation += f"   Slowest day is significantly worse than industry norm\n\n"
        explanation += f"🟠 **HIGH** (35-40% drop){'  ← You are here' if severity == 'high' else ''}\n"
        explanation += f"   Notable underperformance on slowest day\n\n"
        explanation += f"🟡 **MEDIUM** (Within 5pp of benchmark){'  ← You are here' if severity == 'medium' else ''}\n"
        explanation += f"   Near expected range but could improve\n\n"
        explanation += f"🟢 **GOOD** (At or better than benchmark){'  ← You are here' if severity == 'good' else ''}\n"
        explanation += f"   Slowest day performance is normal\n\n"

    explanation += f"**Your Performance:** {value}"

    return explanation


def generate_data_source_badge(source_type: str, details: Dict) -> str:
    """
    Generate data source badge text.

    Args:
        source_type: Type of data source
        details: Details about the data source

    Returns:
        Formatted badge text
    """
    if source_type == 'transactions':
        date_range = details.get('date_range', 'Unknown period')
        count = details.get('count', 0)
        return f"📊 From Your Transactions: {date_range} ({count:,} records)"

    elif source_type == 'benchmark':
        restaurant_type = details.get('restaurant_type', 'Unknown type')
        return f"📈 Industry Benchmark: {restaurant_type}"

    elif source_type == 'calculated':
        method = details.get('method', 'Real-time')
        return f"🔢 {method} calculation"

    return "📋 Data Source"


def calculate_confidence_score(factors: Dict) -> float:
    """
    Calculate confidence score based on data quality factors.

    Args:
        factors: Dictionary with confidence factors

    Returns:
        Confidence score between 0 and 1
    """
    score = 0.0
    weight_total = 0.0

    # Sample size factor (weight: 0.4)
    sample_size = factors.get('sample_size', 0)
    if sample_size >= 1000:
        score += 0.4
        weight_total += 0.4
    elif sample_size >= 500:
        score += 0.3
        weight_total += 0.4
    elif sample_size >= 100:
        score += 0.2
        weight_total += 0.4
    else:
        score += 0.1
        weight_total += 0.4

    # Time range factor (weight: 0.3)
    days = factors.get('days_of_data', 0)
    if days >= 60:
        score += 0.3
        weight_total += 0.3
    elif days >= 30:
        score += 0.25
        weight_total += 0.3
    elif days >= 14:
        score += 0.15
        weight_total += 0.3
    else:
        score += 0.05
        weight_total += 0.3

    # Benchmark quality (weight: 0.3)
    benchmark_quality = factors.get('benchmark_sample_size', 0)
    if benchmark_quality >= 500:
        score += 0.3
        weight_total += 0.3
    elif benchmark_quality >= 100:
        score += 0.2
        weight_total += 0.3
    else:
        score += 0.1
        weight_total += 0.3

    return score


def format_confidence_bar(confidence: float) -> str:
    """
    Format confidence score as a visual bar.

    Args:
        confidence: Confidence score between 0 and 1

    Returns:
        Visual bar representation
    """
    filled = int(confidence * 10)
    empty = 10 - filled
    bar = "█" * filled + "░" * empty
    percentage = int(confidence * 100)

    return f"{bar} {percentage}%"


def generate_confidence_explanation(factors: Dict, confidence: float) -> str:
    """
    Generate explanation of confidence score.

    Args:
        factors: Dictionary with confidence factors
        confidence: Overall confidence score

    Returns:
        Formatted markdown explanation
    """
    explanation = f"**Confidence Score:** {format_confidence_bar(confidence)}\n\n"
    explanation += "**Based on:**\n\n"

    # Sample size
    sample_size = factors.get('sample_size', 0)
    if sample_size >= 1000:
        explanation += f"✓ {sample_size:,} transactions (High confidence - large sample)\n"
    elif sample_size >= 500:
        explanation += f"✓ {sample_size:,} transactions (Good confidence - adequate sample)\n"
    else:
        explanation += f"⚠ {sample_size:,} transactions (Limited confidence - small sample)\n"

    # Time range
    days = factors.get('days_of_data', 0)
    if days >= 60:
        explanation += f"✓ {days} days of data (High confidence - good time range)\n"
    elif days >= 30:
        explanation += f"✓ {days} days of data (Medium confidence - decent time range)\n"
    else:
        explanation += f"⚠ {days} days of data (Limited confidence - short time range)\n"

    # Benchmark
    benchmark_size = factors.get('benchmark_sample_size', 500)
    if benchmark_size >= 500:
        explanation += f"✓ Benchmark from {benchmark_size}+ restaurants (High confidence)\n"
    else:
        explanation += f"⚠ Limited benchmark sample\n"

    # Location coverage
    locations = factors.get('locations', 1)
    if locations == 1:
        explanation += f"⚠ Single location data (May not reflect full brand performance)\n"
    else:
        explanation += f"✓ Data from {locations} locations\n"

    return explanation


def generate_audit_trail_entry(step: int, description: str, details: Dict) -> Dict:
    """
    Create an audit trail entry for the analysis process.

    Args:
        step: Step number
        description: Description of the step
        details: Details about what happened

    Returns:
        Audit trail entry dictionary
    """
    return {
        'step': step,
        'timestamp': datetime.now().isoformat(),
        'description': description,
        'details': details
    }


def format_audit_trail(trail: List[Dict]) -> str:
    """
    Format complete audit trail for display.

    Args:
        trail: List of audit trail entries

    Returns:
        Formatted markdown audit trail
    """
    output = "**Analysis Audit Trail**\n\n"

    for entry in trail:
        step = entry['step']
        desc = entry['description']
        details = entry.get('details', {})

        output += f"**Step {step}: {desc}**\n"

        for key, value in details.items():
            if isinstance(value, (int, float)):
                output += f"  - {key}: {value}\n"
            else:
                output += f"  - {key}: {value}\n"

        output += "\n"

    return output
