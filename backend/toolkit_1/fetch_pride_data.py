# fetch_pride_data.py

import requests
from urllib.request import urlopen
import time
import os

def get_pride_data(pride_id, max_retries=3, retry_delay=5):
    url = f"https://www.ebi.ac.uk/pride/ws/archive/v2/projects/{pride_id}/files"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            files = data['_embedded']['files']
            suitable_file = next((file for file in files if file['fileName'].endswith('.prot.xml')), None)
            
            if suitable_file:
                ftp_url = next((loc['value'] for loc in suitable_file['publicFileLocations'] if loc['name'] == 'FTP Protocol'), None)
                
                if ftp_url:
                    print(f"Downloading file: {suitable_file['fileName']}")
                    return download_file(ftp_url, suitable_file['fileName'], max_retries, retry_delay)
                else:
                    print("No FTP URL found for the suitable file.")
                    return use_local_file(suitable_file['fileName'])
            else:
                print("No suitable .prot.xml file found in the project.")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("All attempts to retrieve PRIDE data failed. Trying to use local file if available.")
                return use_local_file(pride_id + ".prot.xml")
    
    return None

def download_file(ftp_url, file_name, max_retries, retry_delay):
    for download_attempt in range(max_retries):
        try:
            with urlopen(ftp_url) as response:
                xml_content = response.read()
            return xml_content
        except Exception as e:
            print(f"Download attempt {download_attempt + 1} failed: {str(e)}")
            if download_attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("All download attempts failed. Trying to use local file if available.")
                return use_local_file(file_name)
    return None

def use_local_file(filename):
    if os.path.exists(filename):
        print(f"Using local file: {filename}")
        with open(filename, 'rb') as f:
            return f.read()
    else:
        print(f"Local file {filename} not found.")
        return None

