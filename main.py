import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

def load_and_process_data(file):
    """Load and process the CSV file."""
    df = pd.read_csv(file)
    
    # Convert date columns to datetime
    df['Activity date'] = pd.to_datetime(df['Activity date'])
    df['Matter pending date'] = pd.to_datetime(df['Matter pending date'])
    df['Matter close date'] = pd.to_datetime(df['Matter close date'])
    
    # Calculate additional metrics
    df['Total hours'] = df['Billable hours'] + df['Non-billable hours']
    df['Utilization rate'] = (df['Billable hours'] / df['Total hours'] * 100).fillna(0)
    
    return df

def create_sidebar_filters(df):
    """Create sidebar filters."""
    st.sidebar.header("Filters")
    
    # Time period filters
    selected_year = st.sidebar.selectbox(
        "Select Year",
        options=sorted(df['Activity year'].unique()),
        index=len(df['Activity year'].unique()) - 1
    )
    
    selected_quarter = st.sidebar.selectbox(
        "Select Quarter",
        options=sorted(df['Activity quarter'].unique())
    )
    
    # Practice area filter
    practice_areas = st.sidebar.multiselect(
        "Select Practice Areas",
        options=sorted(df['Practice area'].dropna().unique())
    )
    
    # Attorney filter
    attorneys = st.sidebar.multiselect(
        "Select Attorneys",
        options=sorted(df['User full name (first, last)'].unique())
    )
    
    return selected_year, selected_quarter, practice_areas, attorneys

def filter_data(df, year, quarter, practice_areas, attorneys):
    """Apply filters to the dataframe."""
    filtered_df = df.copy()
    
    filtered_df = filtered_df[filtered_df['Activity year'] == year]
    filtered_df = filtered_df[filtered_df['Activity quarter'] == quarter]
    
    if practice_areas:
        filtered_df = filtered_df[filtered_df['Practice area'].isin(practice_areas)]
    
    if attorneys:
        filtered_df = filtered_df[filtered_df['User full name (first, last)'].isin(attorneys)]
    
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
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        df = load_and_process_data(uploaded_file)
        
        # Apply filters
        year, quarter, practice_areas, attorneys = create_sidebar_filters(df)
        filtered_df = filter_data(df, year, quarter, practice_areas, attorneys)
        
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
