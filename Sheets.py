import os
import sys
import requests
import json
from datetime import datetime
import pytz
import pandas as pd
import time
API_KEY_FILE = "api_key.txt"

def get_local_time():
    user_tz = datetime.now(pytz.utc).astimezone().tzinfo
    local_time = datetime.now(user_tz).strftime('%a, %d %b %Y %H:%M:%S %Z')
    return local_time

def create_memory(api_key, memory_data):
    base_url = 'https://api.personal.ai/v1/memory'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    print(f"Creating memory with data: {memory_data}")

    response = requests.post(base_url, headers=headers, json=memory_data)

    if response.status_code == 200:
        creation_status = response.json()['status']
        print(f"Server responded with status: {creation_status}")
        return creation_status
    else:
        print(f"Server responded with status code: {response.status_code}")
        print(f"Response body: {response.text}")
        return None

def select_file(files):
    print("Available files:")
    for i, file_name in enumerate(files, start=1):
        print(f"{i}. {file_name}")

    choice = input("Enter the number corresponding to the file you want to upload: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(files):
            return files[index]
        else:
            print("Invalid choice. Please try again.")
            return select_file(files)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return select_file(files)

def get_api_key():
    api_key = input("Enter your Personal.ai API key: ")
    with open(API_KEY_FILE, "w") as f:
        f.write(api_key)
    return api_key

def main():
    # Check if API key file exists
    if not os.path.exists(API_KEY_FILE):
        print("API key file not found. Please enter your API key.")
        api_key = get_api_key()
    else:
        with open(API_KEY_FILE, "r") as f:
            api_key = f.read().strip()
        if not api_key:
            print("API key not found in the file. Please enter your API key.")
            api_key = get_api_key()

    local_time = get_local_time()

    # Prompt user for file type
    file_type = input("Select the file type to upload (1 for CSV, 2 for XLSX): ")
    if file_type not in ['1', '2']:
        print("Invalid choice. Exiting the program.")
        sys.exit(1)

    # Determine the file extension based on the user's choice
    file_extension = '.csv' if file_type == '1' else '.xlsx'

    # Get the list of files in the current directory with the chosen extension
    files = [file for file in os.listdir() if file.endswith(file_extension)]

    if len(files) == 0:
        print(f"No {file_extension} files found in the current directory. Exiting the program.")
        sys.exit(1)

    # Prompt the user to select a file
    selected_file = select_file(files)
    file_path = os.path.abspath(selected_file)

    # Ask the user for the file description
    file_description = input("Enter a description for the file: ")

    # Read data from the selected file
    if file_type == '1':
        data = pd.read_csv(file_path)
    else:
        data = pd.read_excel(file_path)

    headers = data.columns.tolist()
    memories = []

    for _, row in data.iterrows():
        text_content = ', '.join([f'{header}: {str(row[header])}' for header in headers])

        memory_data = {
            'Text': f'#Filename: {selected_file}, #FileDescription: {file_description}, CreatedTime: {local_time}, {text_content}',
            'SourceName': "My Custom Python Script",
            'CreatedTime': local_time,
            'DeviceName': "My Computer",
        }

        memories.append(memory_data)

    for memory in memories:
        creation_status = create_memory(api_key, memory)

        if creation_status is not None:
            print(f"Memory creation status: {creation_status}")
        else:
            print("Error creating memory")
            
        time.sleep(1)   
# end code statement for if name is main
if __name__ == '__main__':
    main()
    
