'''
----------------------------------------------------------
This is the proyect developed during the 'Taller de Python'
----------------------------------------------------------
'''


from datetime import date, datetime
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



 
#Separate in four parts one for each season

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

'''
*OBTAIN THE DATA AND PLOT DATA ABOUT THE SUN POSITION*
------------------------------------------------------

'''

# Api Key and server url
api_key = 42
serviceurl = "http://py4e-data.dr-chuck.net/json?"

# Ask the user the location, equals \n if nothing is introduce
address=st.text_input("Introduce the location")

# Declare the title for the sidebar
st.sidebar.title("Selection panel")

# declare the interval of time
st.sidebar.subheader("Range of time")
end_date=st.sidebar.date_input("End date")
start_date=st.sidebar.date_input("Start date",key=str,max_value=end_date)
end_date=end_date.isoformat()
start_date=start_date.isoformat()

# Select the parameter
st.sidebar.subheader("Options")
options=["Elevation","Azimuth","Zenith"]
selection=["Select","Elevation","Azimuth","Zenith","All"]
param2show=st.sidebar.selectbox("Select the parameter",selection).lower()

# Selection to Show Plot or to show data frame
if param2show!='select':
    dataFlag=st.sidebar.checkbox("Show data frame")
    if param2show == "all":
        plotFlag=False
    else:
        plotFlag=st.sidebar.checkbox("Show plot")
else:
    dataFlag=False
    plotFlag=False



# -------------------------------------------------------------------
#    Run the rest of the program if an address has been introduced
# -------------------------------------------------------------------

if address!="" and address!=None:

    ##------------- Calls the API server and retrieve the data ----------
    
    # Concatenates the parametres for the API request using a dictionary
    parms = dict()
    parms["address"] = address
    if api_key is not False: parms['key'] = api_key
    
    # Creates a unify url and request to retrieve the data
    url = serviceurl + urllib.parse.urlencode(parms)

    # Request the API and if it fails it displays an error message
    try:
        st.text("Retrieving Data...")
        urlhandler=requests.get(url)
        isopen=True

        # Parse the json  
        uh_json=urlhandler.json()

        if uh_json['status']!="OK":
            st.warning(f"Unable to find the address. \tTry another one")    
        else:
            st.success("Succesfuly retrieved")
    except:
        isopen=False
        st.error("Unable to retrieve the data\nTry another location")
        pass
    


    # ------------------------------------------------------
    #     Continue if there is a Json file non-Empty       
    # -------------------------------------------------------

    if isopen == True and uh_json['status']=="OK":

        # Retrieve and separates the latitud and longitud
        # from the retrieving the data from the API
        location=uh_json['results'][0]['geometry']['location']
        lat=location['lat']
        lon=location['lng']
        # It shows the address from the API (gmaps)
        faddress=uh_json['results'][0]['formatted_address']
        st.text(f"The retrived address is {faddress}")
        st.header("Open the side panel to select the data")  
        # Is it the same day?
        if start_date==end_date:
            st.text("No data.....")
        else:

            #  -----------------------------------------------
            #               Obtaining all the data
            # -------------------------------------------------

            times = pd.date_range(f'{start_date} 00:00:00', f'{end_date}', closed='left',
                                freq='H')
            solpos = solarposition.get_solarposition(times, lat, lon)

            # remove nighttime
            solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]
            # Separates dates by season to do calculations
            seasons_date=separate_season(solpos.index,lat)



            # -----------------------------------------------------------
            #              Plot data frame if the users wants it       
            # -----------------------------------------------------------
            
            # Declare and define flags if the parameter
            # selected to plot is inside the variables
            # of the data frame
            if param2show != 'select' and param2show!='all':
                inRange=True
            elif param2show == 'all':
                inRange=False 

            # If the user wants to show the dataframe, display it
            if dataFlag is True:
                #  Display the selection
                if param2show != 'select' and param2show!='all':
                    st.dataframe(solpos[param2show])
                elif param2show == 'all':
                    st.dataframe(solpos)     

            # Creates the line plot if the users wants it
            # and only if it is in the range
            if plotFlag is True and inRange is True:
                figura=px.line(solpos[param2show],labels={param2show:"Degrees"},title="Plotting parameters")
                figur=go.Figure(data=figura)
                st.plotly_chart(figur)


            # ----------------------------------------------------------
            #              Calculates the mean and std desviation
            #                   by what the users decides
            # ----------------------------------------------------------

            #Continue


    
else:
    st.title("Waiting for a location")
