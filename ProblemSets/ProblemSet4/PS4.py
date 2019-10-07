import numpy as np
import pandas as pd
#from scipy.optimize import differential_evolution as de

# Read in the data
# Maybe use read_excel instead?
#rad_dat = pd.ExcelFile("../../Matching/radio_merger_data.xlsx")
#rad = rad_dat.parse("Sheet1")
rad = pd.read_excel("../../Matching/radio_merger_data.xlsx", sheet_name= "Sheet1",
                        header=0)
#print(rad)

# Look at the variables in the dataframe
#for col in rad.columns:
#    print(col)

# Look at a summary of the data
#rad.describe()

# Scale the population and price variables
rad['logk_price'] = np.log((rad['price']) / 1000)
rad['logk_pop'] = np.log((rad['population_target']) / 1000)
# Check the new variables to make sure they are as expected
#rad['logk_price'].describe()
#rad['logk_pop'].describe()

# Define the variables to be used in the payoff equation
#x1 = rad['num_stations_buyer']
#y = rad['population_target']
#x2 = (rad['corp_owner_buyer'] == 1).astype(int)

# Create new dataframe to be filled with all of the comparisons
for i in rad.buyer_id:
    for j in rad.target_id:
        rad_DF = pd.DataFrame([rad.year, rad.buyer_id[i], rad.target_id[j], rad.logk_pop, rad.logk_price, 
                               rad.num_stations_buyer, rad.corp_owner_buyer])
                               # rad.num_stations_buyer and rad.corp_owner_buyer appear to be the problems...

#print(rad_DF)
## Need to append the distances


############################################################
# Next steps:
# -Create new dataframe with all (2,421) of the comparisons
# -Loop for making the "distance" variable for each comparison (using \
#       geopy.distance.vincenty)
# -Create function that computes the payoffs
# -Define the objective function to be maximized
# -Optimization routine to find the Maximum Score Estimates of the objective
# -Repeat for the model with transfers
############################################################
