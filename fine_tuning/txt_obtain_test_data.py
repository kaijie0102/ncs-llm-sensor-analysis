def in_range(val,lower, upper):
    if val<lower or val>upper:
        return False
    return True

def extract_lines(filename):
    TEST_DATA_FILE_PATH = "raw_data.txt"
    THRESHOLD = 0.05
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # pre processing
        for index in range(len(lines)):
            lines[index] = lines[index].split() # to make line an row of 3 elements
            lines[index][2].strip()

        print(lines)

        # setting lower and upper bound
        upper_bound = float(lines[0][2]) + THRESHOLD
        lower_bound = float(lines[0][2]) - THRESHOLD
        tap_started = False
        end_count=0

        for i in range(len(lines)):
            # find start index
            current = float(lines[i][2])
            if not in_range(current,lower_bound,upper_bound) and not tap_started:
                start_index = i
                tap_started = True
            
            elif tap_started:
                if in_range(current,lower_bound,upper_bound):
                    end_count+=1
                if end_count>5:
                    # tap has ended
                    end_index = i - 5
                    break
    test_data = lines[start_index-5:end_index+5]
    return test_data



        # print("Lines: ",lines)
        # first_row = lines[0].split(',')
        # print("first line: ",lines[0].split(','))

        # for i in range(len(first_row)):
        #     print(first_row[i].strip())
        #     first_row[i]=first_row[i].strip()
        # print("new line: ",first_row)
        

        # middle_start = len(lines) // 2 - 5  # Compute starting index for the middle 10 lines
        # middle_end = middle_start + 10  # Compute ending index for the middle 10 lines
        # middle_lines = lines[middle_start:middle_end]  # Extract the middle 10 lines
        # for line in middle_lines:
        #     print(line.strip())  # Print the line, removing trailing newline character

# Use the function
filename = 'raw_data.txt'
extract_lines(filename)
