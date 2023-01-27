import json
from math import radians, pi, sin, cos, sqrt, asin
import requests
import itertools


def find_dist(latlng_1, latlng_2):
    # print(latlng_1[0],latlng_1[1])
    lat1, lon1 = radians(latlng_1[0][0]), radians(latlng_1[0][1])
    lat2, lon2 = radians(latlng_2[0][0]), radians(latlng_2[0][1])
    d = 2*6371*asin(sqrt(sin((lat2-lat1)/2)**2 + cos(lat1)
                    * cos(lat2)*sin((lon2-lon1)/2)**2))

    return round(d, 2)


file = "https://cdn.jsdelivr.net/gh/apilayer/restcountries@3dc0fb110cd97bce9ddf27b3e8e1f7fbe115dc3c/src/main/resources/countriesV2.json"

r = requests.get(file)
limit = 277500

countries = r.json()

currency_codes = [[currency['code']
                   for currency in country['currencies']]for country in countries]
currency_codes = list(itertools.chain(*currency_codes))
unique_codes = [
    val for val in currency_codes if currency_codes.count(val) == 1]

first_20 = {}
for country in countries:
    if country['population'] >= limit and any(code in unique_codes for code in [curr['code'] for curr in country['currencies']]):
        first_20[country['alpha3Code']] = []
        first_20[country['alpha3Code']].append(country['latlng'])
        first_20[country['alpha3Code']].append(country['population'])

first_20 = dict(sorted(first_20.items(), key=lambda x: x[1][1])[:20])


total_dist = 0
keys = list(first_20.keys())
# print(keys)
N = len(keys)
for i in range(N):
    for j in range(i+1, N):
        total_dist += find_dist(first_20[keys[i]], first_20[keys[j]])
total_dist = round(total_dist, 2)


print(total_dist)
