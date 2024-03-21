from flask import Flask, request
import os
import win32api
import win32print

app = Flask(__name__)

@app.route('/printjob', methods=['GET'])
def print_file():
    file_path = request.args.get('printfilepath')
    if file_path:
        # Set the default printer
        printer_name = win32print.GetDefaultPrinter()

        # Set the printing preferences
        printing_preferences = {
            "Collate": True,
            "Copies": 1,
            "Duplex": win32print.DMDUP_VERTICAL,  # Double-sided printing
            "PaperSize": win32print.DMPAPER_A4,  # A4 paper size
            "Scale": 120  # 120% scale
        }

        # Open the file
        os.startfile(file_path, "print")

        # Wait for the print job to complete
        print("Printing the file...")
        win32api.Sleep(5000)  # Wait for 5 seconds (adjust as needed)

        # Get the printer handle
        printer_handle = win32print.OpenPrinter(printer_name)

        try:
            # Get the current printer job
            job_info = win32print.GetJob(printer_handle, -1)

            # Set the printing preferences for the job
            win32print.SetJob(printer_handle, job_info["JobId"], 0, printing_preferences, 0)

            # Check if the job is complete
            while job_info["Status"] != 0:
                win32api.Sleep(1000)  # Wait for 1 second
                job_info = win32print.GetJob(printer_handle, -1)

            return "File printed successfully."
        except Exception as e:
            return f"An error occurred while printing: {str(e)}"
        finally:
            # Close the printer handle
            win32print.ClosePrinter(printer_handle)
    else:
        return "No file path provided."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
