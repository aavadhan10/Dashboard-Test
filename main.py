import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
import numpy as np

# Configuration and setup
st.set_page_config(page_title="Legal Dashboard", layout="wide")

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
        
        # Convert numeric columns with robust error handling
        numeric_columns = [
            'Tracked hours',
            'Billed & Unbilled hours',
            'Billed & Unbilled hours value',
            'Billed hours',
            'Billed hours value',
            'Non-billable hours',
            'Non-billable hours value',
            'Unbilled hours',
            'Unbilled hours value',
            'User rate',
            'Utilization rate'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Convert Matter description to string
        df['Matter description'] = df['Matter description'].fillna('').astype(str)
        
        # Add missing columns if they don't exist
        required_columns = [
            'Activity quarter', 'Activity month', 'Originating attorney', 
            'Practice area', 'Matter location', 'Matter status', 
            'Billable matter', 'Matter billing method', 
            'Company name', 'Contact full name (last, first)'
        ]
        for col in required_columns:
            if col not in df.columns:
                df[col] = ''
        
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
        
        # Clean attorney names and add level
        df['User full name (first, last)'] = df['User full name (first, last)'].str.strip()
        df['Attorney level'] = df['User full name (first, last)'].map(attorney_levels).fillna('Unknown')
        
        # Add year column for filtering
        df['year'] = df['Activity date'].dt.year
        
        # Add missing information if not present
        if 'Activity quarter' not in df.columns:
            df['Activity quarter'] = df['Activity date'].dt.quarter.apply(lambda x: f'Q{x}')
        if 'Activity month' not in df.columns:
            df['Activity month'] = df['Activity date'].dt.month_name()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None

def create_sidebar_filters(df):
    """Create comprehensive sidebar filters."""
    st.sidebar.header("Filters")
    
    # Create tabs for filter categories
    filter_tabs = st.sidebar.tabs(["Time", "Attorneys", "Practice", "Matter", "Financial", "Clients"])
    
    with filter_tabs[0]:  # Time Filters
        st.subheader("Time Period")
        
        # Handle year selection
        year_options = sorted(df['year'].unique())
        if len(year_options) > 0:
            selected_year = st.selectbox(
                "Year",
                options=year_options,
                index=len(year_options) - 1
            )
        else:
            selected_year = None
        
        selected_quarter = st.selectbox(
            "Quarter",
            options=sorted(df['Activity quarter'].unique()),
            index=0
        )
        
        selected_months = st.multiselect(
            "Months",
            options=sorted(df['Activity month'].unique())
        )
        
        try:
            min_date = pd.to_datetime(df['Activity date']).min()
            max_date = pd.to_datetime(df['Activity date']).max()
        except:
            min_date = datetime.now()
            max_date = datetime.now()
        
        date_range = st.date_input(
            "Custom Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    with filter_tabs[1]:  # Attorney Filters
        st.subheader("Attorney Information")
        
        attorney_levels = sorted(df['Attorney level'].dropna().unique())
        selected_attorney_levels = st.multiselect(
            "Attorney Levels",
            options=attorney_levels
        )
        
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
        
        tracked_hours_max = df['Tracked hours'].fillna(0).max()
        min_hours = st.slider(
            "Minimum Billable Hours",
            min_value=0.0,
            max_value=float(tracked_hours_max),
            value=0.0,
            step=0.1
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
        
        billed_value_max = df['Billed & Unbilled hours value'].fillna(0).max()
        min_amount = st.number_input(
            "Minimum Billable Amount",
            min_value=0.0,
            max_value=float(billed_value_max),
            value=0.0,
            step=100.0
        )
        
        user_rate_min = df['User rate'].fillna(0).min()
        user_rate_max = df['User rate'].fillna(0).max()
        rate_range = st.slider(
            "Hourly Rate Range",
            min_value=float(user_rate_min),
            max_value=float(user_rate_max),
            value=(float(user_rate_min), float(user_rate_max)),
            step=10.0
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
        
        client_hours_max = df.groupby('Matter description')['Tracked hours'].sum().fillna(0).max()
        min_client_hours = st.slider(
            "Minimum Client Hours",
            min_value=0.0,
            max_value=float(client_hours_max),
            value=0.0,
            step=0.1
        )

    # Display refresh information
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Last Data Refresh:** " + datetime.now().strftime("%B %d, %Y"))
    st.sidebar.markdown("**Data Range:** January 2024 - Present")

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
    """Apply filters to the dataframe."""
    try:
        # Print initial dataframe info for debugging
        st.write(f"Initial dataframe shape: {df.shape}")
        st.write("Initial columns:", df.columns.tolist())
        
        filtered_df = df.copy()
        
        # Debug print for each filter
        st.write("Applied Filters:")
        
        # Time filters
        if filters['year']:
            st.write(f"Year filter: {filters['year']}")
            filtered_df = filtered_df[filtered_df['year'] == filters['year']]
            st.write(f"After year filter: {filtered_df.shape}")
        
        if filters['quarter']:
            st.write(f"Quarter filter: {filters['quarter']}")
            filtered_df = filtered_df[filtered_df['Activity quarter'] == filters['quarter']]
            st.write(f"After quarter filter: {filtered_df.shape}")
        
        if filters['months']:
            st.write(f"Months filter: {filters['months']}")
            filtered_df = filtered_df[filtered_df['Activity month'].isin(filters['months'])]
            st.write(f"After months filter: {filtered_df.shape}")
        
        if len(filters['date_range']) == 2:
            st.write(f"Date range filter: {filters['date_range']}")
            filtered_df = filtered_df[
                (filtered_df['Activity date'].dt.date >= filters['date_range'][0]) &
                (filtered_df['Activity date'].dt.date <= filters['date_range'][1])
            ]
            st.write(f"After date range filter: {filtered_df.shape}")
        
        # Attorney filters
        if filters['attorney_levels']:
            st.write(f"Attorney levels filter: {filters['attorney_levels']}")
            filtered_df = filtered_df[filtered_df['Attorney level'].isin(filters['attorney_levels'])]
            st.write(f"After attorney levels filter: {filtered_df.shape}")
        
        if filters['attorneys']:
            st.write(f"Attorneys filter: {filters['attorneys']}")
            filtered_df = filtered_df[filtered_df['User full name (first, last)'].isin(filters['attorneys'])]
            st.write(f"After attorneys filter: {filtered_df.shape}")
        
        if filters['originating_attorneys']:
            st.write(f"Originating attorneys filter: {filters['originating_attorneys']}")
            filtered_df = filtered_df[filtered_df['Originating attorney'].isin(filters['originating_attorneys'])]
            st.write(f"After originating attorneys filter: {filtered_df.shape}")
        
        # Add similar debug prints for other filter sections...
        
        if len(filtered_df) == 0:
            st.warning("No data available for the selected filters. Please adjust your criteria.")
            st.write("Original dataframe unique values:")
            for col in ['year', 'Activity quarter', 'Activity month', 'Attorney level', 'User full name (first, last)', 'Originating attorney']:
                st.write(f"{col}: {df[col].unique()}")
            return df
            
        return filtered_df
        
    except Exception as e:
        st.error(f"Error applying filters: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return df

def calculate_metrics(df):
    """Calculate key performance metrics."""
    try:
        metrics = {
            'total_hours': df['Tracked hours'].sum(),
            'billable_hours': df['Billed & Unbilled hours'].sum(),
            'billed_hours': df['Billed hours'].sum(),
            'non_billable_hours': df['Non-billable hours'].sum(),
            'total_revenue': df['Billed & Unbilled hours value'].sum(),
            'billed_revenue': df['Billed hours value'].sum(),
            'utilization_rate': (df['Billed & Unbilled hours'].sum() / df['Tracked hours'].sum() * 100) if df['Tracked hours'].sum() > 0 else 0
        }
        
        # Calculate average rate excluding zero hours
        billable_entries = df[df['Billed & Unbilled hours'] > 0]
        if len(billable_entries) > 0:
            metrics['average_rate'] = billable_entries['Billed & Unbilled hours value'].sum() / billable_entries['Billed & Unbilled hours'].sum()
        else:
            metrics['average_rate'] = 0
            
        return metrics
        
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return {
            'total_hours': 0,
            'billable_hours': 0,
            'billed_hours': 0,
            'non_billable_hours': 0,
            'total_revenue': 0,
            'billed_revenue': 0,
            'utilization_rate': 0,
            'average_rate': 0
        }

def display_metrics(metrics):
    """Display key metrics in the dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Billable Hours",
            f"{metrics['billable_hours']:,.1f}",
            f"${metrics['total_revenue']:,.2f}"
        )
    
    with col2:
        st.metric(
            "Billed Hours",
            f"{metrics['billed_hours']:,.1f}",
            f"${metrics['billed_revenue']:,.2f}"
        )
    
    with col3:
        st.metric(
            "Utilization Rate",
            f"{metrics['utilization_rate']:.1f}%",
            "of total hours"
        )
    
    with col4:
        st.metric(
            "Average Rate",
            f"${metrics['average_rate']:.2f}/hr",
            "(billable hours)"
        )

def create_visualizations(df):
    """Create all visualizations for the dashboard."""
    if df.empty:
        st.warning("No data available to create visualizations.")
        return None, None, None
    
    try:
        # Hours Distribution
        hours_data = pd.DataFrame({
            'Category': ['Billable', 'Non-Billable', 'Unbilled'],
            'Hours': [
                df['Billed & Unbilled hours'].sum(),
                df['Non-billable hours'].sum(),
                df['Unbilled hours'].sum()
            ]
        })
        
        fig_hours = px.pie(
            hours_data,
            values='Hours',
            names='Category',
            title='Hours Distribution'
        )
        
        # Practice Area Analysis
        practice_data = df.groupby('Practice area').agg({
            'Billed & Unbilled hours': 'sum',
            'Billed & Unbilled hours value': 'sum'
        }).reset_index()
        
        fig_practice = px.bar(
            practice_data,
            x='Practice area',
            y=['Billed & Unbilled hours', 'Billed & Unbilled hours value'],
            title='Practice Area Performance',
            barmode='group'
        )
        
        # Attorney Performance 
        attorney_data = df.groupby('User full name (first, last)').agg({
            'Billed & Unbilled hours': 'sum',
            'Billed hours': 'sum',
            'Billed & Unbilled hours value': 'sum',
            'Tracked hours': 'sum'
        }).reset_index()
        
        # Safely calculate utilization rate
        attorney_data['Utilization Rate'] = np.where(
            attorney_data['Tracked hours'] > 0,
            (attorney_data['Billed & Unbilled hours'] / attorney_data['Tracked hours'] * 100),
            0
        )
        
        # Prepare data for scatter plot with robust size handling
        attorney_data_clean = attorney_data[
            attorney_data['Billed & Unbilled hours'].notna() & 
            attorney_data['Billed & Unbilled hours value'].notna()
        ].copy()
        
        # Create a safe size column with a default minimum
        min_size = 5
        max_size = 20
        
        # Normalize size, handling potential edge cases
        if len(attorney_data_clean) > 0:
            # Ensure we don't divide by zero or use NaN
            utilization_rates = attorney_data_clean['Utilization Rate'].fillna(0)
            rate_min = utilization_rates.min()
            rate_max = utilization_rates.max()
            
            if rate_max > rate_min:
                attorney_data_clean['marker_size'] = (
                    (utilization_rates - rate_min) / (rate_max - rate_min)
                ) * (max_size - min_size) + min_size
            else:
                # If all rates are the same, use a constant size
                attorney_data_clean['marker_size'] = min_size
        else:
            # If no data, return existing visualizations
            return fig_hours, fig_practice, None
        
        # Ensure marker_size is numeric and has no NaNs
        attorney_data_clean['marker_size'] = attorney_data_clean['marker_size'].fillna(min_size).clip(min_size, max_size)
        
        # Create scatter plot
        fig_attorney = go.Figure(data=go.Scatter(
            x=attorney_data_clean['Billed & Unbilled hours'],
            y=attorney_data_clean['Billed & Unbilled hours value'],
            mode='markers',
            marker=dict(
                size=attorney_data_clean['marker_size'],
                sizemode='area',
                sizeref=2.*max(attorney_data_clean['marker_size'])/(40.**2),
                sizemin=4
            ),
            text=attorney_data_clean['User full name (first, last)'],
            hoverinfo='text+x+y'
        ))
        fig_attorney.update_layout(title='Attorney Performance')
        
        return fig_hours, fig_practice, fig_attorney
        
    except Exception as e:
        st.error(f"Error creating visualizations: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None, None, None
def main():
    st.title("Legal Dashboard")
    
    # Load data
    with st.spinner('Loading data...'):
        df = load_and_process_data()
    
    if df is not None:
        # Add refresh date
        st.markdown(
            f"""
            <div style='text-align: right; color: gray; font-size: 0.8em;'>
            Last Refresh: {datetime.now().strftime("%B %d, %Y")}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Create filters
        filters = create_sidebar_filters(df)
        
        # Apply filters
        filtered_df = filter_data(df, filters)
        
        if not filtered_df.empty:
            # Calculate and display metrics
            metrics = calculate_metrics(filtered_df)
            display_metrics(metrics)
            
            # Create visualizations USING THE FILTERED DATAFRAME
            fig_hours, fig_practice, fig_attorney = create_visualizations(filtered_df)
            
            if fig_hours and fig_practice:
                # Display visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(fig_hours, use_container_width=True)
                
                with col2:
                    st.plotly_chart(fig_practice, use_container_width=True)
                
                if fig_attorney:
                    st.plotly_chart(fig_attorney, use_container_width=True)
        else:
            st.warning("No data available for the selected filters. Please adjust your criteria.")
    else:
        st.error("Error loading data. Please check the data source and try again.")
