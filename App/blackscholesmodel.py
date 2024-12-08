#-----------------------------------------------------------------------------
#Author  : Nithik Nishanth Sudhakar
#Date    : 03-DEC-2024
#Topic   : Black Scholes Model Implementation 
#
#
#Changelog
#20241203 - Initial Draft of Black Scholes Model with basic Parameters
#
#------------------------------------Import Section------------------------------------

# Import Section
import streamlit as st
import numpy as np
from scipy.stats import norm

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
#-----------------------------------------------------------------------------


#--------------------------------Main Section-----------------------------------------
st.write ("Black Scholes Option Pricing Model")

st.number_input("Enter Interest Rate", key="intrate")
st.number_input("Enter your Underlying ß", key = "underlying")
st.number_input("Enter your Strike price",key = "strikeprice")
st.number_input("Enter your No of Days", key = "Days")
st.number_input("Enter your Voltality", key="voltality")
st.text_input("CALL/PUTT", key="CallPutt")


# Variables Section
r = st.session_state.intrate            # Interest
s = st.session_state.underlying             # Underlyingß
K = st.session_state.strikeprice              # Strike Price
T = st.session_state.Days / 365         # 240 Days
sigma = st.session_state.voltality         # 30% Voltality
Type = st.session_state.CallPutt          # Call Option 

st.write("Option Price is: ", round(blackscholes(r, s, K, T, sigma, Type = 'P'), 2))