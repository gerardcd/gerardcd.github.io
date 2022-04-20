import pandas as pd
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open("data_cases.json", "r") as fd:
    data = json.load(fd)

df = pd.DataFrame(data["records"])
print(df)



# Start with one review

# Create and generate a word cloud image:
freqs = {}
for _, rec in df.iterrows():
    freq = freqs.get(rec["countryterritoryCode"], 0)
    deaths = 0 if pd.isna(rec["deaths"]) else rec["deaths"]
    freqs[rec["countryterritoryCode"]] = freq + deaths

wordcloud = WordCloud(collocations=False, background_color="white").generate_from_frequencies(freqs)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('cloud.png')
plt.show()