"""
Master script to run all Economic Census data cleaning in sequence
Cleans EC98, EC05, and EC13 data files for market segmentation analysis
"""

import pandas as pd
import subprocess
import sys
from pathlib import Path
import time

# Define paths
SCRIPTS_DIR = Path(r"d:\BDA_project\BDA_project\prithvi_rand\IndiaMarketProject\scripts\data_cleaning")
CLEANED_FILES_DIR = Path(r"d:\BDA_project\BDA_project\prithvi_rand\IndiaMarketProject\data\processed\cleaned_files")

def run_script(script_name):
    """Run a cleaning script and capture results"""
    print(f"\n{'='*80}")
    print(f"STARTING: {script_name}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, script_name], 
            cwd=SCRIPTS_DIR,
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Print output
        print(result.stdout)
        if result.stderr:
            print("WARNINGS:")
            print(result.stderr)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✅ COMPLETED: {script_name} in {duration:.1f} seconds")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR in {script_name}:")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def check_output_files():
    """Check that all expected output files were created"""
    print(f"\n{'='*80}")
    print("CHECKING OUTPUT FILES")
    print(f"{'='*80}")
    
    expected_files = [
        "ec98_shrid_simplified.csv",
        "ec98_shrid_summary_stats.csv", 
        "ec98_shrid_column_documentation.csv",
        "ec05_shrid_simplified.csv",
        "ec05_shrid_summary_stats.csv",
        "ec05_shrid_column_documentation.csv", 
        "ec13_shrid_simplified.csv",
        "ec13_shrid_summary_stats.csv",
        "ec13_shrid_column_documentation.csv"
    ]
    
    all_files_exist = True
    file_info = []
    
    for filename in expected_files:
        filepath = CLEANED_FILES_DIR / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            file_info.append({
                'file': filename,
                'status': '✅ EXISTS',
                'size_mb': f'{size_mb:.1f} MB'
            })
            print(f"✅ {filename} - {size_mb:.1f} MB")
        else:
            file_info.append({
                'file': filename,
                'status': '❌ MISSING',
                'size_mb': 'N/A'
            })
            print(f"❌ {filename} - MISSING")
            all_files_exist = False
    
    # Save file inventory
    file_df = pd.DataFrame(file_info)
    inventory_file = CLEANED_FILES_DIR / "cleaning_output_inventory.csv"
    file_df.to_csv(inventory_file, index=False)
    print(f"\n📋 File inventory saved to: {inventory_file}")
    
    return all_files_exist

def generate_summary_report():
    """Generate a summary report of all cleaned data"""
    print(f"\n{'='*80}")
    print("GENERATING SUMMARY REPORT")
    print(f"{'='*80}")
    
    try:
        # Load all simplified datasets for summary
        ec98_file = CLEANED_FILES_DIR / "ec98_shrid_simplified.csv"
        ec05_file = CLEANED_FILES_DIR / "ec05_shrid_simplified.csv" 
        ec13_file = CLEANED_FILES_DIR / "ec13_shrid_simplified.csv"
        
        summary_data = []
        
        if ec98_file.exists():
            df98 = pd.read_csv(ec98_file)
            summary_data.append({
                'dataset': 'Economic Census 1998',
                'filename': 'ec98_shrid_simplified.csv',
                'records': len(df98),
                'columns': len(df98.columns),
                'file_size_mb': ec98_file.stat().st_size / (1024 * 1024),
                'total_employment': df98['ec98_emp_all'].sum(),
                'total_firms': df98['ec98_count_all'].sum()
            })
        
        if ec05_file.exists():
            df05 = pd.read_csv(ec05_file)
            summary_data.append({
                'dataset': 'Economic Census 2005',
                'filename': 'ec05_shrid_simplified.csv', 
                'records': len(df05),
                'columns': len(df05.columns),
                'file_size_mb': ec05_file.stat().st_size / (1024 * 1024),
                'total_employment': df05['ec05_emp_all'].sum(),
                'total_firms': df05['ec05_count_all'].sum()
            })
            
        if ec13_file.exists():
            df13 = pd.read_csv(ec13_file)
            summary_data.append({
                'dataset': 'Economic Census 2013',
                'filename': 'ec13_shrid_simplified.csv',
                'records': len(df13), 
                'columns': len(df13.columns),
                'file_size_mb': ec13_file.stat().st_size / (1024 * 1024),
                'total_employment': df13['ec13_emp_all'].sum(),
                'total_firms': df13['ec13_count_all'].sum()
            })
        
        # Create summary dataframe
        summary_df = pd.DataFrame(summary_data)
        summary_file = CLEANED_FILES_DIR / "economic_census_summary.csv"
        summary_df.to_csv(summary_file, index=False)
        
        print("📊 ECONOMIC CENSUS DATA SUMMARY:")
        print(summary_df.to_string(index=False))
        print(f"\n📋 Summary report saved to: {summary_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating summary report: {e}")
        return False

def main():
    """Main function to run all cleaning scripts"""
    print("🚀 STARTING ECONOMIC CENSUS DATA CLEANING PIPELINE")
    print("="*80)
    print("This script will clean EC98, EC05, and EC13 datasets")
    print("Each dataset will be simplified from ~137 columns to ~38 columns")
    print("Industry codes will be grouped into 14 meaningful categories")
    print("Market segmentation indicators will be calculated")
    print("="*80)
    
    start_time = time.time()
    
    # Scripts to run in order
    cleaning_scripts = [
        "clean_ec98_shrid.py",
        "clean_ec05_shrid.py", 
        "clean_ec13_shrid.py"
    ]
    
    success_count = 0
    
    # Run each cleaning script
    for script in cleaning_scripts:
        if run_script(script):
            success_count += 1
        else:
            print(f"\n⚠️ Script {script} failed - continuing with others...")
    
    # Check output files
    print(f"\n{'='*80}")
    print(f"PIPELINE RESULTS: {success_count}/{len(cleaning_scripts)} scripts completed successfully")
    print(f"{'='*80}")
    
    files_ok = check_output_files()
    report_ok = generate_summary_report()
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Final summary
    print(f"\n{'='*80}")
    print("🎯 CLEANING PIPELINE COMPLETE!")
    print(f"{'='*80}")
    print(f"⏱️  Total time: {total_duration:.1f} seconds")
    print(f"✅ Scripts completed: {success_count}/{len(cleaning_scripts)}")
    print(f"📁 Files created: {'✅ All files OK' if files_ok else '⚠️ Some files missing'}")
    print(f"📊 Summary report: {'✅ Generated' if report_ok else '❌ Failed'}")
    
    if success_count == len(cleaning_scripts) and files_ok:
        print("\n🎉 SUCCESS: All Economic Census data cleaned and ready for analysis!")
        print(f"📂 Output location: {CLEANED_FILES_DIR}")
        print("\n📋 Next steps:")
        print("1. Review summary statistics in *_summary_stats.csv files")
        print("2. Check column documentation in *_column_documentation.csv files") 
        print("3. Proceed to Phase 2A: Feature Engineering")
    else:
        print("\n⚠️ WARNING: Some issues occurred during cleaning")
        print("Please check the error messages above and retry failed scripts")

if __name__ == "__main__":
    main()
