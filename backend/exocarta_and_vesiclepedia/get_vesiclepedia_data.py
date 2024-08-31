import requests
import pandas as pd
from io import StringIO
import argparse
import sys
import os

def test_connection(url):
    try:
        response = requests.get(url)
        print(f"Connection to {url} - Status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Connection error to {url}: {str(e)}")
        return None

def get_vesiclepedia_data(url):
    print(f"Attempting to retrieve data from: {url}")
    response = test_connection(url)

    if response and response.status_code == 200:
        try:
            data = pd.read_csv(StringIO(response.content.decode('utf-8')), sep='\t')
            print(f"Data retrieved successfully from {url}!")
            return data
        except Exception as e:
            print(f"Error parsing data: {str(e)}")
            return None
    else:
        print(f"Failed to retrieve data from {url}.")
        return None

def analyze_vesiclepedia_data(data, url):
    if data is None:
        print(f"No data to analyze from {url}")
        return

    print(f"\nAnalysis for data from {url}:")
    print(f"Retrieved {len(data)} entries")
    print("\nColumns in the dataset:")
    print(data.columns.tolist())
    
    print("\nFirst few rows:")
    print(data.head())

def save_data_to_file(data, filename):
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Retrieve and analyze Vesiclepedia data files.")
    parser.add_argument('url', type=str, help='URL to retrieve data from')
    parser.add_argument('--output', type=str, default='vesiclepedia_data.csv', help='Output file name')
    args = parser.parse_args()

    data = get_vesiclepedia_data(args.url)
    if data is not None:
        analyze_vesiclepedia_data(data, args.url)
        save_data_to_file(data, args.output)
    else:
        print("Failed to retrieve data. Please check the URL and try again.")

    print("\nIf the attempt failed, please check the Vesiclepedia website for current data access methods.")
    print("You may need to register or log in to access the data files.")

if __name__ == "__main__":
    main()
