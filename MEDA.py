# Import Libraries
from zipfile import ZipFile
import numpy as np 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Read the dataset
zip_file_path = "./sources/Airbnb_Open_Data.zip"
with ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall()
extracted_files = zip_ref.namelist()
csv_file_name = extracted_files[0] 
df = pd.read_csv(csv_file_name)

# Cleaning the data:

# Convert column names to lowercase and replace spaces with underscores
df.columns=df.columns.str.strip().str.lower()
df.columns = df.columns.str.replace(' ', '_', regex= True)

# Drop unnecessary columns
df.drop(['host_id','country','license','country_code','name','host_name','last_review','house_rules'],axis=1,inplace=True)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Drop rows with missing values in specific columns
df.dropna(subset= ['neighbourhood_group','neighbourhood','instant_bookable','cancellation_policy','host_identity_verified'],inplace = True)

# Reset index after dropping rows
df.reset_index(drop= True, inplace= True)

# Rename columns for consistency
df.rename(columns={'price': 'price($)', 'service_fee': 'service_fee($)'}, inplace=True)

# Remove dollar signs and commas from certain columns and convert to numeric
cols=['price($)','service_fee($)']
for i in cols:
    df[i] = df[i].str.replace('$', '').str.replace(',', '')
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# Fill missing values in numeric columns with mean values
df[cols]=df[cols].fillna(df[cols].mean().round())

# Fill missing values in construction_year column with mode value
df.construction_year.fillna(df.construction_year.mode()[0],inplace=True)

# Fill missing values in specific numeric columns with median values
cols_2=['minimum_nights','number_of_reviews','reviews_per_month','review_rate_number','calculated_host_listings_count','availability_365']
df[cols_2]=df[cols_2].fillna(df[cols_2].median())

# Fill missing latitude and longitude values with mean values based on neighbourhood
fill_lat = df.groupby('neighbourhood')['lat'].transform('mean')
fill_long = df.groupby('neighbourhood')['long'].transform('mean')
df.long.fillna(fill_long, inplace=True)
df.lat.fillna(fill_lat, inplace=True)

# Replace misspelled neighbourhood_group value
df['neighbourhood_group'] = df['neighbourhood_group'].replace('brookln', 'Brooklyn')

# Filter out rows based on certain conditions
df = df[df['minimum_nights'] >= 0]
df = df[df['minimum_nights'] <= 365]
df = df[df['availability_365'] < 426]
df = df[df['reviews_per_month'] < 30]



# Analysis:-

# Tab_1

# function using Scatter plot for latitude and longitude using Plotly
def plot_distribution():
    fig = px.scatter(df, x='long', y='lat', color_discrete_sequence=px.colors.sequential.PuBu_r, title='Spatial Distribution of Listings', 
                    labels={'long': 'Longitude', 'lat': 'Latitude'})
    return fig

# function to visualize a map of data
def cluster_map():
    # Combine latitude and longitude into a single array
    coordinates = df[['lat', 'long']].values

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    cluster_labels = kmeans.fit_predict(coordinates)

    # Visualize the clusters
    fig = px.scatter_mapbox(df, lat='lat', lon='long', color=cluster_labels,
                            title='Cluster Analysis of Listings',
                            hover_name='neighbourhood_group',
                            mapbox_style='carto-positron', zoom=10)
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
    return fig

# Function to create a line plot for construction_year
def construction_count():
    construction_year_counts = df['construction_year'].value_counts().sort_index()
    fig = px.line(x=construction_year_counts.index, y=construction_year_counts.values,
                color_discrete_sequence=px.colors.sequential.PuBu_r,
                title='Construction of Rooms Over the Years',
                labels={'x': 'Year', 'y': 'Number of Rooms Constructed'})
    return fig

#  Function takes the year and return plot of count reiew rate number
def plot_reviews_by_year(selected_year):
    # Filter the data for the specified year
    group_data = df[df['construction_year'] == selected_year]

    # Count the number of reviews for each construction year
    review_counts = group_data['review_rate_number'].value_counts().reset_index()
    review_counts.columns = ['review_rate_number', 'count']

    # Create a bar chart
    fig = px.bar(review_counts, x='review_rate_number', y='count',
                 title=f'Count of review rate number in {selected_year}',
                 color_discrete_sequence=px.colors.sequential.PuBu_r,
                 labels={'review_rate_number': 'review rate number', 'count': 'Count'})
    fig.update_layout(xaxis_title='review rate number', yaxis_title='Count')
    return fig

# function takes 1 parameter ("number_of_reviews" or "reviews_per_month") and return bar chart with construction_year
def plot_yearly_reviews(review):
    # Group the data by construction year and sum the number of reviews for each year
    reviews_by_year = df.groupby('construction_year')[review].sum().reset_index()

    # Create a scatter plot
    fig = px.bar(reviews_by_year, x='construction_year', y=review,
                    color_discrete_sequence=px.colors.sequential.PuBu_r, title='Yearly reviews',
                    labels={'construction_year': 'Year', review: review})
    return fig




# Tab_2

# creaate function to Count the number of constructions or price in each neighbourhood_group
def plot_neighbourhood_data(chart_type):
    if chart_type == 'construction_distribution':
        # Count the number of constructions in each neighbourhood_group
        construction_counts = df["neighbourhood_group"].value_counts().reset_index()
        construction_counts.columns = ["neighbourhood_group", 'number_of_constructions']

        # Create a pie chart for construction distribution
        fig = px.pie(construction_counts, 
                     names="neighbourhood_group", 
                     values='number_of_constructions',
                     color_discrete_sequence=px.colors.sequential.PuBu_r)
        fig.update_layout(title='Distribution of Constructions Across Neighbourhood Groups')
        
    elif chart_type == 'neighbourhood_group_prices':
        # Group by 'neighbourhood_group' and calculate the mean of 'price'
        neighbourhood_group_prices = df.groupby('neighbourhood_group')['price($)'].mean().reset_index()

        # Sort the neighbourhood_group by the average price in descending order
        neighbourhood_group_prices = neighbourhood_group_prices.sort_values(by='price($)', ascending=False).reset_index(drop=True)

        # Create a pie chart for the most expensive neighborhood_groups
        fig = px.pie(neighbourhood_group_prices, 
                     names='neighbourhood_group', 
                     values='price($)',
                     title='neighbourhood_group_prices',
                     color_discrete_sequence=px.colors.sequential.PuBu_r)

    return fig

# Creat function to display the No.of constructions or price($) for all neighbourhoods in the same group.
def plot_neighborhood_data(neighborhood_group, data_type):
    # Filter the data for the specified neighborhood group
    filtered_df = df[df['neighbourhood_group'] == neighborhood_group]
    
    if data_type == 'price($)':
        # Group the filtered data by neighborhood and calculate the average price
        pivot_table = filtered_df.groupby('neighbourhood')['price($)'].mean().reset_index()

        # Create a bar chart for neighborhood prices
        fig = px.bar(pivot_table, x='neighbourhood', y='price($)',
                     title=f'Average Price by Neighborhood in {neighborhood_group}',
                     labels={'price($)': 'Average Price ($)', 'neighbourhood': 'Neighbourhood'},
                     hover_name='neighbourhood')
        
    elif data_type == 'construction_year':
        # Count the number of constructions in each neighborhood
        construction_counts = filtered_df['neighbourhood'].value_counts().reset_index()
        construction_counts.columns = ['neighbourhood', 'number_of_constructions']

        # Create a bar chart for neighborhood constructions
        fig = px.bar(construction_counts, x='neighbourhood', y='number_of_constructions',
                     title=f'Number of Constructions in {neighborhood_group} Neighbourhoods',
                     color_discrete_sequence=px.colors.sequential.PuBu_r,
                     labels={'neighbourhood': 'Neighbourhood', 'number_of_constructions': 'Number of Constructions'})

    return fig

# Create function takes 'neighbourhood_group' and return avg price of each room type
def room_price(neighbourhood_group):

     # Filter the DataFrame for the specified neighbourhood_group
    filtered_df = df[df['neighbourhood_group'] == neighbourhood_group]
        
    # Generate a pivot table from the filtered DataFrame
    pivot_table = filtered_df.pivot_table(index='neighbourhood_group', columns='room_type', values='price($)')
        
    # Reset index to convert neighbourhood_group from index to a column
    pivot_table = pivot_table.reset_index()

    # Create an interactive bar chart using Plotly with vertical bars
    fig = px.bar(pivot_table, y='neighbourhood_group', x=pivot_table.columns[1:], orientation='h', color_discrete_sequence=px.colors.sequential.PuBu_r,
                title=f'Average Price($) of room_type by {neighbourhood_group}',
                labels={'value': 'avg_price($)', 'neighbourhood_group': neighbourhood_group},
                barmode='group')

    # Show the figure
    return fig



# Tab_3

# Create function to display the most (n) Expensive Neighbourhoods
def plot_top_prices(x:int):
    # Group by 'neighbourhood' and calculate the mean of 'price'
    neighbourhood_prices = df.groupby('neighbourhood')['price($)'].mean().reset_index()
    # Sort the neighborhoods by the average price in descending order
    neighbourhood_prices = neighbourhood_prices.sort_values(by='price($)', ascending=False).reset_index(drop=True)

    # Use Plotly to create an interactive bar chart for the top 10 most expensive neighborhoods
    fig = px.bar(neighbourhood_prices.head(x), x='neighbourhood', y='price($)',color_discrete_sequence=px.colors.sequential.PuBu_r,
                title=f'Top {x} Most Expensive Neighbourhoods')
    return fig 

# Create function to display the least (n) Expensive Neighbourhoods
def plot_least_prices(x:int): 
    # Group by 'neighbourhood' and calculate the mean of 'price'
    neighbourhood_prices = df.groupby('neighbourhood')['price($)'].mean().reset_index()
    # Sort the neighborhoods by the average price in descending order
    neighbourhood_prices = neighbourhood_prices.sort_values(by='price($)', ascending=False).reset_index(drop=True)
    # Use Plotly to create an interactive bar chart for the least expensive neighborhoods
    fig = px.bar(neighbourhood_prices.tail(x), x='price($)', y='neighbourhood',orientation='h',color_discrete_sequence=px.colors.sequential.PuBu_r,
                title=f'The least {x} Expensive Neighbourhoods')
    return fig


# Create function to display the relation between Price and host_identity_verified
def mean_price_by_verification():
    # Calculate the mean price for each value in the host_identity_verified column
    mean_prices = df.groupby('host_identity_verified')['price($)'].mean().reset_index()

    # Create a bar chart
    fig = px.bar(mean_prices, x='host_identity_verified', y='price($)', color='host_identity_verified',
                 color_discrete_sequence=px.colors.sequential.PuBu_r,
                 title='Mean Price by Host Identity Verification Status',
                 labels={'price($)': 'Mean Price ($)', 'host_identity_verified': 'Host Identity Verified'})

    # Show the plot
    return fig

# function to create a heatmap of the correlation matrix for numerical columns
def plot_correlatin():
    fig=px.imshow(df.select_dtypes(include= 'number').corr().round(2),color_continuous_scale=px.colors.sequential.PuBu_r, text_auto= True,width=850 ,height=800)
    return fig 


# Tab_4

# Function return The percentage of each room type
def show_room():
    room_df = pd.DataFrame(df['room_type'].value_counts())
    room_df = room_df.rename(columns={'room_type': 'count'})
    fig = go.Figure(go.Funnelarea(
        text=["Entire home/apt", "Private room", "Shared room", "Hotel room "],
        values=room_df['count'],  # Access the 'room_type' column
        title="Room types"))
    return fig


# Function shows The avg_price of every room type in every neighbourhood_group
def room_type_price(room_type):

     # Filter the DataFrame for the specified room_types
    filtered_df = df[df['room_type'] == room_type]
        
    # Generate a pivot table from the filtered DataFrame
    pivot_table = filtered_df.pivot_table(index='room_type', columns='neighbourhood_group', values='price($)')
        
    # Reset index to convert neighbourhood_group from index to a column
    pivot_table = pivot_table.reset_index(level='room_type')

    # Create an interactive bar chart using Plotly with vertical bars
    fig = px.bar(pivot_table, y='room_type', x=pivot_table.columns[1:6], orientation='h', color_discrete_sequence=px.colors.sequential.PuBu_r,
                title=f'Average Price($) of {room_type} in neighbourhood groups',
                labels={'value': 'avg_price($)', 'room_type': room_type},
                barmode='group')

    # Show the figure
    return fig

# Function return The avg minimum nights for every room type
def plot_min_nights():
    # Calculate average minimum nights for each room type
    avg_min_nights = df.groupby('room_type')['minimum_nights'].mean().reset_index()

    # Create a bar chart
    fig = px.bar(avg_min_nights, x='room_type', y='minimum_nights', color_discrete_sequence=px.colors.sequential.PuBu_r, 
                title='Average Minimum Nights by Room Type', labels={'minimum_nights': 'Average Minimum Nights', 'room_type': 'Room Type'})
    return fig
