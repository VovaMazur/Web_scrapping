# Code written as part of Codecademy course on web scrapping with BS
# as a result dataFrame is created & populated with data parsed from the web
# few visuals are created based on the dataframe

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

webpage = requests.get("https://content.codecademy.com/courses/beautifulsoup/cacao/index.html")
soup = BeautifulSoup(webpage.content, "html.parser")

ratings = []
for i in soup.select('.Rating'):
    try:
        ratings.append(float(i.string))
    except:
        None


company_names = []
for i in soup.select('.Company'):
    company_names.append(i.string)

company_names = company_names[1:]

data = pd.DataFrame({
    'Company': company_names,
    'Ratings': ratings})

data_grouped = data.groupby(['Company']).mean()
n_larg10 = data_grouped.nlargest(10, 'Ratings')

cocoa_perc = []
for i in soup.select('.CocoaPercent'):
    try:
        cocoa_perc.append(float(i.string[:-1])/100)
    except:
        None

data['CocoaPercentage'] = cocoa_perc


fig, ax = plt.subplots(2)

ax[0].hist(data.Ratings)
ax[1].scatter(data.CocoaPercentage, data.Ratings)

z = np.polyfit(data.CocoaPercentage, data.Ratings, 1)
line_function = np.poly1d(z)
ax[1].plot(data.CocoaPercentage, line_function(data.CocoaPercentage), "r--")
plt.show()

company_loc = []
for i in soup.select('.CompanyLocation'):
    company_loc.append(i.string)

origin = []
for i in soup.select('.BroadBeanOrigin'):
    origin.append(i.string)

company_loc = company_loc[1:]
origin = origin[1:]

data['Company_Loc'] = company_loc
data['Origin'] = origin

print(data.groupby(['Company_Loc']).mean().nlargest(5, 'Ratings'))
print(data.groupby(['Origin']).mean().nlargest(5, 'Ratings'))
