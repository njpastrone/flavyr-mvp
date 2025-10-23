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
from src.recommender import generate_recommendations, KPI_TO_PROBLEM
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
            xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black')
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
            if rec['business_problem'] == KPI_TO_PROBLEM.get(kpi):
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
