# Data Cleaning Scripts

This folder contains all data cleaning and processing scripts for the India Market Segmentation project.

## Folder Structure

```
scripts/data_cleaning/
├── clean_ec05_shrid.py           # Economic Census 2005 data cleaning
├── clean_ec98_shrid.py           # Economic Census 1998 data cleaning
├── clean_ec13_shrid.py           # Economic Census 2013 data cleaning
├── run_all_cleaning.py           # Master script to run all cleaning tasks
├── README.md                     # This file
└── [future cleaning scripts]
```

## Output Location

All cleaned files are saved to:
```
data/processed/cleaned_files/
├── ec05_shrid_simplified.csv               # Main cleaned EC05 data
├── ec05_shrid_summary_stats.csv            # Statistical summaries
├── ec05_shrid_column_documentation.csv     # Column documentation
└── [future cleaned files]
```

## Data Cleaning Approach

### Industry Group Consolidation
- **Original**: 90 individual SHRIC employment columns (SHRIC 1-90)
- **Simplified**: 14 meaningful industry categories for market segmentation

### Industry Categories:
1. **Primary Industries** (SHRIC 1-4): Forestry, fishing, mining
2. **Food & Agriculture** (SHRIC 5-12): Food processing, beverages, dairy
3. **Manufacturing Traditional** (SHRIC 13-17, 24): Textiles, clothing, wood
4. **Manufacturing Industrial** (SHRIC 18-27): Chemicals, pharma, metals, steel
5. **Manufacturing Consumer** (SHRIC 28-32): Electronics, appliances, furniture
6. **Utilities & Infrastructure** (SHRIC 33-38): Power, construction, water
7. **Automotive & Transport** (SHRIC 39-41, 53-61): Auto, logistics, travel
8. **Wholesale Trade** (SHRIC 42-46): Business-to-business commerce
9. **Retail & Consumer** (SHRIC 47-52): Retail stores, restaurants, hotels
10. **Communication & Digital** (SHRIC 62-64, 73): Telecom, IT, software
11. **Financial Services** (SHRIC 65-69): Banking, insurance, real estate
12. **Business Services** (SHRIC 70-79, 87): Legal, accounting, consulting
13. **Social Services** (SHRIC 80-85): Education, healthcare, social work
14. **Entertainment & Culture** (SHRIC 84-90): Arts, media, personal services

### Market Segmentation Features Created:
- **Economic Diversity Score**: Number of industry sectors present
- **Non-farm Employment Ratio**: % working outside agriculture
- **Firm Density**: Businesses per 1000 workers
- **Employment per Firm**: Average firm size
- **Retail Diversity**: Presence of trade/retail sectors
- **Service Sophistication Score**: Advanced service sectors present
- **Female Employment Ratio**: Gender equality measure
- **Formal Employment Ratio**: % in government/private vs informal

## Data Reduction Results

### EC05 (Economic Census 2005):
- **Original columns**: 137 → **Simplified columns**: 38 (72.3% reduction)
- **Records**: 517,389 geographic units

### EC98 (Economic Census 1998):
- **Status**: Ready for cleaning
- **Expected reduction**: ~72% (similar to EC05)

### EC13 (Economic Census 2013):
- **Status**: Ready for cleaning  
- **Expected reduction**: ~72% (similar to EC05)

### **Key improvements for all datasets**: 
  - Removed 99+ unnecessary columns per dataset
  - Grouped 90 SHRIC codes into 14 categories
  - Created 8 derived market segmentation indicators
  - Preserved all essential identifiers and core employment data

## Usage Instructions

1. **Run individual cleaning script**:
   ```bash
   cd scripts/data_cleaning
   python clean_ec05_shrid.py
   python clean_ec98_shrid.py
   python clean_ec13_shrid.py
   ```

2. **Run all cleaning scripts at once**:
   ```bash
   cd scripts/data_cleaning
   python run_all_cleaning.py
   ```

3. **Check output**:
   - Main files: `data/processed/cleaned_files/*_simplified.csv`
   - Documentation: `data/processed/cleaned_files/*_column_documentation.csv`
   - Statistics: `data/processed/cleaned_files/*_summary_stats.csv`
   - Summary report: `data/processed/cleaned_files/economic_census_summary.csv`

## For Market Segmentation Analysis

The cleaned data is optimized for the three-tier India market classification:

- **India 1 (Top 5% Affluent)**: High service sophistication, financial services, formal employment
- **India 2 (Next 25% Aspirational)**: Manufacturing diversity, retail presence, communication/digital
- **India 3 (Bottom 70% Mass Market)**: Primary industries, informal employment, lower diversity

## Next Steps

1. Clean all Economic Census files (EC98, EC05, EC13) using `run_all_cleaning.py`
2. Integrate all cleaned datasets for cross-temporal analysis
3. Proceed to Phase 2A: Feature engineering for machine learning models
