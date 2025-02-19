import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_and_process_data():
    """Load and process the CSV file and add attorney level information."""
    try:
        # Load the CSV file
        df = pd.read_csv('Test_Full_Year.csv')
        
        # Convert date strings to datetime objects
        date_columns = ['Activity date', 'Matter open date', 'Matter pending date', 'Matter close date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')
        
        # Convert Matter description to string
        df['Matter description'] = df['Matter description'].fillna('').astype(str)
        
        # Attorney levels mapping
        attorney_levels = {
            'Aaron Swerdlow': 'Senior Counsel',
            'Aidan Toombs': 'Mid-Level Counsel',
            'Alexander Gershen': 'Senior Counsel',
            'Alexander Slafkosky': 'Senior Counsel',
            'Alfred Bridi': 'Senior Counsel',
            'Aliona Ierega': 'Mid-Level Counsel',
            'Amy Duvanich': 'Senior Counsel',
            'Andres Idarraga': 'Senior Counsel',
            'Andy Baxter': 'Mid-Level Counsel',
            'Antigone Peyton': 'Senior Counsel',
            'Ayala Magder': 'Senior Counsel',
            'Benjamin Golopol': 'Mid-Level Counsel',
            'Brian Detwiler': 'Senior Counsel',
            'Brian Elliott': 'Senior Counsel',
            'Brian Hicks': 'Senior Counsel',
            'Brian McEvoy': 'Senior Counsel',
            'Brian Scherer': 'Senior Counsel',
            'Caitlin Cunningham': 'Mid-Level Counsel',
            'Cary Ullman': 'Senior Counsel',
            'Channah Rose': 'Mid-Level Counsel',
            'Charles Caliman': 'Senior Counsel',
            'Charles Wallace': 'Senior Counsel',
            'Chris Geyer': 'Senior Counsel',
            'Chris Jones': 'Mid-Level Counsel',
            'Christopher Grewe': 'Senior Counsel',
            'Chuck Kraus': 'Senior Counsel',
            'Corey Pedersen': 'Senior Counsel',
            'Darren Collins (DS)': 'Document Specialist',
            'David Lundeen': 'Senior Counsel',
            'Derek Gilman': 'Senior Counsel',
            'Donica Forensich': 'Mid-Level Counsel',
            'Dori Karjian': 'Senior Counsel',
            'Doug Mitchell': 'Senior Counsel',
            'Elliott Gee (DS)': 'Document Specialist',
            'Emma Thompson': 'Senior Counsel',
            'Eric Blatt': 'Senior Counsel',
            'Erica Shepard': 'Senior Counsel',
            'Garrett Ordower': 'Senior Counsel',
            'Gregory Winter': 'Senior Counsel',
            'Hannah Valdez': 'Mid-Level Counsel',
            'Heather Cantua': 'Mid-Level Counsel',
            'Henry Ciocca': 'Senior Counsel',
            'Jacqueline Post Ladha': 'Senior Counsel',
            'James Cashel': 'Mid-Level Counsel',
            'James Creedon': 'Senior Counsel',
            'Jamie Wells': 'Senior Counsel',
            'Jason Altieri': 'Senior Counsel',
            'Jason Harrison': 'Mid-Level Counsel',
            'Jeff Lord': 'Senior Counsel',
            'Jeff Love': 'Senior Counsel',
            'Jenna Geuke': 'Mid-Level Counsel',
            'Joanne Wolforth': 'Mid-Level Counsel',
            'John Mitnick': 'Senior Counsel',
            'Jonathan Van Loo': 'Senior Counsel',
            'Joseph Kiefer': 'Mid-Level Counsel',
            'Josh Banerje': 'Mid-Level Counsel',
            'Julie Snyder': 'Senior Counsel',
            'Julien Apollon': 'Mid-Level Counsel',
            'Justin McAnaney': 'Mid-Level Counsel',
            'Katy Barreto': 'Senior Counsel',
            'Katy Reamon': 'Mid-Level Counsel',
            'Kimberly Griffin': 'Mid-Level Counsel',
            'Kirby Drake': 'Senior Counsel',
            'Kristen Dayley': 'Senior Counsel',
            'Kristin Bohm': 'Mid-Level Counsel',
            'Lauren Titolo': 'Mid-Level Counsel',
            'Lindsey Altmeyer': 'Senior Counsel',
            'M. Sidney Donica': 'Senior Counsel',
            'Marissa Fox': 'Senior Counsel',
            'Mary Spooner': 'Senior Counsel',
            'Matthew Angelo': 'Senior Counsel',
            'Matthew Dowd (DS)': 'Document Specialist',
            'Maureen Bumgarner': 'Mid-Level Counsel',
            'Melissa Balough': 'Senior Counsel',
            'Melissa Clarke': 'Senior Counsel',
            'Michael Keskey': 'Mid-Level Counsel',
            'Michelle Maticic': 'Senior Counsel',
            'Natasha Fedder': 'Senior Counsel',
            'Nicole Baldocchi': 'Senior Counsel',
            'Nora Wong': 'Mid-Level Counsel',
            'Ornella Bourne': 'Mid-Level Counsel',
            'Rainer Scarton': 'Mid-Level Counsel',
            'Robert Gans': 'Senior Counsel',
            'Robin Shofner': 'Senior Counsel',
            'Robyn Marcello': 'Mid-Level Counsel',
            'Sabina Schiller': 'Mid-Level Counsel',
            'Samer Korkor': 'Senior Counsel',
            'Sara Rau Frumkin': 'Senior Counsel',
            'Scale LLP': 'Other',
            'Scott Wiegand': 'Senior Counsel',
            'Shailika Kotiya': 'Mid-Level Counsel',
            'Shannon Straughan': 'Senior Counsel',
            'Stephen Bosco': 'Mid-Level Counsel',
            'Steve Forbes': 'Senior Counsel',
            'Steve Zagami, Paralegal': 'Paralegal',
            'Thomas Soave': 'Mid-Level Counsel',
            'Thomas Stine': 'Senior Counsel',
            'Tim Furin': 'Senior Counsel',
            'Trey Calver': 'Senior Counsel',
            'Tyler Hayden': 'Mid-Level Counsel',
            'Whitney Joubert': 'Senior Counsel',
            'Zach Ruby': 'Mid-Level Counsel'
        }
        
        # Clean attorney names before mapping (remove extra spaces)
        df['User full name (first, last)'] = df['User full name (first, last)'].str.strip()
        
        # Add attorney level column
        df['Attorney level'] = df['User full name (first, last)'].map(attorney_levels)
        
        # Debug: Print unmapped attorneys
        unmapped = df[df['Attorney level'].isna()]['User full name (first, last)'].unique()
        if len(unmapped) > 0:
            print("\nUnmapped attorneys:", unmapped)
        
        # Use the columns as they appear in your data
        df['Billable hours'] = df['Billed & Unbilled hours'].fillna(0)
        df['Billable hours amount'] = df['Billed & Unbilled hours value'].fillna(0)
        df['Billed hours'] = df['Billed hours'].fillna(0)
        df['Billed hours amount'] = df['Billed hours value'].fillna(0)
        df['Unbilled hours'] = df['Unbilled hours'].fillna(0)
        df['Unbilled hours amount'] = df['Unbilled hours value'].fillna(0)
        df['Non-billable hours'] = df['Non-billable hours'].fillna(0)
        df['Non-billable hours amount'] = df['Non-billable hours value'].fillna(0)
        
        # Calculate total hours and utilization rate
        df['Total hours'] = df['Tracked hours'].fillna(0)
        df['Utilization rate'] = df['Utilization rate'].fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        print(f"Detailed error information: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
        return None

def create_sidebar_filters(df):
    """Create comprehensive sidebar filters including attorney level filter."""
    st.sidebar.header("Filters")
    
    # Create tabs for filter categories
    filter_tabs = st.sidebar.tabs(["Time", "Attorneys", "Practice", "Matter", "Financial", "Clients"])
    
    with filter_tabs[0]:  # Time Filters
        st.subheader("Time Period")
        
        # Get the year from the Activity date column
        df['year'] = pd.to_datetime(df['Activity date']).dt.year
        selected_year = st.selectbox(
            "Year",
            options=sorted(df['year'].unique()),
            index=len(df['year'].unique()) - 1
        )
        
        selected_quarter = st.selectbox(
            "Quarter",
            options=sorted(df['Activity quarter'].unique())
        )
        
        selected_months = st.multiselect(
            "Months",
            options=sorted(df['Activity month'].unique())
        )
        
        date_range = st.date_input(
            "Custom Date Range",
            value=(pd.to_datetime(df['Activity date']).min(), pd.to_datetime(df['Activity date']).max()),
            min_value=pd.to_datetime(df['Activity date']).min(),
            max_value=pd.to_datetime(df['Activity date']).max()
        )

    with filter_tabs[1]:  # Attorney Filters
        st.subheader("Attorney Information")
        
        # Add attorney level filter
        selected_attorney_levels = st.multiselect(
            "Attorney Levels",
            options=sorted(df['Attorney level'].dropna().unique()),
            help="Select one or more attorney levels to filter"
        )
        
        # Filter attorneys based on selected levels
        attorney_options = sorted(df['User full name (first, last)'].unique())
        if selected_attorney_levels:
            attorney_options = sorted([
                name for name in df['User full name (first, last)'].unique()
                if df[df['User full name (first, last)'] == name]['Attorney level'].iloc[0] in selected_attorney_levels
            ])
        
        selected_attorneys = st.multiselect(
            "Attorneys",
            options=attorney_options
        )
        
        selected_originating = st.multiselect(
            "Originating Attorneys",
            options=sorted(df['Originating attorney'].dropna().unique())
        )
        
        # Safe handling of tracked hours with proper numeric conversion
        df['Tracked hours'] = pd.to_numeric(df['Tracked hours'], errors='coerce')
        tracked_hours_max = df['Tracked hours'].fillna(0).max()
        min_hours = st.slider(
            "Minimum Billable Hours",
            min_value=0.0,
            max_value=float(tracked_hours_max),
            value=0.0
        )

    with filter_tabs[2]:  # Practice Filters
        st.subheader("Practice Areas")
        selected_practice_areas = st.multiselect(
            "Practice Areas",
            options=sorted(df['Practice area'].dropna().unique())
        )
        
        selected_locations = st.multiselect(
            "Matter Locations",
            options=sorted(df['Matter location'].dropna().unique())
        )

    with filter_tabs[3]:  # Matter Filters
        st.subheader("Matter Details")
        selected_matter_status = st.multiselect(
            "Matter Status",
            options=sorted(df['Matter status'].dropna().unique())
        )
        
        billable_matter = st.multiselect(
            "Billable Matter",
            options=sorted(df['Billable matter'].dropna().unique())
        )
        
        selected_billing_methods = st.multiselect(
            "Matter Billing Method",
            options=sorted(df['Matter billing method'].dropna().unique())
        )

    with filter_tabs[4]:  # Financial Filters
        st.subheader("Financial Metrics")
        
        # Safe handling of billed hours value with numeric conversion
        df['Billed hours value'] = pd.to_numeric(df['Billed hours value'], errors='coerce')
        billed_value_max = df['Billed hours value'].fillna(0).max()
        min_amount = st.number_input(
            "Minimum Billable Amount",
            min_value=0.0,
            max_value=float(billed_value_max),
            value=0.0
        )
        
        # Safe handling of user rate range with numeric conversion
        df['User rate'] = pd.to_numeric(df['User rate'], errors='coerce')
        user_rate_min = df['User rate'].fillna(0).min()
        user_rate_max = df['User rate'].fillna(0).max()
        rate_range = st.slider(
            "Hourly Rate Range",
            min_value=float(user_rate_min),
            max_value=float(user_rate_max),
            value=(float(user_rate_min), float(user_rate_max))
        )

    with filter_tabs[5]:  # Client Filters
        st.subheader("Client Information")
        selected_companies = st.multiselect(
            "Company Name",
            options=sorted(df['Company name'].dropna().unique())
        )
        
        selected_clients = st.multiselect(
            "Client Name",
            options=sorted(df['Contact full name (last, first)'].dropna().unique())
        )
        
        selected_matters = st.multiselect(
            "Matter Description",
            options=sorted(df['Matter description'].unique())
        )
        
        # Safe handling of client hours with numeric conversion
        df['Tracked hours'] = pd.to_numeric(df['Tracked hours'], errors='coerce')
        client_hours_max = df.groupby('Matter description')['Tracked hours'].sum().fillna(0).max()
        min_client_hours = st.slider(
            "Minimum Client Hours",
            min_value=0.0,
            max_value=float(client_hours_max),
            value=0.0
        )

    # Display refresh information
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Last Data Refresh:** " + datetime.now().strftime("%B %d, %Y"))
    st.sidebar.markdown("**Data Range:** November 2024 - Present")

    # Return all filter values
    return {
        'year': selected_year,
        'quarter': selected_quarter,
        'months': selected_months,
        'date_range': date_range,
        'attorney_levels': selected_attorney_levels,
        'attorneys': selected_attorneys,
        'originating_attorneys': selected_originating,
        'min_hours': min_hours,
        'practice_areas': selected_practice_areas,
        'locations': selected_locations,
        'matter_status': selected_matter_status,
        'billable_matter': billable_matter,
        'billing_methods': selected_billing_methods,
        'min_amount': min_amount,
        'rate_range': rate_range,
        'companies': selected_companies,
        'clients': selected_clients,
        'matters': selected_matters,
        'min_client_hours': min_client_hours
    }

def filter_data(df, filters):
    """Apply all filters to the dataframe including attorney level filter."""
    filtered_df = df.copy()
    
    # Debug: Print initial state
    print(f"\nInitial dataframe size: {len(filtered_df)}")
    print(f"Initial attorney levels present: {filtered_df['Attorney level'].unique()}")
    
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
    
    # Attorney level filter
    if filters['attorney_levels']:
        filtered_df = filtered_df[filtered_df['Attorney level'].isin(filters['attorney_levels'])]
    
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
    if filters['billable_matter']:
        filtered_df = filtered_df[filtered_df['Billable matter'].isin(filters['billable_matter'])]
    if filters['billing_methods']:
        filtered_df = filtered_df[filtered_df['Matter billing method'].isin(filters['billing_methods'])]
    
    # Financial filters
    if filters['min_amount'] > 0:
        filtered_df = filtered_df[filtered_df['Billed & Unbilled hours value'] >= filters['min_amount']]
    if len(filters['rate_range']) == 2:
        filtered_df = filtered_df[
            (filtered_df['User rate'] >= filters['rate_range'][0]) &
            (filtered_df['User rate'] <= filters['rate_range'][1])
        ]
    
    # Client filters
    if filters['companies']:
        filtered_df = filtered_df[filtered_df['Company name'].isin(filters['companies'])]
    if filters['clients']:
        filtered_df = filtered_df[filtered_df['Contact full name (last, first)'].isin(filters['clients'])]
    if filters['matters']:
        filtered_df = filtered_df[filtered_df['Matter description'].isin(filters['matters'])]
    if filters['min_client_hours'] > 0:
        client_hours = filtered_df.groupby('Matter description')['Tracked hours'].sum()
        valid_clients = client_hours[client_hours >= filters['min_client_hours']].index
        filtered_df = filtered_df[filtered_df['Matter description'].isin(valid_clients)]
    
    return filtered_df

def calculate_filtered_metrics(df):
    """Calculate metrics with proper handling of flat fees."""
    work_df = df.copy()
    
    # Identify flat fee entries (billing method is 'Flat Rate' or special cases)
    flat_fee_mask = (
        (work_df['Matter billing method'] == 'Flat Rate') |
        ((work_df['Billed & Unbilled hours'] <= 1) & (work_df['Billed & Unbilled hours value'] >= 1500)) |
        (work_df['Billed & Unbilled hours'] == 0)
    )
    
    flat_fee_entries = work_df[flat_fee_mask]
    hourly_entries = work_df[~flat_fee_mask]
    
    metrics = {
        'hourly_hours': hourly_entries['Billed & Unbilled hours'].sum(),
        'hourly_amount': hourly_entries['Billed & Unbilled hours value'].sum(),
        'flat_fee_count': len(flat_fee_entries),
        'flat_fee_amount': flat_fee_entries['Billed & Unbilled hours value'].sum(),
        'total_tracked': work_df['Tracked hours'].sum(),
        'total_billed': work_df['Billed hours'].sum(),
        'total_billed_amount': work_df['Billed hours value'].sum(),
        'utilization_rate': (work_df['Billed & Unbilled hours'].sum() / work_df['Tracked hours'].sum() * 100) if work_df['Tracked hours'].sum() > 0 else 0
    }
    
    # Calculate average hourly rate only for hourly entries
    if metrics['hourly_hours'] > 0:
        metrics['average_rate'] = round(metrics['hourly_amount'] / metrics['hourly_hours'], 2)
    else:
        metrics['average_rate'] = 0
    
    return metrics

def display_key_metrics(df):
    """Display key metrics in the dashboard header."""
    metrics = calculate_filtered_metrics(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_billable = metrics['hourly_hours'] + metrics['flat_fee_count']
        total_amount = metrics['hourly_amount'] + metrics['flat_fee_amount']
        st.metric(
            "Total Billable",
            f"{total_billable:,.1f} hrs",
            f"${total_amount:,.2f}"
        )
    
    with col2:
        st.metric(
            "Billed Hours",
            f"{metrics['total_billed']:,.1f}",
            f"${metrics['total_billed_amount']:,.2f}"
        )
    
    with col3:
        st.metric(
            "Utilization Rate",
            f"{metrics['utilization_rate']:.1f}%",
            "of total hours"
        )
    
    with col4:
        if metrics['average_rate'] > 0:
            rate_display = f"${metrics['average_rate']:,.2f}/hr"
            delta = f"{metrics['flat_fee_count']} flat fee matters"
        else:
            rate_display = "Flat fees only"
            delta = f"${metrics['flat_fee_amount']:,.2f} total"
        
        st.metric(
            "Average Rate",
            rate_display,
            delta
        )

def create_hours_distribution(df):
    """Create hours distribution pie chart."""
    hours_data = pd.DataFrame({
        'Category': ['Billable', 'Non-Billable', 'Unbilled'],
        'Hours': [
            df['Billed & Unbilled hours'].sum(),
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
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )
    
    return fig

def create_practice_area_analysis(df):
    """Create practice area analysis chart."""
    practice_data = df.groupby('Practice area').agg({
        'Billed & Unbilled hours': 'sum',
        'Billed & Unbilled hours value': 'sum'
    }).reset_index()
    
    practice_data = practice_data[practice_data['Practice area'].notna()]
    
    fig = px.bar(
        practice_data,
        x='Practice area',
        y=['Billed & Unbilled hours', 'Billed & Unbilled hours value'],
        title='Practice Area Performance',
        barmode='group',
        labels={
            'Billed & Unbilled hours': 'Billable Hours',
            'Billed & Unbilled hours value': 'Revenue ($)',
            'Practice area': 'Practice Area'
        }
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=True
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
def create_client_analysis_charts(df):
    """Create client analysis visualizations."""
    # Top clients by billable hours
    top_clients = df.groupby('Matter description').agg({
        'Billed & Unbilled hours': 'sum',
        'Billed & Unbilled hours value': 'sum'
    }).sort_values('Billed & Unbilled hours', ascending=False).head(10)
    
    fig1 = px.bar(
        top_clients,
        y=top_clients.index,
        x='Billed & Unbilled hours',
        title='Top 10 Clients by Billable Hours',
        orientation='h',
        labels={
            'Billed & Unbilled hours': 'Billable Hours',
            'Matter description': 'Client'
        }
    )
    
    fig1.update_layout(height=500)
    
    # Client hours distribution
    client_hours = df.groupby('Matter description').agg({
        'Billed & Unbilled hours': 'sum',
        'Non-billable hours': 'sum',
        'Unbilled hours': 'sum'
    }).reset_index()
    
    fig2 = px.treemap(
        client_hours,
        path=['Matter description'],
        values='Billed & Unbilled hours',
        title='Client Hours Distribution',
        labels={'Billed & Unbilled hours': 'Billable Hours'}
    )
    
    return fig1, fig2

def create_client_practice_area_chart(df):
    """Create client by practice area analysis."""
    client_practice = df.groupby(['Matter description', 'Practice area']).agg({
        'Billed & Unbilled hours': 'sum'
    }).reset_index()
    
    # Filter out rows where Practice area is null
    client_practice = client_practice[client_practice['Practice area'].notna()]
    
    fig = px.sunburst(
        client_practice,
        path=['Practice area', 'Matter description'],
        values='Billed & Unbilled hours',
        title='Client Distribution by Practice Area'
    )
    
    return fig

def create_attorney_performance(df):
    """Create attorney performance scatter plot."""
    attorney_data = df.groupby('User full name (first, last)').agg({
        'Billed & Unbilled hours': 'sum',
        'Billed hours': 'sum',
        'Billed & Unbilled hours value': 'sum',
        'Tracked hours': 'sum'
    }).reset_index()
    
    # Calculate utilization rate
    attorney_data['Utilization Rate'] = (
        attorney_data['Billed & Unbilled hours'] / attorney_data['Tracked hours'] * 100
    ).round(2)
    
    fig = px.scatter(
        attorney_data,
        x='Billed & Unbilled hours',
        y='Billed & Unbilled hours value',
        size='Utilization Rate',
        hover_name='User full name (first, last)',
        title='Attorney Performance',
        labels={
            'Billed & Unbilled hours': 'Billable Hours',
            'Billed & Unbilled hours value': 'Revenue ($)'
        }
    )
    
    return fig

def create_attorney_utilization_chart(df):
    """Create attorney utilization chart."""
    attorney_util = df.groupby('User full name (first, last)').agg({
        'Billed & Unbilled hours': 'sum',
        'Non-billable hours': 'sum',
        'Tracked hours': 'sum'
    }).reset_index()
    
    attorney_util['Utilization Rate'] = (
        attorney_util['Billed & Unbilled hours'] / attorney_util['Tracked hours'] * 100
    ).round(2)
    
    # Sort by utilization rate
    attorney_util = attorney_util.sort_values('Utilization Rate', ascending=True)
    
    fig = px.bar(
        attorney_util,
        x='Utilization Rate',
        y='User full name (first, last)',
        title='Attorney Utilization Rates',
        orientation='h',
        color='Utilization Rate',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=max(500, len(attorney_util) * 25),
        yaxis_title='Attorney Name',
        xaxis_title='Utilization Rate (%)'
    )
    
    return fig

def create_attorney_level_metrics(df):
    """Create attorney level analysis."""
    level_data = df.groupby('Attorney level').agg({
        'Billed & Unbilled hours': 'sum',
        'Billed & Unbilled hours value': 'sum',
        'Tracked hours': 'sum',
        'User full name (first, last)': 'nunique'
    }).reset_index()
    
    level_data = level_data.rename(columns={
        'User full name (first, last)': 'Number of Attorneys'
    })
    
    # Calculate averages
    level_data['Avg Hours per Attorney'] = (
        level_data['Billed & Unbilled hours'] / level_data['Number of Attorneys']
    ).round(2)
    
    level_data['Avg Revenue per Attorney'] = (
        level_data['Billed & Unbilled hours value'] / level_data['Number of Attorneys']
    ).round(2)
    
    level_data['Utilization Rate'] = (
        level_data['Billed & Unbilled hours'] / level_data['Tracked hours'] * 100
    ).round(2)
    
    return level_data

def create_trending_chart(df):
    """Create trending analysis chart."""
    daily_data = df.groupby('Activity date').agg({
        'Billed & Unbilled hours': 'sum',
        'Billed hours': 'sum',
        'Non-billable hours': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_data['Activity date'],
        y=daily_data['Billed & Unbilled hours'],
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
        yaxis_title='Hours',
        height=500,
        showlegend=True
    )
    
    return fig

def create_client_metrics_table(df):
    """Create detailed client metrics table."""
    client_metrics = df.groupby('Matter description').agg({
        'Billed & Unbilled hours': 'sum',
        'Billed hours': 'sum',
        'Non-billable hours': 'sum',
        'Billed & Unbilled hours value': 'sum',
        'Billed hours value': 'sum',
        'Tracked hours': 'sum',
        'Company name': 'first',
        'Practice area': lambda x: ', '.join(sorted(x.unique())),
        'Matter status': 'first',
        'Matter billing method': 'first'
    }).round(2)
    
    # Calculate additional metrics
    client_metrics['Utilization Rate'] = (
        client_metrics['Billed & Unbilled hours'] / client_metrics['Tracked hours'] * 100
    ).round(2)
    
    client_metrics['Average Rate'] = (
        client_metrics['Billed & Unbilled hours value'] / 
        client_metrics['Billed & Unbilled hours']
    ).round(2)
    
    client_metrics['Realization Rate'] = (
        client_metrics['Billed hours'] / 
        client_metrics['Billed & Unbilled hours'] * 100
    ).round(2)
    
    return client_metrics
    
def main():
    """Main application setup and layout."""
    st.set_page_config(page_title="Legal Dashboard", layout="wide")
    st.title("Scale Management Dashboard")
    
    with st.spinner('Loading data...'):
        df = load_and_process_data()
    
    # Add refresh date to header
    st.markdown(
        f"""
        <div style='text-align: right; color: gray; font-size: 0.8em;'>
        Last Refresh: {datetime.now().strftime("%B %d, %Y")}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if df is not None:
        # Data range info
        date_range = f"{df['Activity date'].min().strftime('%B %d, %Y')} - {df['Activity date'].max().strftime('%B %d, %Y')}"
        st.info(f"Current data covers: {date_range}")
        
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
        
        # Display key metrics
        display_key_metrics(filtered_df)
        
        # Create tabs for different analysis sections
        main_tabs = st.tabs([
            "Overview", 
            "Client Analysis", 
            "Attorney Analysis", 
            "Practice Areas", 
            "Trending"
        ])
        
        with main_tabs[0]:  # Overview Tab
            st.subheader("Overview Dashboard")
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
                    'Billed & Unbilled hours': 'sum',
                    'Non-billable hours': 'sum',
                    'Billed hours': 'sum',
                    'Billed & Unbilled hours value': 'sum',
                    'Billed hours value': 'sum',
                    'Tracked hours': 'sum'
                }).round(2)
                
                # Create a formatted metrics display
                metrics_df = pd.DataFrame({
                    'Metric': [
                        'Total Billable Hours',
                        'Total Non-billable Hours',
                        'Total Billed Hours',
                        'Total Billable Amount',
                        'Total Billed Amount',
                        'Total Tracked Hours'
                    ],
                    'Value': overview_metrics.values
                }, index=overview_metrics.index)
                
                st.dataframe(
                    metrics_df,
                    column_config={
                        "Value": st.column_config.NumberColumn(
                            "Value",
                            format="%.2f"
                        )
                    }
                )
        
        with main_tabs[1]:  # Client Analysis Tab
            st.subheader("Client Analysis")
            
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
            
            # Display the metrics table with formatting
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
                    "Realization Rate": st.column_config.NumberColumn(
                        "Realization Rate",
                        format="%.2f%%"
                    ),
                    "Billed & Unbilled hours value": st.column_config.NumberColumn(
                        "Revenue",
                        format="$%.2f"
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
            st.subheader("Attorney Analysis")
            
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
            
            # Attorney Level Analysis
            st.subheader("Attorney Level Analysis")
            level_metrics = create_attorney_level_metrics(filtered_df)
            
            # Display attorney level metrics
            st.dataframe(
                level_metrics,
                column_config={
                    "Utilization Rate": st.column_config.NumberColumn(
                        "Utilization Rate",
                        format="%.2f%%"
                    ),
                    "Avg Revenue per Attorney": st.column_config.NumberColumn(
                        "Avg Revenue",
                        format="$%.2f"
                    )
                }
            )
            
            # Individual Attorney Metrics Table
            st.subheader("Individual Attorney Metrics")
            attorney_metrics = filtered_df.groupby('User full name (first, last)').agg({
                'Billed & Unbilled hours': 'sum',
                'Non-billable hours': 'sum',
                'Billed hours': 'sum',
                'Billed & Unbilled hours value': 'sum',
                'Tracked hours': 'sum',
                'Attorney level': 'first'
            }).round(2)
            
            # Calculate additional metrics
            attorney_metrics['Utilization Rate'] = (
                attorney_metrics['Billed & Unbilled hours'] / 
                attorney_metrics['Tracked hours'] * 100
            ).round(2)
            
            attorney_metrics['Average Rate'] = (
                attorney_metrics['Billed & Unbilled hours value'] / 
                attorney_metrics['Billed & Unbilled hours']
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
            st.subheader("Practice Area Analysis")
            
            # Practice Area Distribution
            st.plotly_chart(
                create_practice_area_analysis(filtered_df),
                use_container_width=True
            )
            
            # Practice Area Metrics Table
            st.subheader("Practice Area Metrics")
            practice_metrics = filtered_df.groupby('Practice area').agg({
                'Billed & Unbilled hours': 'sum',
                'Non-billable hours': 'sum',
                'Billed hours': 'sum',
                'Billed & Unbilled hours value': 'sum',
                'Billed hours value': 'sum',
                'Matter description': 'nunique'
            }).round(2)
            
            practice_metrics = practice_metrics.rename(columns={
                'Matter description': 'Number of Matters'
            })
            
            st.dataframe(
                practice_metrics,
                column_config={
                    "Billed & Unbilled hours value": st.column_config.NumberColumn(
                        "Revenue",
                        format="$%.2f"
                    )
                }
            )
        
        with main_tabs[4]:  # Trending Tab
            st.subheader("Time Trends")
            
            # Daily trending chart
            st.plotly_chart(
                create_trending_chart(filtered_df),
                use_container_width=True
            )
            
            # Monthly trends
            st.subheader("Monthly Trends")
            monthly_data = filtered_df.groupby([
                pd.Grouper(key='Activity date', freq='M')
            ]).agg({
                'Billed & Unbilled hours': 'sum',
                'Billed hours': 'sum',
                'Non-billable hours': 'sum',
                'Billed & Unbilled hours value': 'sum'
            }).reset_index()
            
            # Create monthly trend chart
            fig = px.line(
                monthly_data,
                x='Activity date',
                y=['Billed & Unbilled hours', 'Billed hours', 'Non-billable hours'],
                title='Monthly Hours Trend',
                labels={
                    'value': 'Hours',
                    'variable': 'Hour Type',
                    'Activity date': 'Month'
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add revenue trend
            revenue_fig = px.line(
                monthly_data,
                x='Activity date',
                y='Billed & Unbilled hours value',
                title='Monthly Revenue Trend',
                labels={
                    'Billed & Unbilled hours value': 'Revenue ($)',
                    'Activity date': 'Month'
                }
            )
            
            st.plotly_chart(revenue_fig, use_container_width=True)

if __name__ == "__main__":
    main()
