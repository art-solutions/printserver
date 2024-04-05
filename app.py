from flask import Flask, request
import os
import tempfile
import requests
import win32print


app = Flask(__name__)

def print_file_from_url(url):
    # Download the file from the URL
    response = requests.get(url)

    # Create a temporary file to store the downloaded file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name

    try:
        # Set the default printer
        printer_name = win32print.GetDefaultPrinter()

        # Open the printer handle
        printer_handle = win32print.OpenPrinter(printer_name)

        try:
            # Create a new print job
            job_info = win32print.StartDocPrinter(printer_handle, 1, ("PrintJob", None, "RAW"))

            try:
                # Open the temporary file and read its content
                with open(temp_file_path, "rb") as file:
                    file_content = file.read()

                # Send the file content to the printer
                win32print.StartPagePrinter(printer_handle)
                win32print.WritePrinter(printer_handle, file_content)
                win32print.EndPagePrinter(printer_handle)

                print("File printed successfully.")
            finally:
                # End the print job
                win32print.EndDocPrinter(printer_handle)
        except Exception as e:
            print(f"An error occurred while printing: {e}")
        finally:
            # Close the printer handle
            win32print.ClosePrinter(printer_handle)
    finally:
        # Delete the temporary file
        os.unlink(temp_file_path)

@app.route('/<path:url>')
def print_url(url):
    print_file_from_url(url)
    return "Print request received"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5700)

