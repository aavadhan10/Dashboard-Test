import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

def load_and_process_data():
    """Load and process the CSV file."""
    try:
        # Load the CSV file directly
        df = pd.read_csv('Test.csv')
        
        # Convert date columns to datetime
        df['Activity date'] = pd.to_datetime(df['Activity date'])
        if 'Matter pending date' in df.columns:
            df['Matter pending date'] = pd.to_datetime(df['Matter pending date'])
        if 'Matter close date' in df.columns:
            df['Matter close date'] = pd.to_datetime(df['Matter close date'])
        
        # Convert Matter description to string
        df['Matter description'] = df['Matter description'].fillna('').astype(str)
        
        # Add attorney level mapping
        attorney_levels = {
            'Adrian Dirassar': 'Senior Counsel',
            'Adrian Roomes': 'Mid-Level Counsel',
            'Ajay Krishnan': 'Mid-Level Counsel',
            'Alexander James Stack': 'Senior Counsel',
            'Aliza Dason': 'Counsel',
            'Andrea Freund': 'Senior Counsel',
            'Alan Sless': 'Senior Counsel',
            'Annie Belecki': 'Senior Counsel',
            'Anjali Ekta Banka': 'Senior Counsel',
            'Anthony Shapiro': 'Senior Counsel',
            'Antoine Malek': 'Senior Counsel',
            'April Pettigrew': 'Corporate Document Assistant',
            'Avril Hasselfield': 'Senior Counsel',
            'Benjamin Derek Rovet': 'Senior Counsel',
            'Beth Gearing': 'Senior Counsel',
            'Bill Stanger': 'Senior Counsel',
            'Bill Herman': 'Senior Counsel',
            'Binita Jacob': 'Senior Counsel',
            'Brenda Chandler': 'Senior Counsel',
            'Bruce Baron': 'Senior Counsel',
            'Cerise Latibeaudiere': 'Senior Counsel',
            'Constance Wai Min Chan': 'Senior Counsel',
            'Corrie Stepan': 'Senior Counsel',
            'Cynthia Yang': 'Senior Counsel',
            'Daniel Batista': 'Senior Counsel',
            'Daniel Lawrence McKay': 'Senior Counsel',
            'Dave McIntyre': 'Senior Counsel',
            'David Dunbar': 'Senior Counsel',
            'David Masse': 'Senior Counsel',
            'David Bryan Zender': 'Senior Counsel',
            'Dina Moore': 'Law Clerk',
            'Doris Riker': 'Document Specialist',
            'Ebony Stoffels': 'Law Clerk',
            'Ellen Victoria Swan': 'Senior Counsel',
            'Elyse Mallins': 'Senior Counsel',
            'Ernest Belyea': 'Senior Counsel',
            'Esia (Theodosia) Giaouris': 'Senior Counsel',
            'Eva Melamed': 'Senior Counsel',
            'Evelyn Ackah': 'Senior Counsel',
            'Frances Petryshen': 'Corporate Secretary',
            'Frank Gary Giblon': 'Senior Counsel',
            'Glen Harder': 'Senior Counsel',
            'Greg Porter': 'Senior Counsel',
            'Greg Ramsay': 'Senior Counsel',
            'Hamish Cumming': 'Senior Counsel',
            'Hugh Kerr': 'Senior Counsel',
            'Ian Alexander Ness': 'Senior Counsel',
            'Iana Namestnikova': 'Mid-Level Counsel',
            'James Oborne': 'Mid-Level Counsel',
            'Jason Lakhan': 'Senior Counsel',
            'Jeff Bright': 'Senior Counsel',
            'Jeffrey David Klam': 'Senior Counsel',
            'Jeremy Budd': 'Senior Counsel',
            'Joel Guralnick': 'Senior Counsel',
            'John Tyrrell': 'Senior Counsel',
            'John Whyte': 'Senior Counsel',
            'Josee Cameron-Virgo': 'Senior Counsel',
            'Judy Hyeonseon Chun': 'Senior Counsel',
            'Kendall Barban': 'Start-Up Lawyer',
            'Kevin Michael Shnier': 'Senior Counsel',
            'Kim Guy Von Arx': 'Senior Counsel',
            'Lance Lehman': 'Senior Counsel',
            'Leonard Gaik': 'Senior Counsel',
            'Leslie Allan': 'Senior Counsel',
            'Lisa Conway': 'Senior Counsel',
            'Lisa McDowell': 'Senior Counsel',
            'Lori Lyn Adams': 'Senior Counsel',
            'Luke Kuzio': 'Senior Counsel',
            'Mark Wainman': 'Senior Counsel',
            'Meenal Gole': 'Corporate Secretary',
            'Melissa Babel': 'Senior Counsel',
            'Michael Fitzgerald': 'Senior Counsel',
            'Michele Koyle': 'Senior Counsel',
            'Michelle Grant-Asselin': 'Law Clerk',
            'Monica Goyal': 'Senior Counsel',
            'Morli Shemesh': 'Senior Counsel',
            'Neil Kothari': 'Senior Counsel',
            'Nikki Stewart-St. Arnault': 'Senior Counsel',
            'Olivia Dutka': 'Law Clerk',
            'Patrick Dolan': 'Senior Counsel',
            'Peter Torn': 'Senior Counsel',
            'Peter Dale': 'Senior Counsel',
            'Peter Goode': 'Senior Counsel',
            'Peter Prattas': 'Senior Counsel',
            'Peter Kalins': 'Senior Counsel',
            'Philippe Chouinard-Rousseau': 'Senior Counsel',
            'Randall Witten': 'Senior Counsel',
            'Robert Bosenius': 'Senior Counsel',
            'Rose Oushalkas': 'Senior Counsel',
            'Sarah Blackburn': 'Counsel',
            'Sara Kunto': 'Senior Counsel',
            'Sarah Sidhu': 'Senior Counsel',
            'Sean Mitra': 'Mid-Level Counsel',
            'Sean Williamson': 'Counsel',
            'Seung-Yoon Lisa Lee': 'Senior Counsel',
            'Sherry Roxanne Hanlon': 'Senior Counsel',
            'Simon Brian Anthony Rawson Levett': 'Senior Counsel',
            'Solange Brard': 'Senior Counsel',
            'Sonny Bhalla': 'Senior Counsel',
            'Stephen Dan Black': 'Senior Counsel',
            'Sue Gaudi': 'Senior Counsel',
            'Susan Rai': 'Senior Counsel',
            'Tim Froese': 'Senior Counsel',
            'Tracey Lynn Durand': 'Senior Counsel',
            'Vinoja Wichweswaran': 'Mid-Level Counsel',
            'Wanda Shreve': 'Senior Counsel',
            'Wendy Bach': 'Senior Counsel',
            'Yah Yao': 'Senior Counsel',
            'Zoe Rossolatos': 'Senior Counsel'
        }
        
        # Add attorney level to dataframe
        df['Attorney Level'] = df['User full name (first, last)'].map(attorney_levels)
        
        # Calculate additional metrics
        df['Total hours'] = df['Billable hours'] + df['Non-billable hours']
        df['Utilization rate'] = (df['Billable hours'] / df['Total hours'] * 100).fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def calculate_average_rate(df):
    """
    Calculate average rate excluding flat fees and expenses.
    Flat fees are identified as entries with 0 or 1 hours and amount >= 1500
    """
    # Create a mask for flat fee entries
    flat_fee_mask = (
        ((df['Billable hours'] <= 1) & (df['Billable hours amount'] >= 1500)) |
        (df['Billable hours'] == 0)
    )
    
    # Filter out flat fees
    billable_df = df[~flat_fee_mask]
    
    # Calculate average rate
    if billable_df['Billable hours'].sum() > 0:
        return billable_df['Billable hours amount'].sum() / billable_df['Billable hours'].sum()
    return 0

def calculate_utilization_rate(df):
    """
    Calculate utilization rate based on attorney level:
    - Counsel/Senior Counsel/Mid-Level Counsel: 80 billable hours per month
    - Associates: 160 total hours per month (billable + non-billable)
    """
    # Calculate months in the dataset
    months = len(df['Activity date'].dt.to_period('M').unique())
    
    # Group attorneys by level
    counsel_levels = ['Senior Counsel', 'Counsel', 'Mid-Level Counsel']
    
    # Initialize totals
    total_actual_hours = 0
    total_target_hours = 0
    
    # Calculate for each attorney
    for attorney, attorney_df in df.groupby('User full name (first, last)'):
        level = attorney_df['Attorney Level'].iloc[0]
        
        if level in counsel_levels:
            # For counsel levels: 80 billable hours per month
            actual_hours = attorney_df['Billable hours'].sum()
            target_hours = 80 * months
        else:
            # For associates and others: 160 total hours per month
            actual_hours = attorney_df['Tracked hours'].sum()
            target_hours = 160 * months
            
        total_actual_hours += actual_hours
        total_target_hours += target_hours
    
    # Calculate overall utilization rate
    return (total_actual_hours / total_target_hours * 100) if total_target_hours > 0 else 0

def calculate_origination_stats(df, attorney_name):
    """
    Calculate stats for hours worked by others on originated files
    """
    # Filter for matters originated by the attorney
    originated_matters = df[df['Originating attorney'] == attorney_name]
    
    # Calculate hours worked by others on these matters
    others_hours = originated_matters[
        originated_matters['User full name (first, last)'] != attorney_name
    ]['Billable hours'].sum()
    
    return others_hours
    
def create_sidebar_filters(df):
    """Create comprehensive sidebar filters."""
    st.sidebar.header("Filters")
    
    # Create tabs for filter categories
    filter_tabs = st.sidebar.tabs(["Time", "Attorneys", "Practice", "Matter", "Financial", "Clients"])
    
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
        
        # Add date range filter
        date_range = st.date_input(
            "Custom Date Range",
            value=(df['Activity date'].min(), df['Activity date'].max()),
            min_value=df['Activity date'].min(),
            max_value=df['Activity date'].max()
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
        
        # Add minimum hours filter
        min_hours = st.slider(
            "Minimum Billable Hours",
            min_value=0.0,
            max_value=float(df['Billable hours'].max()),
            value=0.0
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

    with filter_tabs[4]:  # Financial Filters
        st.subheader("Financial Metrics")
        min_amount = st.number_input(
            "Minimum Billable Amount",
            min_value=0.0,
            max_value=float(df['Billable hours amount'].max()),
            value=0.0
        )
        
        rate_range = st.slider(
            "Hourly Rate Range",
            min_value=float(df['Billable hours amount'].min()),
            max_value=float(df['Billable hours amount'].max()),
            value=(float(df['Billable hours amount'].min()), float(df['Billable hours amount'].max()))
        )

    with filter_tabs[5]:  # Client Filters
        st.subheader("Client Information")
        selected_clients = st.multiselect(
            "Select Clients",
            options=sorted(df['Matter description'].unique())
        )
        
        min_client_hours = st.slider(
            "Minimum Client Hours",
            min_value=0.0,
            max_value=float(df.groupby('Matter description')['Billable hours'].sum().max()),
            value=0.0
        )

    # Display refresh information
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Last Data Refresh:** December 16, 2024")
    st.sidebar.markdown("**Data Range:** November 2024 - Present")

    return {
        'year': selected_year,
        'quarter': selected_quarter,
        'months': selected_months,
        'date_range': date_range,
        'attorneys': selected_attorneys,
        'originating_attorneys': selected_originating,
        'min_hours': min_hours,
        'practice_areas': selected_practice_areas,
        'locations': selected_locations if 'Matter location' in df.columns else [],
        'matter_status': selected_matter_status,
        'matter_stage': selected_matter_stage if 'Matter stage' in df.columns else [],
        'billable_matter': billable_matter if 'Billable matter' in df.columns else [],
        'min_amount': min_amount,
        'rate_range': rate_range,
        'clients': selected_clients,
        'min_client_hours': min_client_hours
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
    if len(filters['date_range']) == 2:
        filtered_df = filtered_df[
            (filtered_df['Activity date'].dt.date >= filters['date_range'][0]) &
            (filtered_df['Activity date'].dt.date <= filters['date_range'][1])
        ]
    
    # Attorney filters
    if filters['attorneys']:
        filtered_df = filtered_df[filtered_df['User full name (first, last)'].isin(filters['attorneys'])]
    if filters['originating_attorneys']:
        filtered_df = filtered_df[filtered_df['Originating attorney'].isin(filters['originating_attorneys'])]
    if filters['min_hours'] > 0:
        attorney_hours = filtered_df.groupby('User full name (first, last)')['Billable hours'].sum()
        valid_attorneys = attorney_hours[attorney_hours >= filters['min_hours']].index
        filtered_df = filtered_df[filtered_df['User full name (first, last)'].isin(valid_attorneys)]
    
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
    
    # Financial filters
    if filters['min_amount'] > 0:
        filtered_df = filtered_df[filtered_df['Billable hours amount'] >= filters['min_amount']]
    if len(filters['rate_range']) == 2:
        filtered_df = filtered_df[
            (filtered_df['Billable hours amount'] >= filters['rate_range'][0]) &
            (filtered_df['Billable hours amount'] <= filters['rate_range'][1])
        ]
    
    # Client filters
    if filters['clients']:
        filtered_df = filtered_df[filtered_df['Matter description'].isin(filters['clients'])]
    if filters['min_client_hours'] > 0:
        client_hours = filtered_df.groupby('Matter description')['Billable hours'].sum()
        valid_clients = client_hours[client_hours >= filters['min_client_hours']].index
        filtered_df = filtered_df[filtered_df['Matter description'].isin(valid_clients)]
    
    return filtered_df

def display_key_metrics(df):
    """Display key metrics with updated calculations."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Billable Hours",
            f"{df['Billable hours'].sum():,.1f}",
            f"${df['Billable hours amount'].sum():,.2f}"
        )
    
    with col2:
        # Calculate average rate excluding flat fees
        avg_rate = calculate_average_rate(df)
        st.metric(
            "Average Rate (Excl. Flat Fees)",
            f"${avg_rate:.2f}/hr",
            "billable rate"
        )
    
    with col3:
        utilization_rate = calculate_utilization_rate(df)
        st.metric(
            "Utilization Rate",
            f"{utilization_rate:.1f}%",
            "of target hours"
        )
    
    with col4:
        # YTD Collections placeholder - you'll need to add actual YTD collection data
        ytd_collections = df['Billed hours amount'].sum()  # Placeholder calculation
        st.metric(
            "YTD Collections",
            f"${ytd_collections:,.2f}",
            "year to date"
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

def create_client_analysis_charts(df):
    """Create client analysis visualizations."""
    # Top clients by billable hours
    top_clients = df.groupby('Matter description').agg({
        'Billable hours': 'sum',
        'Billable hours amount': 'sum'
    }).sort_values('Billable hours', ascending=False).head(10)
    
    fig1 = px.bar(
        top_clients,
        y=top_clients.index,
        x='Billable hours',
        title='Top 10 Clients by Billable Hours',
        orientation='h'
    )
    
    # Client hours distribution
    client_hours = df.groupby('Matter description').agg({
        'Billable hours': 'sum',
        'Non-billable hours': 'sum',
        'Unbilled hours': 'sum'
    }).reset_index()
    
    fig2 = px.treemap(
        client_hours,
        path=['Matter description'],
        values='Billable hours',
        title='Client Hours Distribution'
    )
    
    return fig1, fig2

def create_client_practice_area_chart(df):
    """Create client by practice area analysis."""
    client_practice = df.groupby(['Matter description', 'Practice area']).agg({
        'Billable hours': 'sum'
    }).reset_index()
    
    fig = px.sunburst(
        client_practice,
        path=['Practice area', 'Matter description'],
        values='Billable hours',
        title='Client Distribution by Practice Area'
    )
    return fig

def create_trending_chart(df):
    """Create trending analysis chart."""
    daily_data = df.groupby('Activity date').agg({
        'Billable hours': 'sum',
        'Billed hours': 'sum',
        'Non-billable hours': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_data['Activity date'],
        y=daily_data['Billable hours'],
        name='Billable Hours',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=daily_data['Activity date'],
        y=daily_data['Billed hours'],
        name='Billed Hours',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=daily_data['Activity date'],
        y=daily_data['Non-billable hours'],
        name='Non-billable Hours',
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title='Daily Hours Trend',
        xaxis_title='Date',
        yaxis_title='Hours'
    )
    return fig

def create_attorney_utilization_chart(df):
    """Create attorney utilization chart."""
    attorney_util = df.groupby('User full name (first, last)').agg({
        'Billable hours': 'sum',
        'Non-billable hours': 'sum',
        'Tracked hours': 'sum'
    }).reset_index()
    
    attorney_util['Utilization Rate'] = (
        attorney_util['Billable hours'] / attorney_util['Tracked hours'] * 100
    ).round(2)
    
    fig = px.bar(
        attorney_util,
        x='User full name (first, last)',
        y='Utilization Rate',
        title='Attorney Utilization Rates',
        color='Utilization Rate',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def create_practice_area_sunburst(df):
    """Create practice area sunburst chart."""
    practice_data = df.groupby(['Practice area', 'User full name (first, last)']).agg({
        'Billable hours': 'sum'
    }).reset_index()
    
    fig = px.sunburst(
        practice_data,
        path=['Practice area', 'User full name (first, last)'],
        values='Billable hours',
        title='Practice Area Distribution by Attorney'
    )
    return fig

def create_client_metrics_table(df):
    """Create detailed client metrics table."""
    client_metrics = df.groupby('Matter description').agg({
        'Billable hours': 'sum',
        'Billed hours': 'sum',
        'Non-billable hours': 'sum',
        'Billable hours amount': 'sum',
        'Billed hours amount': 'sum',
        'Tracked hours': 'sum'
    }).round(2)
    
    # Calculate additional metrics
    client_metrics['Utilization Rate'] = (
        client_metrics['Billable hours'] / client_metrics['Tracked hours'] * 100
    ).round(2)
    
    client_metrics['Average Rate'] = (
        client_metrics['Billable hours amount'] / client_metrics['Billable hours']
    ).round(2)
    
    client_metrics['Efficiency Rate'] = (
        client_metrics['Billed hours'] / client_metrics['Billable hours'] * 100
    ).round(2)
    
    return client_metrics

def main():
    st.set_page_config(page_title="Legal Dashboard", layout="wide")
    st.title("Scale Management Dashboard")
    
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
        st.info("Current data covers: November 1 2024 - December 16, 2024")
        
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
        
        # Create tabs for different analysis sections
        main_tabs = st.tabs(["Overview", "Client Analysis", "Attorney Analysis", "Practice Areas", "Trending"])
        
        with main_tabs[0]:  # Overview Tab
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
            
            # Additional overview metrics in expandable section
            with st.expander("Detailed Overview Metrics"):
                overview_metrics = filtered_df.agg({
                    'Billable hours': 'sum',
                    'Non-billable hours': 'sum',
                    'Billed hours': 'sum',
                    'Billable hours amount': 'sum',
                    'Billed hours amount': 'sum'
                }).round(2)
                st.write(overview_metrics)
        
        with main_tabs[1]:  # Client Analysis Tab
            # Client Analysis Section
            client_bar, client_treemap = create_client_analysis_charts(filtered_df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(client_bar, use_container_width=True)
            with col2:
                st.plotly_chart(client_treemap, use_container_width=True)
            
            # Client Practice Area Distribution
            st.plotly_chart(
                create_client_practice_area_chart(filtered_df),
                use_container_width=True
            )
            
            # Client Metrics Table
            st.subheader("Client Metrics")
            client_metrics = create_client_metrics_table(filtered_df)
            st.dataframe(
                client_metrics,
                column_config={
                    "Utilization Rate": st.column_config.NumberColumn(
                        "Utilization Rate",
                        format="%.2f%%"
                    ),
                    "Average Rate": st.column_config.NumberColumn(
                        "Average Rate",
                        format="$%.2f"
                    ),
                    "Efficiency Rate": st.column_config.NumberColumn(
                        "Efficiency Rate",
                        format="%.2f%%"
                    )
                }
            )
            
            # Download button for client metrics
            csv = client_metrics.to_csv().encode('utf-8')
            st.download_button(
                label="Download Client Metrics CSV",
                data=csv,
                file_name="client_metrics.csv",
                mime="text/csv",
            )
        
        with main_tabs[2]:  # Attorney Analysis Tab
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    create_attorney_performance(filtered_df),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    create_attorney_utilization_chart(filtered_df),
                    use_container_width=True
                )
            
            # Attorney Metrics Table
            st.subheader("Attorney Metrics")
            attorney_metrics = filtered_df.groupby('User full name (first, last)').agg({
                'Billable hours': 'sum',
                'Non-billable hours': 'sum',
                'Billed hours': 'sum',
                'Billable hours amount': 'sum',
                'Billed hours amount': 'sum',
                'Tracked hours': 'sum'
            }).round(2)
            
            # Calculate additional metrics
            attorney_metrics['Utilization Rate'] = (
                attorney_metrics['Billable hours'] / attorney_metrics['Tracked hours'] * 100
            ).round(2)
            
            attorney_metrics['Average Rate'] = (
                attorney_metrics['Billable hours amount'] / attorney_metrics['Billable hours']
            ).round(2)
            
            st.dataframe(
                attorney_metrics,
                column_config={
                    "Utilization Rate": st.column_config.NumberColumn(
                        "Utilization Rate",
                        format="%.2f%%"
                    ),
                    "Average Rate": st.column_config.NumberColumn(
                        "Average Rate",
                        format="$%.2f"
                    )
                }
            )
            
            # Download button for attorney metrics
            attorney_csv = attorney_metrics.to_csv().encode('utf-8')
            st.download_button(
                label="Download Attorney Metrics CSV",
                data=attorney_csv,
                file_name="attorney_metrics.csv",
                mime="text/csv",
            )
        
        with main_tabs[3]:  # Practice Areas Tab
            # Practice Area Distribution
            st.plotly_chart(
                create_practice_area_sunburst(filtered_df),
                use_container_width=True
            )
            
            # Practice Area Metrics Table
            st.subheader("Practice Area Metrics")
            practice_metrics = filtered_df.groupby('Practice area').agg({
                'Billable hours': 'sum',
                'Non-billable hours': 'sum',
                'Billed hours': 'sum',
                'Billable hours amount': 'sum',
                'Billed hours amount': 'sum'
            }).round(2)
            
            st.dataframe(practice_metrics)
        
        with main_tabs[4]:  # Trending Tab
            st.plotly_chart(
                create_trending_chart(filtered_df),
                use_container_width=True
            )
            
            # Monthly trends
            monthly_data = filtered_df.groupby([
                pd.Grouper(key='Activity date', freq='M')
            ]).agg({
                'Billable hours': 'sum',
                'Billed hours': 'sum',
                'Non-billable hours': 'sum'
            }).reset_index()
            
            st.subheader("Monthly Trends")
            st.line_chart(
                monthly_data.set_index('Activity date')
            )

if __name__ == "__main__":
    main()
