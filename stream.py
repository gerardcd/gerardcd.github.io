import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import json
from datetime import datetime
import pandas as pd
import numpy as np
from scipy import stats

with open("data_cases.json", "r") as fd:
    data = json.load(fd)

df = pd.DataFrame(data["records"])

df["month_year"] = df["year"].map(str) + "/" + df["month"].map(str)
dates = list(set(df["month_year"]))
dates.sort()

countries = list(set(df["countryterritoryCode"]))[:5]
countries.sort()

data_stacked = []
i = 0
for country in countries:
    country_record = []

    for date in dates:

        print(f"{i}/{len(countries) * len(dates)}")
        i += 1
        records = df[(df["month_year"] == date) & (df["countryterritoryCode"] == country)]

        if len(records) == 0:
            country_record.append(0)
        else:
            country_record.append(records["deaths"].sum())

    data_stacked.append(np.array(country_record))

def gaussian_smooth(x, y, grid, sd):
    x = [i for i in range(len(x))]
    weights = np.transpose([stats.norm.pdf(grid, m, sd) for m in x])
    weights = weights / weights.sum(0)
    return (weights * y).sum(1)

grid = np.linspace(0, len(dates), num=len(dates))
y_smoothed = [gaussian_smooth(dates, y_, grid, 1) for y_ in data_stacked]

fig, ax = plt.subplots(figsize=(10, 7))
#colors = ["#{val}{val}FF".format(val=hex(i)[2:].zfill(2)) for i in range(0, 255, 50)]
colors = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a"]
ax.stackplot(dates, data_stacked, colors=colors, baseline="sym")
#ax.stackplot(dates, data_stacked, baseline="sym")
ax.axhline(0, color="black", ls="--")
plt.xticks(rotation=90)
ps = [Rectangle((0, 0), 1, 1, fc=col) for col in colors]
plt.legend(ps, countries)
plt.title("Morts per COVID-19 per país i mes")
plt.savefig('stream.png')

plt.show()