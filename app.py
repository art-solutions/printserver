from flask import Flask, request
import os
import tempfile
import requests
import subprocess

app = Flask(__name__)

def print_file_from_url(url):
    # Download the file from the URL
    response = requests.get(url)

    # Create a temporary file to store the downloaded file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name

    try:
        # Send the file to the default printer using the 'lp' command
        subprocess.run(["lp", temp_file_path])
        print("File printed successfully.")
    except Exception as e:
        print(f"An error occurred while printing: {e}")
    finally:
        # Delete the temporary file
        os.unlink(temp_file_path)

@app.route('/<path:url>')
def print_url(url):
    print_file_from_url(url)
    return "Print request received"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5700)
