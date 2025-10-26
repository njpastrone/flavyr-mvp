"""
Demo script to preview the visualization components.
Run this to see what the charts look like before launching the full app.
"""

import plotly.graph_objects as go
from src.visualization_helpers import (
    create_metric_comparison_chart,
    create_performance_gauge,
    calculate_performance_score,
    create_metric_card_data
)

# Sample gap data (simulating American Full Service restaurant)
sample_gaps = {
    'avg_ticket': {
        'kpi_name': 'Average Ticket Size',
        'restaurant_value': 32.00,
        'benchmark_value': 35.00,
        'gap_pct': -8.57,
        'lower_is_better': False
    },
    'covers': {
        'kpi_name': 'Total Covers',
        'restaurant_value': 180,
        'benchmark_value': 200,
        'gap_pct': -10.0,
        'lower_is_better': False
    },
    'expected_customer_repeat_rate': {
        'kpi_name': 'Customer Repeat Rate',
        'restaurant_value': 0.35,
        'benchmark_value': 0.40,
        'gap_pct': -12.5,
        'lower_is_better': False
    }
}

print("\n" + "="*70)
print("FLAVYR RECOMMENDATIONS PAGE - VISUALIZATION DEMO")
print("="*70)

# 1. Performance Score and Grade
print("\n1. PERFORMANCE SCORECARD")
print("-" * 70)
score = calculate_performance_score(sample_gaps)
grade = 'C'  # Based on average gap of ~-10%
print(f"   Overall Grade: {grade}")
print(f"   Performance Score: {score}/100")

metric_counts = create_metric_card_data(sample_gaps)
print(f"\n   Metric Breakdown:")
print(f"   - Critical Issues (>15% below): {metric_counts['critical']}")
print(f"   - Areas for Improvement (5-15% below): {metric_counts['warning']}")
print(f"   - Performing Well (within ±5%): {metric_counts['good']}")

# 2. Generate Charts
print("\n2. BENCHMARK COMPARISON CHARTS")
print("-" * 70)

# Average Ticket
fig1 = create_metric_comparison_chart(
    'Average Ticket Size (AOV)',
    32.00,
    35.00,
    -8.57,
    '$'
)
print("   ✓ AOV Comparison Chart created")
print(f"     - Your AOV: $32.00")
print(f"     - Benchmark: $35.00")
print(f"     - Gap: -8.57% (Warning level - Amber)")

# Covers
fig2 = create_metric_comparison_chart(
    'Total Covers',
    180,
    200,
    -10.0,
    ''
)
print("\n   ✓ Covers Comparison Chart created")
print(f"     - Your Covers: 180")
print(f"     - Benchmark: 200")
print(f"     - Gap: -10.0% (Warning level - Amber)")

# Repeat Rate
fig3 = create_metric_comparison_chart(
    'Customer Repeat Rate',
    35.0,  # Convert to percentage for display
    40.0,
    -12.5,
    '%'
)
print("\n   ✓ Repeat Rate Comparison Chart created")
print(f"     - Your Rate: 35.0%")
print(f"     - Benchmark: 40.0%")
print(f"     - Gap: -12.5% (Warning level - Amber)")

# 3. Gauge Chart
print("\n3. PERFORMANCE GAUGE")
print("-" * 70)
gauge_fig = create_performance_gauge(score, grade)
print(f"   ✓ Circular gauge chart created")
print(f"     - Score: {score}/100")
print(f"     - Grade: {grade}")
print(f"     - Color: Amber (Warning zone)")

# 4. Save demo charts
print("\n4. EXPORTING DEMO CHARTS")
print("-" * 70)

try:
    # Save charts as HTML files for preview
    fig1.write_html('/tmp/flavyr_aov_chart.html')
    print("   ✓ AOV chart saved to: /tmp/flavyr_aov_chart.html")

    fig2.write_html('/tmp/flavyr_covers_chart.html')
    print("   ✓ Covers chart saved to: /tmp/flavyr_covers_chart.html")

    fig3.write_html('/tmp/flavyr_repeat_chart.html')
    print("   ✓ Repeat Rate chart saved to: /tmp/flavyr_repeat_chart.html")

    gauge_fig.write_html('/tmp/flavyr_gauge_chart.html')
    print("   ✓ Gauge chart saved to: /tmp/flavyr_gauge_chart.html")

    print("\n   Open these files in your browser to preview the visualizations!")

except Exception as e:
    print(f"   Note: Could not save HTML files ({e})")
    print("   Charts will be visible when running the Streamlit app.")

# 5. Summary
print("\n" + "="*70)
print("VISUALIZATION SUMMARY")
print("="*70)
print("""
The Recommendations page now includes:

✓ Performance Scorecard
  - Large grade badge (C) in amber color
  - Circular gauge showing 51.9/100 score
  - 3 metric count cards (0 critical, 3 warning, 0 good)

✓ Benchmark Comparison Dashboard
  - 3 side-by-side horizontal bar charts
  - Color-coded by severity (all amber/warning)
  - Clear gap percentages displayed

✓ Enhanced Recommendation Cards
  - Colored headers with left borders
  - Visual progress bars showing gaps
  - Severity-based color scheme

To see the full page in action:
1. Run: streamlit run app.py
2. Navigate to Transaction Insights tab
3. Click "Use Sample Data" button
4. Click "Analyze Transactions & Generate Insights"
5. Go to Recommendations tab to see the new visualizations!
""")

print("="*70 + "\n")
