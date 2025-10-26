"""
Visualization helper functions for FLAVYR recommendations page.
Creates Plotly charts for benchmark comparisons and performance metrics.
"""

import plotly.graph_objects as go
from typing import Dict, List, Tuple


def get_severity_color(gap_pct: float) -> str:
    """
    Get color based on gap severity.

    Args:
        gap_pct: Gap percentage (negative = below benchmark)

    Returns:
        Hex color code
    """
    if gap_pct < -15:  # Critical
        return '#DC3545'  # Red
    elif gap_pct < -5:  # Warning
        return '#FFC107'  # Amber
    elif gap_pct < 5:  # Good
        return '#28A745'  # Green
    else:  # Excellent
        return '#17A2B8'  # Teal


def create_metric_comparison_chart(metric_name: str, actual: float, benchmark: float,
                                   gap_pct: float, unit: str = '') -> go.Figure:
    """
    Create horizontal bar chart comparing actual vs benchmark for a single metric.

    Args:
        metric_name: Display name of the metric
        actual: Restaurant's actual value
        benchmark: Benchmark value
        gap_pct: Gap percentage
        unit: Unit symbol (e.g., '$', '%')

    Returns:
        Plotly Figure object
    """
    # Determine colors
    actual_color = get_severity_color(gap_pct)
    benchmark_color = '#6C757D'  # Neutral gray

    # Format values for display
    if unit == '%':
        actual_label = f"{actual:.1f}%"
        benchmark_label = f"{benchmark:.1f}%"
    elif unit == '$':
        actual_label = f"${actual:.2f}"
        benchmark_label = f"${benchmark:.2f}"
    else:
        actual_label = f"{actual:,.0f}"
        benchmark_label = f"{benchmark:,.0f}"

    # Create figure
    fig = go.Figure()

    # Add benchmark bar
    fig.add_trace(go.Bar(
        y=['Benchmark'],
        x=[benchmark],
        orientation='h',
        name='Industry Benchmark',
        marker=dict(color=benchmark_color),
        text=[benchmark_label],
        textposition='inside',
        textfont=dict(color='white', size=14),
        hovertemplate=f'<b>Industry Benchmark</b><br>{benchmark_label}<extra></extra>'
    ))

    # Add actual bar
    fig.add_trace(go.Bar(
        y=['Your Performance'],
        x=[actual],
        orientation='h',
        name='Your Restaurant',
        marker=dict(color=actual_color),
        text=[actual_label],
        textposition='inside',
        textfont=dict(color='white', size=14),
        hovertemplate=f'<b>Your Performance</b><br>{actual_label}<extra></extra>'
    ))

    # Update layout
    gap_text = f"{abs(gap_pct):.1f}% {'below' if gap_pct < 0 else 'above'} benchmark"

    fig.update_layout(
        title=dict(
            text=f"{metric_name}<br><sub>{gap_text}</sub>",
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)',  # Transparent gray for dark mode
            title=unit if unit else 'Value'
        ),
        yaxis=dict(
            showgrid=False
        ),
        height=200,
        margin=dict(l=150, r=20, t=60, b=40),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        template='plotly'  # Use Plotly's default template which adapts to theme
    )

    return fig


def create_performance_gauge(score: float, grade: str) -> go.Figure:
    """
    Create circular gauge chart showing overall performance score.

    Args:
        score: Performance score (0-100)
        grade: Performance grade (A-F)

    Returns:
        Plotly Figure object
    """
    # Determine color based on score
    if score >= 85:
        color = '#17A2B8'  # Teal
    elif score >= 70:
        color = '#28A745'  # Green
    elif score >= 50:
        color = '#FFC107'  # Amber
    else:
        color = '#DC3545'  # Red

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Performance Score<br><span style='font-size:24px'>{grade}</span>",
               'font': {'size': 18}},
        number={'font': {'size': 48}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "rgba(0,0,0,0)",  # Transparent background
            'borderwidth': 2,
            'bordercolor': "rgba(128, 128, 128, 0.3)",  # Semi-transparent border
            'steps': [
                {'range': [0, 50], 'color': 'rgba(220, 53, 69, 0.15)'},  # Light red with transparency
                {'range': [50, 70], 'color': 'rgba(255, 193, 7, 0.15)'},  # Light amber with transparency
                {'range': [70, 85], 'color': 'rgba(40, 167, 69, 0.15)'},  # Light green with transparency
                {'range': [85, 100], 'color': 'rgba(23, 162, 184, 0.15)'}  # Light teal with transparency
            ],
            'threshold': {
                'line': {'color': "rgba(128, 128, 128, 0.5)", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        template='plotly'  # Use Plotly's default template
    )

    return fig


def calculate_performance_score(gaps: Dict[str, Dict]) -> float:
    """
    Calculate overall performance score (0-100) based on gap analysis.

    Args:
        gaps: Gap analysis dictionary from analyzer

    Returns:
        Score from 0-100
    """
    # Calculate average gap across all KPIs
    total_gap = sum(data['gap_pct'] for data in gaps.values())
    avg_gap = total_gap / len(gaps)

    # Convert gap to score (0-100 scale)
    # avg_gap of +20% = 100 score
    # avg_gap of 0% = 70 score
    # avg_gap of -20% = 40 score
    # avg_gap of -40% or worse = 0 score

    if avg_gap >= 20:
        score = 100
    elif avg_gap >= 0:
        score = 70 + (avg_gap / 20) * 30
    elif avg_gap >= -40:
        score = 70 + (avg_gap / 40) * 70
    else:
        score = 0

    return round(score, 1)


def create_metric_card_data(gaps: Dict[str, Dict]) -> Dict[str, int]:
    """
    Count metrics by severity category.

    Args:
        gaps: Gap analysis dictionary from analyzer

    Returns:
        Dictionary with counts of critical, warning, and good metrics
    """
    critical = 0
    warning = 0
    good = 0

    for kpi, data in gaps.items():
        gap_pct = data['gap_pct']
        if gap_pct < -15:
            critical += 1
        elif gap_pct < -5:
            warning += 1
        else:
            good += 1

    return {
        'critical': critical,
        'warning': warning,
        'good': good
    }


def generate_performance_score_explanation(gaps: Dict[str, Dict], score: float) -> str:
    """
    Generate detailed explanation of how performance score was calculated.

    Args:
        gaps: Gap analysis dictionary from analyzer
        score: Calculated performance score

    Returns:
        Markdown-formatted explanation string
    """
    # Calculate metrics used in score
    kpi_gaps = [(kpi, data['gap_pct']) for kpi, data in gaps.items()]
    total_gap = sum(data['gap_pct'] for data in gaps.values())
    avg_gap = total_gap / len(gaps)

    # Build explanation
    explanation = f"""
### How Your Performance Score Was Calculated

Your score of **{score:.1f}/100** is based on how your restaurant performs across all key metrics compared to industry benchmarks.

#### Step 1: Calculate Individual Gaps

We measured your performance gap for each metric:

"""

    # List each KPI gap
    for kpi, data in gaps.items():
        kpi_name = data['kpi_name']
        gap_pct = data['gap_pct']
        restaurant_val = data['restaurant_value']
        benchmark_val = data['benchmark_value']

        # Format values based on metric type
        if 'repeat' in kpi.lower() or 'rate' in kpi.lower():
            rest_display = f"{restaurant_val*100:.1f}%"
            bench_display = f"{benchmark_val*100:.1f}%"
        elif 'ticket' in kpi.lower():
            rest_display = f"${restaurant_val:.2f}"
            bench_display = f"${benchmark_val:.2f}"
        else:
            rest_display = f"{restaurant_val:,.0f}"
            bench_display = f"{benchmark_val:,.0f}"

        gap_text = "above" if gap_pct >= 0 else "below"
        explanation += f"- **{kpi_name}**: {rest_display} vs {bench_display} benchmark = **{abs(gap_pct):.1f}% {gap_text}**\n"

    explanation += f"""

#### Step 2: Calculate Average Gap

We take the average of all your gaps:

```
({' + '.join([f'{data["gap_pct"]:.1f}%' for data in gaps.values()])}) ÷ {len(gaps)} = {avg_gap:.1f}%
```

**Average Gap: {avg_gap:.1f}%** {'above' if avg_gap >= 0 else 'below'} benchmark

#### Step 3: Convert to Score (0-100)

We use this scale to convert your average gap into a score:

| Average Gap | Score Range | Performance Level |
|-------------|-------------|-------------------|
| +20% or better | 100 | Exceptional |
| 0% to +20% | 70-100 | Above Average |
| 0% (at benchmark) | 70 | Average |
| -20% to 0% | 40-70 | Below Average |
| -40% to -20% | 0-40 | Needs Improvement |
| -40% or worse | 0 | Critical |

**Your Calculation:**
"""

    # Show which formula was used
    if avg_gap >= 20:
        explanation += f"""
- Average gap of {avg_gap:.1f}% is ≥ +20%
- Score = **100** (Exceptional!)
"""
    elif avg_gap >= 0:
        calculation = f"70 + ({avg_gap:.1f} ÷ 20) × 30"
        explanation += f"""
- Average gap of {avg_gap:.1f}% is between 0% and +20%
- Score = {calculation} = **{score:.1f}**
"""
    elif avg_gap >= -40:
        calculation = f"70 + ({avg_gap:.1f} ÷ 40) × 70"
        explanation += f"""
- Average gap of {avg_gap:.1f}% is between -40% and 0%
- Score = {calculation} = **{score:.1f}**
"""
    else:
        explanation += f"""
- Average gap of {avg_gap:.1f}% is ≤ -40%
- Score = **0** (Critical - immediate action needed)
"""

    explanation += """

#### What This Means

Your performance score reflects how well you're doing across all metrics compared to similar restaurants in your category. A score of:
- **85-100**: You're outperforming most peers
- **70-84**: You're meeting industry standards
- **50-69**: There's room for improvement
- **Below 50**: Focus on the critical issues highlighted below
"""

    return explanation


def create_gap_progress_bar(gap_pct: float, width: int = 200) -> str:
    """
    Create HTML progress bar visualization for gap percentage.

    Args:
        gap_pct: Gap percentage (negative = below benchmark)
        width: Width of progress bar in pixels

    Returns:
        HTML string for progress bar
    """
    # Calculate progress (0-100)
    # Gap of -100% = 0% progress
    # Gap of 0% = 100% progress
    # Gap of +20% = 100% progress

    if gap_pct >= 0:
        progress = 100
    else:
        progress = max(0, 100 + gap_pct)

    color = get_severity_color(gap_pct)

    html = f"""
    <div style="width: {width}px; background-color: rgba(128, 128, 128, 0.2); border-radius: 4px; height: 24px; position: relative;">
        <div style="width: {progress}%; background-color: {color}; border-radius: 4px; height: 100%; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-weight: bold; font-size: 12px;">{abs(gap_pct):.1f}%</span>
        </div>
    </div>
    """

    return html
