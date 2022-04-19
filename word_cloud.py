import pandas as pd
import json

with open("data_cases.json", "r") as fd:
    data = json.load(fd)

df = pd.DataFrame(data["records"])
