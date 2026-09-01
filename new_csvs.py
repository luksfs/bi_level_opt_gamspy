# import csv

# file_name = 'result/D-SDA_7D.csv'

# # ==========================================
# # STEP 1: Create the file with JUST the header
# # ==========================================
# # Using mode='w' (write) creates a new file or overwrites an existing one.
# with open(file_name, mode='w', newline='') as file:
#     # Set the delimiter to a semicolon
#     writer = csv.writer(file, delimiter=';') 
    
#     # Write only the header row
#     writer.writerow(['Initial Candidate','Best solution','Fobj' ,'Execution Time', 'Objective function evaluations'])`
# 
import csv
i=0
initial_y_list=[1,2,3] 
y_best=[1,2.3,4]
fobj_best = 1.2
time_list=[20]
counter=1
with open('result/D-SDA_5D.csv', mode='a', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    new_row = [initial_y_list[i], y_best, fobj_best,time_list[i], counter]
    writer.writerow(new_row)