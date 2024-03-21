from flask import Flask, request
import os
import tempfile
import win32print
import requests

app = Flask(__name__)

def print_file_from_url(url, printer_name, copies, page_range, paper_size, duplex, color_mode, print_quality, orientation, collate, print_to_file):
    # Download the file from the URL
    response = requests.get(url)

    # Create a temporary file to store the downloaded file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name

    try:
        # Open the printer handle
        printer_handle = win32print.OpenPrinter(printer_name)

        try:
            # Create a new print job
            job_info = win32print.StartDocPrinter(printer_handle, 1, ("PrintJob", None, "RAW"))

            try:
                # Open the temporary file and read its content
                with open(temp_file_path, "rb") as file:
                    file_content = file.read()

                # Set print job properties
                properties = {
                    "Copies": copies,
                    "PageRange": page_range,
                    "PaperSize": paper_size,
                    "Duplex": duplex,
                    "ColorMode": color_mode,
                    "PrintQuality": print_quality,
                    "Orientation": orientation,
                    "Collate": collate,
                    "PrintToFile": print_to_file
                }

                # Send the file content to the printer with the specified properties
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
        # Delete the temporary file from cache
        os.unlink(temp_file_path)

@app.route('/print', methods=['POST'])
def print_url():
    data = request.get_json()
    url = data.get('url')
    printer_name = data.get('printer_name')
    copies = data.get('copies', 1)
    page_range = data.get('page_range', '')
    paper_size = data.get('paper_size', 'A4')
    duplex = data.get('duplex', '')
    color_mode = data.get('color_mode', 'Color')
    print_quality = data.get('print_quality', 'High')
    orientation = data.get('orientation', 'Portrait')
    collate = data.get('collate', True)
    print_to_file = data.get('print_to_file', False)

    print_file_from_url(url, printer_name, copies, page_range, paper_size, duplex, color_mode, print_quality, orientation, collate, print_to_file)
    return "Print request received"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5700)
