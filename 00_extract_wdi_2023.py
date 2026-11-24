# Extract the 2023 column from the World Bank WDI bulk file.
# Input:  data/raw/WDIEXCEL.xlsx
# Output: data/raw/WDI_2023.csv, data/raw/WDI_country_metadata.csv
import pandas as pd

cols = ["Country Name", "Country Code", "Indicator Name", "Indicator Code", "2023"]
data = pd.read_excel("../data/raw/WDIEXCEL.xlsx", sheet_name="Data", usecols=cols)
data = data.rename(columns={"2023": "Value_2023"})
data.to_csv("../data/raw/WDI_2023.csv", index=False)

meta = pd.read_excel("../data/raw/WDIEXCEL.xlsx", sheet_name="Country")
meta.to_csv("../data/raw/WDI_country_metadata.csv", index=False)
