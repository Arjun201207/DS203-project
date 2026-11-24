# DS203 Classification Project — HDI category classification (2023)

Predict a country's **project-defined HDI band** (0 Low: HDI < 0.550; 1 Medium/High: 0.550 ≤ HDI < 0.800; 2 Very High: HDI ≥ 0.800) from World Bank WDI indicators for 2023. This follows `DS203_2026_project-classification.pdf`. The three-band grouping is not an official UNDP or developed/developing classification.

## Repository layout
```
data/raw/          hdr.xlsx (UNDP HDR export, 2023), WDI_2023.csv (WDI, 2023 column only),
                   WDI_country_metadata.csv (Region etc.)
data/processed/    hdi_classification_2023.csv (fixed dataset, 193 countries), data_dictionary.md
code/              00_extract_wdi_2023.py   WDIEXCEL.xlsx -> 2023-only CSVs
                   01_build_dataset.ipynb   merge, target, DominantSector, fixed CSV + dictionary
                   02_eda.ipynb             exploratory data analysis (6 tasks)
                   03_modeling.ipynb        split, pipelines, imputation, PCA, models, evaluation, interpretation
figures/           all plots used in the report and slides
report/            report.tex, report.pdf (4 pages)
presentation/      slides.tex, slides.pdf, speaker_script.md (for the 10-min video)
```

## How to reproduce
```bash
pip install -r requirements.txt
# optional: regenerate the 2023 extract (needs the ~80 MB WDI bulk file at data/raw/WDIEXCEL.xlsx)
cd code && python 00_extract_wdi_2023.py
# run the notebooks in order (from inside code/)
jupyter nbconvert --to notebook --execute --inplace 01_build_dataset.ipynb 02_eda.ipynb 03_modeling.ipynb
```
All tables are shown in the notebook outputs. All randomness uses `random_state=42`. Tested with Python 3.12 and scikit-learn 1.9.1.

## Data sources
* **UNDP HDR 2025 data (HDI, reference year 2023)** — HDR Data Center, https://hdr.undp.org/data-center (indicator `hdi`).
* **World Bank WDI**, bulk Excel download — https://datatopics.worldbank.org/world-development-indicators/. Indicators: `NY.GDP.MKTP.KD.ZG, FP.CPI.TOTL.ZG, SL.UEM.TOTL.ZS, SP.DYN.IMRT.IN, EG.ELC.ACCS.ZS, IT.NET.USER.ZS, NV.AGR.TOTL.ZS, NV.IND.TOTL.ZS, NE.TRD.GNFS.ZS`. Region comes from the WDI `Country` sheet.
* Year rule: 2023 values only, no look-back window. Manual fix: Nauru `NRO` → `NRU`. See `data/processed/data_dictionary.md`.

## Key design decisions
* **Leakage exclusions:** HDI score and category, life expectancy, expected and mean years of schooling, and GNI per capita are never predictors. Country name and ISO3 are identifiers only.
* **Split:** stratified 60/20/20 (115/39/39 countries).
* **Preprocessing:** all steps are inside `Pipeline` + `ColumnTransformer` and fitted on training data only. Numerical: median imputation + `StandardScaler`. Categorical: explicit `"Missing"` category + `OneHotEncoder(handle_unknown="ignore")`. Mean vs median imputation and missingness indicators were compared by CV.
* **Models:** majority baseline, multinomial logistic regression, decision tree, random forest; LR and RF were also run with PCA. Tuned with stratified 5-fold `GridSearchCV` (macro-F1) on the training split; selected on the validation split; tested once.

## Headline result (held-out test set, 39 countries)
The selected model, logistic regression (C = 10), reaches accuracy 0.795, balanced accuracy 0.658 and macro-F1 0.663. The majority baseline gets accuracy 0.487 and macro-F1 0.218. Very High and Medium/High are classified well; Low (5 test countries) is the hard class. Infant mortality is the most informative feature.
