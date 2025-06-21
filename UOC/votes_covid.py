import pandas as pd

#https://covid.cdc.gov/covid-data-tracker/#vaccinations_vacc-total-admin-rate-total

# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX
df = pd.read_csv("1976-2020-president.csv")
df = df[df["year"] == 2020]
idx = df.groupby(["state"], sort=False)["candidatevotes"].transform(max) == df['candidatevotes']
df[idx].to_csv("2020-president.csv")