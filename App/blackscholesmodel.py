#-----------------------------------------------------------------------------
#Author  : Nithik Nishanth Sudhakar
#Date    : 03-DEC-2024
#Topic   : Black Scholes Model Implementation 
#
#
#Changelog
#20241203 - Initial Draft of Black Scholes Model with basic Parameters
#
#-----------------------------------------------------------------------------

# Import Section
import numpy as np
from scipy.stats import norm


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
        print("Please ensure parameters are correct")



# Variables Section
r = 0.01            # Interest
s = 30              # Underlyingß
K = 40              # Strike Price
T = 240/365         # 240 Days
sigma = 0.3         # 30% Voltality
Type = 'c'          # Call Option 

print("Option Price is: ", round(blackscholes(r, s, K, T, sigma, Type = 'P'), 2))