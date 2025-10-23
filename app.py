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


def upload_page():
    """Page 1: Upload restaurant POS data."""
    st.title("Upload Restaurant Data")

    st.markdown("""
    ### Welcome to FLAVYR

    Upload your restaurant's POS data to get performance insights and deal recommendations.

    **Required CSV columns:**
    - date, cuisine_type, dining_model
    - avg_ticket, covers, labor_cost_pct, food_cost_pct
    - table_turnover, sales_per_sqft, expected_customer_repeat_rate
    """)

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
        st.dataframe(df.head(10), use_container_width=True)

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
            with st.spinner("Processing..."):
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

                st.success("Data processed successfully! Go to Dashboard to view results.")
                st.balloons()


def dashboard_page():
    """Page 2: Dashboard with KPI comparisons."""
    st.title("Performance Dashboard")

    if st.session_state.analysis_results is None:
        st.warning("Please upload data first on the Upload page.")
        return

    analysis = st.session_state.analysis_results

    # Header
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Restaurant Type", f"{analysis['cuisine_type']} - {analysis['dining_model']}")
    with col2:
        st.metric("Performance Grade", analysis['performance_grade'])
    with col3:
        issues = len(analysis['underperforming_kpis'])
        st.metric("Areas Needing Attention", issues)

    st.divider()

    # KPI Comparison Cards
    st.subheader("KPI Performance")

    gaps = analysis['gaps']

    # Create 2 rows of metrics
    row1_kpis = ['avg_ticket', 'covers', 'table_turnover', 'sales_per_sqft']
    row2_kpis = ['labor_cost_pct', 'food_cost_pct', 'expected_customer_repeat_rate']

    # Row 1
    cols = st.columns(4)
    for i, kpi in enumerate(row1_kpis):
        data = gaps[kpi]
        with cols[i]:
            gap_pct = data['gap_pct']
            delta_color = "normal" if gap_pct >= 0 else "inverse"

            st.metric(
                data['kpi_name'],
                f"{data['restaurant_value']:.2f}",
                f"{gap_pct:+.1f}% vs benchmark",
                delta_color=delta_color
            )

    # Row 2
    cols = st.columns(4)
    for i, kpi in enumerate(row2_kpis):
        data = gaps[kpi]
        with cols[i]:
            gap_pct = data['gap_pct']
            delta_color = "normal" if gap_pct >= 0 else "inverse"

            st.metric(
                data['kpi_name'],
                f"{data['restaurant_value']:.2f}",
                f"{gap_pct:+.1f}% vs benchmark",
                delta_color=delta_color
            )

    st.divider()

    # Gap visualization
    st.subheader("Performance Gaps")

    # Prepare data for chart
    kpi_names = [gaps[kpi]['kpi_name'] for kpi in gaps.keys()]
    gap_values = [gaps[kpi]['gap_pct'] for kpi in gaps.keys()]

    # Color bars based on performance
    colors = ['green' if gap >= 0 else 'red' for gap in gap_values]

    # Create bar chart
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
        height=500,
        showlegend=False,
        xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black')
    )

    st.plotly_chart(fig, use_container_width=True)


def recommendations_page():
    """Page 3: Deal recommendations."""
    st.title("Deal Recommendations")

    if st.session_state.recommendation_results is None:
        st.warning("Please upload data first on the Upload page.")
        return

    rec_results = st.session_state.recommendation_results
    analysis = st.session_state.analysis_results

    # Summary
    st.subheader("Performance Summary")
    st.info(analysis['summary'])

    st.divider()

    # Recommendations
    st.subheader("Recommended Actions")

    recommendations = rec_results['recommendations']

    if not recommendations:
        st.success("Your performance is strong across all metrics. No specific recommendations at this time.")
        return

    # Display each recommendation
    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"**{i}. {rec['business_problem']}**", expanded=(i <= 2)):
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


def report_page():
    """Page 4: Generate and download reports."""
    st.title("Performance Report")

    if st.session_state.analysis_results is None:
        st.warning("Please upload data first on the Upload page.")
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


# Main app navigation
def main():
    """Main application with page navigation."""

    # Sidebar navigation
    st.sidebar.title("FLAVYR Analytics")

    page = st.sidebar.radio(
        "Navigation",
        ["Upload", "Dashboard", "Recommendations", "Report"]
    )

    # Add some spacing
    st.sidebar.divider()

    # Show current status
    if st.session_state.analysis_results is not None:
        st.sidebar.success("Data loaded")
        analysis = st.session_state.analysis_results
        st.sidebar.write(f"**Type:** {analysis['cuisine_type']}")
        st.sidebar.write(f"**Grade:** {analysis['performance_grade']}")
    else:
        st.sidebar.info("No data loaded")

    # Route to pages
    if page == "Upload":
        upload_page()
    elif page == "Dashboard":
        dashboard_page()
    elif page == "Recommendations":
        recommendations_page()
    elif page == "Report":
        report_page()


if __name__ == "__main__":
    main()
