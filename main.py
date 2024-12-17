import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

# Constants
GITHUB_CSV_URL = "https://raw.githubusercontent.com/[your-username]/[your-repo]/main/Test.csv"

def load_and_process_data():
    """Load and process the CSV file from GitHub."""
    try:
        # Load the CSV file directly
        df = pd.read_csv('Test.csv')
        
        # Convert date columns to datetime
        df['Activity date'] = pd.to_datetime(df['Activity date'])
        if 'Matter pending date' in df.columns:
            df['Matter pending date'] = pd.to_datetime(df['Matter pending date'])
        if 'Matter close date' in df.columns:
            df['Matter close date'] = pd.to_datetime(df['Matter close date'])
        
        # Calculate additional metrics
        df['Total hours'] = df['Billable hours'] + df['Non-billable hours']
        df['Utilization rate'] = (df['Billable hours'] / df['Total hours'] * 100).fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_sidebar_filters(df):
    """Create comprehensive sidebar filters."""
    st.sidebar.header("Filters")
    
    # Create tabs for filter categories
    filter_tabs = st.sidebar.tabs(["Time", "Attorneys", "Practice", "Matter"])
    
    with filter_tabs[0]:  # Time Filters
        st.subheader("Time Period")
        selected_year = st.selectbox(
            "Year",
            options=sorted(df['Activity year'].unique()),
            index=len(df['Activity year'].unique()) - 1
        )
        
        selected_quarter = st.selectbox(
            "Quarter",
            options=sorted(df['Activity quarter'].unique())
        )
        
        selected_months = st.multiselect(
            "Months",
            options=sorted(df['Activity month'].unique())
        )

    with filter_tabs[1]:  # Attorney Filters
        st.subheader("Attorney Information")
        selected_attorneys = st.multiselect(
            "Attorneys",
            options=sorted(df['User full name (first, last)'].unique())
        )
        
        selected_originating = st.multiselect(
            "Originating Attorneys",
            options=sorted(df['Originating attorney'].dropna().unique())
        )

    with filter_tabs[2]:  # Practice Filters
        st.subheader("Practice Areas")
        selected_practice_areas = st.multiselect(
            "Practice Areas",
            options=sorted(df['Practice area'].dropna().unique())
        )
        
        if 'Matter location' in df.columns:
            selected_locations = st.multiselect(
                "Locations",
                options=sorted(df['Matter location'].dropna().unique())
            )

    with filter_tabs[3]:  # Matter Filters
        st.subheader("Matter Details")
        selected_matter_status = st.multiselect(
            "Matter Status",
            options=sorted(df['Matter status'].dropna().unique())
        )
        
        if 'Matter stage' in df.columns:
            selected_matter_stage = st.multiselect(
                "Matter Stage",
                options=sorted(df['Matter stage'].dropna().unique())
            )
        
        if 'Billable matter' in df.columns:
            billable_matter = st.multiselect(
                "Billable Matter",
                options=sorted(df['Billable matter'].dropna().unique())
            )

    # Display refresh information
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Last Data Refresh:** December 16, 2024")
    st.sidebar.markdown("**Data Range:** November 2024 - Present")

    return {
        'year': selected_year,
        'quarter': selected_quarter,
        'months': selected_months,
        'attorneys': selected_attorneys,
        'originating_attorneys': selected_originating,
        'practice_areas': selected_practice_areas,
        'locations': selected_locations if 'Matter location' in df.columns else [],
        'matter_status': selected_matter_status,
        'matter_stage': selected_matter_stage if 'Matter stage' in df.columns else [],
        'billable_matter': billable_matter if 'Billable matter' in df.columns else []
    }

def filter_data(df, filters):
    """Apply all filters to the dataframe."""
    filtered_df = df.copy()
    
    # Time filters
    if filters['year']:
        filtered_df = filtered_df[filtered_df['Activity year'] == filters['year']]
    if filters['quarter']:
        filtered_df = filtered_df[filtered_df['Activity quarter'] == filters['quarter']]
    if filters['months']:
        filtered_df = filtered_df[filtered_df['Activity month'].isin(filters['months'])]
    
    # Attorney filters
    if filters['attorneys']:
        filtered_df = filtered_df[filtered_df['User full name (first, last)'].isin(filters['attorneys'])]
    if filters['originating_attorneys']:
        filtered_df = filtered_df[filtered_df['Originating attorney'].isin(filters['originating_attorneys'])]
    
    # Practice area filters
    if filters['practice_areas']:
        filtered_df = filtered_df[filtered_df['Practice area'].isin(filters['practice_areas'])]
    if filters['locations']:
        filtered_df = filtered_df[filtered_df['Matter location'].isin(filters['locations'])]
    
    # Matter filters
    if filters['matter_status']:
        filtered_df = filtered_df[filtered_df['Matter status'].isin(filters['matter_status'])]
    if filters['matter_stage']:
        filtered_df = filtered_df[filtered_df['Matter stage'].isin(filters['matter_stage'])]
    if filters['billable_matter']:
        filtered_df = filtered_df[filtered_df['Billable matter'].isin(filters['billable_matter'])]
    
    return filtered_df

def display_key_metrics(df):
    """Display key metrics in the top row."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Billable Hours",
            f"{df['Billable hours'].sum():,.1f}",
            f"${df['Billable hours amount'].sum():,.2f}"
        )
    
    with col2:
        st.metric(
            "Total Billed Hours",
            f"{df['Billed hours'].sum():,.1f}",
            f"${df['Billed hours amount'].sum():,.2f}"
        )
    
    with col3:
        utilization_rate = (
            df['Billable hours'].sum() / df['Tracked hours'].sum() * 100
            if df['Tracked hours'].sum() > 0 else 0
        )
        st.metric(
            "Utilization Rate",
            f"{utilization_rate:.1f}%",
            "of total hours"
        )
    
    with col4:
        avg_rate = (
            df['Billable hours amount'].sum() / df['Billable hours'].sum()
            if df['Billable hours'].sum() > 0 else 0
        )
        st.metric(
            "Average Rate",
            f"${avg_rate:.2f}/hr",
            "billable rate"
        )

def create_hours_distribution(df):
    """Create hours distribution chart."""
    hours_data = pd.DataFrame({
        'Category': ['Billable', 'Non-Billable', 'Unbilled'],
        'Hours': [
            df['Billable hours'].sum(),
            df['Non-billable hours'].sum(),
            df['Unbilled hours'].sum()
        ]
    })
    
    fig = px.pie(
        hours_data,
        values='Hours',
        names='Category',
        title='Hours Distribution'
    )
    return fig

def create_practice_area_analysis(df):
    """Create practice area analysis chart."""
    practice_data = df.groupby('Practice area').agg({
        'Billable hours': 'sum',
        'Billable hours amount': 'sum'
    }).reset_index()
    
    fig = px.bar(
        practice_data,
        x='Practice area',
        y=['Billable hours', 'Billable hours amount'],
        title='Practice Area Performance',
        barmode='group'
    )
    return fig

def create_attorney_performance(df):
    """Create attorney performance chart."""
    attorney_data = df.groupby('User full name (first, last)').agg({
        'Billable hours': 'sum',
        'Billed hours': 'sum',
        'Billable hours amount': 'sum'
    }).reset_index()
    
    fig = px.scatter(
        attorney_data,
        x='Billable hours',
        y='Billable hours amount',
        size='Billed hours',
        hover_name='User full name (first, last)',
        title='Attorney Performance'
    )
    return fig

def main():
    st.set_page_config(page_title="Legal Dashboard", layout="wide")
    st.title("Legal Practice Management Dashboard")
    
    # Add refresh date to header
    st.markdown(
        """
        <div style='text-align: right; color: gray; font-size: 0.8em;'>
        Last Refresh: December 16, 2024
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load data directly
    df = load_and_process_data()
    
    if df is not None:
        # Data range info
        st.info("Current data covers: November 2024 - December 16, 2024")
        
        # Get filters
        filters = create_sidebar_filters(df)
        
        # Apply filters
        filtered_df = filter_data(df, filters)
        
        # Show active filters
        active_filters = {k: v for k, v in filters.items() if v}
        if active_filters:
            st.markdown("### Active Filters")
            for filter_name, filter_value in active_filters.items():
                st.markdown(f"**{filter_name.replace('_', ' ').title()}:** {', '.join(map(str, filter_value)) if isinstance(filter_value, list) else filter_value}")
        
        # Display metrics and charts
        display_key_metrics(filtered_df)
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_hours_distribution(filtered_df),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                create_practice_area_analysis(filtered_df),
                use_container_width=True
            )
        
        # Attorney performance chart
        st.plotly_chart(
            create_attorney_performance(filtered_df),
            use_container_width=True
        )
        
        # Detailed metrics table
        st.header("Detailed Metrics")
        attorney_metrics = filtered_df.groupby('User full name (first, last)').agg({
            'Billable hours': 'sum',
            'Non-billable hours': 'sum',
            'Billed hours': 'sum',
            'Billable hours amount': 'sum',
            'Billed hours amount': 'sum'
        }).round(2)
        
        st.dataframe(attorney_metrics)

if __name__ == "__main__":
    main()
