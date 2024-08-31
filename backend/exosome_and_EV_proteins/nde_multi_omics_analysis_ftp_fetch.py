from ftplib import FTP

def find_dataset_directory(ftp, year_directories, pride_id):
    for year_dir in year_directories:
        print(f"Checking year directory: {year_dir}")
        ftp.cwd(f"/pride/data/archive/{year_dir}")
        dirs = []
        ftp.retrlines('LIST', dirs.append)
        # Check if the dataset is in this directory
        for line in dirs:
            if pride_id in line:
                print(f"Found dataset directory: {line}")
                return f"/pride/data/archive/{year_dir}/{pride_id}/"
        # Go back to root for next iteration
        ftp.cwd('..')
    return None

def download_proteomics_data(pride_id, file_name):
    ftp = FTP('ftp.pride.ebi.ac.uk')
    ftp.login()
    # List year directories
    ftp.cwd('/pride/data/archive/')
    year_dirs = []
    ftp.retrlines('LIST', year_dirs.append)

    # Extract year directory names
    year_dirs = [line.split()[-1] for line in year_dirs]

    # Find the correct dataset directory
    dataset_dir = find_dataset_directory(ftp, year_dirs, pride_id)
    if dataset_dir:
        ftp.cwd(dataset_dir)
        local_file = open(file_name, 'wb')
        ftp.retrbinary(f'RETR {file_name}', local_file.write)
        local_file.close()
        print(f"Downloaded {file_name} successfully.")
    else:
        print(f"Dataset {pride_id} not found.")
    
    ftp.quit()

# Use the local path to the downloaded mzML file
pride_id = 'PXD000561'  # Example PRIDE dataset ID
file_name = 'desired_file.mzML'
download_proteomics_data(pride_id, file_name)

