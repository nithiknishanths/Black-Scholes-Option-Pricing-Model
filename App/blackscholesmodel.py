#-----------------------------------------------------------------------------
#Author  : Nithik Nishanth Sudhakar
#Date    : 03-DEC-2024
#Topic   : Black Scholes Model Implementation 
#
#
#Changelog
#20241203 - Initial Draft of Black Scholes Model with basic Parameters
#20241208 - Creating Streamlit Initialization on the Model
#20241210 - Implemented Heatmap function to show Voltality rates change on spot price
#------------------------------------Import Section------------------------------------

# Import Section
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
#-----------------------------------Page Configuration------------------------------------

st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded")
#-----------------------------------Math Function------------------------------------

def blackscholes(r, s, K, T, sigma, Type):
    # Calculate Black Scholes Option Price for CALL/PUT

    d1 = (np.log(s/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    try:
        if Type == 'C':
            price = s*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif Type == 'P':
            price = K*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - s*norm.cdf(-d1, 0, 1)

        return price

    except:
        return "Please ensure parameters are correct"
#--------------------------------Heatmap Function-----------------------------------------

def plotheatmap(spot_range, vol_range, strikeprice,r,T):
    #Plots the heatmap for a given blackscholes equation
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            currbscall = blackscholes(r, spot, strikeprice, T, vol,'C')
            currbsputt = blackscholes(r, spot, strikeprice, T, vol,'P')

            call_prices[i,j] = currbscall
            put_prices[i,j] = currbsputt

    #Plotting call Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_call)
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')


    #Plotting Putt Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_put)
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')
    
    return fig_call, fig_put


#--------------------------------SidebarSection-----------------------------------------

st.sidebar.markdown("## Black-Scholes Model")
st.sidebar.link_button("Linked In : Nithik Nishanth S ", "https://www.linkedin.com/in/nithik-nishanth-sudhakar-452137212/", help="Click Here to go to My LinkedIn")
st.sidebar.number_input("Enter Interest Rate", key="intrate", value=0.05)
st.sidebar.number_input("Enter your Underlying ß", key = "underlying", value=100)
st.sidebar.number_input("Enter your Strike price",key = "strikeprice", value=100)
st.sidebar.number_input("Enter your No of Days", key = "Days", value=365)
st.sidebar.number_input("Enter your Voltality", key="voltality", value=0.20)
st.sidebar.markdown("## Heatmap Parameters")
st.sidebar.number_input('Enter Min Current price',key="spotmin", min_value=0.01, value=st.session_state.underlying *0.8, step=0.01)
st.sidebar.number_input('Enter Min Current price', key="spotmax",min_value=0.01, value=st.session_state.underlying *1.2, step=0.01)
st.sidebar.slider('Enter Min Voltality',key="voltmin", min_value=0.01, max_value=1.0, value=st.session_state.voltality*0.5, step=0.01)
st.sidebar.slider('Enter Max Voltality', key="voltmax",min_value=0.01, max_value=1.0, value=st.session_state.voltality*1.5, step=0.01)
spot_range = np.linspace(st.session_state.spotmin, st.session_state.spotmax, 10)
vol_range = np.linspace(st.session_state.voltmin, st.session_state.voltmax, 10)

# Variables Section
r = st.session_state.intrate            # Interest
s = st.session_state.underlying             # Underlyingß
K = st.session_state.strikeprice              # Strike Price
T = st.session_state.Days / 365         # 240 Days
sigma = st.session_state.voltality         # 30% Voltality

#--------------------------------Main Section-----------------------------------------
st.title("Black Scholes Option Pricing")

colm1, colm2, colm3, colm4, colm5 = st.columns(5)
colm1.metric("Interest Rate", st.session_state.intrate)
colm2.metric("Underlying", st.session_state.underlying)
colm3.metric("Strike Price",st.session_state.underlying )
colm4.metric("Period (Years)", st.session_state.Days / 365)
colm5.metric("Voltality", st.session_state.voltality)

col1, col2 = st.columns(2)
col1.metric("CALL Price", round(blackscholes(r, s, K, T, sigma, Type='C'), 2))
col2.metric("PUT Price", round(blackscholes(r, s, K, T, sigma, Type='P'), 2))


st.title("Heatmap Strike Price vs Voltality")
col1, col2 = st.columns([1,1], gap="small")
with col1 :
    callfig = plotheatmap(spot_range, vol_range, K, r, T)[0]
    st.pyplot(callfig)

with col2 : 
    puttfig = plotheatmap(spot_range, vol_range, K, r, T)[1]
    st.pyplot(puttfig)