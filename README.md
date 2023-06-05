# PAI-sheets
An app to upload csv and exel xlsx files to your personal.ai bot.

# Personal.ai CSV or XSLX file to Memory Uploader

This command-line interface (CLI) application allows you to upload data from a CSV or XLSX file to Personal.ai as memories using the column names as headers.

## Prerequisites

- Python 3.6 or above

- `pip` package manager

## Installation

1. Clone the repository or download the source code.

2. Install the required dependencies by running the following command:

   ```bash

   pip install -r requirements.txt


##Usage

Obtain your Personal.ai API key. If you don't have one, you can sign up at Personal.ai.

Run the script using the following command:

    '''bash
    python upload_memory_cli.py

The CLI will prompt you to choose the file type (CSV or XLSX) you want to upload.

After selecting the file type, the CLI will display the available files with the chosen extension in the current directory.

Enter the number corresponding to the file you want to upload.

The script will read the data from the selected file and upload each row as a memory using the column names as headers.

##Configuration

The application uses an API key file (api_key.txt) to store your Personal.ai API key securely. On the first run, you will be prompted to enter your API key, and it will be saved in the file. On subsequent runs, the script will read the API key from the file.

If you need to update your API key or if the api_key.txt file gets deleted, the CLI will prompt you again to enter your API key.
