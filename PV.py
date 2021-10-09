'''Import all the necessary libraries'''
from datetime import datetime, time
from pvlib import solarposition
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import requests
import urllib.request, urllib.parse, urllib.error
import plotly.graph_objects as go

'''Ask the user the location and range of time'''

# Ask for the location
address=st.text_input("Introduce the location")
st.text(address)
# declare the interval of time
if address!=None:
    start_date=st.sidebar.date_input("Start date",key=str).isoformat()  
    end_date=st.sidebar.date_input("End date").isoformat()

'''Calls the API server and retrieve the data'''
# Api Key and server url
api_key = 42
serviceurl = "http://py4e-data.dr-chuck.net/json?"

# Concatenates the parametres for the API request using a dictionary
parms = dict()
parms["address"] = address
if api_key is not False: parms['key'] = api_key

# Creates a unify url and request to retrieve the data
url = serviceurl + urllib.parse.urlencode(parms)
try:
    fh=requests.get(url)
    print(f"This is the state of the request {fh}")
    if fh.status_code==200:
        fh_json=fh.json()
        location=fh_json['results'][0]['geometry']['location']
        lat=location['lat']
        lon=location['lng']
        print(f"The location is {address}, the latitud and longitud are {(lat,lon)}")
    else:
        st.error(f"Unable to get the location: {address}")
        pass   
except:
    st.error(f"Unable to get the url\n Introduce a new location")
    lat, lon = 40.4165, -3.70256
    start_date= end_date=datetime.now().ctime()
    times = pd.date_range(f'{start_date} 00:00:00', f'{end_date}', closed='left',
                        freq='H')
    

'''
 Obtain all the data
'''
if fh.status_code==200 and address!="":
    times = pd.date_range(f'{start_date} 00:00:00', f'{end_date}', closed='left',
                        freq='H')    

solpos = solarposition.get_solarposition(times, lat, lon)

# remove nighttime
solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]


''' 
Separate in four parts one for each season
'''
# Define the function
def separate_season(dates,latitud=0):
    '''This function separates the dates by season 
    depending in which hesmiphere the cursor is
    '''
    # Defines if it is in the north hemisphere or not
    if latitud >=0:
        north=True
    else:
        north=False
    # Defines the dictionary to separete by season
    seasons={"Spring":[],"Summer":[],"Autumn":[],"Winter":[]}
    # For through each date and separetes it 
    for d in dates:
        if (3,20)<(d.month,d.day)<=(6,21):
            if north:
                seasons["Spring"].append(d)
            else:
                seasons["Winter"].append(d)
        elif (6,21)<(d.month,d.day)<=(9,22):
            if north:
                seasons["Summer"].append(d)
            else:
                seasons["Autumn"].append(d)
        elif (9,22)<(d.month,d.day)<=(12,2):
            if north:
                seasons["Autumn"].append(d)
            else:
                seasons["Summer"].append(d)
        else:
            if north:
                seasons["Winter"].append(d)
            else:
                seasons["Spring"].append(d)
            pass
    return seasons

# Separates dates by season to do calculations
seasons_date=separate_season(solpos.index,lat)
# Extract from the sun position the elevation, azimuth and zenith
# and saves it to new variables, type Serie
elevation=solpos.elevation
azimuth=solpos.azimuth
zenith=solpos.zenith
example=elevation.mean() 
# Print the dataframe
st.dataframe(solpos)



''' 
---------------------------------------------------
               Plotting the graphs
---------------------------------------------------
'''

# Creates the line plot 
figura=px.line(elevation,labels={"elevation":"Degrees"},title="Plotting parameters")
figur=go.Figure(data=figura)
st.plotly_chart(figur)

#Calculates the average of the apperent_zenith and displays it
a=solpos['apparent_zenith']
a_avg=a.mean()
print(f"The value of the maximum is {a.max(skipna=True)}")
st.text(a_avg)

# Plots 

fig, ax = plt.subplots(figsize=(50, 50))
ax.plot(solpos['elevation'],label="Elevation",scalex=True,scaley=True)
ax.set_title("The title")
ax.plot(solpos['zenith'],label="Zenith")
ax.legend()
st.pyplot(fig)

B=plt.figure(2,(10,10))
fig=plt.plot(solpos['azimuth'],scalex=True,scaley=True)
plt.xlabel("degrees")
plt.title("The azimuth for each hour")
plt.legend(["Azimuth"])
st.pyplot(B)

print(f"Is (3,5) greater than (3,6) {(2,7)>(3,6)}")
