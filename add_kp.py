import pandas
import csv
from csv import writer
def append_list_to_new_row(file_name, list_of_elements):
    #Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module 
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file 


        csv_writer.writerow(list_of_elements)

row_contents = [1, 8, 1, 'Đại số']
row_contents1 = [1, 8, 2, 'Hình Học']
append_list_to_new_row('Area1L.csv', row_contents)
append_list_to_new_row('Area1L.csv', row_contents1)

print(Area1L.csv)

