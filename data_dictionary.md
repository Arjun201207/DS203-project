# Data dictionary — `hdi_classification_2023.csv`

Rows: 193 countries; one row per country; reference year 2023.

| Column | Role | Source code | Description | Source |
|---|---|---|---|---|
| `ISO3` | identifier | `-` | ISO 3166-1 alpha-3 code (identifier, NOT a predictor) | WDI Country sheet |
| `Country` | identifier | `-` | Country name (identifier, NOT a predictor) | WDI Country sheet |
| `Region` | categorical predictor | `-` | World Bank geographic region (7 levels) | WDI Country sheet |
| `GDP_growth` | numerical predictor | `NY.GDP.MKTP.KD.ZG` | GDP growth (annual %) | WDI, year 2023 |
| `Inflation` | numerical predictor | `FP.CPI.TOTL.ZG` | Inflation, consumer prices (annual %) | WDI, year 2023 |
| `Unemployment` | numerical predictor | `SL.UEM.TOTL.ZS` | Unemployment, total (% of labor force) (modeled ILO estimate) | WDI, year 2023 |
| `Infant_mortality` | numerical predictor | `SP.DYN.IMRT.IN` | Mortality rate, infant (per 1,000 live births) | WDI, year 2023 |
| `Electricity_access` | numerical predictor | `EG.ELC.ACCS.ZS` | Access to electricity (% of population) | WDI, year 2023 |
| `Internet_users` | numerical predictor | `IT.NET.USER.ZS` | Individuals using the Internet (% of population) | WDI, year 2023 |
| `Agriculture_VA` | numerical predictor | `NV.AGR.TOTL.ZS` | Agriculture, forestry, and fishing, value added (% of GDP) | WDI, year 2023 |
| `Industry_VA` | numerical predictor | `NV.IND.TOTL.ZS` | Industry (including construction), value added (% of GDP) | WDI, year 2023 |
| `Trade` | numerical predictor | `NE.TRD.GNFS.ZS` | Trade (% of GDP) | WDI, year 2023 |
| `DominantSector` | categorical predictor (engineered) | `-` | argmax of {Agriculture_VA, Industry_VA, 100-Agriculture_VA-Industry_VA}; missing if inputs missing or implausible | derived |
| `HDI` | target source (NOT a predictor) | `hdi` | Human Development Index value, 2023 | UNDP HDR 2025 (HDR Data Center) |
| `y` | target | `-` | 0 = Low (HDI<0.550), 1 = Medium/High (0.550<=HDI<0.800), 2 = Very High (HDI>=0.800) | derived from HDI |
| `HDI_class` | target label | `-` | Text label of y (project-defined grouping, not official) | derived |

## Sources
- UNDP Human Development Report 2025 data (HDI reference year 2023), exported from the HDR Data Center: https://hdr.undp.org/data-center (file `data/raw/hdr.xlsx`, indicator code `hdi`).
- World Bank World Development Indicators, bulk Excel download (`WDIEXCEL.xlsx`): https://datatopics.worldbank.org/world-development-indicators/ — file obtained by the group and processed on 24 Nov 2026. Region from the `Country` sheet of the same file.

## Year-selection rule
- Every predictor uses the **2023** value only. No look-back window was used, so **no values were substituted** from other years and none come after the HDI reference year. Missing 2023 values are left missing for the imputation step.

## Exclusions and manual corrections
- WDI aggregates (no `Region` in the Country sheet; 48 entries) and HDR aggregates (codes beginning `ZZ`; 11 entries) were removed.
- Manual code correction: Nauru `NRO` (UNDP) → `NRU` (ISO 3166-1, World Bank).
- 24 WDI economies have no 2023 HDI and were dropped: American Samoa, Aruba, Bermuda, British Virgin Islands, Cayman Islands, Channel Islands, Curaçao, Faroe Islands, French Polynesia, Gibraltar, Greenland, Guam, Isle of Man, Korea, Dem. People's Rep., Kosovo, Macao SAR, China, Monaco, New Caledonia, Northern Mariana Islands, Puerto Rico (US), Sint Maarten (Dutch part), St. Martin (French part), Turks and Caicos Islands, Virgin Islands (US).

## Target-leakage exclusions
- Not used as predictors: HDI score, HDI category, life expectancy, expected years of schooling, mean years of schooling, GNI per capita. Country names and ISO codes are identifiers only.