%matplotlib inline

import pandas as pd
import matplotlib.pyplot as plt
from yelpapi import YelpAPI
from scipy import stats
from config import api_key

def get_businesses(location):
    client = YelpAPI(api_key)
    businesses = [client.search_query(location=location, limit=1, offset=i)["businesses"][0] for i in range(1000)]
    return pd.DataFrame.from_dict(businesses)

def plot_scatter(data):
    plt.scatter(data["price"], data["rating"], marker="o", facecolors="red", edgecolors="black")

def plot_boxplot(data):
    data.boxplot("rating", by="price", figsize=(10, 5))

def perform_anova(groups):
    return stats.f_oneway(*groups)

def describe_data(data):
    return data.describe()

cities = {
    "CLE": "Cleveland",
    "CBUS": "Columbus, OH",
    "CIN": "Cincinnati, OH",
    "STL": "Saint Louis, MO",
    "PORT": "Portland, OR",
    "DET": "Detroit, MI"
}

clean_data = {}

# Retrieve data for each city
for city, location in cities.items():
    raw_data = get_businesses(location)
    clean_data[city] = raw_data[['price', 'rating']].dropna().astype({"price": str})
    clean_data[city]['price_length'] = clean_data[city]['price'].apply(len)

# Scatter plot for each city
plt.figure(figsize=(10, 6))
for city, data in clean_data.items():
    plot_scatter(data)
plt.xlabel('Price')
plt.ylabel('Rating')
plt.show()

# Box plot for each city
plt.figure(figsize=(10, 6))
for city, data in clean_data.items():
    plot_boxplot(data)
plt.xlabel('Price')
plt.ylabel('Rating')
plt.show()

# Statistical analysis for each city
results = {}
for city, data in clean_data.items():
    groups = [data[data["price"] == i]["rating"] for i in range(1, 5)]
    results[city] = perform_anova(groups)

# Descriptive statistics for each city
statistics = {}
for city, data in clean_data.items():
    statistics[city] = describe_data(data)

# Box plot of Price Level 4 restaurants for each city
plt.figure(figsize=(10, 6))
four_data = [data[data["price"] == "4"]["rating"] for city, data in clean_data.items()]
plt.boxplot(four_data, labels=clean_data.keys())
plt.xlabel('City')
plt.ylabel('Star rating')
plt.show()

# Box plot of Price Level 1 restaurants for each city
plt.figure(figsize=(10, 6))
one_data = [data[data["price"] == "1"]["rating"] for city, data in clean_data.items()]
plt.boxplot(one_data, labels=clean_data.keys())
plt.xlabel('City')
plt.ylabel('Star rating')
plt.show()
