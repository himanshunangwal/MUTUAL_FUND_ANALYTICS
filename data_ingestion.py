import os
import pandas as pd

def ingest_all_datasets():
    raw_folder = "data/raw/"
    
    # Check if the folder exists
    if not os.path.exists(raw_folder):
        print(f"❌ Error: The folder '{raw_folder}' does not exist. Please check your folder structure.")
        return

    # List all CSV files inside data/raw/
    all_files = sorted([f for f in os.listdir(raw_folder) if f.endswith('.csv')])
    
    print("=" * 60)
    print(f"MUTUAL FUND CAPSTONE PROJECT - DATA QUALITY SUMMARY")
    print(f"Found {len(all_files)} CSV datasets inside '{raw_folder}'.")
    print("=" * 60)

    # Variables to track specific data for validation
    fund_master_df = None
    nav_history_df = None

    for file_name in all_files:
        file_path = os.path.join(raw_folder, file_name)
        print(f"\n📄 FILE: {file_name}")
        print("-" * 40)
        
        try:
            # Load file using pandas
            df = pd.read_csv(file_path)
            
            # 1. Print the Shape (Rows, Columns)
            print(f"• Shape (Rows, Columns): {df.shape}")
            
            # 2. Print Data Types of columns
            print("\n• Data Columns & Types:")
            print(df.dtypes)
            
            # 3. Print Head (First 3 sample rows)
            print("\n• First 3 sample rows:")
            print(df.head(3))
            
            # Track master and history dataframes for the required AMFI code validation step
            if "fund_master" in file_name.lower():
                fund_master_df = df
            elif "nav_history" in file_name.lower():
                nav_history_df = df
                
        except Exception as e:
            print(f"❌ Could not read file {file_name}: {e}")
            
        print("=" * 60)

    # --- AMFI Scheme Code Validation ---
    print("\n" + "=" * 60)
    print("VALIDATION STEP: CROSS-CHECKING AMFI CODES")
    print("=" * 60)
    
    if fund_master_df is not None and nav_history_df is not None:
        # dynamically matching column names if they are slightly different (like scheme_code or amfi_code)
        master_col = [col for col in fund_master_df.columns if 'code' in col.lower() or 'amfi' in col.lower()]
        history_col = [col for col in nav_history_df.columns if 'code' in col.lower() or 'amfi' in col.lower()]
        
        if master_col and history_col:
            m_col = master_col[0]
            h_col = history_col[0]
            
            master_codes = set(fund_master_df[m_col].dropna().unique())
            history_codes = set(nav_history_df[h_col].dropna().unique())
            
            missing_codes = master_codes - history_codes
            
            print(f"Total Unique Codes in Fund Master ({m_col}): {len(master_codes)}")
            print(f"Total Unique Codes in NAV History ({h_col}): {len(history_codes)}")
            
            if len(missing_codes) == 0:
                print("✅ Validation Passed: Every scheme code in fund_master matches up inside nav_history.")
            else:
                print(f"⚠️ Validation Warning: {len(missing_codes)} codes from the master file are missing from history.")
                print(f"Missing codes sample: {list(missing_codes)[:5]}")
        else:
            print("Could not automatically locate the code identifier columns for structural cross-validation.")
    else:
        print("Missing '01_fund_master.csv' or '02_nav_history.csv' to execute cross-file code validation.")
    print("=" * 60)

if __name__ == "__main__":
    ingest_all_datasets()