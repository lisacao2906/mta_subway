import streamlit as st
import plotly.express as px
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

def plot_growth(): 
    file_path = '1975.csv'
    df = pd.read_csv(file_path)
    #print(df.head())

    if 'year' not in df.columns or 'annual_ridership' not in df.columns:
        print("Error: 'year' or 'ridership' columns are missing.")
        return

    fig = go.Figure()

    # Add line trace for the ridership growth
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['annual_ridership'],
        mode='lines+markers',  # This ensures you have both lines and markers
        line=dict(color='white', width=2),
        marker=dict(size=10, color='white'),
        name='Ridership'
    ))

    # Customize the layout
    fig.update_layout(
        title='NYC MTA Ridership from 1975 to 2023',
        title_font=dict(size=25, color='white'),
        xaxis_title='Year',
        yaxis_title='Ridership',
        xaxis=dict(
            tickmode='array', 
            tickangle=45, 
            tickfont=dict(color='white',size=14),
            showgrid=False,
            gridcolor='white'
        ),
        yaxis=dict(
            tickfont=dict(color='white',size=14),
            showgrid=True,
            gridcolor='white'
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Dark background color
        paper_bgcolor='rgba(0,0,0,0)',  # Paper background color
        font=dict(color='white'),
        showlegend=True
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig)
    #print(df)

def top_10_stations_updated(): 
    file_path = 'top10stations_chacchan.csv'
    # Connect to SQLite (replace with your actual SQLite connection)
    #conn = sqlite3.connect(":memory:")  # In-memory SQLite, or replace with your actual connection

    # Example SQL Query (replace with your actual query)
    #query = "SELECT * FROM sub LIMIT 10"  # Replace with your actual SQL query
    df_results = pd.read_csv(file_path)
    
    fig = px.treemap(
        df_results,
        path=['station'],  # Hierarchical path, you could use additional layers if needed
        values='daily_avg',  # The size of the blocks based on annual ridership
        color='daily_avg',  # Color based on ridership
        color_continuous_scale='Blues',  # Use a color scale, here we use blue like MTA
        title="Top 50 Busiest Subway Stations by Daily Ridership",
        template='plotly_white',  # Clean, professional theme
        labels={'station': 'Station', 'daily_avg': 'Daily Ridership'}  # Label customization
    )

    fig.update_layout(
        height=600,  # Increase the height (in pixels)
        width=1200,  # Increase the width (in pixels)
        title_x=0.5,  # Center title
        title_y=0.95,  # Adjust title position if needed
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent outer paper background
        title={
        'text': "Top 50 Busiest Subway Stations by Daily Ridership",
        'font': {
            'family': 'Helvetica Neue, Helvetica, Arial, sans-serif',  # Correct font-family stack
            'size': 25,
            'color': 'white'
        },
        'x': 0,  # Align title to the left
        'xanchor': 'left',  # Anchor the title to the left
    }

    )

    # Display the treemap in Streamlit
    st.plotly_chart(fig)


    # Optionally, save results to CSV
    csv_file_path = "top10stations.csv"
    df_results.to_csv(csv_file_path, index=False)
    
    # Allow users to download the CSV
    #st.download_button("Download CSV", data=df_results.to_csv(index=False), file_name="top10stations.csv", mime="text/csv")

    #return fig

def top10_stations():
    file_path = 'top10stations_updated_official.csv'
    # Connect to SQLite (replace with your actual SQLite connection)
    conn = sqlite3.connect(":memory:")  # In-memory SQLite, or replace with your actual connection

    # Example SQL Query (replace with your actual query)
    query = "SELECT * FROM sub LIMIT 10"  # Replace with your actual SQL query
    df_results = pd.read_csv(file_path)
    df_results.to_sql('sub', conn, index = False, if_exists = 'replace')
    df_results = pd.read_sql_query(query,conn)
    # Run the SQL query to fetch data
    # Format numeric columns for better readability

    df_results["annual_avg"] = df_results["annual_avg"].replace({',': ''}, regex=True)

    # Convert the 'annual_avg' column to numeric values
    df_results["annual_avg"] = pd.to_numeric(df_results["annual_avg"], errors="coerce")

    # Apply the formatting only after converting to numeric
    df_results["annual_avg"] = df_results["annual_avg"].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "N/A")
    
    df_results["daily_avg"] = df_results["daily_avg"].replace({',': ''}, regex=True)

    # Convert the 'daily_avg' column to numeric values (handling any invalid values)
    df_results["daily_avg"] = pd.to_numeric(df_results["daily_avg"], errors="coerce")
    
    
    df_results["daily_avg"] = df_results["daily_avg"].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "N/A")
    #df_results["annual_avg"] = df_results["annual_avg"].apply(lambda x: f"{x:,.0f}")
    #df_results["daily_avg"] = df_results["daily_avg"].apply(lambda x: f"{x:,.0f}")

    df_results.index = df_results.index + 1
    # Apply NYC MTA Blue & Font Styling
    styled_df = df_results.style.set_table_styles([
        # Header styling
        {"selector": "thead th", "props": [("background-color", "#0039A6"),
                                           ("color", "white"),
                                           ("font-size", "14px"),
                                           ("text-align", "center"),
                                           ("font-weight", "bold"),
                                           ("border", "1px solid white"),
                                           ("padding", "10px"),
                                           ("font-family", "'Helvetica Neue', Helvetica, Arial, sans-serif")]},

        # Body styling
        {"selector": "tbody td", "props": [("border", "1px solid #ddd"),
                                           ("padding", "10px"),
                                           ("font-size", "13px"),
                                           ("color", "#FFFFFF"),
                                           ("text-align", "left"),
                                           ("font-family", "'Helvetica Neue', Helvetica, Arial, sans-serif")]},


        # Index styling to ensure it has white borders
        # {"selector": "thead th:nth-child(1), tbody td:nth-child(1)", "props": [
        #     ("border", "1px solid white")  # Apply white border to index as well
        # ]},

        # Index styling to ensure it has white borders and white text
        {"selector": "thead th:nth-child(1), tbody td:nth-child(1)", "props": [
            ("border", "1px solid white"),  # Apply white border to index as well
            ("color", "white")  # Make the index numbers white
        ]},

        # Alternating row colors for readability
        {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#2A2A2A")]},

        # Hover effect for interactivity
        {"selector": "tbody tr:hover", "props": [("background-color", "#4A4A4A")]},

        {"selector": "caption", "props": [
            ("color", "white"),
            ("font-size", "16px"),
            ("font-weight", "bold"),
            ("text-align", "center"),
            ("padding", "10px")
        ]}

    ]).set_properties(**{"text-align": "left"}).set_caption("🚇 Top 10 Busiest MTA Stations")

    # Display styled DataFrame in Streamlit
    #st.write("### Top 10 Busiest MTA Stations")
    #st.dataframe(df_results)  # You can also use `styled_df.render()` if you'd prefer styled output

    styled_html = styled_df.to_html()

    # Embed the styled HTML table in Streamlit
    #st.write("### Top 10 Busiest MTA Stations")
    #### st.markdown(styled_html, unsafe_allow_html=True) ####
    #st.write("### Top 10 Busiest MTA Stations")
    #st.markdown(styled_html, unsafe_allow_html=True)


    # Optionally, save results to CSV
    csv_file_path = "top10stations.csv"  # Define the path for the CSV file
    df_results.to_csv(csv_file_path, index=False)  # Save the DataFrame as a CSV file

    # Allow users to download the CSV
    #st.download_button("Download CSV", data=df_results.to_csv(index=False), file_name="top10stations.csv", mime="text/csv")
    return styled_html
def plot_ridership_share_by_borough(): 
    file_path = 'ridership_by_borough.csv'
    df = pd.read_csv(file_path)
    
    # rename columns : 
    df.rename(columns = {
        "B": "Brooklyn",
        "Bx": "Bronx",
        "M": "Manhattan",
        "Q": "Queens"
    }, inplace=True)

    # normalize the column names for color mapping
    df.columns = df.columns.str.strip() # remove any leading/ trailing

    #df.index.name = 'Year'
    #df.reset_index(inplace = True)

    # Define the MTA Blue Color
    mta_blue = "#0039A6"
    boro_colors = { 
        "Brooklyn": "#0766AD",
        "Bronx": "#EFB700",
        "Manhattan": "#00933C",
        "Queens": "#DA291C"
    }
    

    fig = go.Figure()

    # Add bars for each borough 

    for boro in df.columns[df.columns != "Year"]: 
        fig.add_trace(go.Bar(
            x = df["Year"],
            y = df[boro],
            name = boro,
            marker = dict(color=boro_colors.get(boro, "#999999"))
        ))

     # Calculate the sum for each year and display it on top of the bars
    df['Total'] = df[df.columns[df.columns != 'Year']].sum(axis=1)  # Total ridership for each year

    # Format sums as comma-separated numbers
    sums = df['Total'].apply(lambda x: f"{int(x):,}")  # Format as comma-separated

    # Add sum labels above the bars
    fig.add_trace(
        go.Scatter(
            x = df["Year"], 
            y = df['Total'] + 0.02 * df['Total'].max(),  # Position the text slightly above the bars
            mode = "text",
            text = sums,
            textposition = "top center",
            showlegend = False
        )
    )

    # Layout styling 
    fig.update_layout(
        title = 'NYC Subway Ridership by Borough (2018 - 2023)',
        xaxis_title = 'Year',
        yaxis_title = 'Annual Ridership',
        template = 'plotly_dark',
        barmode = 'stack',
        yaxis = dict(gridcolor = 'lightgray',tickformat = ',d'),
        xaxis = dict(showgrid = False),
        font = dict(family="NYCT Subway, 'Helvetica Neue', sans-serif", size=14, color="white"),
        title_font=dict(family="NYCT Subway, 'Helvetica Neue', sans-serif", size=20, color="white"),
        legend = dict(title = 'Borough', font = dict(size=15)),
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        margin = dict(l=60, r=40, t=60, b=40)
    )

    # display the chart in streamlit 
    st.plotly_chart(fig)

def display_logo(): 
    #logo_path = 'png-clipart-lionel-nascar-nyc-subway-mta-officially-licensed-limited-edition-logo-1-64-scale-product-twin-towers-memorial-park-blue-text-thumbnail.png'
    #logo_path = 'MTA_New_York_City_Subway_logo.svg.png'
    logo_path = "MTA_NYC_logo.svg.png"
    st.image(logo_path, width=100)

    #col1, col2, col3 = st.columns([1, 6, 1])
    #with col2:
        #st.image(logo_path, use_column_width=True)

def plot_ridership_change():
    """
    Generates a subplot of bar charts showing percent change in ridership for each borough.
    
    Parameters:
        query_df (pd.DataFrame): DataFrame containing columns 'Boro', 'Year', and 'percent_change'.
    """
    # Filter out 2018
    file_path = "ridership_change.csv"
    query_df = pd.read_csv(file_path)
    query_df = query_df[query_df['Year'] != 2018]

    # Create a subplot grid (1 row, 4 columns)
    fig = make_subplots(
        rows=1, 
        cols=4, 
        shared_yaxes=True,  # Shared y-axis for consistency
        subplot_titles=["Brooklyn", "Bronx", "Manhattan", "Queens"],
        column_widths=[0.24, 0.24, 0.24, 0.24]
    )

    # List of boroughs
    boroughs = ['B', 'Bx', 'M', 'Q']

    query_df['percent_change'] = query_df['percent_change'].round(2)

    # Loop through each borough to create a bar chart
    for i, boro in enumerate(boroughs, start=1):
        # Filter data for the current borough
        boro_data = query_df[query_df['Boro'] == boro]

        # Highlight 2020 in red, others in MTA blue
        boro_data['color'] = boro_data['Year'].apply(lambda x: 'red' if x == 2020 else '#0039A6')

        # Add the bar chart
        fig.add_trace(
            go.Bar(
                x=boro_data['Year'],
                y=boro_data['percent_change'],
                marker=dict(color=boro_data['color']),
                text=[f"{val}%" for val in boro_data['percent_change']],  # Add % sign
                textposition='outside',
            ),
            row=1, col=i
        )

    # Ensure all years (2019-2023) are included on the x-axis
    fig.update_xaxes(tickvals=[2019, 2020, 2021, 2022, 2023])

    # Update layout
    # fig.update_layout(
    #     title="Y-o-Y % Change in Ridership Across 4 Boroughs",
    #     height=500,
    #     showlegend=False,
    #     xaxis_title="Year",
    #     yaxis_title="Percent Change (%)",
    #     template='plotly_white',
    #     title_x=0.5,
    #     title_y=0.95,
    #     title_font=dict(
    #         family="NYCT Subway, 'Helvetica Neue', sans-serif",
    #         size=20),
    #     yaxis=dict(tickformat=".0f"),  # Prevent auto-scaling to thousands
    #     margin=dict(t=80, b=40, l=60, r=40)
    # )

    #return fig
    st.plotly_chart(fig)

def plot_commuter_heavy_stations():
    file_path = 'percent_change.csv'
    query_df = pd.read_csv(file_path)

    # Convert percent_change_compared_to_weekday to string with % sign
    query_df["percent_change_compared_to_weekday"] = query_df["percent_change_compared_to_weekday"].astype(str) + "%"

    # Sort by percentage drop (already sorted in the query, but ensuring order)
    query_df = query_df.sort_values(by="percent_change_compared_to_weekday", ascending=True)

    # Create bar chart
    fig = px.bar(
        query_df,
        x="percent_change_compared_to_weekday",
        y="station",
        orientation="h",
        color="percent_change_compared_to_weekday",
        color_continuous_scale=["gray", "red"],  # Gray for small drop, Red for large drop
        labels={"percent_change_compared_to_weekday": "% Change in Ridership", "station": "Station"},
        title="Commuter-Heavy Stations: Weekend Ridership Drop",
        text="percent_change_compared_to_weekday"
    )

    fig.update_traces(textposition="outside")  # Display % drop on bars
    fig.update_layout(xaxis_title="Percent Change Compared to Weekday", yaxis_title="Station", coloraxis_showscale=False)

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_commuter_heavy_stationss():
    file_path = "percent_change.csv"
    query_df = pd.read_csv(file_path)

    # Ensure percentage change is numeric and formatted correctly
    query_df["percent_change_compared_to_weekday"] = query_df["percent_change_compared_to_weekday"].astype(float)
    query_df["percent_change_compared_to_weekday"] = query_df["percent_change_compared_to_weekday"].round(1)

    # Convert to string with % sign for display
    query_df["percent_change_label"] = query_df["percent_change_compared_to_weekday"].astype(str) + "%"

    # Sort by percent change
    query_df = query_df.sort_values(by="percent_change_compared_to_weekday", ascending=True)

    # Create bar chart
    fig = px.bar(
        query_df,
        x="percent_change_compared_to_weekday",
        y="station",
        orientation="h",
        color_discrete_sequence=["#0039A6"],  # MTA Blue
        labels={"percent_change_compared_to_weekday": "% Change in Ridership", "station": "Station"},
        title="Commuter-Heavy Stations: Weekend Ridership Drop",
        text="percent_change_label"
    )

    # Improve label positioning & readability
    fig.update_traces(
        textposition="outside",
        textfont_size=14,  # Increase font size for better readability
        cliponaxis=False  # Ensures large values like "72%" are visible
    )

    # Adjust layout for better spacing
    fig.update_layout(
        xaxis_title="Percent Change Compared to Weekday", 
        yaxis_title="Station",
        showlegend=False,  # Remove legend
        margin=dict(l=150, r=30, t=50, b=50)  # Extra space for long station names
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def weekend_stations():
    file_path = "weekend_stations.csv"
    query_df = pd.read_csv(file_path)
    # Ensure percentage change is numeric and formatted correctly
    query_df["percent_change_compared_to_weekday"] = query_df["percent_change_compared_to_weekday"].astype(float)
    query_df["percent_change_compared_to_weekday"] = query_df["percent_change_compared_to_weekday"].round(1)

    # Convert to string with % sign for display
    query_df["percent_change_label"] = query_df["percent_change_compared_to_weekday"].astype(str) + "%"

    # Sort by percent change (highest surge first)
    query_df = query_df.sort_values(by="percent_change_compared_to_weekday", ascending=False)

    # Create bar chart
    fig = px.bar(
        query_df,
        x="percent_change_compared_to_weekday",
        y="station",
        orientation="h",
        color_discrete_sequence=["#0039A6"],  # MTA Blue
        labels={"percent_change_compared_to_weekday": "% Change in Ridership", "station": "Station"},
        title="Stations with Weekend Ridership Surges",
        text="percent_change_label"
    )

    # Improve label positioning & readability
    fig.update_traces(
        textposition="outside",
        textfont_size=14,  # Increase font size for better readability
        cliponaxis=False  # Ensures large values like "152%" are visible
    )

    # Adjust layout for better spacing
    fig.update_layout(
        xaxis_title="Percent Change Compared to Weekday", 
        yaxis_title="Station",
        showlegend=False,  # Remove legend
        margin=dict(l=200, r=30, t=50, b=50)  # Extra space for long station names
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def box_plot():
    # file_path = "annual_df.csv"
    # annual_df = pd.read_csv(file_path)
    # plt.figure(figsize=(10, 6))  # Set the figure size

    # # Create the boxplot
    # sns.boxplot(x='num_services', y='annual_ridership', data=annual_df, palette='Blues')

    # # Set the title and labels
    # plt.title('Annual Ridership Distribution by Number of Services', fontsize=16, fontweight='bold', family='Arial')
    # plt.xlabel('Number of Services', fontsize=12, family='Arial')
    # plt.ylabel('Annual Ridership', fontsize=12, family='Arial')

    # # Show the plot in the Streamlit app
    # st.pyplot(plt)

    file_path = "annual_df.csv"
    annual_df = pd.read_csv(file_path)

    # Create the boxplot using Plotly
    fig = go.Figure()

    fig.add_trace(go.Box(
        x=annual_df['num_services'],
        y=annual_df['annual_ridership'],
        marker=dict(color='#0039A6'),  # MTA blue color for consistency
        line=dict(color='#0039A6'),  # MTA blue for the box line
        fillcolor='rgba(0, 57, 166, 0.3)',  # Lighter fill color to match MTA theme
        name='Annual Ridership',
        whiskerwidth=0.5,  # Adjust whisker width to be between 0 and 1
        boxmean='sd',  # Show the standard deviation
    ))

    # Update layout to match the professional theme
    fig.update_layout(
        title='Annual Ridership Distribution by Number of Services',
        title_font=dict(family="Arial", size=25, color='white', weight='bold'),  # 'weight' for bold
        xaxis_title='Number of Services',
        yaxis_title='Annual Ridership',
        font=dict(family="Arial", size=12, color='white'),
        template='plotly_white',  # Use a clean and modern white background
        margin=dict(t=80, b=40, l=60, r=40),
    )

    # Show the plot in the Streamlit app
    st.plotly_chart(fig)

def display_info_box(number, description):
    st.markdown(
        f"""
        <style>
        .info-box {{
            background-color: #0039A6;
            color: white;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            width: 100%;
            margin: 10px auto;
        }}
        .info-box h1 {{
            font-size: 40px;
            font-weight: bold;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        }}
        .info-box .description {{
            font-size: 20px;
            margin-top: 10px;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        }}
        .info-box .small-text {{
            font-size: 14px;
            margin-top: 5px;
            color: #B0B0B0;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        }}
        </style>
        <div class="info-box">
            <h1>{number}</h1>
            <div class="description">{description}</div>
        </div>
        """, unsafe_allow_html=True
    )

def modify_top10(): 
    file_path = "top10stations_updated_official.csv"
    # trim the station name 
    df = pd.read_csv(file_path)

    df['station'] = df['station'].str.split('(').str[0]

    # convert annual and daily avg into numeric 

    # remove the commas and space in annual_avg
    #df['annual_avg'] = df['annual_avg'].str.replace(',', '').str.replace(' ', '').astype(float)
    #df['annual_avg'] = pd.to_numeric(df['annual_avg'], errors = 'coerce')
    df['annual_avg'] = pd.to_numeric(df['annual_avg'].str.replace(',', '').str.replace(' ', ''), errors='coerce')
    #df['daily_avg'] = df['daily_avg'].str.replace(',', '').str.replace(' ', '').astype(float)
    #df['daily_avg'] = pd.to_numeric(df['daily_avg'], errors = 'coerce')
    df['daily_avg'] = pd.to_numeric(df['daily_avg'].str.replace(',', '').str.replace(' ', ''), errors='coerce')

    with open("new_top10.csv", "w") as file: 
        df.to_csv(file, index=False)


    print(df.head())


def cv_plot(): 
    file_path = "query_df.csv"
    query_df = pd.read_csv(file_path)

    college_data = query_df[query_df['college_station'] == 'Yes']['cv_monthly']
    non_college_data = query_df[query_df['college_station'] == 'No']['cv_monthly']

    # Perform the t-test
    t_stat, p_value = stats.ttest_ind(college_data, non_college_data)

    # Check significance
    alpha = 0.05
    significance = "Reject H₀: University-adjacent stations have significantly higher ridership variability." if p_value < alpha else "Fail to reject H₀: No significant difference in ridership variability."

    # Create a strip plot in Plotly
    fig = px.strip(query_df, 
               x='college_station', 
               y='cv_monthly', 
               color='college_station', 
               color_discrete_map={'Yes': '#0039A6', 'No': 'red'},
               category_orders={'college_station': ['Yes', 'No']},  # Make sure 'Yes' and 'No' are in the right order
               title="Comparison of Ridership Variability (CV) by Station Type",
               labels={"college_station": "Is a college station", "cv_monthly": "Coefficient of Variation (CV)"})

    # Update layout to add jitter
    fig.update_traces(jitter=0.5, marker=dict(size=8, opacity=0.6, line=dict(width=1, color='black')))

    # Update layout for dark background and white text
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        font=dict(color='white'),  # White text
        title_font=dict(color='white'),  # White title font
        xaxis=dict(title_font=dict(color='white'), tickfont=dict(color='white')),
        yaxis=dict(title_font=dict(color='white'), tickfont=dict(color='white'))
    )

    # Add annotation for t-statistic and p-value
    fig.add_annotation(
        x=0.5,  # Position horizontally (centered between the boxes)
        y=1.1,  # Position vertically (above the plot)
        text=f"T-Statistic: {t_stat:.4f}<br>P-Value: {p_value:.4f}<br>{significance}",
        showarrow=False,
        font=dict(size=14, color='white'),
        align='center',
        bgcolor='rgba(0, 0, 0, 0.7)'  # Semi-transparent background for annotation
    )

    # Show the plot
    st.plotly_chart(fig)


def plot_seasonality(filepath):
    # Assuming decomposition_df is already created with seasonal data

    #file_path = "nyu_decomposition_df.csv"
    decomposition_df = pd.read_csv(filepath)
    seasonality = decomposition_df['seasonal']
    # Ensure the 'date' column is in datetime format
    decomposition_df['date'] = pd.to_datetime(decomposition_df['date'])
    # Create a Plotly line plot for the seasonality
    fig = px.line(decomposition_df, 
                  x='date', 
                  y='seasonal', 
                  title="Seasonality of Ridership",
                  labels={"date": "Date", "seasonal": "Seasonal Component (Ridership)"})

    decomposition_df['year'] = decomposition_df['date'].dt.year
    decomposition_df['month'] = decomposition_df['date'].dt.month


    lowest_months = decomposition_df.groupby(['month']).agg(
        avg_seasonal_value=('seasonal', 'mean')
    ).reset_index()

    # Sort to get the three months with the lowest average seasonal values
    lowest_months = lowest_months.sort_values(by='avg_seasonal_value').head(3)

    # Filter the original dataframe for the rows corresponding to these months
    highlight_data = decomposition_df[decomposition_df['month'].isin(lowest_months['month'])]

    # Add red dots for the highlighted months
    fig.add_trace(go.Scatter(
        x=highlight_data['date'], 
        y=highlight_data['seasonal'], 
        mode='markers', 
        marker=dict(color='red', size=8, symbol='circle'), 
        name='Lowest 3 Recurring Months'
    ))


    # min_seasonal_value = decomposition_df['seasonal'].min()
    # lowest_months = decomposition_df[decomposition_df['seasonal'] == min_seasonal_value]

    # recurring_lowest_months = lowest_months.groupby('year').agg(
    #     lowest_month=('month', 'first'),
    #     lowest_seasonal_value=('seasonal', 'first')
    # ).reset_index()

    # highlight_data = pd.merge(decomposition_df, recurring_lowest_months, 
    #                           left_on=['year', 'month'], 
    #                           right_on=['year', 'lowest_month'], 
    #                           how='inner')

    # fig.add_trace(go.Scatter(
    #     x=highlight_data['date'], 
    #     y=highlight_data['seasonal'], 
    #     mode='markers', 
    #     marker=dict(color='red', size=8, symbol='circle'), 
    #     name='Lowest Months'
    # ))
    
    # Highlight recurring months like January, February, and June with red dots
    # highlight_months = ['2021-01-31', '2021-02-28', '2021-06-30',  # Example years and months
    #                     '2022-01-31', '2022-02-28', '2022-06-30',
    #                     '2023-01-31', '2023-02-28', '2023-06-30',
    #                     '2024-01-31', '2024-02-29', '2024-06-30']

    # highlight_months = pd.to_datetime(highlight_months)
    # highlight_data = decomposition_df[decomposition_df['date'].isin(pd.to_datetime(highlight_months))]

    # Add red dots for the highlighted months
    # fig.add_trace(go.Scatter(
    #     x=highlight_data['date'], 
    #     y=highlight_data['seasonal'], 
    #     mode='markers', 
    #     marker=dict(color='red', size=8, symbol='circle'), 
    #     name='Jan, Feb, June'
    # ))

    # Update layout for dark theme and transparent background
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        font=dict(color='white'),  # White text
        title=dict(font=dict(color='white')),  # White title
        xaxis_title=dict(font=dict(color='white')),
        yaxis_title=dict(font=dict(color='white')),
    )

    # Show the plot in the Streamlit app
    st.plotly_chart(fig)

def plot_ridership_resource_utilization():

    file_path = "nyu_avg_monthly.csv"
    month_year_query_df = pd.read_csv(file_path)
    # Convert year_month to integer for proper sorting and plotting
    month_year_query_df['month'] = month_year_query_df['year_month'].astype(int)

    # Create a color column for highlighting
    month_year_query_df['bar_color'] = month_year_query_df['month'].apply(lambda x: 'red' if x in [1, 2, 6] else 'lightblue')

    # Find the busiest month based on highest avg_monthly_ridership
    busiest_month = month_year_query_df.loc[month_year_query_df['avg_monthly_ridership'].idxmax()]

    # Create the figure
    fig = go.Figure()

    # Add the avg_monthly_ridership trace (bar chart)
    fig.add_trace(go.Bar(
        x=month_year_query_df['month'], 
        #y=month_year_query_df['negative_percentage_drop'],
        y=month_year_query_df['avg_monthly_ridership'], 
        name='Average Monthly Ridership', 
        marker_color=month_year_query_df['bar_color'],
        yaxis='y' # Use the second y-axis for avg_monthly_ridership
    ))

    # Add the resource_utilization as text on the bars for highlighted months (on top)
    for i, row in month_year_query_df.iterrows():
        if row['month'] in [1, 2, 6]:  # Only highlight months 1, 2, and 6
            fig.add_trace(go.Scatter(
                x=[row['month']], 
                y=[row['avg_monthly_ridership'] + 50],  # Position above the bar
                #mode='text', 
                #text=[f"{row['negative_percentage_drop']:.2f}% from businest month"],
                #text=[f"{row['resource_utilization']:.2f}%"], 
                #textposition='bottom center',
                showlegend=False,
                textfont=dict(color='white')  # White text for contrast with dark background
            ))

    # Add a horizontal dashed line at the level of the busiest month (max avg_monthly_ridership)
    fig.add_trace(go.Scatter(
        x=[min(month_year_query_df['month']), max(month_year_query_df['month'])],  # Full x-axis range
        y=[busiest_month['avg_monthly_ridership'], busiest_month['avg_monthly_ridership']],  # Constant y value for the max month
        mode='lines',
        line=dict(color='white', dash='dash'),
        name="Busiest Month",
        showlegend=True,
        yaxis='y'  # Ensure the line uses the second y-axis for avg_monthly_ridership
    ))

    # Update the layout for dual y-axes and dark theme
    fig.update_layout(
        title='Avg Monthly Ridership & Resource Utilization',
        xaxis_title='Month',
        xaxis=dict(
            tickmode='array', 
            tickvals=list(range(1, 13)),  # Ensure all months (1 to 12) are displayed
            ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']  # Labels for months 1 to 12
        ),
        yaxis_title='Average Monthly Ridership',  # Y-axis for resource_utilization
        yaxis=dict(
        title='Average Monthly Ridership',
        range=[month_year_query_df['avg_monthly_ridership'].min(), month_year_query_df['avg_monthly_ridership'].max()]  # Set range based on the data
        ),
        #yaxis=dict(range=[0, 100]),  # Set the range for resource utilization
        # yaxis2=dict(
        #     title='Avg Monthly Ridership',
        #     overlaying='y',
        #     side='right'
        # ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        font=dict(color='white'),  # White text for contrast with dark background
        showlegend=True
    )

    # Show the plot
    st.plotly_chart(fig)
    


def plot_ridership_resource_utilization_testing(): 

    file_path = "nyu_avg_monthly.csv"
    month_year_query_df = pd.read_csv(file_path)
    # Convert year_month to integer for proper sorting and plotting
    month_year_query_df['month'] = month_year_query_df['year_month'].astype(int)

    # Create a color column for highlighting
    month_year_query_df['bar_color'] = month_year_query_df['month'].apply(lambda x: 'red' if x in [1, 2, 6] else 'lightblue')

    # Find the busiest month based on highest avg_monthly_ridership
    busiest_month = month_year_query_df.loc[month_year_query_df['avg_monthly_ridership'].idxmax()]

    # Create the figure
    fig = go.Figure()

    # Add the avg_monthly_ridership trace (bar chart)
    fig.add_trace(go.Bar(
        x=month_year_query_df['month'], 
        y=month_year_query_df['avg_monthly_ridership'], 
        name='Avg Monthly Ridership', 
        marker_color=month_year_query_df['bar_color'],
        yaxis='y2'  # Use the second y-axis for avg_monthly_ridership
    ))

    # Add the resource_utilization as text on the bars for highlighted months (on top)
    for i, row in month_year_query_df.iterrows():
        if row['month'] in [1, 2, 6]:  # Only highlight months 1, 2, and 6
            fig.add_trace(go.Scatter(
                x=[row['month']], 
                y=[row['avg_monthly_ridership'] + 50],  # Position above the bar
                mode='text', 
                text=[f"{row['negative_percentage_drop']:.2f}%"],
                #text=[f"{row['resource_utilization']:.2f}%"], 
                textposition='bottom center',
                showlegend=False,
                textfont=dict(color='red', size=14)  # Red text for resource utilization
            ))

    # Add a horizontal dashed line at the level of the busiest month (max avg_monthly_ridership)
    fig.add_trace(go.Scatter(
        x=[min(month_year_query_df['month']), max(month_year_query_df['month'])],  # Full x-axis range
        y=[busiest_month['avg_monthly_ridership'], busiest_month['avg_monthly_ridership']],  # Constant y value for the max month
        mode='lines',
        line=dict(color='white', dash='dash'),
        name="100% Resource Utilized - Busiest Month",
        showlegend=True,
        yaxis='y2'  # Ensure the line uses the second y-axis for avg_monthly_ridership
    ))

    # Update the layout for dual y-axes and dark theme
    fig.update_layout(
        title='Avg Monthly Ridership & Resource Utilization',
        xaxis_title='Month',
        xaxis=dict(
            tickmode='array', 
            tickvals=list(range(1, 13)),  # Ensure all months (1 to 12) are displayed
            ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']  # Labels for months 1 to 12
        ),
        yaxis_title='Resource Utilization (%)',  # Y-axis for resource_utilization
        yaxis=dict(range=[0, 100]),  # Set the range for resource utilization
        yaxis2=dict(
            title='Avg Monthly Ridership',
            overlaying='y',
            side='right'
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        font=dict(color='white'),  # White text for contrast with dark background
        showlegend=True
    )

    # Show the plot
    st.plotly_chart(fig)

def plot_month_vs_ridership(filepath): 
    #file_path = "nyu_avg_monthly.csv"
    df = pd.read_csv(filepath)

    df_sorted = df.sort_values(by='avg_monthly_ridership').reset_index(drop=True)
    lowest_months = df_sorted.head(3)

    #colors = ['lightblue'] * len(df)
    colors = ['#0039A6'] * len(df)

    # for idx in lowest_months.index:
    #     colors[idx] = 'red'
    for month in lowest_months['year_month']:
        colors[df[df['year_month'] == month].index[0]] = 'red'

    fig = go.Figure()

    # Add bars for all months with the correct color for each
    fig.add_trace(go.Bar(
        x=df['year_month'],
        y=df['avg_monthly_ridership'],
        name='Monthly Ridership',
        marker=dict(color=colors)
    ))

    # fig = px.bar(df, x='year_month', y='avg_monthly_ridership', 
    #          labels={'year_month': 'Year-Month', 'avg_monthly_ridership': 'Average Monthly Ridership'},
    #          title='Monthly Ridership')

    # for index, row in lowest_months.iterrows():
    #     fig.add_trace(go.Bar(
    #         x=[row['year_month']],
    #         y=[row['avg_monthly_ridership']],
    #         name='Lowest Months',
    #         marker=dict(color='red')
    #     ))
    
    fig.add_trace(go.Scatter(
    x=df['year_month'],
    y=df['avg_monthly_ridership'],
    mode='lines+markers',
    name='Fluctuation Line',
    line=dict(color='white', width=2),
    marker=dict(color='white', size=8)
    ))



    # Customize the layout for transparent background and white text
    fig.update_layout(
        title= "Average Monthly Ridership",
        xaxis_title = "Month",
        yaxis_title = "Average Monthly Ridership",
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        font=dict(color='white'),  # White text for contrast
        title_font=dict(color='white', size=20),  # White title
        xaxis_title_font=dict(color='white'),
        yaxis_title_font=dict(color='white')
    )

    # Display the graph in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

def plot_percentage_change_from_max(filepath):
    #file_path = "nyu_avg_monthly.csv"
    df = pd.read_csv(filepath)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['year_month'],
        y=df['resource_utilization'],
        marker=dict(color='#0039A6'),  # NYC MTA Blue
        text=df['resource_utilization'].apply(lambda x: f"{x:.1f}%"),  # Percentage labels
        textposition='outside'
    ))

    # Add Reference Line at 100% Utilization
    fig.add_hline(y=100, line=dict(color="white", dash="dash"), name="Full Capacity")

    # Customize layout
    fig.update_layout(
        title='Monthly Resource Utilization Rate',
        xaxis_title='Month',
        yaxis_title='Resources Utilization Rate (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font=dict(size=20, color='white'),
        xaxis=dict(showgrid=False, title_font=dict(color='white')),
        yaxis=dict(showgrid=False, title_font=dict(color='white')),
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)
        



def low_months(): 
    file_path = "nyu_avg_monthly.csv"
    month_year_query_df = pd.read_csv(file_path)

    # identify 3 months with the lowest resource_utilization
    # Sort the DataFrame by resource_utilization in ascending order and select the first 3 rows
    lowest_resource_utilization_months = month_year_query_df.sort_values(by='resource_utilization').head(3)

    # Display the months with the lowest resource_utilization
    print(lowest_resource_utilization_months[['year_month', 'resource_utilization']])

    general_recommendation = "Consider reviewing service levels across all months to optimize resource allocation."

    # Add the recommendations column to the DataFrame
    month_year_query_df['Recommendations'] = general_recommendation

    # Display the table in Streamlit
    st.table(month_year_query_df)
    #print(month_year_query_df)
        

        

    #low_months()


if "interpretation_open" not in st.session_state:
    st.session_state["interpretation_open"] = False

# Custom CSS to force MTA Blue and Helvetica Neue font

st.set_page_config(layout = "wide")
st.markdown(
    """
    <style>

    .custom-text { 
        font-family: 'Helvetica Neue', sans-serif !important;
        font-size: 25px !important;
        color: white !important;
    }

    .stToggle label {
            font-family: 'NYCT Subway', 'Helvetica Neue', sans-serif !important;
            font-size: 25px;
            font-weight: bold;
            background-color: #0039A6;
            color: white;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }

    .slide-box {
            background-color: rgba(0, 0, 0, 0.6); /* Transparent dark background */
            color: white;
            font-family: 'NYCT Subway', 'Helvetica Neue', sans-serif;
            padding: 15px;
            border: 1px solid #B0B0B0; /* Light gray border */
            border-radius: 10px;
            text-align: center;
            width: 100%;
        }

    .toggle-button label {
            background-color: #0039A6; /* MTA Blue */
            color: white;
            font-family: 'NYCT Subway', 'Helvetica Neue', sans-serif !important;
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 30px !important;
            margin-bottom: 10px;
        }

    .toggle-button:hover {
            background-color: #002f87; /* Darker MTA Blue */
        }

    /* Apply MTA Subway font and style to the title */
    .mta-title { 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: bold; 
        font-size: 100px;
        color: #FFFFFF !important;
        text-align: left;
        margin-top: 30px !important;
    } 
    .mta-header { 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: bold;
        font-size: 30px;
        color: white !important; 
        text-align: left; 
        padding: 10px;
        background-color: #0039A6;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .mta-subheader { 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important; 
        font-weight: bold !important; 
        font-size: 10px !important;
        color: #FFFFFF !important; 
    }

    /* Set the body to take up 100% of the height and width */
    body, .main {
        margin: 0;
        padding: 0;
        width: 100vw;  /* Full width of the viewport */
        height: 100vh;  /* Full height of the viewport */
        overflow-x: hidden;  /* Prevent horizontal scroll */
        display: flex;
        flex-direction: column;
    }

    /* Apply MTA Blue to the title */
    .css-1v3fvcr {
        background-color: #0039A6;
        color: white;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: bold;
    }
    /* Apply MTA Blue to the sidebar */
    .css-1d391kg {
        background-color: #0039A6;
        color: white;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }
    /* Change font for the title of the tabs */
    .stRadio label {
        color: white;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-weight: bold;
    }
    /* Apply MTA Blue to the header */
    .stHeader {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: white;
        background-color: #0039A6;
    }
    /* Apply font-family and color to all markdown elements */
    .stMarkdown, .stPlotlyChart, .stSubheader, .stText {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #333 !important;
    }
    /* Apply white font color to subheaders and other text */
    .stSubheader {
        color: #0039A6 !important;
    }
    /* Add hover effect to sidebar options */
    .css-1d391kg label:hover {
        background-color: #002C74;
    }
    /* Sticky header styles for the MTA logo */
    .header { 
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        background-color: #0039A6; 
        width: 100%; 
        z-index: 1000;
        text-align: center;
    }
    .header img {
        width: 100%; 
        max-width: 100%;
        height: auto;
        object-fit: contain;
    }
    </style>
    """, unsafe_allow_html=True
)

# Title with MTA Blue
#display_logo()

col1, col2 = st.columns([1,10])  # Adjust ratio for spacing

with col1:
    st.markdown('<div class="header">', unsafe_allow_html=True)# Show MTA logo
    display_logo()
    st.markdown('</div>', unsafe_allow_html=True) # end sticky header

with col2:
    #st.markdown('<h1 class= "mta-title">Insights Dashboard</h1>', unsafe_allow_html=True)
    #st.write("This is where your content goes below the sticky header.")
    st.markdown('<h1 class="mta-title">Insights Dashboard</h1>', unsafe_allow_html=True)

#with col2:
    #st.markdown("<h1 style='margin-top:10px;'>NYC Subway Ridership Dashboard</h1>", unsafe_allow_html=True)
#st.title("MTA Insights Dashboard")

# Sidebar Navigation
tabs = ["General", "Recommendations to MTA Management"]
selected_tab = st.sidebar.radio("Choose a Tab", tabs)

if selected_tab == "General":
    #st.markdown('<h2 class="mta-subtitle"> By: Lisa C. </h2>', unsafe_allow_html = True)
    st.markdown('<h3 class ="custom-text"> Transporting millions of people everyday, the NYC MTA system is an essential part of every New Yorker\'s life, though not many knows too well about this incredible system. This dashboard, leveraging data, tells the story about this incredible system, from its early days, to the low points during the COVID-19 Pandemic, to many insights and actionable recommendations that not only would fascinate the viewers but also prove helpful for MTA Management in improving the efficiency of the subway system.</h3>', unsafe_allow_html=True)
    #st.markdown('<h3 class="custom-text">Transporting millions of people everyday, the NYC MTA system is an essential part of every New Yorker\'s life, though not many knows too well about</p>', unsafe_allow_html=True)
    # st.markdown('h3 class = "custom-text">)
    #st.subheader("By: Lisa Cao")
    #st.subheader("General Ridership Overview")

    # Section 1: Top 10 Stations 
    # st.markdown(
    #     """
    #     <div style="background-color: #0039A6; color: white; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; padding: 10px, font-size: 30px; font-weight: bold">
    #         Top 10 Stations 
    #     </div>
    #     """, unsafe_allow_html=True
    # )

    st.markdown('<div class="mta-header">Performance Overview</div>', unsafe_allow_html=True)
    
    # Table displaying top 10 subway stations

    col1, col2 = st.columns([3,1], gap = "small") # 3 parts for the table, 1 part for the box
    
    with col1: 
        plot_growth()
        toggle_plot_growth = st.toggle("💡 Why did ridership take off since late 90s?", value = False)

        if toggle_plot_growth: 
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇 Why did ridership take off since the late 90s? </h3>
                    <p style="text-align: left;">This data traces back to 1975, when ridership was hovering below the 1 Billion mark for about more than 2 decades long. But in 1998, ridership decided to take off. From 1998 up until the point of COVID-19, ridership enjoyed continuous growth.
                    <br> 
                    <br>
                    But why did ridership suddenly take off in 1998 and continue to grow into the 2000s (despite being stagnant for so long in the 70s,80s, and early 90s)? The late 1990s - 2000s tech boom is one amongst key factors. 
                    The rise of internet-based companies and expansion of the tech industry in the US means there was an influx of today’s tech giants flocking to NYC, the city where many leading companies have offices in. More companies open offices in NYC mean more workers are employed in NYC. Nowadays, when walking on the streets of New York, it is not hard to spot people who work in Tech. Takeaway? The growth in the tech industry had benefitted the NYC MTA System!
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )
        # add toggle 

        #styled_table_html = top_10_stations_updated()
        #st.markdown(styled_table_html, unsafe_allow_html = True)
        #st.download_button("Download CSV", data=df_results.to_csv(index=False), file_name="top10stations.csv", mime="text/csv")

    with col2: 
        display_info_box("#1", "Public Transit in North America")
        display_info_box("1904", "Year of Establishment")
        display_info_box("3,600,000", "Daily rides")
        #display_info_box("24/7", "hours of operation")
        #display_info_box("1904", "Established since")

    #plot_growth()
    styled_table_html = top_10_stations_updated()
        

    #top10_stations()
    
    #display_info_box("428", "stations as of 2023")
    # DELAY THIS : plot_commuter_heavy_stationss()

    # DELAY THIS: weekend_stations()

    # DELAY THIS: box_plot()

    # Section 2: Ridership by Boroughs 
    # st.markdown(
    #     """
    #     <div style="background-color: #0039A6; color: white; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; padding: 10px, font-size: 30px; font-weight: bold">
    #         Ridership by Boroughs
    #     </div>
    #     """, unsafe_allow_html=True
    # )

    # Table displaying MTA Ridership Growth by Borough
    
    st.markdown('<div class="mta-header"> Explore NYC Boroughs </div>', unsafe_allow_html=True)
    #col1, col2 = st.columns([5, 2])

    #st.markdown('<div class="mta-header"> Explore NYC Boroughs </div>', unsafe_allow_html=True)
    plot_ridership_share_by_borough()  # Displays graph


    # Create toggle (selectbox or radiobutton) with unique keys: 

            
    show_interpretation = st.toggle("💡 What does share of ridership by borough tell us?", value = False)

    if show_interpretation: 
        st.markdown(
            """
            <div class="slide-box">
                <h3 style="text-align: left;">🚇 What does share of ridership by borough tell us? </h3>
                <p style="text-align: left;">This graph shows each borough's share of ridership over the years. 
                <br>
                #1. In 2020 (COVID-19 Pandemic), ridership dropped by ~1 Billion, a 62.5% reduction compared to 2019. 
                <br>
                #2. Post COVID-19, ridership steadily increases but unfortunately has yet to recover to pre-pandemic levels. As of 2023, we were still down by ~32% compared to 2019. 
                <br>
                #3. Manhattan (unsurprisingly) consistently maintains the highest share of ridership over the years, with Brooklyn the runner-up, Queens the third place, and Bronx last.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )



    
    # # Toggle button for interpretation
    #     if st.button(
    #         "🔍 Interpret the Graph" if not st.session_state["interpretation_open"] else "❌ Close Interpretation"
    #     ):
    #         st.session_state["interpretation_open"] = not st.session_state["interpretation_open"]
    #     if st.session_state["interpretation_open"]: 
    #         st.markdown(
    #         """
    #         <div class="slide-box">
    #             <h3>🚇 Interpretation</h3>
    #             <p>Over the years, Manhattan consistently maintains the highest ridership, 
    #             while the Bronx and Queens show steady growth. The ridership share reflects 
    #             population density and economic activity, influencing MTA's resource allocation.</p>
    #         </div>
    #         """,
    #         unsafe_allow_html=True
    #     )

        #toggle = st.button("💡 Interpret the Graph")

    #if toggle:
        # st.markdown(
        #     """
        #     <div class="slide-box">
        #         <h3>🚇 Interpretation</h3>
        #         <p>Over the years, Manhattan consistently maintains the highest ridership, 
        #         while the Bronx and Queens show steady growth. The ridership share reflects 
        #         population density and economic activity, influencing MTA's resource allocation.</p>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )


    #plot_ridership_share_by_borough()

    st.markdown(
    """
    <h2 style="text-align: left; font-family: 'NYCT Subway', 'Helvetica Neue', sans-serif; color: white; font-size: 20px; margin-top: 0px; margin-bottom: 0px;">
        Y-o-Y % Change in Ridership Across 4 Boroughs
    </h2>
    """, 
    unsafe_allow_html=True
    )

    plot_ridership_change()

    show_interpretation = st.toggle("💡 What does this tell us about Ridership recovery post COVID-19 Pandemic?", value = False)

    if show_interpretation: 
        st.markdown(
            """
            <div class="slide-box">
                <h3 style="text-align: left;">🚇 This graph highlights Ridership recovery after the COVID-19 Pandemic. </h3>
                <p style="text-align: left;"> 
                 In 2021, when more people return to work, ridership shows some sign of recovery. 2022 is when ridership recovers the most across all boroughs, with Manhattan posting a high Y-o-Y growth of 43% compared to 2021 whereas the other boroughs see only slightly higher Y-o-Y growth. 
                In the context of the COVID-19 Pandemic, the significant recovery of ridership in Manhattan relative to other boroughs highlights the return of office workers to Manhattan's central business districts in 2022, compared to 2021, when many office workers remained remote or worked less frequently in the city.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # add a header for a section here: 

    st.markdown('<div class="mta-header"> Weekend vs. Weekday Analysis </div>', unsafe_allow_html=True)
    #st.markdown('## In New York, millions of people commute to work every day. The stations that workers use most to commute to work are therefore "commuter-heavy" stations. Let's analyze the ridership data on weekend & weekday to pinpoint those that are "commuter-heavy, those with significant drops in ridership on weekend compared to weekday!', unsafe_allow_html=True)
   # st.markdown('## In New York, millions of people commute to work every day. The stations most frequently used by these workers are considered "commuter-heavy" stations. Let\'s analyze the ridership data for both weekends and weekdays to identify "commuter-heavy" stations --  those that experiences significant drops in the weekends relative to weekdays', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 25px; color: white;">In New York, millions of people commute to work daily. "Commuter-heavy" stations are those predominantly used by workers, rather than tourists or for leisure purposes. Can you guess which stations are commuter-heavy? By analyzing ridership data for both weekends and weekdays, we can identify these stations—those that show a noticeable decline in ridership on weekends compared to weekdays.</h3>', unsafe_allow_html=True)
    #st.markdown('<p class="custom-text" style="font-size: 15px;">In New York, millions of people commute to work every day. The stations most frequently used by these workers are considered "commuter-heavy" stations. Let\'s analyze the ridership data for both weekends and weekdays to identify "commuter-heavy" stations -- those that experience significant drops on weekends relative to weekdays.</p>', unsafe_allow_html=True)
    plot_commuter_heavy_stationss()
    # toggle 
    commuter_heavy_toggle = st.toggle("💡Does any of these commuter-heavy stations surprise you?", value = False)
    
    if commuter_heavy_toggle: 
        st.markdown(
            """
            <div class="slide-box">
                <h3 style="text-align: left;">🚇 Does any of these commuter-heavy stations surprise you?</h3>
                <p style="text-align: left;"> 
                This graph highlights the top 12 stations with the highest commuter ridership—stations primarily used by workers rather than for tourism or leisure. The Wall St station in FiDi is a prime example of a commuter-heavy station, with weekend ridership 41% lower than on weekdays. However, what's interesting is that, despite its significant commuter traffic, Wall Street is not the busiest station overall. Of the top 12 commuter-heavy stations, only two are located in Manhattan, while five are in Brooklyn, three are in the Bronx, and two are in Queens.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown('<h3 style="font-size: 25px; color: white;"> On the weekends, residents of New York unplug from work by going to places. Let\'s explore where do they go by identifying "weekend-destination" stations -- those that see signifcant surges in weekend riderships!</h3>', unsafe_allow_html=True)

    weekend_stations()
    weekend_destination_toggle = st.toggle("💡 Explore the stations flooded with weekend riders")
    if weekend_destination_toggle:
        st.markdown(
            """
            <div class="slide-box">
                <h3 style="text-align: left;">🚇 Explore the stations flooded with weekend riders?</h3>
                <p style="text-align: left;"> 
                One thing these top stations have in common is that they are all located in major recreational or entertainment destinations (or shopping hub Spring St in Soho)! For instance, Mets-Willet Point is located near Citi Field, Aqueduct near horse racing and other popular venues, Beach 90th St &  Beach 105th St near, of-course, beach! People often visit these areas for leisure, entertainment, or events, which perfectly explains why these stations experience incredible weekend ridership surges.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )




    #box_plot()
    # Streamlit setup to display the title
    #st.title('NYC MTA Ridership Analysis')
    #st.header('Ridership Growth Over the Years')
    #plot_growth()



    # Bar chart for ridership data
    data = {
   'Station': ['Station A', 'Station B', 'Station C', 'Station D'],
    'Ridership': [50000, 120000, 90000, 60000],
    'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
 }

    df = pd.DataFrame(data)
    fig = px.bar(df, x="Station", y="Ridership", title="Monthly Ridership at Different Stations")
    #st.plotly_chart(fig)

elif selected_tab == "Recommendations to MTA Management":
    st.subheader("Making MTA subway more efficient")
    #st.subheader("A huge share of NYC subway riders are college students, and these students go to school according to the school’s respective academic calendar. One might expect that the subway stations located near these schools experience significant drops in ridership during school breaks like summer and winter break. What this means for the MTA is that the riderships at these college-adjacent stations are influenced by each school’s academic calendars. During school breaks, ridership will see a sharp drop. Conversely, during academic months, ridership will see an increase. Leveraging this trend, there will be operational changes that MTA could pursue to increase efficiency in these stations.")

    st.markdown('<h3 class ="custom-text"> Did you know that college students make up a significant portion of NYC subway riders? As their schedules align with academic calendars, stations near schools face sharp fluctuations in ridership during breaks. These patterns present an opportunity for the MTA to improve operational efficiency by tailoring service to the ebbs and flows of student traffic.</h3>', unsafe_allow_html=True)
    st.markdown('<div class="mta-header"> Do college-adjacent stations experience more fluctations than general stations?</div>', unsafe_allow_html=True)
    
    # Recommendations based on analysis
    # st.markdown("""

    # A huge share of NYC subway riders are college students, and these students go to school according to the school’s respective academic calendar. One might expect that the subway stations located near these schools experience significant drops in ridership during school breaks like summer and winter break. What this means for the MTA is that the riderships at these college-adjacent stations are influenced by each school’s academic calendars. During school breaks, ridership will see a sharp drop. Conversely, during academic months, ridership will see an increase. Leveraging this trend, there will be operational changes that MTA could pursue to increase efficiency in these stations. 
    # Based on the analysis of ridership trends across various stations, the following recommendations are made:
    
    # - **Station A**: Ridership is lower than expected. Consider improving accessibility or adding promotional offers to attract more riders.
    # - **Station B**: This station is operating at peak capacity. Plan for additional services during high-ridership months, especially in the summer.
    # - **Station C**: Although ridership is steady, improving amenities could boost ridership further. Focus on customer experience here.
    # - **Station D**: Consider adjustments to schedules based on fluctuations in ridership, especially in the winter months when the ridership dips.
    # """)
#     st.markdown("""
#     <div 
#         A huge share of NYC subway riders are college students, and these students go to school according to the school'\s respective academic calendar. One might expect that the subway stations located near these schools experience significant drops in ridership during school breaks like summer and winter break. What this means for the MTA is that the riderships at these college-adjacent stations are influenced by each school’s academic calendars. During school breaks, ridership will see a sharp drop. Conversely, during academic months, ridership will see an increase. Leveraging this trend, there will be operational changes that MTA could pursue to increase efficiency in these stations. 
#         Based on the analysis of ridership trends across various stations, the following recommendations are made:
#         - **Station A**: Ridership is lower than expected. Consider improving accessibility or adding promotional offers to attract more riders.
#         - **Station B**: This station is operating at peak capacity. Plan for additional services during high-ridership months, especially in the summer.
#         - **Station C**: Although ridership is steady, improving amenities could boost ridership further. Focus on customer experience here.
#         - **Station D**: Consider adjustments to schedules based on fluctuations in ridership, especially in the winter months when the ridership dips.
#     </div>
# """, unsafe_allow_html=True)

    # Visualization of the recommendations
    #st.markdown("### ege-adjacent subway stations experience more fluctuations than general stations on a monthly basis?")
    
    # CV t-test Do coll
    cv_plot()

    cv_plot_toggle = st.toggle("Reveal the results of the Statistical Test", value=False)

    if cv_plot_toggle: 
        # st.markdown(
        #     """
        #     <div class="slide-box">
        #         <h3 style="text-align: left;">🚇 Yes. The result shows that college-adjacent stations have significantly more ridership fluctuations than non-college stations, indicating seasonality, and warrants further analysis on monthly ridership trends at these stations.</h3>
        #         <p style="text-align: left;"> 
                    
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )

        st.markdown(
            """
            <div class="slide-box" style ="text-align: left; font-size: 15px;">
                <h3 style="text-align: left;">🚇 Yes. The result shows that college-adjacent stations have significantly more ridership fluctuations than non-college stations, indicating seasonality, and warrants further analysis on monthly ridership trends at these stations.</h3>
                <p style="text-align: left; font-size: 15px !important;"> 
                    I first aggregated the ridership data by month-year for each station from 2020 to 2024, then created a derived column named <code>college_station</code>, categorizing stations into two groups:
                    <ul>
                        <li><strong>Yes</strong> (college-adjacent stations)</li>
                        <li><strong>No</strong> (non-college stations)</li>
                    </ul>
                    I focused on high student-population colleges in New York City and specifically classified the following 3 stations as college-adjacent:
                    <ul>
                        <li><strong>8th St-NYU</strong></li>
                        <li><strong>116 St-Columbia University</strong></li>
                        <li><strong>68 St-Hunter College</strong></li>
                    </ul>
                    Next, I calculated the <strong>Coefficient of Variation (CV)</strong> for each station. CV is the ratio of <strong>Standard Deviation</strong> to <strong>Mean</strong> and reflects the ridership fluctuations in relation to the average ridership at a particular station. CV is useful for comparing stations with different average ridership sizes because it normalizes the fluctuation.
                    <br><br>
                    With the CV values, I performed a <strong>t-test</strong> to compare the two groups (college-adjacent vs. non-college stations) based on their mean CV. Here are the test details:
                    <ul>
                        <li><strong>Null Hypothesis (H0):</strong> The CV at college-adjacent stations is not significantly different from other stations (Mean CV of university stations ≤ Mean CV of other stations).</li>
                        <li><strong>Alternative Hypothesis (H1):</strong> The CV at college-adjacent stations is significantly higher than other stations due to seasonality influenced by the academic calendar (Mean CV of university stations > Mean CV of other stations).</li>
                    </ul>
                    If <strong>p-value < 0.05</strong>, we reject the Null Hypothesis and conclude that university-adjacent stations experience significantly greater ridership variability.
                    <br><br>
                    <strong>The result:</strong>
                    <ul>
                        <li><strong>T-statistic:</strong> 2.3931</li>
                        <li><strong>P-value:</strong> 0.0172</li>
                    </ul>
                    <strong>Conclusion:</strong>
                    <ul>
                        <li>The above results indicate that the ridership fluctuations between college-adjacent stations and non-college stations are significantly different, and this difference is unlikely to be due to random chance.</li>
                        <li>However, this result does not explain the driving force behind the ridership fluctuations at the three college stations. Let's dive deeper into analyzing the seasonality of each station.</li>
                    </ul>
                </p> 
            </div>
            """,
            unsafe_allow_html=True
        )
    # place a mta-header: 
    st.markdown('<div class="mta-header"> Explore how academic calendar affect ridership at college-adjacent stations & what MTA Management can do</div>', unsafe_allow_html=True)


    # create Streamlit UI to select the station 
    station = st.selectbox( 
        'Pick a college station to analyze:',
        ['NYU', 'Columbia University', 'Hunters College']
    )
    if station == "NYU": 
        plot_seasonality("nyu_decomposition_df.csv")
        plot_seasonality_toggle = st.toggle("What is Seasonality?", value = False)
        if plot_seasonality_toggle: 
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇 What is seasonality?</h3>
                    <p style="text-align: left;"> 
                    Seasonality: the recurring patterns or fluctuations in ridership that occur at specific regular intervals in monthly cycles.
                    It matters our analysis of how academic calendar affects ridership because it helps pinpoint times when ridership CONSISTENLY drops. 
                    I used the seasonal_decompose function from statsmodels to calculate Seasonality, whereby the additive model assumes the observed data is the sum of trend, seasonal, and residual components. 
                    The Seasonality in the above graph is the extraction of the Seasonal component from the model's output, representing the recurring seasonal fluctuations in riderships & help us clearly identify the periods of higher or lower ridership.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )


        plot_month_vs_ridership("nyu_avg_monthly.csv")

        plot_month_vs_ridership_toggle = st.toggle("What does Average Monthly Ridership tell us?", value = False)
        if plot_month_vs_ridership_toggle: 
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇</h3>
                    <p style="text-align: left;"> 
                    This graph presents the average monthly ridership at NYU station from 2020 - 2024. 
                    NYU Ridership is the lowest in the months of Jan, Feb, and June.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )

        plot_percentage_change_from_max("nyu_avg_monthly.csv")
        plot_percentage_change_from_max_toggle = st.toggle("What is Monthly Resource Utilization Rate?")
        if plot_percentage_change_from_max_toggle: 
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇</h3>
                    <p style="text-align: left;"> 
                    A station utilizes 100% of its resources during busiest months. For example, if NYU station has nearly 3,500 rides in its busiest month, this means NYU station can handle this much rides at its maximum. However, during months with lower ridership demand, the station continues to operate with the same resources (such as train frequency and staff), but serves way fewer passengers. Imagine a subway train or station that has significantly fewer people compared to its peak month – this difference defines the utilization rate.
                    The utilization rate is calculated by dividing the ridership for any given month by the ridership during the busiest month. For instance, if NYU station has only 41.2% of the rides in January compared to its busiest month, the utilization rate for January would be 41.2%.
                    This insight offers an opportunity for MTA management to optimize resources, reducing subway operations during months with lower ridership, such as academic breaks, to better align with demand.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )

        #plot_ridership_resource_utilization()
        # just testing 
        #plot_ridership_resource_utilization_testing()
    elif station == "Columbia University": 
        plot_seasonality("columbia_decomposition_df.csv")
        plot_seasonality_toggle_columbia = st.toggle("What is Seasonality in Ridership?", value = False)
        if plot_seasonality_toggle_columbia: 
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇 Ridership is consistently down in May, June, Dec at Columbia Station.</h3>
                    <p style="text-align: left;"> 
                    Seasonality: the recurring patterns or fluctuations in ridership that occur at specific regular intervals in monthly cycles.
                    It matters our analysis of how academic calendar affects ridership because it helps pinpoint times when ridership CONSISTENLY drops. 
                    I used the seasonal_decompose function from statsmodels to calculate Seasonality, whereby the additive model assumes the observed data is the sum of trend, seasonal, and residual components. 
                    The Seasonality in the above graph is the extraction of the Seasonal component from the model's output, representing the recurring seasonal fluctuations in riderships & help us clearly identify the periods of higher or lower ridership.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )
        plot_month_vs_ridership("columbia_avg_monthly.csv")

        plot_month_vs_ridership_toggle_columbia = st.toggle("What does Average Monthly Ridership tell us?", value = False)
        if plot_month_vs_ridership_toggle_columbia: 
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇</h3>
                    <p style="text-align: left;"> 
                    This graph presents the average monthly ridership at Columbia station from 2020 - 2024. 
                    Columbia Ridership is the lowest in the months of May, June, August, and Dec.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )

        plot_percentage_change_from_max("columbia_avg_monthly.csv")
        plot_percentage_change_from_max_toggle_columbia = st.toggle("What is Resource Utilization Rate?")
        if plot_percentage_change_from_max_toggle_columbia:
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇 What is Resource Utilization Rate?</h3>
                    <p style="text-align: left;"> 
                    A station's maximum capacity refers to its ridership during the busiest month of the year. For example, if NYU station has nearly 3,500 rides in its busiest month, this number represents its maximum capacity. However, during months with lower ridership demand, the station continues to operate with the same resources (such as train frequency and staff), but serves fewer passengers. Imagine a subway train or station that has significantly fewer people compared to its peak month – this difference defines the utilization rate.
                    The utilization rate is calculated by dividing the ridership for any given month by the ridership during the busiest month. For instance, if NYU station has only 41.2% of the rides in January compared to its busiest month, the utilization rate for January would be 41.2%.
                    This insight offers an opportunity for MTA management to optimize resources, reducing subway operations during months with lower ridership, such as academic breaks, to better align with demand.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )

    elif station == "Hunters College": 
        plot_seasonality("hunter_decomposition_df.csv")
        plot_seasonality_toggle_hunters = st.toggle("Explain Seasonality", value = False)
        if plot_seasonality_toggle_hunters: 
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇 What is seasonality?</h3>
                    <p style="text-align: left;"> 
                    Seasonality: the recurring patterns or fluctuations in ridership that occur at specific regular intervals in monthly cycles.
                    It matters our analysis of how academic calendar affects ridership because it helps pinpoint times when ridership CONSISTENLY drops. 
                    I used the seasonal_decompose function from statsmodels to calculate Seasonality, whereby the additive model assumes the observed data is the sum of trend, seasonal, and residual components. 
                    The Seasonality in the above graph is the extraction of the Seasonal component from the model's output, representing the recurring seasonal fluctuations in riderships & help us clearly identify the periods of higher or lower ridership.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )


        plot_month_vs_ridership("hunter_avg_monthly.csv")
        plot_month_vs_ridership_toggle_hunters = st.toggle("Reveal trends", value = False)
        if plot_month_vs_ridership_toggle_hunters: 
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇</h3>
                    <p style="text-align: left;"> 
                    This graph presents the average monthly ridership at 68th St-Hunter College from 2020 - 2024. 
                    68 St-Hunter College is the lowest in the months of June, August, and Dec.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )
        plot_percentage_change_from_max("hunter_avg_monthly.csv")
        plot_percentage_change_from_max_toggle_hunter = st.toggle("What is the Resource Utilization Rate?")
        if plot_percentage_change_from_max_toggle_hunter:
            st.markdown(
                """
                <div class="slide-box">
                    <h3 style="text-align: left;">🚇 What is the Resource Utilization Rate?</h3>
                    <p style="text-align: left;"> 
                    A station's maximum capacity refers to its ridership during the busiest month of the year. For example, if NYU station has nearly 3,500 rides in its busiest month, this number represents its maximum capacity. However, during months with lower ridership demand, the station continues to operate with the same resources (such as train frequency and staff), but serves fewer passengers. Imagine a subway train or station that has significantly fewer people compared to its peak month – this difference defines the utilization rate.
                    The utilization rate is calculated by dividing the ridership for any given month by the ridership during the busiest month. For instance, if NYU station has only 41.2% of the rides in January compared to its busiest month, the utilization rate for January would be 41.2%.
                    This insight offers an opportunity for MTA management to optimize resources, reducing subway operations during months with lower ridership, such as academic breaks, to better align with demand.
                    </p>
                </div>
                """,
            unsafe_allow_html=True
        )

    st.markdown(
    """
    <h3 class="custom-text" style="text-align: left; font-size: 25px; font-family: 'Helvetica Neue', sans-serif; color: white;">
        🚇 Recommendations to MTA Management
    </h3>
    <p style="text-align: left; font-size: 18px; font-family: 'Helvetica Neue', sans-serif; color: white;">
        How should MTA Management better improve operational efficiency in these 3 college stations? 
        By tailoring their service to the ebbs and flow of student ridership during the months where student ridership drops significantly due to school break. 
        Key findings that MTA could act on based on this analysis:
    </p>
    <ul style="font-size: 18px; font-family: 'Helvetica Neue', sans-serif; color: white;">
        <li>These 3 stations do in fact experience significant student ridership drop during academic months.</li>
        <li>Although they share similar academic schedules, the months during which student ridership drops do differ across these 3 schools.</li>
    </ul>
    <br>
    <p style="font-size: 18px; font-family: 'Helvetica Neue', sans-serif; color: white;">
        <strong>Summary of each school’s lowest months and their respective Resources Utilization Rate:</strong>
    </p>
    <ul style="font-size: 18px; font-family: 'Helvetica Neue', sans-serif; color: white;">
        <li><strong>New York University:</strong> Jan (41.2%), Feb (45.9%), June (50.3%)</li>
        <li><strong>Columbia University:</strong> May (45.5%), June (53.4%), August (51.4%)</li>
        <li><strong>Hunter College:</strong> April (53%), June (45%), December (42.1%)</li>
    </ul>
    <p style="font-size: 18px; font-family: 'Helvetica Neue', sans-serif; color: white;">
        Based on these findings, MTA should consider the following strategies to adjust service during the above low ridership periods at these stations:
    </p>

    <ul style="font-size: 18px; font-family: 'Helvetica Neue', sans-serif; color: white;">
        <li><strong>Scale back service frequencies:</strong> During each station's respective low months to better align with resource utilization rates, ensuring that fewer resources are wasted during low-demand months. For instance, at NYU, where ridership resource utilization dips to 41.2% in January and 45.9% in February, the MTA could reduce train frequency to match these lower utilization rates, ensuring that fewer trains are running when demand is low. Similarly, at Columbia in August (51.4%) and Hunter in December (42.1%), service could be scaled down to better match the actual ridership demand.</li>
        <li><strong>Reduce staff presence during low months:</strong> For example, fewer station agents or conductors could be scheduled during off-peak months, or certain services (e.g., information desks, maintenance) could be scaled back. By doing so, MTA can redirect these resources to higher-traffic periods where ridership is more robust, thus achieving a balance between efficient staffing and service delivery.</li>
    </ul>
    """, 
    unsafe_allow_html=True
)

#     st.markdown(
#     """
#     <h3 class="custom-text" style="text-align: left; font-size: 25px; font-family: 'Helvetica Neue', sans-serif; color: white;">🚇 Recommendations to MTA Management </h3>
#     <p style="text-align: left; font-size: 25px; font-family: 'Helvetica Neue', sans-serif; color: white;">
#     <br> 
#     How should MTA Management better improve operational efficiency in these 3 college stations? By tailoring their service to the ebbs and flow of student ridership during the months where student ridership drops significantly due to school break. Key findings that MTA could act on based on this analysis: 
#     <ul>
#         <li>These 3 stations do in fact experience significant student ridership drop during academic months.</li>
#         <li>Although they share similar academic schedules, the months during which student ridership drops do differ across these 3 schools.</li>
#     </ul>
#     <br>
#     <strong>Summary of each school’s lowest months and their respective utilization rate:</strong>
#     <ul>
#         <li><strong>New York University:</strong> Jan (41.2%), Feb (45.9%), June (50.3%)</li>
#         <li><strong>Columbia University:</strong> May (45.5%), June (53.4%), August (51.4%)</li>
#         <li><strong>Hunter College:</strong> April (53%), June (45%), December (42.1%)</li>
#     </ul>

#     Based on these findings, MTA should consider the following strategies to adjust service during the above low ridership periods at these stations:
#     </p>

#     <ul>
#         <li><strong>Scale back service frequencies:</strong> During each station's respective low months to better align with utilization rates, ensuring that fewer resources are wasted during low-demand months. For instance, at NYU, where ridership utilization dips to 41.2% in January and 45.9% in February, the MTA could reduce train frequency to match these lower utilization rates, ensuring that fewer trains are running when demand is low. Similarly, at Columbia in August (51.4%) and Hunter in December (42.1%), service could be scaled down to better match the actual ridership demand.</li>
#         <li><strong>Reduce staff presence during low months:</strong> For example, fewer station agents or conductors could be scheduled during off-peak months, or certain services (e.g., information desks, maintenance) could be scaled back. By doing so, MTA can redirect these resources to higher-traffic periods where ridership is more robust, thus achieving a balance between efficient staffing and service delivery.</li>
#     </ul>
#     """, 
#     unsafe_allow_html=True
# )

#     st.markdown(
#                 """
#                 <div class="slide-box">
#                     <h3 style="text-align: left;">🚇 Recommendations to MTA Management </h3>
#                     <p style="text-align: left;">
#                     <br> 
#                     How should MTA Management better improve operational efficiency in these 3 college stations?  By tailoring their service to the ebbs and flow of student ridership during the months where student ridership drops significantly due to school break. Key findings that MTA could act on based on this analysis: 
#                     These 3 stations do in fact experience significant student ridership drop during academic months. 
#                     Although they share similar academic schedules, the months during which student ridership drops do differ across these 3 schools. 
#                     <br>
#                     Summary of each school’s lowest months and their respective utilization rate: 
#                     New York University: Jan (41.2%), Feb ( 45.9%), June (50.3%)
#                     Columbia University: May (45.5%), June (53.4%), August (51.4%)
#                     Hunter: April (53%), June (45%), December (42.1%)
#                     Based on these findings, MTA should consider the following strategies to adjust service during the above low ridership periods at these stations:
#                     Scale back service frequencies during each station's respective low months to better align with utilization rates, ensuring that less resources is wasted during low-demand months. MTA should adjust service frequencies to better align with the utilization rates during months of lower ridership. For instance, at NYU, where ridership utilization dips to 41.2% in January and 45.9% in February, the MTA could reduce train frequency to match these lower utilization rates, ensuring that fewer trains are running when demand is low. Similarly, at Columbia in August (51.4%) and Hunter in December (42.1%), service could be scaled down to better match the actual ridership demand.
#                     Reducing staff presence during low-months. For example, fewer station agents or conductors could be scheduled during off-peak months, or certain services (e.g., information desks, maintenance) can be scaled back accordingly. By doing so, MTA can redirect these resources to higher-traffic periods where ridership is more robust, thus achieving a balance between efficient staffing and service delivery.
#                     </p>
#                 </div>
#                 """,
#             unsafe_allow_html=True
#         )

#     st.markdown(
#     """
#     <div class="slide-box">
#         <h3 style="text-align: left;">🚇 Recommendations to MTA Management </h3>
#         <p style="text-align: left;">
#         <br> 
#         How should MTA Management better improve operational efficiency in these 3 college stations? By tailoring their service to the ebbs and flow of student ridership during the months where student ridership drops significantly due to school break. Key findings that MTA could act on based on this analysis: 
#         - These 3 stations do in fact experience significant student ridership drop during academic months. 
#         - Although they share similar academic schedules, the months during which student ridership drops do differ across these 3 schools. 
#         <br>
#         **Summary of each school’s lowest months and their respective utilization rate:** 
#         - **New York University**: Jan (41.2%), Feb (45.9%), June (50.3%)
#         - **Columbia University**: May (45.5%), June (53.4%), August (51.4%)
#         - **Hunter**: April (53%), June (45%), December (42.1%)
        
#         Based on these findings, MTA should consider the following strategies to adjust service during the above low ridership periods at these stations:
#         </p>

#         <ul>
#             <li><strong>Scale back service frequencies:</strong> During each station's respective low months to better align with utilization rates, ensuring that fewer resources are wasted during low-demand months. MTA should adjust service frequencies to match these lower utilization rates. For instance, at NYU, where ridership utilization dips to 41.2% in January and 45.9% in February, the MTA could reduce train frequency to match these lower utilization rates, ensuring fewer trains run when demand is low. Similarly, at Columbia in August (51.4%) and Hunter in December (42.1%), service could be scaled down to better align with actual ridership demand.</li>
            
#             <li><strong>Reduce staff presence during low months:</strong> For example, fewer station agents or conductors could be scheduled during off-peak months, or certain services (e.g., information desks, maintenance) could be scaled back. By doing so, MTA can redirect resources to higher-traffic periods where ridership is more robust, achieving a balance between efficient staffing and service delivery.</li>
#         </ul>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

    
#     st.markdown(
#     """
#     <div class="slide-box">
#         <h3 style="text-align: left;">🚇 Recommendations to MTA Management </h3>
#         <p style="text-align: left;">
#         <br> 
        
#         How should MTA Management better improve operational efficiency in these 3 college stations? By tailoring their service to the ebbs and flow of student ridership during the months where student ridership drops significantly due to school break. Key findings that MTA could act on based on this analysis: 
        
#         - These 3 stations do in fact experience significant student ridership drop during academic months. 
#         - Although they share similar academic schedules, the months during which student ridership drops do differ across these 3 schools.
        
#         <br>
#         Summary of each school’s lowest months and their respective utilization rate: 
        
#         - **New York University**: Jan (41.2%), Feb (45.9%), June (50.3%)
#         - **Columbia University**: May (45.5%), June (53.4%), August (51.4%)
#         - **Hunter**: April (53%), June (45%), December (42.1%)

#         <br>
#         Based on these findings, MTA should consider the following strategies to adjust service during the above low ridership periods at these stations:
        
#         <ul>
#             <li><strong>Scale back service frequencies</strong> during each station's respective low months to better align with utilization rates, ensuring that fewer resources are wasted during low-demand months. MTA should adjust service frequencies to match these lower utilization rates. For instance, at NYU, where ridership utilization dips to 41.2% in January and 45.9% in February, the MTA could reduce train frequency to match these lower utilization rates, ensuring fewer trains run when demand is low. Similarly, at Columbia in August (51.4%) and Hunter in December (42.1%), service could be scaled down to better align with actual ridership demand.</li>
            
#             <li><strong>Reduce staff presence during low months</strong>. For example, fewer station agents or conductors could be scheduled during off-peak months, or certain services (e.g., information desks, maintenance) could be scaled back. By doing so, MTA can redirect resources to higher-traffic periods where ridership is more robust, achieving a balance between efficient staffing and service delivery.</li>
#         </ul>
#         </p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
    
    
    
#     # Example plot for recommendations
#     rec_data = {
#         'Station': ['Station A', 'Station B', 'Station C', 'Station D'],
#         'Recommendation Score': [4, 9, 7, 5],
#     }
#     rec_df = pd.DataFrame(rec_data)
    
#     fig_rec = px.bar(rec_df, x="Station", y="Recommendation Score", title="Station Recommendation Scores")
#     st.plotly_chart(fig_rec)

    

    

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>By: Lisa Cao <br> nmc9389@stern.nyu.edu </p>", unsafe_allow_html=True)


