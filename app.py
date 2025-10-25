"""
FLAVYR MVP - Restaurant Performance Diagnostic Platform
Main Streamlit application with 4 pages: Upload, Dashboard, Recommendations, Report
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
    get_all_deal_bank_data
)
from src.analyzer import analyze_restaurant_performance
from src.recommender import generate_recommendations
from src.report_generator import export_to_pdf, export_to_html
from src.transaction_analyzer import analyze_transactions, format_results_for_display
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


def home_page():
    """Home/Welcome page with introduction."""
    st.title("Welcome to FLAVYR")

    st.markdown("""
    ### Restaurant Performance Diagnostic Platform

    FLAVYR helps restaurants identify operational issues and receive targeted recommendations
    based on industry benchmarks.

    **How it works:**

    1. **Upload Data** - Upload your restaurant's POS data in CSV format
    2. **View Dashboard** - Compare your performance against industry benchmarks
    3. **Get Recommendations** - Receive personalized deal suggestions to improve performance
    4. **Export Reports** - Download comprehensive reports in PDF or HTML format

    ---

    ### Getting Started

    Navigate to the **Upload Data** tab to begin analyzing your restaurant's performance.

    **Required data format:**
    - Daily POS data in CSV format
    - Must include: date, cuisine_type, dining_model
    - Key metrics: avg_ticket, covers, labor_cost_pct, food_cost_pct, table_turnover,
      sales_per_sqft, expected_customer_repeat_rate

    ---

    ### What You'll Get

    - Performance grade (A-F) based on industry benchmarks
    - Detailed gap analysis for 7 key performance indicators
    - Prioritized recommendations for improvement
    - Downloadable reports for sharing with your team

    """)

    if st.session_state.analysis_results is not None:
        st.success("You have data loaded. Navigate to Dashboard to view your results.")
    else:
        st.info("No data loaded yet. Go to Upload Data to get started.")


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

        **Performance Metrics:**
        - `avg_ticket` - Average dollar amount per customer visit
        - `covers` - Number of customers served
        - `labor_cost_pct` - Labor costs as % of revenue (lower is better)
        - `food_cost_pct` - Food/beverage costs as % of revenue (lower is better)
        - `table_turnover` - Times a table is used per service period
        - `sales_per_sqft` - Revenue per square foot of space
        - `expected_customer_repeat_rate` - % of customers expected to return

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
        numeric_cols = ['avg_ticket', 'labor_cost_pct', 'food_cost_pct', 'table_turnover',
                        'sales_per_sqft', 'expected_customer_repeat_rate']
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


def dashboard_page():
    """Page 2: Dashboard with KPI comparisons."""
    st.title("Performance Dashboard")

    if st.session_state.analysis_results is None:
        st.info("**Get Started with FLAVYR**")
        st.markdown("""
        Upload your restaurant's POS data to see:
        - Performance grade and KPI comparisons
        - Gaps vs industry benchmarks
        - Visual performance charts

        Navigate to the **Upload** page using the sidebar to begin.
        """)
        return

    analysis = st.session_state.analysis_results

    # Header
    col1, col2, col3 = st.columns(3)
    with col1:
        cuisine = analysis['cuisine_type']
        dining = analysis['dining_model']
        st.metric(
            "Restaurant Type",
            f"{cuisine} - {dining}",
            help=f"Full type: {cuisine} - {dining}"
        )
    with col2:
        st.metric("Performance Grade", analysis['performance_grade'])
    with col3:
        issues = len(analysis['underperforming_kpis'])
        st.metric("Areas Needing Attention", issues)

    st.divider()

    # KPI Comparison Cards
    st.subheader("KPI Performance")

    gaps = analysis['gaps']

    # Row 1
    cols = st.columns(4)
    for i, kpi in enumerate(KPIConfig.ROW1_KPIS):
        data = gaps[kpi]
        with cols[i]:
            gap_pct = data['gap_pct']
            # Apply metric-type-aware color logic
            if kpi in KPIConfig.COST_METRICS:
                # For costs: negative gap is good (lower costs)
                delta_color = "inverse" if gap_pct >= 0 else "normal"
            else:
                # For revenue: positive gap is good (higher revenue)
                delta_color = "normal" if gap_pct >= 0 else "inverse"

            # Create label with both values
            value_label = f"Your: {data['restaurant_value']:.2f}"
            delta_label = f"Benchmark: {data['benchmark_value']:.2f} ({gap_pct:+.1f}%)"

            st.metric(
                data['kpi_name'],
                value_label,
                delta_label,
                delta_color=delta_color,
                help=KPIConfig.HELP_TEXT.get(kpi, '')
            )

    # Row 2
    cols = st.columns(4)
    for i, kpi in enumerate(KPIConfig.ROW2_KPIS):
        data = gaps[kpi]
        with cols[i]:
            gap_pct = data['gap_pct']
            # Apply metric-type-aware color logic
            if kpi in KPIConfig.COST_METRICS:
                # For costs: negative gap is good (lower costs)
                delta_color = "inverse" if gap_pct >= 0 else "normal"
            else:
                # For revenue: positive gap is good (higher revenue)
                delta_color = "normal" if gap_pct >= 0 else "inverse"

            # Create label with both values
            value_label = f"Your: {data['restaurant_value']:.2f}"
            delta_label = f"Benchmark: {data['benchmark_value']:.2f} ({gap_pct:+.1f}%)"

            st.metric(
                data['kpi_name'],
                value_label,
                delta_label,
                delta_color=delta_color,
                help=KPIConfig.HELP_TEXT.get(kpi, '')
            )

    st.divider()

    # Gap visualization
    st.subheader("Performance Gaps")

    # Prepare data
    kpi_list = []
    for kpi_key, kpi_data in gaps.items():
        kpi_list.append({
            'kpi': kpi_data['kpi_name'],
            'gap_pct': kpi_data['gap_pct']
        })

    df_gaps = pd.DataFrame(kpi_list)

    # Separate normal gaps from outliers
    outlier_threshold = 100  # +/- 100%
    normal_gaps = df_gaps[df_gaps['gap_pct'].abs() < outlier_threshold]
    outlier_gaps = df_gaps[df_gaps['gap_pct'].abs() >= outlier_threshold]

    # Display normal gaps chart
    if not normal_gaps.empty:
        kpi_names = normal_gaps['kpi'].tolist()
        gap_values = normal_gaps['gap_pct'].tolist()
        colors = ['green' if gap >= 0 else 'red' for gap in gap_values]

        fig = go.Figure(data=[
            go.Bar(
                x=gap_values,
                y=kpi_names,
                orientation='h',
                marker=dict(color=colors),
                text=[f"{gap:+.1f}%" for gap in gap_values],
                textposition='auto',
            )
        ])

        fig.update_layout(
            title="Performance vs Industry Benchmark",
            xaxis_title="Gap Percentage",
            yaxis_title="KPI",
            height=400,
            showlegend=False,
            xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black'),
            shapes=[
                dict(
                    type='line',
                    x0=0, x1=0,
                    y0=0, y1=1,
                    yref='paper',
                    line=dict(color='black', width=2, dash='dash')
                )
            ],
            annotations=[
                dict(
                    x=0, y=1.05,
                    yref='paper',
                    text='Industry Benchmark',
                    showarrow=False,
                    font=dict(size=12)
                )
            ]
        )

        st.plotly_chart(fig, use_container_width=True)

    # Display outliers separately
    if not outlier_gaps.empty:
        st.info("**Exceptional Performance Metrics**")
        st.markdown("These metrics show extreme variance from industry benchmarks:")

        cols = st.columns(len(outlier_gaps))
        for i, (idx, row) in enumerate(outlier_gaps.iterrows()):
            with cols[i]:
                delta_color = "normal" if row['gap_pct'] >= 0 else "inverse"
                st.metric(
                    row['kpi'],
                    f"{row['gap_pct']:+.0f}%",
                    "vs benchmark",
                    delta_color=delta_color,
                    help="This metric significantly exceeds typical industry range"
                )


def recommendations_page():
    """Page 3: Deal recommendations."""
    st.title("Deal Recommendations")

    if st.session_state.recommendation_results is None:
        st.info("**Deal Recommendations**")
        st.markdown("""
        Get personalized deal suggestions based on your performance gaps.

        Navigate to the **Upload** page to get started.
        """)
        return

    rec_results = st.session_state.recommendation_results
    analysis = st.session_state.analysis_results

    # Summary
    st.subheader("Performance Summary")
    st.info(analysis['summary'])

    st.divider()

    # Get all ranked issues (top 3)
    ranked_issues = analysis['ranked_issues'][:3]
    recommendations = rec_results['recommendations']

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

    # Always display Critical Issues section
    st.subheader("Critical Issues")
    st.markdown("Issues classified as >15% below benchmark")

    if critical_issues:
        for i, rec in enumerate(critical_issues, 1):
            with st.expander(f"**{i}. {rec['business_problem']}**", expanded=True):
                st.markdown(f"**Severity:** {abs(rec['severity']):.1f}% below benchmark")

                st.markdown("**Suggested Deal Types:**")
                deal_list = rec.get('deal_types_list', [])
                if deal_list:
                    for deal in deal_list:
                        st.markdown(f"- {deal}")
                else:
                    st.markdown(rec['deal_types'])

                st.markdown("**Rationale:**")
                st.markdown(rec['rationale'])
    else:
        st.success("No critical issues identified. All metrics are within 15% of industry benchmarks.")

    # Display Other Issues
    if other_issues:
        st.divider()
        st.subheader("Other Areas for Improvement")

        for i, rec in enumerate(other_issues, 1):
            st.markdown(f"**{i}. {rec['business_problem']}**")
            st.markdown(f"**Severity:** {abs(rec['severity']):.1f}% below benchmark")

            st.markdown("**Suggested Deal Types:**")
            deal_list = rec.get('deal_types_list', [])
            if deal_list:
                for deal in deal_list:
                    st.markdown(f"- {deal}")
            else:
                st.markdown(rec['deal_types'])

            st.markdown("**Rationale:**")
            st.markdown(rec['rationale'])

            if i < len(other_issues):
                st.divider()

    # If no issues at all
    if not critical_issues and not other_issues:
        st.success("Your performance is strong across all metrics. No specific recommendations at this time.")


def report_page():
    """Page 4: Generate and download reports."""
    st.title("Performance Report")

    if st.session_state.analysis_results is None:
        st.info("**Performance Reports**")
        st.markdown("""
        Generate comprehensive PDF and HTML reports with:
        - Executive summary
        - KPI comparison tables
        - Deal recommendations

        Navigate to the **Upload** page to begin.
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
    """Page 5: Transaction-level analytics."""
    st.title("Transaction Insights")

    st.markdown("""
    ### Granular Sales Analytics

    Upload transaction-level data to get detailed insights:
    - Slowest days by transactions and revenue
    - Customer loyalty rate
    - Average order value (AOV) analysis
    - Best and worst selling items
    - Day-specific tactical recommendations

    **Required CSV format:**
    - date, total, customer_id, item_name, day_of_week
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose your transaction data CSV file",
        type=['csv'],
        help="Upload transaction-level data with required columns",
        key="transaction_uploader"
    )

    if uploaded_file is not None:
        # Show file info
        st.info(f"File: {uploaded_file.name}")

        # Load CSV
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
            return

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
        if st.button("Analyze Transactions", type="primary"):
            with st.spinner("Analyzing transaction data..."):
                # Prepare data
                cleaned_df = prepare_transaction_data(df)

                # Run analysis
                results = analyze_transactions(cleaned_df)
                formatted_results = format_results_for_display(results)

                # Store in session state
                st.session_state.transaction_data = cleaned_df
                st.session_state.transaction_analysis = formatted_results

            st.success("Analysis complete!")
            st.balloons()

    # Display results if available
    if st.session_state.transaction_analysis is not None:
        st.divider()
        st.subheader("Analysis Results")

        results = st.session_state.transaction_analysis

        # Add download button for results
        import json
        results_json = json.dumps(results, indent=2)

        st.download_button(
            label="Download Transaction Insights (JSON)",
            data=results_json,
            file_name=f"transaction_insights_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            help="Download complete analysis results in JSON format"
        )

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

        # Customer Loyalty
        st.markdown("### Customer Loyalty")
        loyalty = results['Customer Loyalty']

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Loyalty Rate", loyalty['Loyalty Rate'])
        with col2:
            st.metric("Repeat Customers", loyalty['Repeat Customers'])
        with col3:
            st.metric("New Customers", loyalty['New Customers'])

        # Loyalty chart
        fig = go.Figure(data=[go.Pie(
            labels=['Repeat Customers', 'New Customers'],
            values=[loyalty['Repeat Customers'], loyalty['New Customers']],
            hole=0.3
        )])
        fig.update_layout(title="Customer Distribution", height=300)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Average Order Value
        st.markdown("### Average Order Value (AOV)")
        aov = results['Average Order Value']

        st.metric("Overall AOV", aov['Overall AOV'])

        # AOV by day chart
        aov_by_day = aov['By Day of Week']
        days = list(aov_by_day.keys())
        values = [float(v.replace('$', '').replace(',', '')) for v in aov_by_day.values()]

        fig = go.Figure(data=[go.Bar(
            x=days,
            y=values,
            text=[f"${v:.2f}" for v in values],
            textposition='auto',
        )])
        fig.update_layout(
            title="AOV by Day of Week",
            xaxis_title="Day",
            yaxis_title="Average Order Value ($)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

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
        st.markdown("Items with lowest revenue performance:")
        # Convert to dataframe for sortable display
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

    # Horizontal tabs without emojis
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Home",
        "Upload Data",
        "Dashboard",
        "Recommendations",
        "Transaction Insights",
        "Export Report"
    ])

    with tab1:
        home_page()

    with tab2:
        upload_page()

    with tab3:
        dashboard_page()

    with tab4:
        recommendations_page()

    with tab5:
        transaction_insights_page()

    with tab6:
        report_page()


if __name__ == "__main__":
    main()
