import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from streamlit_letsplot import st_letsplot
from lets_plot import *
from lets_plot.geo_data import *
import numpy as np
from scipy.interpolate import griddata
from shapely.geometry import Point
LetsPlot.setup_html()

st.title("STUDY OF INCOME DATA OF UNITES STATES")

#Sample Data
income_dat = pd.read_csv('./datasets/kaggle_income.csv', encoding='latin-1')
st.header("Sample Dataframe with all the attributes")
st.write(income_dat.head(3))

#Mean Income of US
income_dat = income_dat[~income_dat["State_Name"].isin(["Alaska", "Hawaii", "Puerto Rico"])]
income_dat = income_dat[income_dat["Mean"] > 0]
mean_US = income_dat["Mean"].describe()["mean"]
st.header("Mean US Income")
st.write(mean_US)

state_gcoder = geocode_states("US-48")
income_dat["lat"] = income_dat["Lat"]
income_dat["lon"] = income_dat["Lon"]

#US MAP PLOTTING FOR MEAN INCOME
st.header("Map according to the distributed income")
st.map(income_dat)

#Color Contrast
st.header("Scattering with a different color contrast")
p = ggplot() + geom_map(map=state_gcoder) + geom_point(aes("Lon", "Lat", color="Mean"), data=income_dat, size=1)
st_letsplot(p)

#Better Scattering
st.header("Better scattering of the Map")
fill_PiYG= scale_fill_gradient2(name="Mean income", 
                                low="#8e0152",mid="#f7f7f7",high="#276419", 
                                midpoint=mean_US)
color_PiYG = scale_color_gradient2(name="Mean income", 
                                   low="#8e0152",mid="#f7f7f7",high="#276419", 
                                   midpoint=mean_US)

# Define some setting to use on plots later on:
# - Remove axis.
# - Define plot coordinate system and size.
map_settings = (theme(axis="blank", panel_grid="blank") +
                coord_fixed(1.27) +
                ggsize(785, 350))

# Customize the tooltip.
tooltip_scatter=(layer_tooltips()
    .format('Mean', '.2s')
    .line("Mean income|$@Mean"))

p1 = (ggplot() + 
 geom_map(map=state_gcoder) +
 geom_point(aes("Lon", "Lat", color="Mean"), 
            data=income_dat, 
            size=1, 
            tooltips=tooltip_scatter) + 
 map_settings + color_PiYG)

st_letsplot(p1)

#StateWise Tile Map
st.header("Scattering Statewise according to tiles in the map")
mean_income_state = income_dat.groupby("State_Name", as_index=False)["Mean"].mean()
tooltip_state=(layer_tooltips()
          .format('Mean', '.2s')
          .title('@State_Name')
          .line('Mean income|$@Mean'))

#Create a choropleth of the mean income using our `state_gcoder`
p2 = (ggplot(mean_income_state) + 
 geom_polygon(aes(fill="Mean"), 
              # Use geocoder with a slightly better resolution for the boundaries.
              map=state_gcoder.inc_res(), 
              # Use "State_Name" value in the data as a key for joining it with the "map".
              map_join="State_Name",       
              tooltips=tooltip_state,
              color="white") + 
 map_settings + fill_PiYG)

st_letsplot(p2)

#Countywise Mean Income Tile Map
st.header("County Wise Tile Map for the whole US")
def interpolate_us(lons, lats, values, step, method):
    # method : "linear", "cubic" or "nearest".
    
    # target grid to interpolate to
    grid_lons = np.arange(-125, -66, step)
    grid_lats = np.arange(25, 52, step)
    grid_lons, grid_lats = np.meshgrid(grid_lons, grid_lats)
    
    # interpolate
    grid_values = griddata((lons, lats), values, (grid_lons, grid_lats), method)

    # lon, lat, value DataFrame
    return pd.DataFrame(dict(lon=grid_lons.flatten(), 
                           lat=grid_lats.flatten(), 
                           value=grid_values.flatten()))

X = income_dat.Lon
Y = income_dat.Lat
Z = income_dat.Mean
mean_income_interpolated = interpolate_us(X, Y, Z, step=.3, method="linear")

p3 = (ggplot(mean_income_interpolated) + 
 geom_tile(aes("lon", "lat", fill="value")) + 
 geom_map(map=state_gcoder, size=.5, color="dark_magenta") +
 map_settings + fill_PiYG)

st_letsplot(p3)

#County Wise Tile Mapping
# Apply 'spatial union' operation.
states_union = state_gcoder.get_boundaries()["geometry"]
#st.write(states_union)
# Pick the biggest polygon.
states_union = max(states_union, key=lambda p: p.area)

mask = mean_income_interpolated.apply(lambda p: states_union.contains(Point(p.lon, p.lat)), axis=1)
mean_income_interpolated_masked = mean_income_interpolated[mask]

tooltip_tiles=(layer_tooltips()
    .format('value', '.2s')
    .line("Mean income|$@value"))

#Largest State
st.header("County wise tile map scattering in the largest US state")
p5 = (ggplot(mean_income_interpolated_masked) +
 geom_livemap(zoom=6) +
 geom_tile(aes("lon", "lat", fill="value"), alpha=.7, tooltips=tooltip_tiles) + 
 map_settings + fill_PiYG)

st_letsplot(p5)
