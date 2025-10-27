"""
FLAVYR MVP - Restaurant Performance Diagnostic Platform
Main Streamlit application with transaction-first analytics workflow
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import tempfile
import os

from src.data_loader import (
    setup_database,
    validate_and_load_restaurant_csv,
    aggregate_daily_to_monthly,
    store_restaurant_data,
    get_restaurant_data,
    get_benchmark_data,
    get_transaction_benchmarks,
    get_transaction_deal_mapping,
    get_all_deal_bank_data,
    store_transaction_data,
    get_transaction_data
)
from src.analyzer import analyze_restaurant_performance
from src.recommender import generate_recommendations, generate_combined_recommendations
from src.report_generator import export_to_pdf, export_to_html
from src.transaction_analyzer import analyze_transactions, format_results_for_display, derive_aggregated_metrics
from src.transaction_performance_analyzer import generate_transaction_performance_report
from src.transparency_helpers import (
    generate_loyalty_calculation_explanation,
    generate_aov_calculation_explanation,
    generate_slowest_day_calculation_explanation,
    generate_severity_explanation,
    generate_data_source_badge,
    calculate_confidence_score,
    format_confidence_bar,
    generate_confidence_explanation
)
from src.visualization_helpers import (
    create_metric_comparison_chart,
    create_performance_gauge,
    calculate_performance_score,
    create_metric_card_data,
    create_gap_progress_bar,
    generate_performance_score_explanation
)
from utils.transaction_validator import validate_transaction_csv, get_transaction_data_summary, prepare_transaction_data
from src.config import KPIConfig


# Page configuration
st.set_page_config(
    page_title="FLAVYR - Restaurant Analytics",
    page_icon="📊",
    layout="wide"
)

# Initialize database on first run
if 'db_initialized' not in st.session_state:
    setup_database()
    st.session_state.db_initialized = True

# Initialize session state variables
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'restaurant_id' not in st.session_state:
    st.session_state.restaurant_id = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'recommendation_results' not in st.session_state:
    st.session_state.recommendation_results = None
if 'transaction_data' not in st.session_state:
    st.session_state.transaction_data = None
if 'transaction_analysis' not in st.session_state:
    st.session_state.transaction_analysis = None
if 'transaction_performance' not in st.session_state:
    st.session_state.transaction_performance = None
if 'data_source' not in st.session_state:
    st.session_state.data_source = None  # 'transactions' or 'aggregated'
if 'pipeline_stage' not in st.session_state:
    st.session_state.pipeline_stage = None  # 'upload', 'analysis', 'recommendations'
if 'cuisine_type' not in st.session_state:
    st.session_state.cuisine_type = None
if 'dining_model' not in st.session_state:
    st.session_state.dining_model = None


def home_page():
    """Home/Welcome page with introduction."""
    st.title("Welcome to FLAVYR")

    st.markdown("""
    ### Restaurant Performance Diagnostic Platform

    FLAVYR transforms your transaction data into actionable insights and strategic recommendations.

    **Data Pipeline:**

    **Transaction Insights** → **Dashboard** → **Recommendations**

    ---

    ### How It Works

    1. **Transaction Insights** - Upload transaction-level data (date, total, customer_id, item_name, day_of_week)
    2. **Dashboard** - View detailed transaction analytics (loyalty, AOV, slowest days, item rankings)
    3. **Automatic Analysis** - System derives performance metrics and compares to industry benchmarks
    4. **Recommendations** - Get personalized deal suggestions to improve performance

    ---

    ### Getting Started

    Navigate to the **Transaction Insights** tab to upload your data and begin analysis.

    **What You'll Get:**

    **Tactical Insights:**
    - Slowest days identification
    - Customer loyalty rate analysis
    - Average order value breakdown
    - Best/worst selling items

    **Strategic Analysis:**
    - Performance grade (A-F) vs. industry benchmarks
    - Gap analysis for 3 core performance indicators
    - Prioritized deal recommendations
    - Visual benchmark comparisons

    ---

    """)

    # Pipeline status indicator
    if st.session_state.data_source is not None:
        st.success(f"Data Source: {st.session_state.data_source.capitalize()}")

        if st.session_state.analysis_results is not None:
            analysis = st.session_state.analysis_results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Restaurant Type", f"{analysis['cuisine_type']} - {analysis['dining_model']}")
            with col2:
                st.metric("Performance Grade", analysis['performance_grade'])
            with col3:
                st.metric("Pipeline Stage", "Complete")

            st.info("Navigate to **Dashboard** to view transaction insights, or **Recommendations** for deal suggestions.")
        else:
            st.warning("Data uploaded but analysis incomplete. Please re-upload in Transaction Insights.")
    else:
        st.info("No data loaded yet. Go to **Transaction Insights** to get started.")


def upload_page():
    """Page 1: Upload restaurant POS data."""
    st.title("Upload Restaurant Data")

    st.markdown("""
    ### Welcome to FLAVYR

    Upload your restaurant's POS data to get performance insights and deal recommendations.
    """)

    # Column Glossary
    with st.expander("Column Definitions & Requirements", expanded=False):
        st.markdown("""
        ### Required Columns

        **Identifiers:**
        - `date` - Date of service (YYYY-MM-DD format)
        - `cuisine_type` - Restaurant cuisine (e.g., Italian, American, Asian)
        - `dining_model` - Service type (e.g., Fine Dining, Casual, QSR)

        **Performance Metrics (3 Core KPIs):**
        - `avg_ticket` - Average dollar amount per customer visit (also known as AOV - Average Order Value)
        - `covers` - Number of customers served
        - `expected_customer_repeat_rate` - % of customers expected to return (loyalty rate)

        **Format Notes:**
        - All percentage fields should be decimals (e.g., 0.35 for 35%)
        - Dollar amounts should be numbers without $ symbols
        - Dates must be consistent format
        """)

    # Sample CSV download button
    st.markdown("**Need a template?**")
    try:
        with open('data/sample_restaurant_pos_data.csv', 'rb') as f:
            st.download_button(
                label="Download Sample CSV",
                data=f,
                file_name="flavyr_sample_data.csv",
                mime="text/csv",
                help="Download a properly formatted example file"
            )
    except FileNotFoundError:
        st.warning("Sample CSV file not found. Please check the data directory.")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose your POS data CSV file",
        type=['csv'],
        help="Upload daily POS data in CSV format"
    )

    if uploaded_file is not None:
        # Show file info
        st.info(f"File: {uploaded_file.name}")

        # Validate and load
        is_valid, df, errors = validate_and_load_restaurant_csv(uploaded_file)

        if not is_valid:
            st.error("Validation errors found:")
            for error in errors:
                st.error(f"- {error}")
            return

        # Show preview
        st.success("File validated successfully!")
        st.subheader("Data Preview")

        # Format data for better display
        df_display = df.head(10).copy()

        # Format date column
        if 'date' in df_display.columns:
            df_display['date'] = pd.to_datetime(df_display['date']).dt.strftime('%Y-%m-%d')

        # Round numeric columns to 2 decimals
        numeric_cols = ['avg_ticket', 'expected_customer_repeat_rate']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].round(2)

        st.dataframe(df_display, use_container_width=True)

        # Show summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Days", len(df))
        with col2:
            st.metric("Cuisine Type", df['cuisine_type'].iloc[0])
        with col3:
            st.metric("Dining Model", df['dining_model'].iloc[0])

        # Process button
        if st.button("Process Data", type="primary"):
            with st.spinner("Processing your restaurant data..."):
                # Aggregate data
                aggregated_df = aggregate_daily_to_monthly(df)

                # Store in database
                restaurant_id = store_restaurant_data(aggregated_df)

                # Store in session state
                st.session_state.uploaded_data = df
                st.session_state.restaurant_id = restaurant_id

                # Get benchmark data
                cuisine = df['cuisine_type'].iloc[0]
                model = df['dining_model'].iloc[0]
                benchmark_df = get_benchmark_data(cuisine, model)

                if benchmark_df is None:
                    st.error(f"No benchmark data found for {cuisine} - {model}")
                    return

                # Run analysis
                restaurant_df = get_restaurant_data(restaurant_id)
                analysis_results = analyze_restaurant_performance(restaurant_df, benchmark_df)
                st.session_state.analysis_results = analysis_results

                # Generate recommendations
                deal_bank_df = get_all_deal_bank_data()
                recommendation_results = generate_recommendations(analysis_results, deal_bank_df)
                st.session_state.recommendation_results = recommendation_results

            st.success("Data processed successfully!")
            st.info("Navigate to the Dashboard page using the sidebar to view your results.")
            st.balloons()


def recommendations_page():
    """Page 3: Deal recommendations."""
    st.title("Deal Recommendations")

    if st.session_state.recommendation_results is None:
        st.info("**Step 4: Get Personalized Deal Recommendations**")
        st.markdown("""
        Once your data is analyzed, this page will show:
        - Personalized deal suggestions based on your performance gaps
        - Ranked recommendations by severity
        - Rationale for each recommendation
        - Tactical and strategic improvement opportunities

        **To get started:**
        1. Navigate to the **Transaction Insights** tab
        2. Upload your transaction data and click "Analyze Transactions & Generate Insights"
        3. View detailed analytics in the **Dashboard** tab
        4. Return here to see your personalized recommendations
        """)
        return

    rec_results = st.session_state.recommendation_results
    analysis = st.session_state.analysis_results

    # ============================================================
    # SECTION 1: Performance Scorecard
    # ============================================================
    st.markdown("### Performance Overview")

    # Calculate performance score and metrics
    gaps = analysis.get('gaps', {})
    performance_score = calculate_performance_score(gaps)
    metric_counts = create_metric_card_data(gaps)

    # Row 1: Grade badge, gauge chart, and metric cards
    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        # Grade badge
        grade = analysis['performance_grade']
        grade_colors = {
            'A': '#17A2B8', 'B': '#28A745', 'C': '#FFC107',
            'D': '#FF8C00', 'F': '#DC3545'
        }
        grade_color = grade_colors.get(grade, '#6C757D')

        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: {grade_color};
                    border-radius: 10px; color: white;">
            <div style="font-size: 48px; font-weight: bold; margin-bottom: 10px;">{grade}</div>
            <div style="font-size: 16px;">Overall Grade</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <div style="font-size: 14px; opacity: 0.7;">
                {analysis['cuisine_type']}<br>
                {analysis['dining_model']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Performance gauge
        gauge_fig = create_performance_gauge(performance_score, grade)
        st.plotly_chart(gauge_fig, use_container_width=True)

        # Add transparency expandable
        with st.expander("How is this score calculated?"):
            explanation = generate_performance_score_explanation(gaps, performance_score)
            st.markdown(explanation)

    with col3:
        # Metric count cards
        st.markdown("""
        <div style="margin-top: 30px;">
        """, unsafe_allow_html=True)

        # Critical issues
        st.markdown(f"""
        <div style="padding: 15px; background-color: rgba(220, 53, 69, 0.1); border-left: 4px solid #DC3545; margin-bottom: 10px; border-radius: 4px;">
            <div style="font-size: 24px; font-weight: bold; color: #DC3545;">{metric_counts['critical']}</div>
            <div style="font-size: 14px; opacity: 0.7;">Critical Issues (&gt;15% below)</div>
        </div>
        """, unsafe_allow_html=True)

        # Warning issues
        st.markdown(f"""
        <div style="padding: 15px; background-color: rgba(255, 193, 7, 0.1); border-left: 4px solid #FFC107; margin-bottom: 10px; border-radius: 4px;">
            <div style="font-size: 24px; font-weight: bold; color: #FF8C00;">{metric_counts['warning']}</div>
            <div style="font-size: 14px; opacity: 0.7;">Areas for Improvement (5-15% below)</div>
        </div>
        """, unsafe_allow_html=True)

        # Good metrics
        st.markdown(f"""
        <div style="padding: 15px; background-color: rgba(40, 167, 69, 0.1); border-left: 4px solid #28A745; border-radius: 4px;">
            <div style="font-size: 24px; font-weight: bold; color: #28A745;">{metric_counts['good']}</div>
            <div style="font-size: 14px; opacity: 0.7;">Performing Well</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ============================================================
    # SECTION 2: Benchmark Comparison Dashboard
    # ============================================================
    st.markdown("### Benchmark Comparison")
    st.markdown("**How your key metrics compare to industry benchmarks:**")

    # Create comparison charts for strategic KPIs
    kpi_display = {
        'avg_ticket': {'name': 'Average Ticket Size (AOV)', 'unit': '$'},
        'covers': {'name': 'Total Covers', 'unit': ''},
        'expected_customer_repeat_rate': {'name': 'Customer Repeat Rate', 'unit': '%'}
    }

    chart_col1, chart_col2, chart_col3 = st.columns(3)

    for idx, (kpi, info) in enumerate(kpi_display.items()):
        if kpi in gaps:
            gap_data = gaps[kpi]
            actual = gap_data['restaurant_value']
            benchmark = gap_data['benchmark_value']
            gap_pct = gap_data['gap_pct']

            # Convert to percentage if needed
            if info['unit'] == '%':
                actual_display = actual * 100
                benchmark_display = benchmark * 100
            else:
                actual_display = actual
                benchmark_display = benchmark

            # Create chart
            fig = create_metric_comparison_chart(
                info['name'],
                actual_display,
                benchmark_display,
                gap_pct,
                info['unit']
            )

            # Display in appropriate column
            if idx == 0:
                with chart_col1:
                    st.plotly_chart(fig, use_container_width=True)
            elif idx == 1:
                with chart_col2:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                with chart_col3:
                    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Original summary section (keep for context)
    with st.expander("📋 View Detailed Performance Summary"):
        st.info(analysis['summary'])

    # Check if we have combined recommendations or old format
    has_combined = 'strategic_recommendations' in rec_results or 'tactical_recommendations' in rec_results

    if has_combined:
        # New combined format
        strategic_recs = rec_results.get('strategic_recommendations', [])
        tactical_recs = rec_results.get('tactical_recommendations', [])

        # Combine all recommendations for display
        all_recommendations = []

        # Add strategic recommendations
        for rec in strategic_recs:
            all_recommendations.append({
                'source': 'Strategic KPI',
                'business_problem': rec['business_problem'],
                'severity': rec.get('severity', 0),
                'deal_types_list': rec.get('deal_types_list', []),
                'deal_types': rec.get('deal_types', ''),
                'rationale': rec.get('rationale', ''),
                'is_strategic': True
            })

        # Add tactical recommendations
        for rec in tactical_recs:
            severity_val = rec.get('severity', 'medium')
            # Convert string severity to numeric for sorting
            severity_map = {'critical': -30, 'high': -20, 'medium': -10, 'low': -5}
            severity_num = severity_map.get(severity_val, -10) if isinstance(severity_val, str) else severity_val

            all_recommendations.append({
                'source': 'Transaction Insight',
                'business_problem': rec['business_problem'],
                'severity': severity_num,
                'severity_label': rec.get('severity_label', 'Medium'),
                'deal_types_list': rec.get('deal_types_list', []),
                'deal_types': rec.get('deal_types', ''),
                'rationale': rec.get('rationale', ''),
                'actionable_insight': rec.get('actionable_insight', ''),
                'metric': rec.get('metric', ''),
                'actual_value': rec.get('actual_value', ''),
                'benchmark_value': rec.get('benchmark_value', ''),
                'gap': rec.get('gap', ''),
                'is_strategic': False
            })

        # Separate into critical and other
        critical_threshold = -15.0
        critical_issues = [rec for rec in all_recommendations if rec['severity'] < critical_threshold]
        other_issues = [rec for rec in all_recommendations if rec['severity'] >= critical_threshold]

    else:
        # Old format - maintain backward compatibility
        ranked_issues = analysis['ranked_issues'][:3]
        recommendations = rec_results.get('recommendations', [])

        # Ensure we have recommendations for all top 3 issues
        all_recommendations = []

        for kpi, kpi_data in ranked_issues:
            # Find existing recommendation for this issue
            existing_rec = None
            for rec in recommendations:
                if rec['business_problem'] == KPIConfig.TO_PROBLEM.get(kpi):
                    existing_rec = rec
                    break

            if existing_rec:
                all_recommendations.append(existing_rec)
            else:
                # Create a generic recommendation for this gap
                all_recommendations.append({
                    'business_problem': f"Improve {kpi_data['kpi_name']}",
                    'severity': kpi_data['gap_pct'],
                    'deal_types_list': [],
                    'deal_types': 'Review operational processes and industry best practices',
                    'rationale': f"Your {kpi_data['kpi_name']} is {abs(kpi_data['gap_pct']):.1f}% below industry benchmark. Consider analyzing this metric in detail to identify root causes."
                })

        # Separate into critical and other
        critical_threshold = -15.0
        critical_issues = [rec for rec in all_recommendations if rec['severity'] < critical_threshold]
        other_issues = [rec for rec in all_recommendations if rec['severity'] >= critical_threshold]

    # ============================================================
    # SECTION 3: Deal Recommendations
    # ============================================================
    st.markdown("### Deal Recommendations")
    st.markdown("**Prioritized actions to improve performance:**")

    # Always display Critical Issues section
    st.markdown("#### 🔴 Critical Issues")
    st.markdown("_Issues >15% below benchmark requiring immediate attention_")

    if critical_issues:
        for i, rec in enumerate(critical_issues, 1):
            # Format title with source indicator
            source_label = f"[{rec.get('source', 'Strategic')}]" if 'source' in rec else ""

            # Get severity for color coding
            severity_pct = abs(rec['severity']) if isinstance(rec['severity'], (int, float)) else 15

            # Create colored card header (using rgba for dark mode compatibility)
            card_color = 'rgba(220, 53, 69, 0.1)' if severity_pct >= 15 else 'rgba(255, 193, 7, 0.1)'
            border_color = '#DC3545' if severity_pct >= 15 else '#FFC107'

            st.markdown(f"""
            <div style="background-color: {card_color}; border-left: 5px solid {border_color};
                        padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                <h4 style="margin: 0;">{i}. {rec['business_problem']} <small style="opacity: 0.6;">{source_label}</small></h4>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📊 View Details & Recommendations", expanded=True):
                # Visual progress bar showing gap
                if isinstance(rec['severity'], (int, float)):
                    st.markdown("**Performance Gap:**")
                    gap_html = create_gap_progress_bar(rec['severity'], width=300)
                    st.markdown(gap_html, unsafe_allow_html=True)
                    st.markdown(f"_{abs(rec['severity']):.1f}% below industry benchmark_")
                    st.markdown("")  # Spacing

                # Display severity with confidence indicator for tactical recommendations
                col1, col2 = st.columns([3, 1])

                # Add confidence indicator for transaction insights
                with col2:
                    if not rec.get('is_strategic', True) and st.session_state.transaction_data is not None:
                        confidence_factors = {
                            'sample_size': len(st.session_state.transaction_data),
                            'days_of_data': 30,  # Placeholder - can calculate from data
                            'benchmark_sample_size': 500,
                            'locations': 1
                        }
                        confidence = calculate_confidence_score(confidence_factors)
                        st.markdown(f"**Confidence:**")
                        st.markdown(format_confidence_bar(confidence))

                # Data source badge for transaction insights
                if not rec.get('is_strategic', True) and st.session_state.transaction_data is not None:
                    trans_df = st.session_state.transaction_data
                    date_range = f"{trans_df['date'].min()} to {trans_df['date'].max()}"
                    badge = generate_data_source_badge('transactions', {
                        'date_range': date_range,
                        'count': len(trans_df)
                    })
                    st.info(badge)

                # Display metric details for tactical recommendations
                if not rec.get('is_strategic', True):
                    if rec.get('metric'):
                        st.markdown(f"**Metric:** {rec['metric']}")
                    if rec.get('actual_value'):
                        st.markdown(f"**Your Value:** {rec['actual_value']}")
                    if rec.get('benchmark_value'):
                        st.markdown(f"**Benchmark:** {rec['benchmark_value']}")
                    if rec.get('gap'):
                        st.markdown(f"**Gap:** {rec['gap']}")

                # Display actionable insight for tactical recommendations
                if rec.get('actionable_insight'):
                    st.markdown("**Immediate Action:**")
                    st.info(rec['actionable_insight'])

                st.markdown("**Suggested Deal Types:**")
                deal_list = rec.get('deal_types_list', [])
                if deal_list:
                    for deal in deal_list:
                        st.markdown(f"- {deal}")
                else:
                    st.markdown(rec.get('deal_types', 'N/A'))

                st.markdown("**Rationale:**")
                st.markdown(rec.get('rationale', 'N/A'))

                # Add transparency expandables for transaction insights
                if not rec.get('is_strategic', True) and st.session_state.transaction_performance is not None:
                    st.divider()

                    # How Was This Calculated?
                    with st.expander("How Was This Calculated?"):
                        metric = rec.get('metric', '')

                        # Get transparency data from transaction performance
                        perf_data = st.session_state.transaction_performance

                        if 'loyalty' in metric.lower() and 'loyalty_analysis' in perf_data:
                            loyalty_data = perf_data['loyalty_analysis']
                            transparency = loyalty_data.get('transparency', {})

                            calc_data = {
                                'total_customers': transparency.get('calculation_inputs', {}).get('total_customers', 0),
                                'repeat_customers': transparency.get('calculation_inputs', {}).get('repeat_customers', 0),
                                'new_customers': transparency.get('calculation_inputs', {}).get('new_customers', 0),
                                'loyalty_rate': loyalty_data.get('actual_value', 0),
                                'benchmark': loyalty_data.get('benchmark_value', 0),
                                'restaurant_type': st.session_state.get('cuisine_type', 'Your restaurant type')
                            }
                            explanation = generate_loyalty_calculation_explanation(calc_data)
                            st.markdown(explanation)

                        elif 'aov' in metric.lower() and 'aov_analysis' in perf_data:
                            aov_data = perf_data['aov_analysis']

                            # Get transaction data for calculation
                            if st.session_state.transaction_data is not None:
                                trans_df = st.session_state.transaction_data
                                total_revenue = trans_df['total'].sum()
                                total_transactions = len(trans_df)

                                # Calculate weekday/weekend AOV
                                trans_df['day_of_week'] = pd.to_datetime(trans_df['date']).dt.day_name()
                                weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                                weekday_avg = trans_df[trans_df['day_of_week'].isin(weekdays)]['total'].mean()
                                weekend_avg = trans_df[~trans_df['day_of_week'].isin(weekdays)]['total'].mean()

                                calc_data = {
                                    'total_transactions': total_transactions,
                                    'total_revenue': total_revenue,
                                    'actual_aov': aov_data.get('actual_value', 0),
                                    'benchmark_aov': aov_data.get('benchmark_value', 0),
                                    'weekday_aov': weekday_avg,
                                    'weekend_aov': weekend_avg,
                                    'restaurant_type': st.session_state.get('cuisine_type', 'Your restaurant type')
                                }
                                explanation = generate_aov_calculation_explanation(calc_data)
                                st.markdown(explanation)

                        elif 'slow' in metric.lower() and 'slowest_day_analysis' in perf_data:
                            slow_data = perf_data['slowest_day_analysis']

                            calc_data = {
                                'slowest_day': slow_data.get('slowest_day', 'Monday'),
                                'slowest_count': slow_data.get('slowest_count', 0),
                                'average_count': slow_data.get('average_count', 0),
                                'actual_drop_pct': slow_data.get('actual_drop_pct', 0),
                                'expected_drop_pct': slow_data.get('expected_drop_pct', 0),
                                'expected_slowest': slow_data.get('expected_slowest', 'Monday'),
                                'restaurant_type': st.session_state.get('cuisine_type', 'Your restaurant type')
                            }
                            explanation = generate_slowest_day_calculation_explanation(calc_data)
                            st.markdown(explanation)

                    # Why This Severity?
                    with st.expander("Why This Severity?"):
                        metric = rec.get('metric', '')
                        perf_data = st.session_state.transaction_performance

                        # Extract severity explanation based on metric
                        if 'loyalty' in metric.lower() and 'loyalty_analysis' in perf_data:
                            loyalty_data = perf_data['loyalty_analysis']
                            transparency = loyalty_data.get('transparency', {})

                            severity_exp = generate_severity_explanation(
                                metric='loyalty_rate',
                                value=loyalty_data.get('actual_value', 0),
                                severity=loyalty_data.get('severity', 'medium'),
                                thresholds=transparency.get('thresholds', {})
                            )
                            st.markdown(severity_exp)

                        elif 'aov' in metric.lower() and 'aov_analysis' in perf_data:
                            aov_data = perf_data['aov_analysis']

                            severity_exp = generate_severity_explanation(
                                metric='aov',
                                value=aov_data.get('actual_value', 0),
                                severity=aov_data.get('severity', 'medium'),
                                thresholds={'critical': 90, 'medium': 95}
                            )
                            st.markdown(severity_exp)

                        elif 'slow' in metric.lower() and 'slowest_day_analysis' in perf_data:
                            slow_data = perf_data['slowest_day_analysis']

                            severity_exp = generate_severity_explanation(
                                metric='slowest_day',
                                value=slow_data.get('actual_drop_pct', 0),
                                severity=slow_data.get('severity', 'medium'),
                                thresholds={'critical': 40, 'high': 35}
                            )
                            st.markdown(severity_exp)

                    # Confidence Details
                    if st.session_state.transaction_data is not None:
                        with st.expander("Confidence Details"):
                            confidence_factors = {
                                'sample_size': len(st.session_state.transaction_data),
                                'days_of_data': 30,
                                'benchmark_sample_size': 500,
                                'locations': 1
                            }
                            confidence = calculate_confidence_score(confidence_factors)
                            conf_explanation = generate_confidence_explanation(confidence_factors, confidence)
                            st.markdown(conf_explanation)
    else:
        st.success("No critical issues identified. All metrics are within 15% of industry benchmarks.")

    # Display Other Issues
    if other_issues:
        st.divider()
        st.markdown("#### ⚠️ Other Areas for Improvement")
        st.markdown("_Opportunities to enhance performance (5-15% below benchmark)_")

        for i, rec in enumerate(other_issues, 1):
            # Format title with source indicator
            source_label = f"[{rec.get('source', 'Strategic')}]" if 'source' in rec else ""

            # Get severity for color coding
            severity_pct = abs(rec['severity']) if isinstance(rec['severity'], (int, float)) else 10

            # Create colored card header (using rgba for dark mode compatibility)
            card_color = 'rgba(255, 193, 7, 0.1)'
            border_color = '#FFC107'

            st.markdown(f"""
            <div style="background-color: {card_color}; border-left: 5px solid {border_color};
                        padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                <h4 style="margin: 0;">{i}. {rec['business_problem']} <small style="opacity: 0.6;">{source_label}</small></h4>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📊 View Details & Recommendations"):
                # Visual progress bar showing gap
                if isinstance(rec['severity'], (int, float)):
                    st.markdown("**Performance Gap:**")
                    gap_html = create_gap_progress_bar(rec['severity'], width=300)
                    st.markdown(gap_html, unsafe_allow_html=True)
                    st.markdown(f"_{abs(rec['severity']):.1f}% below industry benchmark_")
                    st.markdown("")  # Spacing

                # Display severity with confidence indicator for tactical recommendations
                col1, col2 = st.columns([3, 1])

                # Add confidence indicator for transaction insights
                with col2:
                    if not rec.get('is_strategic', True) and st.session_state.transaction_data is not None:
                        confidence_factors = {
                            'sample_size': len(st.session_state.transaction_data),
                            'days_of_data': 30,
                            'benchmark_sample_size': 500,
                            'locations': 1
                        }
                        confidence = calculate_confidence_score(confidence_factors)
                        st.markdown(f"**Confidence:**")
                        st.markdown(format_confidence_bar(confidence))

                # Data source badge for transaction insights
                if not rec.get('is_strategic', True) and st.session_state.transaction_data is not None:
                    trans_df = st.session_state.transaction_data
                    date_range = f"{trans_df['date'].min()} to {trans_df['date'].max()}"
                    badge = generate_data_source_badge('transactions', {
                        'date_range': date_range,
                        'count': len(trans_df)
                    })
                    st.info(badge)

                # Display metric details for tactical recommendations
                if not rec.get('is_strategic', True):
                    if rec.get('actual_value') and rec.get('benchmark_value'):
                        st.markdown(f"**Performance:** {rec['actual_value']} vs {rec['benchmark_value']} benchmark")

                # Display actionable insight for tactical recommendations
                if rec.get('actionable_insight'):
                    st.markdown("**Action:**")
                    st.markdown(f"_{rec['actionable_insight']}_")

                st.markdown("**Suggested Deal Types:**")
                deal_list = rec.get('deal_types_list', [])
                if deal_list:
                    for deal in deal_list:
                        st.markdown(f"- {deal}")
                else:
                    st.markdown(rec.get('deal_types', 'N/A'))

                st.markdown("**Rationale:**")
                st.markdown(rec.get('rationale', 'N/A'))

                # Add transparency expandables for transaction insights
                if not rec.get('is_strategic', True) and st.session_state.transaction_performance is not None:
                    st.divider()

                    # How Was This Calculated?
                    with st.expander("How Was This Calculated?"):
                        metric = rec.get('metric', '')
                        perf_data = st.session_state.transaction_performance

                        if 'loyalty' in metric.lower() and 'loyalty_analysis' in perf_data:
                            loyalty_data = perf_data['loyalty_analysis']
                            transparency = loyalty_data.get('transparency', {})

                            calc_data = {
                                'total_customers': transparency.get('calculation_inputs', {}).get('total_customers', 0),
                                'repeat_customers': transparency.get('calculation_inputs', {}).get('repeat_customers', 0),
                                'new_customers': transparency.get('calculation_inputs', {}).get('new_customers', 0),
                                'loyalty_rate': loyalty_data.get('actual_value', 0),
                                'benchmark': loyalty_data.get('benchmark_value', 0),
                                'restaurant_type': st.session_state.get('cuisine_type', 'Your restaurant type')
                            }
                            explanation = generate_loyalty_calculation_explanation(calc_data)
                            st.markdown(explanation)

                        elif 'aov' in metric.lower() and 'aov_analysis' in perf_data:
                            aov_data = perf_data['aov_analysis']

                            if st.session_state.transaction_data is not None:
                                trans_df = st.session_state.transaction_data
                                total_revenue = trans_df['total'].sum()
                                total_transactions = len(trans_df)

                                trans_df['day_of_week'] = pd.to_datetime(trans_df['date']).dt.day_name()
                                weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                                weekday_avg = trans_df[trans_df['day_of_week'].isin(weekdays)]['total'].mean()
                                weekend_avg = trans_df[~trans_df['day_of_week'].isin(weekdays)]['total'].mean()

                                calc_data = {
                                    'total_transactions': total_transactions,
                                    'total_revenue': total_revenue,
                                    'actual_aov': aov_data.get('actual_value', 0),
                                    'benchmark_aov': aov_data.get('benchmark_value', 0),
                                    'weekday_aov': weekday_avg,
                                    'weekend_aov': weekend_avg,
                                    'restaurant_type': st.session_state.get('cuisine_type', 'Your restaurant type')
                                }
                                explanation = generate_aov_calculation_explanation(calc_data)
                                st.markdown(explanation)

                        elif 'slow' in metric.lower() and 'slowest_day_analysis' in perf_data:
                            slow_data = perf_data['slowest_day_analysis']

                            calc_data = {
                                'slowest_day': slow_data.get('slowest_day', 'Monday'),
                                'slowest_count': slow_data.get('slowest_count', 0),
                                'average_count': slow_data.get('average_count', 0),
                                'actual_drop_pct': slow_data.get('actual_drop_pct', 0),
                                'expected_drop_pct': slow_data.get('expected_drop_pct', 0),
                                'expected_slowest': slow_data.get('expected_slowest', 'Monday'),
                                'restaurant_type': st.session_state.get('cuisine_type', 'Your restaurant type')
                            }
                            explanation = generate_slowest_day_calculation_explanation(calc_data)
                            st.markdown(explanation)

                    # Why This Severity?
                    with st.expander("Why This Severity?"):
                        metric = rec.get('metric', '')
                        perf_data = st.session_state.transaction_performance

                        if 'loyalty' in metric.lower() and 'loyalty_analysis' in perf_data:
                            loyalty_data = perf_data['loyalty_analysis']
                            transparency = loyalty_data.get('transparency', {})

                            severity_exp = generate_severity_explanation(
                                metric='loyalty_rate',
                                value=loyalty_data.get('actual_value', 0),
                                severity=loyalty_data.get('severity', 'medium'),
                                thresholds=transparency.get('thresholds', {})
                            )
                            st.markdown(severity_exp)

                        elif 'aov' in metric.lower() and 'aov_analysis' in perf_data:
                            aov_data = perf_data['aov_analysis']

                            severity_exp = generate_severity_explanation(
                                metric='aov',
                                value=aov_data.get('actual_value', 0),
                                severity=aov_data.get('severity', 'medium'),
                                thresholds={'critical': 90, 'medium': 95}
                            )
                            st.markdown(severity_exp)

                        elif 'slow' in metric.lower() and 'slowest_day_analysis' in perf_data:
                            slow_data = perf_data['slowest_day_analysis']

                            severity_exp = generate_severity_explanation(
                                metric='slowest_day',
                                value=slow_data.get('actual_drop_pct', 0),
                                severity=slow_data.get('severity', 'medium'),
                                thresholds={'critical': 40, 'high': 35}
                            )
                            st.markdown(severity_exp)

                    # Confidence Details
                    if st.session_state.transaction_data is not None:
                        with st.expander("Confidence Details"):
                            confidence_factors = {
                                'sample_size': len(st.session_state.transaction_data),
                                'days_of_data': 30,
                                'benchmark_sample_size': 500,
                                'locations': 1
                            }
                            confidence = calculate_confidence_score(confidence_factors)
                            conf_explanation = generate_confidence_explanation(confidence_factors, confidence)
                            st.markdown(conf_explanation)

    # If no issues at all
    if not critical_issues and not other_issues:
        st.success("Your performance is strong across all metrics. No specific recommendations at this time.")


def report_page():
    """Page 4: Generate and download reports."""
    st.title("Performance Report")

    if st.session_state.analysis_results is None:
        st.info("**Step 5: Export Your Performance Report**")
        st.markdown("""
        Once your analysis is complete, you can generate comprehensive reports with:
        - Executive summary
        - KPI comparison tables
        - Performance gap visualization
        - Deal recommendations
        - Transaction insights

        **Available Formats:**
        - PDF (for printing and sharing)
        - HTML (for web viewing)

        **To get started:**
        1. Navigate to the **Transaction Insights** tab
        2. Upload your transaction data and run analysis
        3. Review insights in the **Dashboard** tab
        4. Return here to generate and download reports
        """)
        return

    analysis = st.session_state.analysis_results
    recommendations = st.session_state.recommendation_results

    st.markdown("""
    ### Download Your Report

    Generate a comprehensive performance report in PDF or HTML format.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("PDF Report")
        st.markdown("Professional PDF format for printing and sharing.")

        if st.button("Generate PDF", type="primary"):
            with st.spinner("Generating PDF..."):
                try:
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        export_to_pdf(analysis, recommendations, tmp_file.name)

                        # Read the file
                        with open(tmp_file.name, 'rb') as f:
                            pdf_data = f.read()

                        # Clean up
                        os.unlink(tmp_file.name)

                    # Download button
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_data,
                        file_name=f"flavyr_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                    st.success("PDF generated successfully!")

                except Exception as e:
                    st.error(f"PDF generation failed: {str(e)}")
                    st.info("Please try the HTML format instead, or contact support.")

    with col2:
        st.subheader("HTML Report")
        st.markdown("Interactive HTML format for web viewing.")

        if st.button("Generate HTML"):
            with st.spinner("Generating HTML..."):
                html_content = export_to_html(analysis, recommendations)

                # Download button
                st.download_button(
                    label="Download HTML Report",
                    data=html_content,
                    file_name=f"flavyr_report_{datetime.now().strftime('%Y%m%d')}.html",
                    mime="text/html"
                )

    # Preview section
    st.divider()
    st.subheader("Report Preview")

    # Show executive summary
    st.markdown(f"""
    **Restaurant Type:** {analysis['cuisine_type']} - {analysis['dining_model']}

    **Performance Grade:** {analysis['performance_grade']}

    **Top Issues:**
    {analysis['summary']}
    """)


def transaction_insights_page():
    """Page 1: Transaction-level analytics - PRIMARY DATA ENTRY POINT."""
    st.title("Transaction Insights")

    st.markdown("""
    ### Step 1: Upload Your Transaction Data

    This is the starting point of your FLAVYR analysis. Upload transaction-level data to unlock:

    **Tactical Insights:**
    - Slowest days by transactions and revenue
    - Customer loyalty rate
    - Average order value (AOV) analysis
    - Best and worst selling items
    - Day-specific tactical recommendations

    **Strategic Analysis:**
    - Automatic performance metric calculations
    - Industry benchmark comparisons
    - Deal recommendations

    **Required CSV format:**
    - date, total, customer_id, item_name, day_of_week
    """)

    # Restaurant Info Input (for metric derivation)
    st.subheader("Restaurant Information")

    col1, col2 = st.columns(2)
    with col1:
        cuisine_type = st.selectbox(
            "Cuisine Type",
            ["American", "Italian", "Mexican", "Japanese", "Vegetarian", "Indian", "Seafood", "Mediterranean", "Asian Fusion"],
            help="Select your restaurant's primary cuisine type"
        )
    with col2:
        dining_model = st.selectbox(
            "Dining Model",
            ["Full Service", "Casual Dining", "Fast Casual", "Quick Service"],
            help="Select your restaurant's service model"
        )

    st.divider()

    # Sample data button
    st.subheader("Data Upload")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Option 1: Use Sample Data**")
        st.markdown("Load pre-formatted sample transaction data to explore the platform.")
    with col2:
        if st.button("Use Sample Data", type="secondary"):
            st.session_state.use_sample_data = True
            st.rerun()

    st.markdown("**Option 2: Upload Your Own Data**")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose your transaction data CSV file",
        type=['csv'],
        help="Upload transaction-level data with required columns",
        key="transaction_uploader"
    )

    # Handle sample data loading
    if st.session_state.get('use_sample_data', False):
        try:
            df = pd.read_csv('data/sample_transaction_data.csv')
            st.success("Sample data loaded successfully!")

            # Store in session state for persistence across reruns
            st.session_state.sample_transaction_df = df
            st.session_state.is_sample_data_loaded = True
            st.session_state.use_sample_data = False  # Reset trigger

        except FileNotFoundError:
            st.error("Sample data file not found at data/sample_transaction_data.csv")
            st.session_state.use_sample_data = False
            return
        except Exception as e:
            st.error(f"Error loading sample data: {str(e)}")
            st.session_state.use_sample_data = False
            return

    # Check for sample data in session state
    if st.session_state.get('is_sample_data_loaded', False) and uploaded_file is None:
        # User is using sample data - retrieve from session state
        df = st.session_state.sample_transaction_df
        uploaded_file = 'sample'  # Set flag to enter processing block

    # Clear sample data if user uploads new file
    if uploaded_file is not None and uploaded_file != 'sample':
        st.session_state.is_sample_data_loaded = False
        if 'sample_transaction_df' in st.session_state:
            del st.session_state.sample_transaction_df

    if uploaded_file is not None:
        # Show file info
        if uploaded_file != 'sample':
            st.info(f"File: {uploaded_file.name}")

            # Load CSV
            try:
                df = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")
                return
        else:
            # Sample data retrieved from session state
            st.info("File: sample_transaction_data.csv (Sample Data)")

        # Validate
        is_valid, error_message, warnings = validate_transaction_csv(df)

        if not is_valid:
            st.error(f"Validation failed: {error_message}")
            return

        # Show warnings if any
        if warnings:
            for warning in warnings:
                st.warning(warning)

        st.success("File validated successfully!")

        # Show data summary
        summary = get_transaction_data_summary(df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Transactions", summary['total_transactions'])
        with col2:
            st.metric("Unique Customers", summary['unique_customers'])
        with col3:
            st.metric("Unique Items", summary['unique_items'])
        with col4:
            st.metric("Date Range (days)", summary['date_range']['days'])

        # Preview data
        with st.expander("View Sample Data"):
            st.dataframe(df.head(10), use_container_width=True)

        # Analyze button
        if st.button("Analyze Transactions & Generate Insights", type="primary"):
            with st.spinner("Running complete analysis pipeline..."):
                # Step 1: Prepare transaction data
                cleaned_df = prepare_transaction_data(df)

                # Step 2: Run tactical transaction analysis
                results = analyze_transactions(cleaned_df)
                formatted_results = format_results_for_display(results)

                # Step 3: Derive aggregated metrics from transactions
                st.info("Deriving performance metrics from transaction data...")
                aggregated_df = derive_aggregated_metrics(cleaned_df, cuisine_type, dining_model)

                # Step 4: Store in database
                st.info("Storing data...")
                restaurant_id = store_restaurant_data(aggregated_df)
                transaction_count = store_transaction_data(cleaned_df, restaurant_id)

                # Step 5: Get benchmark data (both strategic and transaction)
                st.info("Comparing to industry benchmarks...")
                benchmark_df = get_benchmark_data(cuisine_type, dining_model)
                transaction_benchmarks = get_transaction_benchmarks(cuisine_type, dining_model)

                if benchmark_df is None:
                    st.error(f"No strategic benchmark data found for {cuisine_type} - {dining_model}")
                    st.warning("Analysis complete but strategic benchmark comparison unavailable.")
                else:
                    # Step 6: Run strategic performance analysis
                    restaurant_df = get_restaurant_data(restaurant_id)
                    analysis_results = analyze_restaurant_performance(restaurant_df, benchmark_df)
                    st.session_state.analysis_results = analysis_results

                    # Step 7: Run transaction performance analysis
                    transaction_performance = None
                    if transaction_benchmarks is not None:
                        st.info("Analyzing transaction-level performance...")
                        # Calculate total revenue for item analysis
                        total_revenue = cleaned_df['total'].sum()
                        transaction_performance = generate_transaction_performance_report(
                            formatted_results,
                            transaction_benchmarks,
                            total_revenue
                        )
                        st.session_state.transaction_performance = transaction_performance
                    else:
                        st.warning(f"Transaction benchmarks not found for {cuisine_type} - {dining_model}")

                    # Step 8: Generate combined recommendations
                    deal_bank_df = get_all_deal_bank_data()
                    deal_mapping_df = get_transaction_deal_mapping()

                    if transaction_performance is not None and len(deal_mapping_df) > 0:
                        # Combined recommendations (strategic + tactical)
                        recommendation_results = generate_combined_recommendations(
                            analysis_results,
                            transaction_performance,
                            deal_bank_df,
                            deal_mapping_df
                        )
                    else:
                        # Fallback to strategic only
                        recommendation_results = generate_recommendations(analysis_results, deal_bank_df)

                    st.session_state.recommendation_results = recommendation_results

                # Store in session state
                st.session_state.transaction_data = cleaned_df
                st.session_state.transaction_analysis = formatted_results
                st.session_state.restaurant_id = restaurant_id
                st.session_state.data_source = 'transactions'
                st.session_state.pipeline_stage = 'recommendations'
                st.session_state.cuisine_type = cuisine_type
                st.session_state.dining_model = dining_model

            st.success("Complete analysis pipeline finished!")
            st.success(f"Stored {transaction_count} transactions and generated strategic insights.")
            st.info("Navigate to the **Dashboard** tab to view detailed transaction insights, or **Recommendations** for personalized deal suggestions.")
            st.balloons()


def transaction_dashboard_page():
    """Dashboard displaying detailed transaction analysis results."""
    st.title("Transaction Analytics Dashboard")

    if st.session_state.transaction_analysis is None:
        st.info("**Step 2: View Your Transaction Insights**")
        st.markdown("""
        Once you upload transaction data, this dashboard will show:
        - Customer loyalty rate and distribution
        - Average order value (AOV) analysis by day
        - Slowest days by transactions and revenue
        - Best and worst selling items
        - Tactical recommendations

        **To get started:**
        1. Navigate to the **Transaction Insights** tab
        2. Upload your transaction data
        3. Click "Analyze Transactions & Generate Insights"
        4. Return here to see your detailed results
        """)
        return

    results = st.session_state.transaction_analysis

    # View Data dropdown
    with st.expander("View Data"):
        if st.session_state.transaction_data is not None:
            st.subheader("Transaction Data")
            st.dataframe(st.session_state.transaction_data, use_container_width=True)

            # Show data summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Transactions", len(st.session_state.transaction_data))
            with col2:
                st.metric("Unique Customers", st.session_state.transaction_data['customer_id'].nunique())
            with col3:
                st.metric("Date Range", f"{st.session_state.transaction_data['date'].min()} to {st.session_state.transaction_data['date'].max()}")
        else:
            st.info("No transaction data available to display.")

    st.divider()

    # Customer Loyalty and AOV - Side by side
    col1, col2 = st.columns(2)

    with col1:
        # Customer Loyalty
        st.markdown("### Customer Loyalty")
        loyalty = results['Customer Loyalty']

        # Metrics in a row
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Loyalty Rate", loyalty['Loyalty Rate'])
        with metric_col2:
            st.metric("Repeat", loyalty['Repeat Customers'])
        with metric_col3:
            st.metric("New", loyalty['New Customers'])

        # Loyalty chart
        fig = go.Figure(data=[go.Pie(
            labels=['Repeat Customers', 'New Customers'],
            values=[loyalty['Repeat Customers'], loyalty['New Customers']],
            hole=0.3
        )])
        fig.update_layout(title="Customer Distribution", height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Average Order Value
        st.markdown("### Average Order Value (AOV)")
        aov = results['Average Order Value']

        st.metric("Overall AOV", aov['Overall AOV'])

        # AOV by day chart
        aov_by_day = aov['By Day of Week']

        # Define proper day order (Monday-Sunday)
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Sort days in correct order
        sorted_days = [day for day in day_order if day in aov_by_day]
        sorted_values = [float(aov_by_day[day].replace('$', '').replace(',', '')) for day in sorted_days]

        fig = go.Figure(data=[go.Bar(
            x=sorted_days,
            y=sorted_values,
            text=[f"${v:.2f}" for v in sorted_values],
            textposition='auto',
        )])
        fig.update_layout(
            title="AOV by Day of Week",
            xaxis_title="Day",
            yaxis_title="Average Order Value ($)",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Slowest Days
    st.markdown("### Slowest Day Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**By Transaction Count**")
        slowest_tx = results['Slowest Day (Transactions)']
        st.metric(
            "Slowest Day",
            slowest_tx['Day'],
            f"{slowest_tx['Transaction Count']} transactions"
        )

        # Show all days
        with st.expander("View All Days"):
            for day, count in slowest_tx['All Days'].items():
                st.text(f"{day}: {count} transactions")

    with col2:
        st.markdown("**By Revenue**")
        slowest_rev = results['Slowest Day (Revenue)']
        st.metric(
            "Slowest Day",
            slowest_rev['Day'],
            slowest_rev['Revenue']
        )

        # Show all days
        with st.expander("View All Days"):
            for day, revenue in slowest_rev['All Days'].items():
                st.text(f"{day}: {revenue}")

    st.divider()

    # Top Items
    st.markdown("### Top Selling Items")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**By Revenue**")
        # Convert to dataframe for sortable display
        top_revenue_df = pd.DataFrame(results['Top Items (Revenue)'])
        if not top_revenue_df.empty:
            # Format revenue column
            top_revenue_df['Revenue'] = top_revenue_df['revenue'].apply(lambda x: f"${x:,.2f}")
            top_revenue_df['Quantity'] = top_revenue_df['quantity']
            top_revenue_df['Item'] = top_revenue_df['item']
            st.dataframe(
                top_revenue_df[['Item', 'Revenue', 'Quantity']],
                use_container_width=True,
                hide_index=True
            )

    with col2:
        st.markdown("**By Quantity Sold**")
        # Convert to dataframe for sortable display
        top_quantity_df = pd.DataFrame(results['Top Items (Quantity)'])
        if not top_quantity_df.empty:
            # Format revenue column
            top_quantity_df['Item'] = top_quantity_df['item']
            top_quantity_df['Quantity'] = top_quantity_df['quantity']
            top_quantity_df['Revenue'] = top_quantity_df['revenue'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(
                top_quantity_df[['Item', 'Quantity', 'Revenue']],
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    # Bottom Items
    st.markdown("### Bottom Selling Items")

    # Check if using new format or old format (backward compatibility)
    if 'Bottom Items (Revenue)' in results and 'Bottom Items (Quantity)' in results:
        # New format: two columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**By Revenue**")
            # Convert to dataframe for sortable display
            bottom_revenue_df = pd.DataFrame(results['Bottom Items (Revenue)'])
            if not bottom_revenue_df.empty:
                # Format revenue column
                bottom_revenue_df['Revenue'] = bottom_revenue_df['revenue'].apply(lambda x: f"${x:,.2f}")
                bottom_revenue_df['Quantity'] = bottom_revenue_df['quantity']
                bottom_revenue_df['Item'] = bottom_revenue_df['item']
                st.dataframe(
                    bottom_revenue_df[['Item', 'Revenue', 'Quantity']],
                    use_container_width=True,
                    hide_index=True
                )

        with col2:
            st.markdown("**By Quantity Sold**")
            # Convert to dataframe for sortable display
            bottom_quantity_df = pd.DataFrame(results['Bottom Items (Quantity)'])
            if not bottom_quantity_df.empty:
                # Format revenue column
                bottom_quantity_df['Item'] = bottom_quantity_df['item']
                bottom_quantity_df['Quantity'] = bottom_quantity_df['quantity']
                bottom_quantity_df['Revenue'] = bottom_quantity_df['revenue'].apply(lambda x: f"${x:,.2f}")
                st.dataframe(
                    bottom_quantity_df[['Item', 'Quantity', 'Revenue']],
                    use_container_width=True,
                    hide_index=True
                )
    elif 'Bottom Items' in results:
        # Old format: single column (backward compatibility)
        st.markdown("Items with lowest revenue performance:")
        bottom_items_df = pd.DataFrame(results['Bottom Items'])
        if not bottom_items_df.empty:
            bottom_items_df['Item'] = bottom_items_df['item']
            bottom_items_df['Revenue'] = bottom_items_df['revenue'].apply(lambda x: f"${x:,.2f}")
            bottom_items_df['Quantity'] = bottom_items_df['quantity']
            st.dataframe(
                bottom_items_df[['Item', 'Revenue', 'Quantity']],
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    # Recommendations
    st.markdown("### Tactical Recommendations")
    st.markdown("Day-specific and item-specific actions to improve performance:")

    for i, rec in enumerate(results['Recommendations'], 1):
        st.markdown(f"**{i}.** {rec}")


# Main app navigation
def main():
    """Main application with horizontal tab navigation."""

    # Header with status bar
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("FLAVYR Analytics")
    with col2:
        if st.session_state.analysis_results is not None:
            analysis = st.session_state.analysis_results
            st.caption(f"Data loaded: {analysis['cuisine_type']} | Grade: {analysis['performance_grade']}")
        else:
            st.caption("No data loaded")

    st.divider()

    # Horizontal tabs without emojis - ordered to reflect data pipeline
    tab1, tab2, tab3, tab4 = st.tabs([
        "Home",
        "Transaction Insights",
        "Dashboard",
        "Recommendations"
    ])

    with tab1:
        home_page()

    with tab2:
        transaction_insights_page()

    with tab3:
        transaction_dashboard_page()

    with tab4:
        recommendations_page()


if __name__ == "__main__":
    main()
