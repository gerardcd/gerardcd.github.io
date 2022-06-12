import pandas as pd
import json
import plotly.graph_objs as go

with open("data_cases.json", "r") as fd:
    data = json.load(fd)

df = pd.DataFrame(data["records"])

deaths = {}
for _, rec in df.iterrows():
    freq = deaths.get(rec["countryterritoryCode"], 0)
    death = 0 if pd.isna(rec["popData2020"]) else int(rec["popData2020"])
    deaths[rec["countryterritoryCode"]] = freq + death

pop = {}
cases = {}
for _, rec in df.iterrows():
    freq = cases.get(rec["countryterritoryCode"], 0)
    case = 0 if pd.isna(rec["cases"]) else rec["cases"]
    cases[rec["countryterritoryCode"]] = freq + case

    if rec["countryterritoryCode"] not in pop:
        pop[rec["countryterritoryCode"]] = int(rec["popData2020"])

countries = ["ITA", "FRA", "DEU", "POL", "ESP"]

num_cols = 30
row = 0
column = 0
data = []
for country in countries:
    init_row = row

    heads = []
    rows = []
    columns = []

    for p in range(int(pop[country] / 10**6)):
        if column == num_cols:
            row += 0.5
            column = 0
        rows.append(row)
        heads.append(row+0.18)
        columns.append(column)
        column += 1

    #data.append(go.Scatter(x=columns, y=heads, mode='markers', marker={'color': "black", 'symbol': 'circle', 'size': 10}))
    data.append(go.Scatter(x=columns, y=rows, mode='markers', marker={'color': "grey", 'symbol': 'circle', 'size': 20}, name=f"{country} població"))

    last_row = row
    row = init_row
    column = 0

    heads = []
    rows = []
    columns = []

    for case in range(int(cases[country] / 10**6)):
        if column == num_cols:
            row += 0.5
            column = 0

        heads.append(row+0.18)
        rows.append(row)
        columns.append(column)
        column += 1

    #data.append(go.Scatter(x=columns, y=heads, mode='markers', marker={'color': "blue", 'symbol': 'circle', 'size': 10}))
    data.append(go.Scatter(x=columns, y=rows, mode='markers', marker={'color': "blue", 'symbol': 'circle', 'size': 20},  name=f"{country} casos"))

    row = last_row + 1
    column = 0

fig = go.Figure(dict(data=data, layout=go.Layout(plot_bgcolor='white',
                                                 xaxis=dict(visible=False),
                                                 yaxis=dict(visible=False))))
fig.update_layout(title='Població i casos de COVID-19 per país (per milió)', title_x=0.45, title_y=0.95, font=dict(size=18))
fig.show()