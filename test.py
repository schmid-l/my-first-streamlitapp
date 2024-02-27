### Internet usage in percent of the population - streamlit app
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


internet_df_raw = load_data(path="./data/share-of-individuals-using-the-internet.csv")
internet_df = deepcopy(internet_df_raw)

# Add title and header
st.title("Streamlit Mini Project")
st.header("Share of individuals using the internet around the world")


# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is a slice out of the dataset:")
    st.dataframe(data=internet_df.iloc[127:135])
    # st.table(data=mpg_df)




file = open('data/countries.geojson',) 
countries = json.load(file)

#df = pd.read_csv("data/share-of-individuals-using-the-internet.csv")
#df.head()
# df.rename(columns = {"Individuals using the Internet (% of population)" : "Internet usage" }, inplace = True)

# check for one year
df_2016 = internet_df[internet_df["Year"] == 2016]
# drop
# reg_2016 = reg_2016.dropna(subset=['Code'])

st.subheader("World Map - Individuals using the Internet in % (2016)")

fig1 = px.choropleth_mapbox(df_2016,
                           geojson=countries, 
                           featureidkey = 'properties.ISO_A3', 
                           locations='Code', 
                           color='Individuals using the Internet (% of population)',
                           color_continuous_scale="Viridis",
                           range_color=(df_2016["Individuals using the Internet (% of population)"].min(), df_2016["Individuals using the Internet (% of population)"].max()),
                           mapbox_style="carto-positron",
                           zoom=1, center = {"lat": 0, "lon": 0},
                           opacity=0.5
                          )

fig1.update_layout(
    geo=dict(
        bgcolor='rgba(0,0,0,0)',  # Transparent background; replace with desired color
        showframe=False,  # Remove frame around map
        showcoastlines=True,  # Show coastlines
        projection_type='natural earth'  # Change the projection type if desired
    ),
    margin=dict(l=100, r=10, t=40, b=10),  # Adjust margins (values are in pixels)
    width = 1000
)
#fig1.update_layout(height = 750, width = 1000)


st.plotly_chart(fig1)
##################################################################################################################################################

# Setting up columns
#col1, col2 = st.columns([3, 1])

reg_2016 = df_2016[df_2016['Code'].isna()]

reg_2016 = reg_2016.sort_values(by = "Individuals using the Internet (% of population)", ascending=True)

reg_2016 = reg_2016.drop("Code", axis = 1).reset_index(drop = True)

st.subheader("Barplot for Different World Regions (2016)")

fig = px.bar(reg_2016, x = "Entity", y = "Individuals using the Internet (% of population)")
fig.update_layout(bargap=0.25)
fig.update_xaxes(tickangle=315)

st.plotly_chart(fig)

if st.checkbox("Show underlying data set as table"):
    st.subheader("This is the underlying data:")
    st.dataframe(data=reg_2016)


st.subheader("Internet in World regions - Development over time (1995 - 2016)")

region_df = internet_df[internet_df['Code'].isna()]

# lets start at 1995 and end at 2016 because of data availability
region_df = region_df[(region_df["Year"] >= 1995) & (region_df["Year"] <= 2016)]

# make a selectbox where you can select the region to display one particular region
# region_df = region_df[region_df["Entity"].isin(["Low Income", "Least developed countries: UN classification", "South Asia", "Middle Income", "Upper Middle Income", "High Income"])]

# Widgets: selectbox
# regions = ["All"]+sorted(pd.unique(region_df['Entity']))
# region = st.selectbox("Choose from selected Regions", regions)


# if region == "All":
#    reduced_df = region_df
#elif region == "Low Income":
#    reduced_df = region_df[region_df["Entity"] == "Low Income"]
#elif region == "Least developed countries: UN classification":
#    reduced_df = region_df[region_df["Entity"] == "Least developed countries: UN classification"]
#elif region == "South Asia":
#    reduced_df = region_df[region_df["Entity"] == "South Asia"]
#elif region == "Middle Income":
#    reduced_df = region_df[region_df["Entity"] == "Middle Income"]
#elif region == "Upper Middle Income":
#    reduced_df =  region_df[region_df["Entity"] == "Upper Middle Income"]
#elif region == "High Income":
#    reduced_df =region_df[region_df["Entity"] == "High Income"]

fig2 = px.line(region_df, x="Year", y="Individuals using the Internet (% of population)",
                title='Internet over Time', color='Entity')


st.plotly_chart(fig2)

# put pivoted data frame below to show time series on horizontal