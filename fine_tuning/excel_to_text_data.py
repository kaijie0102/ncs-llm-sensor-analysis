import pandas as pd
import time

INPUT_FILE = "testing_data/light/test378.xlsx"
OUTPUT_FILE = "test_data.txt"

# Load the Excel file
excel_file = pd.read_excel(INPUT_FILE)

# Open the text file to write
with open(OUTPUT_FILE, 'w') as f:
    # Iterate over each row in the first column
    for i in range(len(excel_file.iloc[:, 0])):
        # print("writing to file")
        # Write the value to the text file
        f.write(str(excel_file.iloc[i, 0]) + '\n')
        print(f"Gesture {i+1}: {str(excel_file.iloc[i, 1])}")
        f.flush()  # Ensure that it's written to disk immediately

        # Wait for 5 seconds before writing the next row
        if i != len(excel_file.iloc[:, 0]) - 1:  # No need to wait after writing the last line
            time.sleep(3)

            # clear file
            f.seek(0)    
            f.truncate()

print("Writing to text file completed.")