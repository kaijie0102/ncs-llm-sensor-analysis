import pandas as pd
import time

TEST_DATA_FILE_PATH = "data/raw_data.txt"
THRESHOLD = 0.05
COLUMN_INDEX = 2

def in_range(val,lower, upper):
    if val<lower or val>upper:
        return False
    return True

def find_rows_after_change(filename, sheet_name):
    tapping = False
    end_count = 0
    total_count=0

    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(filename, sheet_name=sheet_name, header=None)

    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        if index == 0:
            continue # skip first row
        elif index == 1:
            # print("when index 1, val is: ",df.iloc[index, COLUMN_INDEX])
            lower = df.iloc[index, COLUMN_INDEX] - THRESHOLD
            upper = df.iloc[index, COLUMN_INDEX] + THRESHOLD 
            # print("lower: ",lower)
            # print("upper: ",upper)
            continue  # Skip the seocnd row
        
        else:
            # Compare the value with the previous row
            current_value = row[COLUMN_INDEX]
            # previous_value = df.iloc[index - 1, COLUMN_INDEX]
            # if index < 70:
            #     print("current: ", current_value)
                # print("difference: ", abs(current_value - previous_value))
            # if abs(current_value - previous_value) >= THRESHOLD:
            #     change_row = index  # Return the index of the first differing row
            #     break

            # finding start of the tap
            if not in_range(current_value,lower,upper) and not tapping:
                # print("Not in range! current_value: ", current_value)
                tap_start = index
                # print("tap_start found: ", tap_start)
                tapping = True        

            # finding end of the tap, check for 5 consecutive "in taps" to signify that tap has ended
            if tapping:
                if in_range(current_value,lower,upper):
                    end_count += 1

                if end_count > 10:
                    tap_end = index - 10
                    # print("Tap from: ",tap_start, "to: ", tap_end)

                    tapping = False
                    end_count = 0
                    total_count+=1
                    print("Sent gesture:", total_count)


        
                    # Find the first row where the value changes
                    # change_row = df[df.iloc[:, 2].diff() != 0].index[0]

                    # print("tap_start ", tap_start)
                    # print("tap_end ", tap_end)

                    # Get the next 10 rows from the first row where the value changes
                    next_10_rows = df.iloc[tap_start - 4 : tap_end + 5, :3]
                    
                    next_10_rows = next_10_rows.to_string(index=False,header=False)
    
                    # Return the resulting DataFrame
                    test_data_file = open(TEST_DATA_FILE_PATH, 'w')
                    test_data_file.write(next_10_rows)
                    test_data_file.close()
                    time.sleep(5)

    return next_10_rows 

# Example usage
filename = 'one_tap.xlsx'  # Replace with your Excel file name
sheet_name = 'one_tap'  # Replace with your sheet name

result = find_rows_after_change(filename, sheet_name)
print(result)
