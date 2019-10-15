import numpy as np
import pandas as pd
import scipy.optimize as opt
#from scipy.optimize import differential_evolution as de

# Read in the data
# Maybe use read_excel instead?
#rad_dat = pd.ExcelFile("../../Matching/radio_merger_data.xlsx")
#rad = rad_dat.parse("Sheet1")
rad = pd.read_excel("../../Matching/radio_merger_data.xlsx", sheet_name= "Sheet1",
                        header=0)

# Look at the variables in the dataframe
#for col in rad.columns:
#    print(col)

# Create lists of buyer and target characteristics
B = ['year', 'buyer_id', 'buyer_lat', 'buyer_long', 'num_stations_buyer', 'corp_owner_buyer']
T = ['target_id', 'target_lat', 'target_long', 'logk_price', 'hhi_target', 'logk_pop']

# Scale the population and price variables
rad['logk_price'] = np.log((rad['price']) / 1000)
rad['logk_pop'] = np.log((rad['population_target']) / 1000)

# Drop now-redundant coulmns
rad = rad.drop(columns = ['price', 'population_target'])

# Add a column for distances and calculate distances (note: geopy.distance.vincenty is deprecated and would no longer run,
# so used geopy.distance.geodesic instead)
from geopy import distance as dist
rad['d'] = rad.apply(lambda row: dist.geodesic((row.buyer_lat, row.buyer_long), (row.target_lat, row.target_long)), axis = 1)

# Split data into 2 markets
rad7 = rad[rad['year'] == 2007]
rad8 = rad[rad['year'] == 2008]
years = [rad7, rad8]

# Create empty matrix to be filled with the loop (or list comp)
rad_CF = pd.DataFrame()

# After spending ~10 hours trying to get a nested for loop to work, I gave up
# and found a way to do a list comprehension instead.
rad_CF = [cf[B].iloc[b].values.tolist() + cf[T].iloc[t].values.tolist() for cf in years for b in range(len(cf) - 1) for t in range(b + 1, len(cf))]
rad_CF = pd.DataFrame(rad_CF, columns = B + T)

# Create the distance column
rad_CF['d'] = rad_CF.apply(lambda row: dist.geodesic((row.buyer_lat, row.buyer_long), (row.target_lat, row.target_long)), axis = 1)

def payoffs(data, i, params):
    '''
    A function to calculate the payoffs of the mergers.

    Args:
        data: the data to be used
        i: used for iterating through the rows
        params: a list of length (2) of initial parameter estimates
    Returns:
        f: the payoff
    '''
    alpha = params[0]
    beta = params[1]

    f = data['num_stations_buyer'].iloc[i] * data['logk_pop'].iloc[i] + alpha * data['corp_owner_buyer'].iloc[i] * data['logk_pop'].iloc[i] + beta * data['d'].iloc[i]

    return(f)
# Calculate payoffs
Params = (0.6, -1)
# 2007 actual
for i in range(len(rad7)):
    freal7 = [payoffs(data = rad7, i = i, params = Params)] # there is a problem here that I cannot figure out. The error message is not helpful.

# 2008 actual
for i in range(len(rad8)):
    freal8 = [payoffs(data = rad8, i = i, params = Params)]

# Counterfactuals
for i in range(0, (len(rad7) * (len(rad7) - 1))):
    fCF7 = [payoffs(data = rad_CF, i = i, params = Params)]

for i in range((len(rad7) * (len(rad7) - 1)), len(rad_CF)):
    fCF8 = [payoffs(data = rad_CF, i = i, params = Params)]

def objective(freal7, freal8, fCF7, fCF8):
    '''
    A function to calculate the value of the objective function to be maximized

    Args:
        data:

    Returns:
        score: the score
    '''
    score = 0
    for i in [[freal7, fCF7], [freal8, fCF8]]:
        for j in range(len(i[0])):
            for k in range(len(i[0])):
                if i[0][j] + i[0][k] >= i[1][k, j] + i[1][k, (j - 1)]:
                    score = score - 1

    return(score)

results = opt.minimize(objective, Params, method = 'Nelder-Mead', options = {'maxiter': 5000})
print(results)

##############################################################
# Now the second part
def payoffs2(data, i, params):
    '''
    A function to calculate the payoffs of the mergers.

    Args:
        data: the data to be used
        i: used for iterating through the rows
        params: a list of length (2) of initial parameter estimates
    Returns:
        f: the payoff
    '''
    delta = params[0]
    alpha = params[1]
    gamma = params[2]
    beta = params[3]

    f = delta * data['num_stations_buyer'].iloc[i] * data['logk_pop'].iloc[i] + alpha * data['corp_owner_buyer'].iloc[i] * data['logk_pop'].iloc[i] + gamma * data['hhi_target']+ beta * data['d'].iloc[i]

    return(f)
