# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 16:45:12 2022
@author: Cedric Fleury, Damian Buess, Fabio Bohren
"""

##########################################################
# Section 1: Load Libraries, the data and prediction model
##########################################################

# Import all the needed libraries
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import pydeck as pdk
from pydeck.types import String
import pickle
from PIL import Image
import copy

# Defining some general properties for the application
st.set_page_config(
    page_title= "Airbnb Pricing App",
    page_icon = "🏘️",
    layout="wide")

# Change design of default settings from streamlit like the menu bar, footer and header.
hide_header_style = """
   <style>
   #MainMenu {visibility: hidden;}
   footer {visibility: hidden;}
   div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
    div.block-container{
        padding-top:1rem;
        padding-bottom:1rem;
        }
    h1{padding:0rem;}
    div.css-1adrfps {padding-top:1rem;}
   </style>
   """

# Execute the design settings "hide_header_style" with st.markdown
st.markdown(hide_header_style, unsafe_allow_html=True)

# Caches the following function
@st.cache(allow_output_mutation=True)
# Loads the main dataset for the appliction 
def load_data():
    df = pd.read_csv("airbnb_data_dev.csv", nrows=20000)
    df = df.drop(["host_id"],axis=1)
    # Here we also add a column "icon_data" which will be used in the a map
    # Each row gets a different marker with a different colour according to its price
    df['icon_data']= None
    icon_data_1 = {
        "url": "https://img.icons8.com/ios-filled/50/1a9641/marker.png",
        "width": 80,
        "height":80,
        "anchorY": 100
    }
    icon_data_2 = {
        "url": "https://img.icons8.com/ios-filled/50/a6d96a/marker.png",
        "width": 80,
        "height":80,
        "anchorY": 100
    }
    icon_data_3 = {
        "url": "https://img.icons8.com/ios-filled/50/ffffbf/marker.png",
        "width": 80,
        "height":80,
        "anchorY": 100
    }
    icon_data_4 = {
        "url": "https://img.icons8.com/ios-filled/50/fdae61/marker.png",
        "width": 80,
        "height":80,
        "anchorY": 100
    }
    icon_data_5 = {
        "url": "https://img.icons8.com/ios-filled/50/d7191c/marker.png",
        "width": 80,
        "height":80,
        "anchorY": 100
    }
    # We group them +/- according to the distribution.
    for i in df.index:
        if df['price'][i] < 50:
            df['icon_data'][i] = icon_data_1
        elif df['price'][i] < 100:
            df['icon_data'][i] = icon_data_2
        elif df['price'][i] < 150:
            df['icon_data'][i] = icon_data_3
        elif df['price'][i] < 200:
            df['icon_data'][i] = icon_data_4
        else:
            df['icon_data'][i] = icon_data_5
    return(df)

# Loads the transformed data on which the prediction model was built
@st.cache()
def load_prediction_data():
    prediction_data = pd.read_csv("airbnb_prediction_data.csv", nrows=20000)
    return(prediction_data)

# Loads the trained model for the price prediction
@st.cache(allow_output_mutation=True)
def load_model():
    filename = "finalized_model.sav"
    loaded_model = pickle.load(open(filename, "rb"))
    return(loaded_model)

# Loads the image for the head of the page
@st.cache()
def load_image():
    image = Image.open('Skyline.png')
    return(image)

# Call the load function
df = load_data()
df_predict = copy.deepcopy(load_prediction_data())
model = load_model()
image = load_image()


##########################################################
# Section 2: Additional preparation for the program
##########################################################

# Load all the names of the neigborhoods in the datasets
@st.cache()
def create_brooklyn_list():
    df_brooklyn = df.loc[df["neighbourhood_group"] == "Brooklyn",:]
    brooklyn_list = df_brooklyn['neighbourhood'].unique().tolist()
    return brooklyn_list

@st.cache()
def create_manhattan_list():
    df_manhattan = df.loc[df["neighbourhood_group"] == "Manhattan",:]
    manhattan_list = df_manhattan['neighbourhood'].unique().tolist()
    return manhattan_list

@st.cache()
def create_queens_list():
    df_queens = df.loc[df["neighbourhood_group"] == "Queens",:]
    queens_list = df_queens['neighbourhood'].unique().tolist()
    return queens_list

@st.cache()
def create_bronx_list():
    df_bronx = df.loc[df["neighbourhood_group"] == "Bronx",:]
    bronx_list = df_bronx['neighbourhood'].unique().tolist()
    return bronx_list

@st.cache()
def create_staten_island_list():
    df_staten = df.loc[df["neighbourhood_group"] == "Staten Island",:]
    staten_list = df_staten['neighbourhood'].unique().tolist()
    return staten_list

# Call the functions to store the lists
brooklyn_neighbourhoods = create_brooklyn_list()
manhattan_neighbourhoods = create_manhattan_list()
queens_neighbourhoods = create_queens_list()
staten_island_neighbourhoods = create_staten_island_list()
bronx_neighbourhoods = create_bronx_list()

# Function used in the filtering section (see below for explanation)
def check_borough(neighbourhood_group_filter):
    filter_options = []
    if "Brooklyn" in neighbourhood_group_filter:
        filter_options.extend(brooklyn_neighbourhoods)
    if "Manhattan" in neighbourhood_group_filter:
        filter_options.extend(manhattan_neighbourhoods)
    if "Bronx" in neighbourhood_group_filter:
            filter_options.extend(bronx_neighbourhoods)
    if "Queens" in neighbourhood_group_filter:
            filter_options.extend(queens_neighbourhoods)
    if "Staten Island" in neighbourhood_group_filter:
            filter_options.extend(staten_island_neighbourhoods)
    return filter_options


##########################################################
# Section 3: Header of the Dashboard
##########################################################

# Insert blank line at the top
st.markdown('#')
# Add a title + anchor and a title image
st.title("  \n  Airbnb Pricing Dashboard for NYC", anchor="Start")
st.image(image,use_column_width="always",)

# Add an expandable page description with links to the corresponding section
with st.expander("See Page Description"):
     st.markdown("This Streamlit dashboard is built to help real estate owners in New York City to price their properties on Airbnb.  \nFor this reason the first part of this dashboard [Explore Data!](#ExploreData) is to analyse the market and see how it reacts to different factors like neighbourhood or room type.  \nIf you now have analyzed the market and know which property you want to place on Airbnb or already knew it, the second part [Price prediction](#Priceprediction) helps you with pricing it. Our intelligent machine learning algorithm which uses a random forest regressor can estimate an appropriate market price for your specific property!", unsafe_allow_html=True)


##########################################################
# Section 4: Filter Section
##########################################################

# Create a header for the filter panel
st.sidebar.header("Filter Panel")

# Creates a slider for selecting the price 
price = st.sidebar.slider("Rent Price:",
                  int(df["price"].min()),
                  int(df["price"].max()),
                  (0, 1000))

# Creates a slider for selecting the number of reviews 
reviews = st.sidebar.slider("Number of reviews:",
                  int(df["number_of_reviews"].min()),
                  int(df["number_of_reviews"].max()),
                  (0, 629))

# Creates a Multiselectbox for selecting the Neighbourhood Group
neighbourhood_group_filter = st.sidebar.multiselect("Select Borough", sorted(df["neighbourhood_group"].unique()), 
                                                    default=df["neighbourhood_group"].unique())
# Calls the check_borough function definied above
# The function looks up all the neighborhoods belonging to the selected neighborhood groups.
# As a result, only the neighbourhoods of the selected groups are available in the filter option.
filter_options = check_borough(neighbourhood_group_filter)

# Creates a Multiselectbox for selecting the Neighbourhood. 
# Add an option for "All" which will be defined in the next lines.
neighbourhood_filter = st.sidebar.multiselect("Select Neighbourhood", options=["All"] + sorted(filter_options), default="All")                                      

# After adding the option for all, here we define what the option does. 
# In this case it stores all neighbourhoods in neighbourhood_filter
if "All" in neighbourhood_filter:
    neighbourhood_filter = sorted(filter_options)

# Creates a Selectbox for selecting the room Type
room_type_filter = st.sidebar.multiselect("Select room type", sorted(df["room_type"].unique()), default=df["room_type"].unique())

# Creates a filtered data set according to the inputs of the filters
filtered_df = df.loc[(df["price"] >= price[0]) & 
                     (df["price"] <= price[1]) &
                     (df["number_of_reviews"] >= reviews[0]) &
                     (df["number_of_reviews"] <= reviews[1]) &
                     (df["neighbourhood_group"].isin(neighbourhood_group_filter)) &
                     (df["neighbourhood"].isin(neighbourhood_filter)) &
                     (df["room_type"].isin(room_type_filter)),:]


##########################################################
# Section 5: Explore Data Section
##########################################################

# Create a header for the section
st.header("  \nExplore Data!", anchor="ExploreData")

# Infobox including the following string
with st.expander("See Section Description"):
     st.markdown("This section provides insights about the Airbnb market in New York, based on the selection filters on the left side. First, the KPIs provide a general description of the accomodations selected. Second, the distribution of the selected group is visualized with plots. Third, the maps provide information on the price range and individual prices of Airbnb in certain areas.")


# KPIs
##########################################################

st.subheader("KPIs")
with st.expander("See KPI Description"):
     st.markdown("The KPIs provide insights about the situation of New York's Airbnb market, based on the selection filters on the left side. ")

# Creating the three columns, to store elements
col1, col2, col3 = st.columns(3)

# Creating a red box entailing the bolt string and the division of filtered number of accomodations divided by total number of accomodations round by to digits, multiplied by 100, and adding a percent sign
col1.error("**Number of Selected Accomodations**  \n"+str(round((len(filtered_df)/len(df))*100,2))+ " %")

# Creating a red box entailing the bolt string and the average price of the filtered df in USD
col2.error("**Average Price with Selected Criteria**  \n"+str(round((filtered_df['price'].mean()),2))+" USD vs. overall " +str(round((df['price'].mean()),2))+" USD")

# Creating a red box entailing the bolt string and the average reviews per month of the filtered df.
col3.error("**Average Reviews per Month**  \n"+(str(round(filtered_df["reviews_per_month"].mean(),2)))+" vs. overall "+(str(round(df["reviews_per_month"].mean(),2)))+ " reviews per month")

# Plots
##########################################################

st.subheader("Plots")
with st.expander("See Plot Description"):
     st.markdown("The plots provide insights about the distribution of the data considering price, room type, and number of accomodations, based on the selection filters on the left side. ")
# Main charts. Created with plotly: https://plotly.com/python/bar-charts/
# Creating the three columns
row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])

# Chart 1
# Creation of a histogram with the price on the x axis and the amount of accomodations on the y axis. 
# Add a title and update the axis labels
fig = px.histogram(filtered_df, x="price", title="<b>Price Distribution</b>",color_discrete_sequence=['indianred'])
fig.update_xaxes(title_text='<b>Price</b>')
fig.update_yaxes(title_text='<b>Amount</b>')
# Plot the figur in the created container row1_col1
chart_1 = row1_col1.plotly_chart(fig, use_container_width=True)

# Chart 2
# Creation of a histogram with the room type on the x axis and the averagge price on the y axis.
fig = px.histogram(filtered_df, x='room_type', y='price',histfunc='avg', title="<b>Avg. Price per Room Type</b>",color_discrete_sequence=['indianred'])
fig.update_xaxes(title_text='<b>Room type</b>',tickangle = -45,)
fig.update_yaxes(title_text='<b>Average Price</b>')
# Plot the figur in the created container row1_col2
chart_2 = row1_col2.plotly_chart(fig, use_container_width=True)

# Chart 3
# Creation of a histogram with the room type on the x axis and the number of accomodations on the y axis.
fig = px.histogram(filtered_df, x='room_type',histfunc='count', title="<b>Room Type Distribution</b>",color_discrete_sequence=['indianred'])
fig.update_xaxes(title_text='<b>Room type</b>',tickangle = -45,)
fig.update_yaxes(title_text='<b>Amount</b>')
# Plot the figur in the created container row1_col3
chart_3 = row1_col3.plotly_chart(fig, use_container_width=True)

# Maps
##########################################################

st.subheader("Price Heatmap")
with st.expander("See Heatmap Description"):
     st.markdown("The Heatmap provides insights about where prices of accomodations are the highest on a map of New York City, based on the selection filters on the left side. The darker red the area on the map, the higher are the prices, the lighter yellow the area, the lower are the prices.")

# Create the initial view state for both maps which will be updated each time we change the filter
# Pitch = pitch of the map. view_proportion = zoom on 95% of the data.
# If the filters exclude all listings -> number of rows of filtered_df = 0, we take the mean from the unfiltered dataset df. Otherwise it would throw an error, because we can't calculate the mean of no data
if filtered_df.shape[0]==0:
    initial_view_state = pdk.ViewState(
        latitude=np.mean(df['latitude']),
        longitude=np.mean(df['longitude']),
        view_proportion=0.95,
        pitch=10,
        )
    
# If there is a filter selected zoom to the mean long and lat of the filtered data.
else:
    initial_view_state = pdk.ViewState(
        latitude=np.mean(filtered_df['latitude']),
        longitude=np.mean(filtered_df['longitude']),
        view_proportion=0.95,
        pitch=10,
        )

# Map 1 (Create a Map with pydeck: https://deckgl.readthedocs.io/en/latest/index.html)
st.pydeck_chart(
    # Define setting for the map
    pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     # Define the inital view state     
     initial_view_state=initial_view_state,
     # Define the layer(s) on the map. Here the map shows a heatmap layer where the price defines the colour intensity
     layers=[         
         pdk.Layer(
             "HeatmapLayer",
            filtered_df,
            opacity=0.6,
            get_position=["longitude", "latitude"],
            aggregation=String('MEAN'),
            get_weight="price"
         ),
     ],
 ))

st.subheader("Detailed Map")
with st.expander("See Detailed Map Description"):
     st.markdown("The Detailed Map provides insights about the specific prices of the accomodations at a certain location on a map of New York City, based on the selection filters on the left side. The colours represent the price per night.")

# Legend & source of the icon
# Div class row -> all child div are in one line.
# Then show each icon with the corresponding value which was defined at the beggining of the script
st.markdown("""
            <div class="row">
              <div style="float: left;"> <b> Legend:  </b></div>
              <img src="https://img.icons8.com/ios-filled/25/1a9641/marker.png" style="float: left;">
              <div style="float: left;"> <50 </div>
              <img src="https://img.icons8.com/ios-filled/25/a6d96a/marker.png" style="float: left;">
              <div style="float: left;"> <100 </div>
              <img src="https://img.icons8.com/ios-filled/25/ffffbf/marker.png" style="float: left;">
              <div style="float: left;"> <150 </div>
              <img src="https://img.icons8.com/ios-filled/25/fdae61/marker.png" style="float: left;">
              <div style="float: left;"> <200 </div>
              <img src="https://img.icons8.com/ios-filled/25/d7191c/marker.png" style="float: left;">
              <div style="float: left;"> >200 </div>
            </div>
            <br>
            <div>
              <a target="_blank" href="https://icons8.com/icon/7880/location" style="font-size:8px;">Location icon by Icons8</a>
            </div>
            """, unsafe_allow_html=True)

# Map 2
st.pydeck_chart(
    # Define setting for the map
    pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     # Define the same inital view state     
     initial_view_state=initial_view_state,
     # Define the layer(s) on the map. 
     # Here the map shows a Iconlayer where each Icon represents one listing in the filtered dataset.
     layers=[         
         pdk.Layer(
             "IconLayer",
            filtered_df,
            # Get the column icon data from the filtered_df which holds a dictionary with all information to display the icon (defined at the beginning)
            get_icon='icon_data',
            get_position=["longitude", "latitude"],
            get_size=4,
            # Needs to be true for the tooltip
            pickable=True,
            size_scale=10,
         ),
     ],
     # Define the tooltip per icon with html and css
     tooltip= {
         "html": "<b>Airbnb ID:</b> {id} <br/> <b>Neighbourhood Group:</b> {neighbourhood_group} <br/> <b>Neighbourhood:</b> {neighbourhood} <br/> <b>Room type:</b> {room_type} <br/> <b>Price:</b> {price}",
         "style": {
                "backgroundColor": "black",
                "opacity": 0.8,
                "color": "white"
         }
     },
 ))

# Create an expander with a subheader and the table
# with st.expander("Show Detailed data"):
#    st.subheader("Dataset")
#    st.dataframe(filtered_df)


##########################################################
# Section 6: Prediction section
##########################################################

# Header and markdown for this section
st.header("  \nPrice prediction", anchor="Priceprediction")
st.markdown("Please fill in the **information about your listing** to predict the **best** listing price:")

# HUD for the prediction section
##########################################################

# Creates four columns to store the elements
row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])

# Creates a selectbox for selecting the neighbourhood
neighbourhood_pred = row1_col1.selectbox("Neighbourhood:", sorted(df["neighbourhood"].unique()))

# Creates a selectbox for selecting the room Type
room_type_pred = row1_col2.selectbox("Room Type:", sorted(df["room_type"].unique()))

# Creates a input field for the number of reviews
reviews_pred = row1_col3.number_input("Number Of Reviews:",min_value=0,step=1)

# Creates a input field for the minimum nights
minimum_nights_pred = row1_col1.number_input("Minimum Nights:",min_value=1,step=1)

# Creates a input field for the amount of listings
listings_pred = row1_col2.number_input("Total number of your listings:",min_value=1,step=1)

# Creates a input field for the availability
availability_pred = row1_col3.slider("Availability per year:",min_value=0, max_value=365,step=1)
st.write("#")

# Function to select the borough according to the selected neighbourhood
def select_borough(neighbourhood_pred):
    if neighbourhood_pred in brooklyn_neighbourhoods:
        return "Brooklyn"
    elif neighbourhood_pred in manhattan_neighbourhoods:
        return "Manhattan"
    elif neighbourhood_pred in queens_neighbourhoods:
        return "Queens"
    elif neighbourhood_pred in staten_island_neighbourhoods:
        return "Staten Island"
    elif neighbourhood_pred in bronx_neighbourhoods:
        return "Bronx"


# Functions to execute the prediction
##########################################################

# Stores the selected input values for the prediction in a new dataframe
def create_pred_df():
    d = {'minimum_nights': int(minimum_nights_pred), 'number_of_reviews': int(reviews_pred),
         'availability_365': int(availability_pred), 'calculated_host_listings_count': int(listings_pred), 
         'neighbourhood_group': select_borough(neighbourhood_pred), # Calls select function above
         'neighbourhood': neighbourhood_pred, 'room_type': room_type_pred}
    input_data = pd.DataFrame(data=d,index=[0])
    # Creates dummies for the features
    input_data = pd.get_dummies(input_data, prefix=['room_type', 'neighbourhood_group','neighbourhood'], 
                                columns=['room_type','neighbourhood_group','neighbourhood']) 
    return input_data

# Prepares the dataframe to use in the prediction model
def prepare_pred_df(input_data): 
    # Puts the input data into the existing prdiction df
    df_predict.loc[input_data.index, :] = input_data[:]
    # Deletes the other entries 
    pred_data = df_predict.iloc[[0]]
    # Drops the price and fills missing values
    pred_data = pred_data.drop("price",axis=1)
    pred_data = pred_data.fillna(value=0) 
    return pred_data

# Uses the imported model to predict the price
def make_prediction(pred_data):
    prediction = model.predict(pred_data)
    price_output = str(int(prediction[0])) + " USD"
    st.write("#")    
    st.metric(label="Estimated Price:", value=price_output)

# Creates a button to start the prediction
if st.button("Start Prediction"):
    # Calls the function to get the input data
    input_data = create_pred_df()
    # Calls the function to prepare the prediction df
    pred_data = prepare_pred_df(input_data)
    # Executes the prediction
    pred_price = make_prediction(pred_data)

# Create a link to get back to the top of the page
st.markdown("[Back to the top](#Start)", unsafe_allow_html=True)
