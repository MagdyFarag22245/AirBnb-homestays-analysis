# import needed libraries
import numpy as np
import pandas as pd
import streamlit as st
import MEDA as md
import sys
# Directing to MEDA file path to be able to read it
sys.path.append("D:\Study\Epsilon DS\Bnb_project") # Path of MEDA file

# Dividing our analysis into tabs, each tab contains information in one dimension and many facts.
tab_over_view,tab_Neighbourhood, tab_Price, tab_Minimum_nights_and_room_type, tab_conclusion = st.tabs(['OverView','Neighbourhood','Price','Minimum_nights & Rooom_typpe','Conclusion'])

# OverView tap
with tab_over_view:
    # The title and iinsiights in the tab
    st.title("Over view and general insights about Air_Bnb data")
    st.header("This tab show the next insights : ") 
    st.write("  1- Distribution and interactive map of the listings.")
    st.write("  2- Distribution of Construction year")
    st.write("  3- Review rate number of every year.")
    st.write("  4- The number of review and reviews per month in every year.")
    # first section
    st.header("1) Distribution of the data")
    st.plotly_chart(md.plot_distribution())
    # second section
    st.header("2) Interactive map of listings ")
    st.plotly_chart(md.cluster_map())
    # third section
    st.header("3) Distribution of Construction year")
    st.write("-The below figure show that '2014' is the highest year with Number of Rooms Constructed = '5388'.")
    st.plotly_chart(md.construction_count())
    # fourth section
    st.header("4) Review rate number of every year")
    year=st.slider("Select a year",min_value=2003,max_value=2022,step=1)
    st.write("The selected year is : ", year)
    st.plotly_chart(md.plot_reviews_by_year(year))
    # fifth section
    st.header("5) Yearly reviews")
    yearly=st.radio("Options",("number_of_reviews","reviews_per_month"),horizontal=True)
    st.plotly_chart(md.plot_yearly_reviews(yearly))

# Neighbourhood tap
with tab_Neighbourhood:
    # The title and iinsiights in the tab
    st.title('Neighbourhood analysis')
    st.header("This tab show the next insights : ") 
    st.write("  1- The distribution of constructions and prices of Neighbourhood groups.")
    st.write("  2- The Prices and constructions of each Neighbourhood.")
    st.write("  3- The avg prices for all room types in every Neighbourhood.")
    # first section
    st.header("1) Distribution of constructions and prices of Neighbourhood groups")
    option=st.selectbox('Select..',('neighbourhood_group_prices','construction_distribution'))
    st.plotly_chart(md.plot_neighbourhood_data(option))
    # second seection
    st.header("2) Prices and constructions of each Neighbourhood")
    con_pie = st.container()
    col1_p, col2_p = con_pie.columns(2)
    with col1_p:
        fact = st.radio(
                "Select value you interest",
                ["construction_year", "price($)"],
                horizontal= True,
            )
    with col2_p:
        dim = st.radio(
                "Select Neighbourhood you interest",
                ['Manhattan','Brooklyn','Queens','Bronx','Staten Island'],
                horizontal= True,
            )       
    st.plotly_chart(md.plot_neighborhood_data(dim, fact))
    # Third section
    st.header("3) The avg prices for all room types in every Neighbourhood")
    option_2=st.radio("Select Neighbourhood Group",['Manhattan','Brooklyn','Queens','Bronx','Staten Island'], horizontal=True)
    st.plotly_chart(md.room_price(option_2))

# Price tap
with tab_Price:
    # The title and iinsiights in the tab
    st.title("Price analysis")
    st.header("This tab show the next insights : ") 
    st.write("  1- The most and least expensive Neighbourhoods.")
    st.write("  2- The mean price for verified and unconfirmed listings")
    st.write("  3- The correelation between price and other factors.")
    # First section
    st.header("1) The most expensive Neighbourhoods")
    number = st.number_input('Insert a number',value=10 ,step=1)
    st.write('The current number is: ' , number)
    st.plotly_chart(md.plot_top_prices(number))
    # Second section
    st.header("2) The least Expensive Neighbourhoods")
    num = st.number_input('Insert a num',value=5 ,step=1)
    st.write('The number is: ' , num)
    st.plotly_chart(md.plot_least_prices(num))
    # Third section
    st.header("3) The mean price for verified and unconfirmed listings")
    st.plotly_chart(md.mean_price_by_verification())
    # fourth section
    st.header("4) The below heatmap of the correlation matrix show that :-")    
    st.write("1- The correlation coefficient between price and service fee is: 1.00 which indicates a perfect positive linear relationship means that the ‘service_fee’ is directly derived from the ‘price’, perhaps being a fixed percentage of the price.")
    st.write("2- The correlation coefficient between price and [ availability_365 , calculated_host_listings_count , review_rate_number , construction_year , long ] equal to (0) which means there is no correlation between price and all of them.")
    st.plotly_chart(md.plot_correlatin())

# Minimum_nights and room_type tap
with tab_Minimum_nights_and_room_type:
    # The title and iinsiights in the tab
    st.title("Minimum_nights and Room_type analysis")
    st.header("This tab show the next insights : ") 
    st.write("  1- Entire home/apt is the most desirable room_type, and Hotel room is the least.")
    st.write("  2- The avg_price of every room type in every different Neighbourhood")
    st.write("  3- Hotel room generally require fewer minimum nights, Entire home can require high minimum nights.")
    # First section
    st.header("1) The percentage of each room type") 
    st.plotly_chart(md.show_room())
    # Second section
    st.header("2) The avg_price of every room type")
    room_option=st.radio("Select Room type",['Private room','Shared room','Hotel room','Entire home/apt'], horizontal=True)
    st.plotly_chart(md.room_type_price(room_option))
    # Third section
    st.header("3) The avg minimum nights for every room type")
    st.plotly_chart(md.plot_min_nights())

with tab_conclusion:
    st.title("Conclusion of what we see through this analysis.")
    st.header("We can see the following results:")
    st.write("1) '2014' is the highest year with Number of Rooms Constructed = '5388'.")
    st.write("2) Manhattan has the highest number of construuctions.")
    st.write("3) Staten island has less than (1%) of constructions!!")
    st.write("4) Staten island has the highest Neighbourhood avg price ('New Drop').and, the cheapest one is : 'light_house hill'!!")
    st.write("5) It doesn't matter whether the listings verified or not, Both have the same price.")
    st.write("6) The service_fee is directly derived from the price, perhaps being a fixed percentage of the price..")
    st.write("7) Entire home/apt is the most desirable room_type, and Hotel room is the least.")
    st.write("8) Hotel room generally require fewer minimum nights, Entire home can require high minimum nights.")
