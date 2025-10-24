import requests
import pandas as pd
from io import StringIO

def fetch_api_data(url):
    """Fetches data from an API and returns it as a JSON object."""
    try:
        response = requests.get(url)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        print("Successfully fetched data from API.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_data(data):
    """Converts JSON data to a Pandas DataFrame and performs simple processing."""
    if data is None:
        return None
    
    # Convert the list of dictionaries (JSON) into a DataFrame
    df = pd.DataFrame(data)
    
    print("Original DataFrame shape:", df.shape)
    
    # --- Simple Data Processing ---
    # 1. Select only the columns we care about
    df_processed = df[['userId', 'id', 'title']]
    
    # 2. Filter the data (e.g., only get posts from 'userId' 1)
    df_filtered = df_processed[df_processed['userId'] == 1].copy()
    
    # 3. Create a new column
    df_filtered['title_length'] = df_filtered['title'].apply(len)
    
    print("Processed DataFrame shape:", df_filtered.shape)
    return df_filtered

def save_to_csv(df, filename):
    """Saves a DataFrame to a CSV file."""
    if df is not None:
        df.to_csv(filename, index=False)
        print(f"Successfully saved data to {filename}")

def main():
    API_URL = "https://jsonplaceholder.typicode.com/posts"
    CSV_FILENAME = "processed_posts.csv"
    
    # 1. Extract
    api_data = fetch_api_data(API_URL)
    
    # 2. Transform
    df_processed = process_data(api_data)
    
    # 3. Load (in this case, "load" just means saving to a file)
    save_to_csv(df_processed, CSV_FILENAME)

if __name__ == "__main__":
    main()