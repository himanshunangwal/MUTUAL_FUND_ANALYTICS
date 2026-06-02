import os
import requests
import pandas as pd

def fetch_live_nav():
    # The specific URL from your assignment sheet
    url = "https://api.mfapi.in/mf/125497"
    print("Connecting to API to fetch live NAV data...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            nav_list = json_data.get('data', [])
            meta_info = json_data.get('meta', {})
            
            if nav_list:
                # Convert the JSON array into a clean Pandas DataFrame
                df = pd.DataFrame(nav_list)
                
                # Attach metadata columns so we know what scheme this belongs to
                df['scheme_code'] = meta_info.get('scheme_code', '125497')
                df['scheme_name'] = meta_info.get('scheme_name', 'HDFC Top 100 Direct')
                
                # Define output path
                output_path = "data/raw/11_live_nav_hdfc.csv"
                
                # Save it
                df.to_csv(output_path, index=False)
                print(f"✅ Success! Saved {len(df)} rows of live NAV data to '{output_path}'")
            else:
                print("❌ No data found inside the API JSON response.")
        else:
            print(f"❌ API connection failed. HTTP Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ An error occurred during the API call: {e}")

if __name__ == "__main__":
    fetch_live_nav()