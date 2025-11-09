"""
Script to clean and simplify ec05_shrid.csv file for market segmentation
Groups 90 SHRIC codes into meaningful industry categories
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Define paths
RAW_DATA_DIR = Path(r"d:\BDA_project\BDA_project\prithvi_rand\IndiaMarketProject\data\raw")
PROCESSED_DATA_DIR = Path(r"d:\BDA_project\BDA_project\prithvi_rand\IndiaMarketProject\data\processed")
CLEANED_FILES_DIR = Path(r"d:\BDA_project\BDA_project\prithvi_rand\IndiaMarketProject\data\processed\cleaned_files")
SHRIC_DESC_FILE = Path(r"d:\BDA_project\BDA_project\prithvi_rand\shric_descriptions.csv")

# Ensure directories exist
PROCESSED_DATA_DIR.mkdir(exist_ok=True)
CLEANED_FILES_DIR.mkdir(exist_ok=True)

def define_industry_groups():
    """Define industry groupings based on SHRIC codes for market segmentation"""
    
    industry_groups = {
        # Primary Industries (Agriculture, Mining, Extraction)
        'primary_industries': [1, 2, 3, 4],  # Forestry, Fishing, Oil/Gas, Mining
        
        # Food & Agriculture Processing 
        'food_agriculture': [5, 6, 7, 8, 9, 10, 11, 12],  # Meat, Oil, Dairy, Grain, Food, Beverages, Tobacco
        
        # Manufacturing - Traditional
        'manufacturing_traditional': [13, 14, 15, 16, 17, 24],  # Textiles, Clothing, Leather, Footwear, Wood, Stone/Cement
        
        # Manufacturing - Industrial
        'manufacturing_industrial': [18, 19, 20, 21, 22, 23, 25, 26, 27],  # Printing, Coke, Petroleum, Pharma, Chemicals, Fibers, Iron/Steel, Metals, Casting
        
        # Manufacturing - Consumer Goods
        'manufacturing_consumer': [28, 29, 30, 31, 32],  # Appliances, Electronics, Transport Equipment, Furniture, Sporting
        
        # Utilities & Infrastructure
        'utilities_infrastructure': [33, 34, 35, 36, 37, 38],  # Power, Gas, Water, Construction, Building, Installation
        
        # Automotive & Transport Services
        'automotive_transport': [39, 40, 41, 53, 54, 55, 56, 57, 58, 59, 60, 61],  # Auto repair/sales/fuel, Transport modes, Storage, Travel
        
        # Wholesale Trade
        'wholesale_trade': [42, 43, 44, 45, 46],  # Various wholesale categories
        
        # Retail & Consumer Services
        'retail_consumer': [47, 48, 49, 50, 51, 52],  # Retail, Personal goods repair, Hotels, Restaurants
        
        # Communication & Digital
        'communication_digital': [62, 63, 64, 73],  # Postal, Courier, Telecoms, IT/Software
        
        # Financial Services
        'financial_services': [65, 66, 67, 68, 69],  # Banking, Insurance, Financial services, Real estate
        
        # Business Services
        'business_services': [70, 71, 72, 74, 75, 76, 77, 78, 79, 87],  # Equipment rental, Manufacturing services, Research, Legal, Accounting, Testing, Advertising, HR, Professional services
        
        # Social Services (High market sophistication indicator)
        'social_services': [80, 81, 82, 83, 85],  # Education, Health, Veterinary, Social work, Community services
        
        # Entertainment & Culture (Premium market indicator)
        'entertainment_culture': [84, 86, 88, 89, 90],  # Sanitation, Arts, Libraries, Broadcasting, Personal services
    }
    
    return industry_groups

def load_and_clean_ec05_data():
    """Load and clean the ec05_shrid.csv file"""
    
    # Load the data
    file_path = RAW_DATA_DIR / "shrug-ec05-csv" / "ec05_shrid.csv"
    print(f"Loading data from {file_path}")
    
    # Read data in chunks to handle large file
    chunk_size = 10000
    chunks = []
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunks.append(chunk)
    
    df = pd.concat(chunks, ignore_index=True)
    print(f"Loaded {len(df):,} records with {len(df.columns)} columns")
    
    return df

def simplify_ec05_data(df):
    """Simplify the EC05 data by grouping SHRIC codes and removing unnecessary columns"""
    
    print("Starting data simplification...")
    
    # 1. Keep essential identifier and aggregate columns
    core_columns = [
        'shrid2',                    # Essential identifier
        'ec05_emp_all',             # Total employment
        'ec05_emp_f',               # Female employment  
        'ec05_emp_m',               # Male employment
        'ec05_emp_hired',           # Hired workers
        'ec05_emp_unhired',         # Unhired workers (family/self-employed)
        'ec05_emp_gov',             # Government employment
        'ec05_emp_priv',            # Private employment
        'ec05_emp_inf',             # Informal employment
        'ec05_count_all',           # Total firms
        'ec05_count_gov',           # Government firms
        'ec05_count_priv',          # Private firms
        'ec05_count_inf',           # Informal firms
        'ec05_emp_manuf',           # Manufacturing employment (already aggregated)
        'ec05_emp_services',        # Services employment (already aggregated)
    ]
    
    # 2. Create new dataset with core columns
    df_simplified = df[core_columns].copy()
    
    # 3. Create industry group employment columns by summing SHRIC codes
    industry_groups = define_industry_groups()
    
    for group_name, shric_codes in industry_groups.items():
        # Sum employment across SHRIC codes in this group
        shric_columns = [f'ec05_emp_shric_{code}' for code in shric_codes]
        
        # Only include columns that exist in the dataset
        existing_shric_columns = [col for col in shric_columns if col in df.columns]
        
        if existing_shric_columns:
            df_simplified[f'ec05_emp_{group_name}'] = df[existing_shric_columns].sum(axis=1)
            print(f"Created {group_name} employment from {len(existing_shric_columns)} SHRIC codes")
    
    # 4. Create derived market segmentation features
    print("Creating derived features for market segmentation...")
    
    # Economic diversity score (number of industry groups with employment > 0)
    industry_emp_columns = [col for col in df_simplified.columns if col.startswith('ec05_emp_') and 'group' not in col and col not in core_columns]
    df_simplified['ec05_economic_diversity_score'] = (df_simplified[industry_emp_columns] > 0).sum(axis=1)
    
    # Non-farm employment ratio (excluding primary industries)
    df_simplified['ec05_non_farm_employment'] = (
        df_simplified['ec05_emp_all'] - df_simplified['ec05_emp_primary_industries']
    )
    df_simplified['ec05_non_farm_employment_ratio'] = (
        df_simplified['ec05_non_farm_employment'] / df_simplified['ec05_emp_all'].replace(0, np.nan)
    ).fillna(0)
    
    # Firm density (firms per 1000 employment)
    df_simplified['ec05_firm_density'] = (
        df_simplified['ec05_count_all'] / (df_simplified['ec05_emp_all'] / 1000).replace(0, np.nan)
    ).fillna(0)
    
    # Employment per firm
    df_simplified['ec05_employment_per_firm'] = (
        df_simplified['ec05_emp_all'] / df_simplified['ec05_count_all'].replace(0, np.nan)
    ).fillna(0)
    
    # Retail diversity (important for market sophistication)
    retail_columns = ['ec05_emp_wholesale_trade', 'ec05_emp_retail_consumer']
    df_simplified['ec05_retail_diversity'] = (df_simplified[retail_columns] > 0).sum(axis=1)
    
    # Service sector sophistication
    service_sophistication_columns = [
        'ec05_emp_financial_services', 
        'ec05_emp_business_services',
        'ec05_emp_communication_digital',
        'ec05_emp_social_services',
        'ec05_emp_entertainment_culture'
    ]
    df_simplified['ec05_service_sophistication_score'] = (df_simplified[service_sophistication_columns] > 0).sum(axis=1)
    
    # Female employment ratio (gender equality indicator)
    df_simplified['ec05_female_employment_ratio'] = (
        df_simplified['ec05_emp_f'] / df_simplified['ec05_emp_all'].replace(0, np.nan)
    ).fillna(0)
    
    # Formal vs informal employment ratio (economic development indicator)
    df_simplified['ec05_formal_employment_ratio'] = (
        (df_simplified['ec05_emp_gov'] + df_simplified['ec05_emp_priv']) / 
        df_simplified['ec05_emp_all'].replace(0, np.nan)
    ).fillna(0)
    
    print(f"Simplified dataset: {len(df_simplified)} rows, {len(df_simplified.columns)} columns")
    print(f"Reduced from {len(df.columns)} to {len(df_simplified.columns)} columns")
    print(f"Reduction: {100 * (1 - len(df_simplified.columns)/len(df.columns)):.1f}%")
    
    return df_simplified

def save_simplified_data(df_simplified):
    """Save the simplified data to cleaned_files directory"""
    
    # Save main simplified file to cleaned_files directory
    output_file = CLEANED_FILES_DIR / "ec05_shrid_simplified.csv"
    df_simplified.to_csv(output_file, index=False)
    print(f"Saved simplified data to {output_file}")
    
    # Create summary statistics
    summary_stats = df_simplified.describe()
    summary_file = CLEANED_FILES_DIR / "ec05_shrid_summary_stats.csv"
    summary_stats.to_csv(summary_file)
    print(f"Saved summary statistics to {summary_file}")
    
    # Create column documentation
    industry_groups = define_industry_groups()
    
    documentation = []
    for group_name, shric_codes in industry_groups.items():
        documentation.append({
            'column_name': f'ec05_emp_{group_name}',
            'description': f'Total employment in {group_name.replace("_", " ")} sector',
            'shric_codes_included': ', '.join(map(str, shric_codes)),
            'variable_type': 'Industry Group Employment'
        })
    
    # Add derived features documentation
    derived_features = [
        ('ec05_economic_diversity_score', 'Number of industry groups with employment > 0', 'Economic Diversity'),
        ('ec05_non_farm_employment_ratio', 'Non-farm employment as % of total employment', 'Economic Structure'),
        ('ec05_firm_density', 'Number of firms per 1000 employees', 'Business Density'),
        ('ec05_employment_per_firm', 'Average employees per firm', 'Firm Size'),
        ('ec05_retail_diversity', 'Number of retail/trade sectors present', 'Market Sophistication'),
        ('ec05_service_sophistication_score', 'Number of sophisticated service sectors', 'Service Economy'),
        ('ec05_female_employment_ratio', 'Female employment as % of total', 'Gender Equality'),
        ('ec05_formal_employment_ratio', 'Formal sector employment as % of total', 'Economic Formalization')
    ]
    
    for col_name, description, var_type in derived_features:
        documentation.append({
            'column_name': col_name,
            'description': description,
            'shric_codes_included': 'Derived feature',
            'variable_type': var_type
        })
    
    doc_df = pd.DataFrame(documentation)
    doc_file = CLEANED_FILES_DIR / "ec05_shrid_column_documentation.csv"
    doc_df.to_csv(doc_file, index=False)
    print(f"Saved column documentation to {doc_file}")
    
    return output_file

def main():
    """Main function to clean and simplify EC05 data"""
    print("="*60)
    print("EC05 SHRID DATA CLEANING AND SIMPLIFICATION")
    print("="*60)
    
    # Load data
    df = load_and_clean_ec05_data()
    
    # Simplify data
    df_simplified = simplify_ec05_data(df)
    
    # Save results
    output_file = save_simplified_data(df_simplified)
    
    print("\n" + "="*60)
    print("CLEANING COMPLETE!")
    print("="*60)
    print(f"Original columns: {len(df.columns)}")
    print(f"Simplified columns: {len(df_simplified.columns)}")
    print(f"Reduction: {100 * (1 - len(df_simplified.columns)/len(df.columns)):.1f}%")
    print(f"Output file: {output_file}")
    print("\nKey improvements for market segmentation:")
    print("✓ Grouped 90 SHRIC codes into 14 meaningful industry categories")
    print("✓ Created economic diversity and sophistication indicators")
    print("✓ Added employment structure ratios (formal/informal, male/female)")
    print("✓ Calculated firm density and business sophistication metrics")
    print("✓ Removed technical columns not needed for segmentation")

if __name__ == "__main__":
    main()
