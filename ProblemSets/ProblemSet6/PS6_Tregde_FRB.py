################################################
# FRB data
################################################
import pandas as pd
import numpy as np
import requests
import json
from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
#%matplotlib inline

frburl = "https://www.federalreserve.gov/releases/g19/current/default.htm"
header = {'User-Agent': 'Mozilla/5.0'}

request = urllib.request.Request(frburl, headers=header)
page = urllib.request.urlopen(request)
soup = BeautifulSoup(page, 'lxml')
#print(soup.prettify())

table = soup.find("table", {"class": "statistics ng-scope sticky-table"})

consumerCredit = {'2014': [], '2015': [], '2016': [], '2017': [], '2018': [], '2018 Q2': [], '2018 Q3': [],
                  '2018 Q4': [], '2019 Q1': [], '2019 Q2': [], '2019 Jun': [], '2019 Jul': [], '2019 Aug': []}
for row in table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) == 13:
        consumerCredit['2014'].append(cells[0].find(text=True))
        consumerCredit['2015'].append(cells[1].find(text=True))
        consumerCredit['2016'].append(cells[2].find(text=True))
        consumerCredit['2017'].append(cells[3].find(text=True))
        consumerCredit['2018'].append(cells[4].find(text=True))
        consumerCredit['2018 Q2'].append(cells[5].find(text=True))
        consumerCredit['2018 Q3'].append(cells[6].find(text=True))
        consumerCredit['2018 Q4'].append(cells[7].find(text=True))
        consumerCredit['2019 Q1'].append(cells[8].find(text=True))
        consumerCredit['2019 Q2'].append(cells[9].find(text=True))
        consumerCredit['2019 Jun'].append(cells[10].find(text=True))
        consumerCredit['2019 Jul'].append(cells[11].find(text=True))
        consumerCredit['2019 Aug'].append(cells[12].find(text=True))

# Put data into pandas dataframe
consumerCreditDf = pd.DataFrame(consumerCredit)

# Give row indexes actual names
consumerCreditDf = consumerCreditDf.rename(index={0: "Total percent change", 1: "Revolving", 2: "Nonrevolving",
                               3: "Total flow (annual rate)", 4: "Revolving", 5: "Nonrevolving",
                               6: "Total Outstanding", 7: "Revolving", 8: "Nonrevolving",
                               9: "48-month NCL", 10: "60-month NCL",
                               11: "Credit card All accounts",
                               12: "Credit card accounts assesed interest",
                               13: "24-month personal loans", 14: "Finance co. interest rates NCL",
                               15: "Finance co. Maturity", 16: "Finance co. amount financed (dollars)"})

list = ['2014', '2015', '2016', '2017', '2018', '2018 Q2', '2018 Q3', '2018 Q4',
        '2019 Q1', '2019 Q2', '2019 Jun', '2019 Jul', '2019 Aug']

# Get rid of commas so can convert strings to float
for i,v in enumerate(list):
    consumerCreditDf[v] = consumerCreditDf[v].str.replace(',', '')



consumerCreditDf = consumerCreditDf.replace('n.a.', np.NaN)
consumerCreditDf = consumerCreditDf.replace('n.a. ', np.NaN)
consumerCreditDf = consumerCreditDf.replace(' n.a.', np.NaN)
consumerCreditDf = consumerCreditDf.replace(' n.a. ', np.NaN)
#print(consumerCreditDf)

# Convert the text in the cells to numbers
consumerCreditDf = consumerCreditDf.astype('float')
#print(consumerCreditDf.head(10))

# Transpose dataframe so columns are categories and rows are time variables
consCredDF_t = consumerCreditDf.T

consCred = consCredDF_t.plot(y = 'Total Outstanding',
                             title = "Level of Total Outstanding Consumer Credit",
                             grid = True, lw = 1, color = 'blue')
# Label the y-axis
#consCred.set_ylabel('Billions of Dollars')
# Provide name of the series for the legend
#consCred.legend(['Total Outstanding Consumer Credit'])
#plt.savefig('consCred_graph')
#plt.show()

dconsCred = consCredDF_t.plot(y = 'Total percent change',
                              title = "Percent Change in Consumer Credit",
                              grid = True, lw = 1, color = 'red')
# Label the y-axis
dconsCred.set_ylabel('Percent')
# Provide name of the series for the legend
dconsCred.legend(['Total Percent Change'])
plt.savefig('dconsCred_graph')
plt.show()
