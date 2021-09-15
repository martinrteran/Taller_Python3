'''
----------------------------------------------------------
This is the proyect developed during the 'Taller de Python'
----------------------------------------------------------
'''


from datetime import datetime
from pvlib import solarposition
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import requests
import urllib.request, urllib.parse, urllib.error


# -------------------------------------------------------
# First it comes the users Interface with the selectors

# 1.- Initialize the api_keys and urls
# 1.- Select the location
# 2.- The program asks gmaps for the latitud and longitud
# 3.- It asks for the dates
# 4.- It retrieves it using PVlib
# 5.- And it graphs the one that is selected
# 6.- If the users wants it can calculated the average by hour and day of all years
#------------------------------------------------------------


# Api Key and server url
api_key = 42
serviceurl = "http://py4e-data.dr-chuck.net/json?"

# Ask the user the location, equals \n if nothing is introduce
address=st.text_input("Introduce the location")

# declare the interval of time
if address!="" and address!=None:
    start_date=st.sidebar.date_input("Start date",key=str).isoformat()
    end_date=st.sidebar.date_input("End date").isoformat()
##------------- Calls the API server and retrieve the data ----------

# Api Key and server url
api_key = 42
serviceurl = "http://py4e-data.dr-chuck.net/json?"

# Concatenates the parametres for the API request using a dictionary
parms = dict()
parms["address"] = address
if api_key is not False: parms['key'] = api_key

# Creates a unify url and request to retrieve the data
url = serviceurl + urllib.parse.urlencode(parms)
